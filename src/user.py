import os
import sqlite3
from helper import get_user_from_token
from flask import abort


cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def get_my_profile(token):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")

    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i]
                                         for i, c in enumerate(C.description)}
        cur = conn.cursor()

        sql = """
            SELECT user_id, name as user_name, 
            email, complaint_count, user_photo
            FROM User
            WHERE user_id = ?
        """

        cur.execute(sql, (user['user_id'],))
        result = cur.fetchone()
        return result


def get_profile_id(user_id):
    # check the user id should be an integer
    try:
        user_id = int(user_id)
    except ValueError as e:
        abort(400, description="User id should be in integer")

    # get the user from the file
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = lambda C, R: {c[0]: R[i]
                                         for i, c in enumerate(C.description)}
        cur = conn.cursor()

        sql_select = """
            SELECT user_id, name as user_name, email,
            complaint_count, user_photo
            FROM User 
            WHERE user_id = ?
        """
        param = (user_id,)

        cur.execute(sql_select, param)
        user = cur.fetchone()

        if not user:
            abort(400, "The user id does not exist")
        else:
            return user


def update_my_profile(token, payload):
    user = get_user_from_token(token)
    if user is None:
        abort(403, description="Invalid token")
    user_name = payload['user_name']
    # update the value
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()

        sql_select = "UPDATE User SET name = ? WHERE user_id = ?"
        param = (user_name, user["user_id"],)
        cur.execute(sql_select, param)
        conn.commit()
    return {"result": "success"}
