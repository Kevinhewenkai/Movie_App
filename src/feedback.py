# from error import AccessError, InputError
import sqlite3
import os

from helper import get_user_from_token
cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def getfeedback():
    sqliteConnection = sqlite3.connect(db_file)
    cursor = sqliteConnection.cursor()
    # connect to sqlite3
    feedback_id_list = cursor.execute(
        'SELECT feedback_id from Feedback').fetchall()
    feedback_list = []
    for feedback_id in feedback_id_list:
        temp_list = {}
        temp_list['feedback_id'] = feedback_id[0]
        temp_list["user_id"] = cursor.execute(
            "SELECT user_id from Feedback where feedback_id = ?", (feedback_id[0],)).fetchone()[0]
        temp_list["time"] = cursor.execute(
            "SELECT time from Feedback where feedback_id = '{}'".format(feedback_id[0])).fetchone()[0]
        temp_list["description"] = cursor.execute(
            "SELECT description from Feedback where feedback_id = '{}'".format(feedback_id[0])).fetchone()[0]
        feedback_list.append(temp_list)
    return feedback_list


def insertfeedback(token, time, description):
    user = get_user_from_token(token)
    if token is None or user is None:
        return {'400': 'No such user'}
    user_id = user['user_id']
    if (type(description) != str):
        return ("invalid input")
    if (len(description) > 1000):
        return ("over maximum description limit")
    sqliteConnection = sqlite3.connect(db_file)
    cursor = sqliteConnection.cursor()
    count = cursor.execute('SELECT count(*) from Feedback').fetchone()[0]
    sql_2 = '''
            INSERT INTO Feedback(feedback_id, user_id, time, description)
            VALUES (?, ?, ?, ?)
        '''
    data = (int(count) + 1, user_id, time, description,)
    cursor.execute(sql_2, data)
    sqliteConnection.commit()
    return {'result': "successfully submit your feedback"}
