from comments_db import add_review, get_review_by_review_id, delete_reveiw, update_reveiw, get_all_review_by_movie
from movie import get_ThisMovie
from helper import get_user_from_token, get_banned_list
import sqlite3
import os
from auth import ban_user

cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def get_rating_by_movie_id(token, movie_id):
    # get everyone's rating
    reviews = get_all_review_by_movie(movie_id)
    if reviews == None or len(reviews) == 0:
        return 0
    # drop the user banned
    banned_list = get_banned_list(token)
    ratings = []
    for review in reviews:
        if token is "None" or banned_list is None:
            ratings.append(int(review['rating']))
        elif banned_list is not None and review['user_id'] not in banned_list:
            ratings.append(int(review['rating']))
            # calculate the rating
    if len(ratings) == 0:
        return 0
    rate = sum(ratings)/len(ratings)
    return round(rate, 2)


def get_comment_by_movie_id(token, movie_id):
    # check if movie exist
    try:
        movie = get_ThisMovie(movie_id, token)
        if movie is None:
            return {'400': "Movie Id does not exists."}
    except:
        return {'400': "Movie does not exist."}
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    banned_list = get_banned_list(token)
    print(banned_list)
    reviews = get_all_review_by_movie(movie_id)
    review_ids = []
    for review in reviews:
        user_id = cursor.execute(
            '''
            SELECT user_id FROM Review where review_id = ?
            ''', (int(review['review_id']),)
        ).fetchone()
        if token is "None" or banned_list is None:
            review_ids.append(int(review['review_id']))
        elif banned_list is not None and user_id is not None and user_id[0] not in banned_list:
            review_ids.append(int(review['review_id']))

    # print(review_ids)
    return review_ids

# this will add the comment to movie for user


def add_comment_rating(token, movie_id, review, rating, added_on):
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}
    user = get_user_from_token(token)
    if user is None:
        return {'400': "Please login."}
    user_id = user['user_id']
    # add review
    review_id = add_review(user_id, movie_id, review, rating, added_on)
    if review_id is None:
        return {'400': "Add comment failed, please retry."}
    return review_id


def update_comment_rating(token, review_id, new_comment, new_rating, added_on):
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}

    user = get_user_from_token(token)
    if user is None:
        return {'400': "Please login."}
    user_id = user['user_id']
    # check if user has the access
    review = get_review_by_review_id(review_id)
    if review['user_id'] != user_id:
        return {'400': "Do not have access."}
    # update the comment
    return update_reveiw(review_id, new_comment, new_rating, added_on)


def delete_comment_rating(token, review_id):
    '''this will delete the comment from movie for user'''
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}
    user = get_user_from_token(token)
    if user is None:
        return {'400': "Please login."}
    user_id = user['user_id']

    # check if user has the access
    review = get_review_by_review_id(review_id)
    if review['user_id'] != user_id:
        return {'400': "Do not have access."}

    # delete review
    result = delete_reveiw(review_id)
    if result is False:
        return {'400': "Do not have access."}
    return True


def add_banlist(token, comment_id):
    if token is None:
        return {'400': "Please login."}
    user = get_user_from_token(token)
    if user is None:
        return {'400': "Please login."}
    user_id = user['user_id']
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    ban_user_id = cursor.execute(
        "SELECT user_id from Review where review_id = ?", (comment_id,)).fetchone()[0]
    return ban_user(user_id, ban_user_id)


def get_comment_by_token(token):
    user = get_user_from_token(token)
    if user is None:
        return {'400': 'No such user'}
    user_id = user['user_id']
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    res = cursor.execute(
        "SELECT review_id from Review where user_id = ?", (user_id,)).fetchall()
    result = []
    for review_id in res:
        temp = {}
        temp['comment_id'] = review_id[0]
        review = cursor.execute(
            "SELECT rating, review,movie_id from Review where review_id = ?", (review_id[0],)).fetchone()
        temp['rate'] = review[0]
        temp['comment'] = review[1]
        movie_pic = cursor.execute(
            "SELECT photo from Movie_Photo where movie_id = ?", (review[2],)).fetchone()
        temp['movie_pic'] = movie_pic[0]
        result.append(temp)
    return result


def get_comment_by_user_id(token, check_user_id):
    user = get_user_from_token(token)
    if user is None:
        return {'400': 'No such user'}
    user_id = user['user_id']
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    banned = cursor.execute(
        '''
        SELECT ban_user_id FROM Banlist WHERE user_id = ? AND ban_user_id = ?
        ''', (check_user_id, user_id,)
    ).fetchone()
    if banned is not None:
        return {'400': 'You have been banned by user'}
    res = cursor.execute(
        "SELECT review_id from Review where user_id = ?", (check_user_id,)).fetchall()
    result = []
    for review_id in res:
        temp = {}
        temp['comment_id'] = review_id[0]
        review = cursor.execute(
            "SELECT rating, review,movie_id from Review where review_id = ?", (review_id[0],)).fetchone()
        temp['rate'] = review[0]
        temp['comment'] = review[1]
        movie_pic = cursor.execute(
            "SELECT photo from Movie_Photo where movie_id = ?", (review[2],)).fetchone()
        temp['movie_pic'] = movie_pic[0]
        result.append(temp)
    return result
