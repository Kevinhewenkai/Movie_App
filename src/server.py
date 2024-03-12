import feedback
import search
import movie
import os
from json import dumps
from auth import auth_register, delete_account, auth_get_user_name, reset_psw, send_code
from flask import Flask, request
import recommend
from flask_cors import CORS
import user
import favourite
import follow
import comments
import comments_db
import wishlist
from auth import auth_login, auth_logout, auth_register, delete_banned_user, add_user_photo, ban_user, get_user_banned

basedir = os.path.abspath(os.path.dirname(__file__))
APP = Flask(__name__)
CORS(APP)


Key_Word = ""  # base on the search keyword to filter
# Sample


@APP.route("/mainpage", methods=['GET'])
def main_page():
    lastestsix_id = movie.get_lastestsix_id()
    # DEBUG
    # print(info)
    return dumps(lastestsix_id)  # return a list contain all movie


@APP.route("/movie", methods=['GET'])
def root_page():
    all = movie.get_AllMovie_id()
    # DEBUG
    # print(info)
    return dumps(all)  # return a list contain all movie


@APP.route("/get_user_name/<user_id>", methods=['GET'])
def get_user_name(user_id):
    user_id = int(user_id)
    return dumps(auth_get_user_name(user_id))

########### Search ###########
# The search result shows the target movies and the recommonded movies


@APP.route("/search/<keyword>", methods=['GET'])
def search_ByKeyword(keyword):
    Key_Word = keyword
    list = search.search(keyword)

    # insert a keyword and return the result filter by the keyword
    return dumps(list)


@APP.route("/search/films/<keyword>", methods=['GET'])
def search_ByKeyword_films(keyword):
    list = search.get_movie_SortByName(keyword)

    # insert a keyword which is movie name and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/Review/<keyword>", methods=['GET'])
def search_ByKeyword_Review(keyword):
    list = search.get_movie_Reviews(keyword)
    # insert a keyword which is movie name and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/wishllist/<keyword>", methods=['GET'])
def search_ByKeyword_Wishlist(keyword):
    list = search.get_Movie_Wishlist(keyword)
    # insert a keyword which is actor and return the movie list(only movie) filter by the keyword
    return dumps(list)

############ Sort By #######################


@APP.route("/search/SortByGenre", methods=['GET'])
def search_ByKeyword_SortByGenre():
    global Key_Word
    list = search.get_movie_SortByGenre(Key_Word)
    # insert a keyword which is movie name and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/SortByCountry", methods=['GET'])
def search_ByKeyword_SortByCountry():
    global Key_Word
    list = search.get_movie_SortByCountry(Key_Word)
    # insert a keyword which is country and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/SortByLanguage", methods=['GET'])
def search_ByKeyword_SortByLanguage(keyword):
    global Key_Word
    list = search.get_movie_SortByLanguage(Key_Word)
    # insert a keyword which is language and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/SortByDescription", methods=['GET'])
def search_ByKeyword_SortByDescription():
    global Key_Word
    list = search.get_movie_SortByDescription(Key_Word)
    # insert a keyword which is decription and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/SortByYear/<keyword>", methods=['GET'])
def search_ByKeyword_SortByYear(keyword):
    global Key_Word
    list = search.get_movie_SortByYear(keyword)
    # insert a keyword which is year and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/SortByName/<keyword>", methods=['GET'])
def search_ByKeyword_SortByName(keyword):
    global Key_Word
    list = search.get_movie_SortByName(keyword)
    # insert a keyword which is year and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/SortByRate/<keyword>", methods=['GET'])
def search_ByKeyword_SortByRate(keyword):
    global Key_Word
    list = search.get_movie_SortByRate(keyword)
    # insert a keyword which is year and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/SortByPopularity/<keyword>", methods=['GET'])
def search_ByKeyword_SortByPpularity(keyword):
    global Key_Word
    print(keyword)
    list = search.get_movie_SortByPpularity(keyword)
    # insert a keyword which is year and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/director/<keyword>", methods=['GET'])
def search_ByKeyword_Director(keyword):
    list = search.get_Director_SortByDirector(keyword)
    # insert a keyword which is director and return the movie list(only movie) filter by the keyword
    return dumps(list)


@APP.route("/search/actor/<keyword>", methods=['GET'])
def search_ByKeyword_Actor(keyword):
    list = search.get_Actor_SortByActor(keyword)
    # insert a keyword which is actor and return the movie list(only movie) filter by the keyword
    return dumps(list)


