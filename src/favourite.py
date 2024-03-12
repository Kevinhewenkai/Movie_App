import os
import sqlite3
from helper import get_user_from_token
from flask import abort


cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def get_my_favourite(token):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")

    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i]
                                         for i, c in enumerate(C.description)}
        cur = conn.cursor()

        # join with Movie table to get all existing movies
        sql_select = """
            SELECT DISTINCT Favourite_Movie.movie_id 
            FROM Favourite_Movie NATURAL JOIN Movie
            WHERE Favourite_Movie.user_id = ?
            ORDER BY Favourite_Movie.movie_id
        """
        param = (user["user_id"],)

        cur.execute(sql_select, param)
        movies = cur.fetchall()
        result = [movie["movie_id"] for movie in movies]
        return result


def get_user_favourite(user_id):
    # the user id should be integer
    try:
        user_id = int(user_id)
    except ValueError:
        abort(400, description="user_id should be an integer")

    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i]
                                         for i, c in enumerate(C.description)}
        cur = conn.cursor()

        # check if the user_id exists
        sql = "SELECT * FROM User WHERE user_id = ?"
        param = (user_id,)
        cur.execute(sql, param)
        user = cur.fetchone()

        if not user:
            abort(400, description="The user id does not exist")

        # now obtain the user's banlist
        sql_select = """
            SELECT DISTINCT Favourite_Movie.movie_id 
            FROM Favourite_Movie NATURAL JOIN Movie
            WHERE Favourite_Movie.user_id = ?
            ORDER BY Favourite_Movie.movie_id
        """
        param = (user_id,)
        cur.execute(sql_select, param)
        movies = cur.fetchall()
        result = [movie["movie_id"] for movie in movies]
        return result


def add_to_my_favourite(token, movie_id):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")

    # the movie_id should be an integer
    try:
        movie_id = int(movie_id)
    except ValueError:
        abort(400, description="The movie_id should be an integer")

    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i]
                                         for i, c in enumerate(C.description)}
        cur = conn.cursor()

        # the movie_id should exist in the database
        sql_select = """SELECT * FROM Movie WHERE movie_id = ?"""
        param = (movie_id,)
        cur.execute(sql_select, param)
        result = cur.fetchone()

        if not result:
            abort(400, description="The movie_id does not exist")

        # now insert into the new relationship into the database
        # use insert or ignore to avoid duplicate
        sql_insert = "INSERT OR IGNORE INTO Favourite_Movie(user_id, movie_id) VALUES (?, ?)"
        param = (user["user_id"], movie_id)
        cur.execute(sql_insert, param)


def remove_from_my_favourite(token, movie_id):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")

    # the movie_id should be an integer
    try:
        movie_id = int(movie_id)
    except ValueError:
        abort(400, description="The movie_id should be an integer")

    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i]
                                         for i, c in enumerate(C.description)}
        cur = conn.cursor()

        # delete straightaway
        sql = "DELETE FROM Favourite_Movie WHERE user_id = ? AND movie_id = ?"
        param = (user["user_id"], movie_id)
        cur.execute(sql, param)

        if cur.rowcount < 1:
            abort(400, description="The movie_id is not in the favourite")


def get_who_favourite_movie(movie_id):
    # the movie_id should be an integer
    try:
        movie_id = int(movie_id)
    except ValueError:
        abort(400, description="The movie_id should be an integer")

    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i]
                                         for i, c in enumerate(C.description)}
        cur = conn.cursor()

        sql = """
            SELECT DISTINCT Favourite_Movie.user_id
            FROM Favourite_Movie
            WHERE Favourite_Movie.movie_id = ?
            ORDER BY Favourite_Movie.user_id
        """

        param = (movie_id,)
        cur.execute(sql, param)
        users = cur.fetchall()
        result = [u['user_id'] for u in users]
        return result
