import os 
import sqlite3
from helper import get_user_from_token
from flask import abort


cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


# helper function
def check_valid_user_id(user_id):
    # the user_id should be an integer
    try:
        user_id = int(user_id)
    except ValueError:
        abort(400, "The user_id should be an integer")
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
        cur = conn.cursor()

        # the user_id should exist in the database
        sql_select = "SELECT * FROM User WHERE user_id = ?"
        param = (user_id,)
        cur.execute(sql_select, param)
        result = cur.fetchone()
        
        if not result:
            abort(400, "The user_id does not exist")


def get_my_following(token):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
        cur = conn.cursor()

        # join with User table
        sql_select = """
            SELECT DISTINCT Follow.follow_user_id 
            FROM Follow INNER JOIN User On Follow.follow_user_id = User.user_id
            WHERE Follow.user_id = ?
            ORDER BY Follow.follow_user_id
        """
        
        param = (user["user_id"],)
        cur.execute(sql_select, param)
        users = cur.fetchall()
        result = [u['follow_user_id'] for u in users]
        return result


def get_user_following(user_id):
    check_valid_user_id(user_id)
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
        cur = conn.cursor()
        
        sql_select = """
            SELECT Distinct Follow.follow_user_id
            FROM Follow INNER JOIN User On Follow.follow_user_id = User.user_id
            WHERE Follow.user_id = ?
            ORDER BY Follow.follow_user_id
        """
        
        param = (user_id,)
        cur.execute(sql_select, param)
        users = cur.fetchall()
        result = [u['follow_user_id'] for u in users]
        return result


def get_who_follow_me(token):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
        cur = conn.cursor()
        
        sql_select = """
            SELECT Distinct Follow.user_id
            FROM Follow INNER JOIN User On Follow.user_id= User.user_id
            WHERE Follow.follow_user_id = ?
            ORDER BY Follow.user_id
        """
        
        param = (user['user_id'],)
        cur.execute(sql_select, param)
        users = cur.fetchall()
        result = [u['user_id'] for u in users]
        return result


def get_who_follow_user(user_id):
    check_valid_user_id(user_id)
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
        cur = conn.cursor()
        
        sql_select = """
            SELECT Distinct Follow.user_id
            FROM Follow INNER JOIN User On Follow.user_id= User.user_id
            WHERE Follow.follow_user_id = ?
            ORDER BY Follow.user_id
        """
        
        param = (user_id,)
        cur.execute(sql_select, param)
        users = cur.fetchall()
        result = [u['user_id'] for u in users]
        return result


def add_to_my_follow(token, user_id):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")

    check_valid_user_id(user_id)
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
        cur = conn.cursor()
    
        # now insert into the new relationship into the database
        # use insert or ignore to avoid duplicate
        sql_insert = "INSERT OR IGNORE INTO Follow(user_id, follow_user_id) VALUES (?, ?)"
        param = (user["user_id"], user_id)
        cur.execute(sql_insert, param)


def remove_from_my_follow(token, user_id):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")
    
    check_valid_user_id(user_id)
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)}
        cur = conn.cursor()

        # delete straightaway
        sql = "DELETE FROM Follow WHERE user_id = ? AND follow_user_id = ?"
        param = (user["user_id"], user_id)
        cur.execute(sql, param)
        
        if cur.rowcount < 1:
            abort(400, "The user_id is not in your follow list")