########### View movie/director's detail ###########
@APP.route("/movie/all", methods=['GET'])
def get_all_movie():
    all = movie.get_AllMovie()
    # DEBUG
    # print(info)
    return dumps(all)  # return a list contain all movie


@APP.route("/movie/<movie_id>", methods=['GET'])
def show_movie_info(movie_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    Thismovie = movie.get_ThisMovie(movie_id, token)

    return dumps(Thismovie)  # return the movie info include photo


@APP.route("/movie/info/ByDirectorId/<director_id>", methods=['GET'])
def show_movie_by_directorid(director_id):
    Thismovie = movie.get_Movie_By_Director(director_id)

    return dumps(Thismovie)  # return the movie by filter director


@APP.route("/movie/info/ByActorId/<actor_id>", methods=['GET'])
def show_movie_by_actorid(actor_id):
    Thismovie = movie.get_Movie_By_Actor(actor_id)

    return dumps(Thismovie)  # return the movie by filter actor


@APP.route("/movie/info/ByGenreId/<genre>", methods=['GET'])
def show_genre_info(genre):
    Thismovie = movie.get_Movie_By_Genre(genre)

    return dumps(Thismovie)  # return the movie by filter genre


########### User authentication ###########


@APP.route("/auth/login", methods=['POST'])
def login():
    '''Flask auth_login'''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    info = auth_login(email, password)
    # DEBUG
    # print(info)
    return dumps(info)


@APP.route("/auth/logout", methods=['POST'])
def logout():
    '''
    Flask auth_logout
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    # payload = request.get_json()
    # token = payload['token']
    auth_logout(token)
    return dumps({})


@APP.route("/auth/register", methods=['POST'])
def register():
    '''
    Flask auth_register
    '''
    payload = request.get_json()
    name = payload['name']
    email = payload['email']
    psw = payload['password']
    info = auth_register(name, email, psw)
    # DEBUG
    # print(info)
    return dumps(info)


@APP.route("/auth/delete",  methods=['DELETE'])
def delete():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    delete_account(token)
    return dumps({})


@APP.route("/auth/reset_psw/send_mail", methods=['POST'])
def reset_psw_send_email_http():
    payload = request.get_json()
    return dumps(send_code(payload['email']))


@APP.route("/auth/reset_psw", methods=['POST'])
def reset_psw_http():
    payload = request.get_json()
    email = payload['email']
    code = payload['code']
    new_psw = payload['new_psw']
    return dumps(reset_psw(email, code, new_psw))


@APP.route("/auth/add_photo", methods=['POST'])
def user_add_photo(token, photo_url):
    return add_user_photo(token, photo_url)


########### Wishlist ###########
# Show someone's wishlists
@APP.route("/wishlists", methods=['GET'])
def show_wishlists():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    info = wishlist.get_wishlists(token)
    return dumps(info)

# Show one of the wishlists' details


@APP.route("/wishlists/user/<user_id>", methods=['GET'])
def show_wishlists_by_user(user_id):
    info = wishlist.get_wishlists_by_user_id(user_id)
    return dumps(info)


@APP.route("/wishlists/list_info/<wishlist_id>", methods=['GET'])
def show_wishlist_info(wishlist_id):
    wishlist_id = int(wishlist_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    info = wishlist.get_wishlist_by_id(wishlist_id, token)
    return dumps(info)

# Build new wishlist


@APP.route("/wishlists/add_list", methods=['POST'])
def build_wishlist():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    payload = request.get_json()
    list_name = payload['list_name']
    status = int(payload['status'])

    return dumps(wishlist.build_wishlist(list_name, token, status))

# Delete wishlist


@APP.route("/wishlists/delete_list/<list_id>", methods=['DELETE'])
def delete_wishlist(list_id):
    list_id = int(list_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    wishlist.destroy_wishlist(list_id, token)
    return dumps({})

# Add/Delete movie to/from a wishlist, rename the wishlist, set privacy


@APP.route("/wishlists/change_name/<wishlist_id>", methods=['POST'])
def change_wishlist_name(wishlist_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    wishlist_id = int(wishlist_id)
    payload = request.get_json()
    new_list_name = payload['list_name']
    wishlist.change_list_name(wishlist_id, token, new_list_name)
    return dumps({})


@APP.route("/wishlists/add_to_wishlist/<wishlist_id>", methods=['POST'])
def add_to_wishlist(wishlist_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    wishlist_id = int(wishlist_id)
    payload = request.get_json()
    movie_id = int(payload['movie_id'])
    wishlist.add_to_wishlist(wishlist_id, token, movie_id)
    return dumps({})


@APP.route("/wishlists/delete_from_wishlist/<wishlist_id>", methods=['DELETE'])
def delete_from_wishlist(wishlist_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    wishlist_id = int(wishlist_id)
    payload = request.get_json()
    movie_id = int(payload['movie_id'])
    wishlist.delete_from_wishlist(token, wishlist_id, movie_id)
    return dumps({})


@APP.route("/wishlists/change_wishlist_status/<wishlist_id>", methods=['POST'])
def change_wishlist_status(wishlist_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    wishlist_id = int(wishlist_id)
    payload = request.get_json()
    status = int(payload['status'])
    wishlist.change_wishlist_private(token, wishlist_id, status)
    return dumps({})


@APP.route("/wishlists/get_wishlist_status/<wishlist_id>", methods=['GET'])
def get_wishlist_status(wishlist_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    wishlist_id = int(wishlist_id)
    status = wishlist.get_wishlist_status(token, wishlist_id)
    return dumps({'status': status})

########### Review/Rating ###########


@APP.route("/review/get_rating/<movie_id>", methods=['GET'])
def get_rating_by_movie_id(movie_id):
    movie_id = int(movie_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    rating = comments.get_rating_by_movie_id(token, movie_id)
    return dumps({'rating': rating})


@APP.route("/review/get_comments/<movie_id>", methods=['GET'])
def get_comment_by_movie_id(movie_id):
    movie_id = int(movie_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    info = comments.get_comment_by_movie_id(token, movie_id)
    # DEBUG
    # print(info)
    return dumps({"review_id": info})


@APP.route("/review/get_comments/<movie_id>/<review_id>", methods=['GET'])
def get_comment_by_review_id(movie_id, review_id):
    movie_id = int(movie_id)
    review_id = int(review_id)
    info = comments_db.get_review_by_review_id(review_id)
    # DEBUG
    # print(info)
    return dumps(info)


@APP.route("/review/add_comment_rating/<movie_id>", methods=['POST'])
def add_comment_rating(movie_id):
    movie_id = int(movie_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    # DEBUG
    # print(token)
    payload = request.get_json()
    review = payload['review']
    rating = float(payload['rating'])
    added_on = int(payload['added_on'])
    info = comments.add_comment_rating(
        token, movie_id, review, rating, added_on)
    return dumps(info)


@APP.route("/review/edit_comment_rating/<review_id>", methods=['POST'])
def edit_comment_rating(review_id):
    review_id = int(review_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    payload = request.get_json()
    review = payload['review']
    rating = int(payload['rating'])
    added_on = int(payload['added_on'])
    info = comments.update_comment_rating(
        token, review_id, review, rating, added_on)
    return dumps(info)


@APP.route("/review/delete_comment_rating/<review_id>", methods=['DELETE'])
def delete_comment_rating(review_id):
    review_id = int(review_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    comments.delete_comment_rating(token, review_id)
    return dumps({})


########### Banned list ###########
# Show the list of user banned
@APP.route("/banned", methods=['GET'])
def show_banned():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    ban = get_user_banned(token)
    return dumps(ban)

# Add the user to the banned list


@APP.route("/banned/add/<ban_user_id>", methods=['POST'])
def add_banned(ban_user_id):
    ban_user_id = int(ban_user_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    ban = ban_user(token, ban_user_id)
    return dumps(ban)


# @APP.route("/banned/comment/<comment_id>", methods=['POST'])
# def add_comment_banned(comment_id):
#     headers = request.headers
#     bearer = headers.get('Authorization')
#     token = bearer.split()[1]
#     ban = add_banlist(token, comment_id)
#     return dumps(ban)

# Delete the user from banned list


@APP.route("/banned/delete/<delete_user_id>", methods=['DELETE'])
def delete_banned(delete_user_id):
    removed_user_id = int(delete_user_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    result = delete_banned_user(token, removed_user_id)
    return dumps(result)

########### Feedback ###########


@APP.route("/feedback", methods=['GET'])
def receive_feedback():
    feedback_all = feedback.getfeedback()
    return dumps(feedback_all)


@APP.route("/insert_feedback", methods=['POST'])
def insert_feedback():
    payload = request.get_json()
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    time = int(payload['time'])
    description = payload['description']
    result = feedback.insertfeedback(token, time, description)
    return dumps(result)


########### Recommend ###########


@APP.route("/recommend/genre/<movie_id>", methods=['GET'])
def reccommond_by_gerne(movie_id):
    movie_id = int(movie_id)
    res = recommend.get_similarity_by_genre(movie_id)
    return dumps(res)


@APP.route("/recommend/director/<movie_id>", methods=['GET'])
def reccommond_by_director(movie_id):
    movie_id = int(movie_id)
    res = recommend.get_similarity_by_director(movie_id)
    return dumps(res)


@APP.route("/recommend/history/<movie_id>", methods=['GET'])
def reccommond_by_history(movie_id):
    movie_id = int(movie_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    res = recommend.get_similarity_by_history(movie_id, token)
    return dumps(res)

########### User profile ###########
# get "my" profile, identified by the token.
# return the user_id, name, email address, complaint_count, user_photo


@APP.route("/user/profile/me", methods=['GET'])
def get_my_profile():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    profile = user.get_my_profile(token)
    return dumps(profile)


# see other's profile
# don't need token.
# return the user_id, name, email address, complaint_count, user_photo
@APP.route("/user/profile/other/<user_id>", methods=['GET'])
def get_other_profile(user_id):
    profile = user.get_profile_id(user_id)
    return dumps(profile)


# update my profile,
# can update user_name, password, user_photo (in base64 format!!!)
# the updates are stored in json body, through POST
# cannot update email address !!! (used for login).
# return empty dict with code 200
@APP.route("/user/profile/update", methods=['POST'])
def update_my_profile():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    payload = request.get_json()
    res = user.update_my_profile(token, payload)
    return dumps(res)


@APP.route("/user/review/me", methods=['GET'])
def get_user_review():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    res = comments.get_comment_by_token(token)
    return dumps(res)


@APP.route("/user/review/<user_id>", methods=['GET'])
def check_others_id(user_id):
    user_id = int(user_id)
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    res = comments.get_comment_by_user_id(token, user_id)
    return dumps(res)
########### Favourite ###########
# obtain my favourite movie id list,
# identify the person through token.
# return {"movies": [movie id list]}


@APP.route("/favourite/me", methods=['GET'])
def get_my_favourite():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    result = favourite.get_my_favourite(token)
    return dumps({"favourite": result})


# check other's favourite movie id list
# no need for token.
# identify using user id
@APP.route("/favourite/user/<user_id>", methods=['GET'])
def get_other_favourite(user_id):
    result = favourite.get_user_favourite(user_id)
    return dumps({"favourite": result})


# add a movie into my favourite
# the same movie can be added multiple times for simplicity.
# 200 OK for success add.
# raise error if the movie id does not exist.
# need token to identify myself
@APP.route("/favourite/add/<movie_id>", methods=['POST'])
def add_favourite(movie_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    favourite.add_to_my_favourite(token, movie_id)
    return dumps({})


# remove the movie from my favourite.
# raise error if the movie does not exist in my favourite
# need token to identify myself
@APP.route("/favourite/delete/<movie_id>", methods=['POST'])
def remove_favourite(movie_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    favourite.remove_from_my_favourite(token, movie_id)
    return dumps({})


# get a list of user_id that favourite a movie_id
@APP.route("/favourite/who_favourite/<movie_id>", methods=['GET'])
def get_who_favourite_movie(movie_id):
    result = favourite.get_who_favourite_movie(movie_id)
    return dumps({'users': result})


########### Follow / Unfollow ###########
# obtain a list of user id that I follow
# identify myself through token
# return an array of user id, that I am following
@APP.route("/follow/me", methods=['GET'])
def get_my_following():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    users = follow.get_my_following(token)
    return dumps({"follow": users})


# check other's following list
# no need for token.
# identify using user id,
# return an array of user id
@APP.route("/follow/user/<user_id>", methods=['GET'])
def get_other_follow(user_id):
    users = follow.get_user_following(user_id)
    return dumps({"follow": users})


# check how many users follow me
@APP.route("/follow/who_follow/me", methods=['GET'])
def get_who_follow_me():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    users = follow.get_who_follow_me(token)
    return dumps({"followed_by": users})


# check how many users follow a particular user,
# use user_id to identify
@APP.route("/follow/who_follow/user/<user_id>", methods=['GET'])
def get_who_follow_that_user(user_id):
    users = follow.get_who_follow_user(user_id)
    return dumps({"followed_by": users})

# add to follow a user id
# 200 OK for success add.
# need token to identify myself


@APP.route("/follow/add/<user_id>", methods=['POST'])
def add_to_my_follow(user_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    follow.add_to_my_follow(token, user_id)
    return dumps({})


# remove a user from my following list
# raise error if the user id does not exist,
# or the user is not in my following list
# need token to identify myself
@APP.route("/follow/delete/<user_id>", methods=['POST'])
def remove_following(user_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    follow.remove_from_my_follow(token, user_id)
    return dumps({})


if __name__ == '__main__':
    APP.run(port=9002)
