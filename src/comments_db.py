import os
import sqlite3


cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def get_all_review_by_movie(movie_id):
    # Connect database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Get the movie by movie id
    try:
        reviews = cursor.execute(
            "SELECT review_id, review, rating, added_on, user_id FROM Review where movie_id = '{}'".format(movie_id)).fetchall()
        connection.commit()
        output = []
        for review in reviews:
            review_id = review[0]
            review_context = review[1]
            rating = review[2]
            added_on = review[3]
            user_id = review[4]
            review_info = {
                'review_id': review_id,
                'review': review_context,
                'rating': rating,
                'added_on': added_on,
                'user_id': user_id,
            }
            # print(review_info)
            output.append(review_info)
    except:
        return {'400': "No such movie"}
    finally:
        # Close the connection
        connection.close()
    # Return the result
    return output


def add_review(user_id, movie_id, review, rating, added_on):
    # build connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # add review
    review_id = None
    try:
        cursor.execute(
            """INSERT INTO Review(user_id, movie_id, review, rating, added_on) 
            VALUES (?,?,?,?,?)""", (user_id, movie_id, review, rating, added_on))
        connection.commit()
        # find review id
        review_id = cursor.execute(
            """SELECT * FROM Review WHERE review = ? AND user_id = ? AND movie_id = ? AND rating = ? AND added_on = ?""", (
                review, user_id, movie_id, rating, added_on)
        ).fetchone()[0]
    except:
        return {'400': "Cannot find review by ID"}
    # close connection
    cursor.close()
    return review_id


def get_review_by_review_id(review_id):
    # build connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # find review
    review = cursor.execute(
        "SELECT review, rating, added_on, user_id FROM Review WHERE review_id = ?",
        (review_id,)
    ).fetchone()
    connection.commit()
    user_id = cursor.execute(
        '''
        SELECT user_id from User where user_id = ?''', (review[3],)
    ).fetchone()[0]
    name = cursor.execute(
        '''
        SELECT name from User where user_id = ?''', (review[3],)
    ).fetchone()[0]
    result = {
        'review': review[0],
        'rating': review[1],
        'added_on': review[2],
        'user_id': user_id,
        'user_name': name,
    }

    # close connection
    cursor.close()
    return result


def update_reveiw(review_id, review, rating, added_on):
    # build connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # find review
    review = cursor.execute(
        """UPDATE Review SET review=?,rating=?,added_on=? WHERE review_id = ?""",
        (review, rating, added_on, review_id,)
    )
    connection.commit()
    # close connection
    cursor.close()
    return review_id


def delete_reveiw(review_id):
    # build connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    try:
        # delete review
        cursor.execute(
            "DELETE FROM Review \
            WHERE review_id = ?",
            (review_id,)
        )
        connection.commit()
    except:
        cursor.close()
        return False
    # close connection
    cursor.close()
    return True


# def get_all_review_by_user():
#     # build connection
#     connection = sqlite3.connect(db_file)
#     cursor = connection.cursor()
#     #
#     connection.commit()
#     # close connection
#     cursor.close()
#     return None
