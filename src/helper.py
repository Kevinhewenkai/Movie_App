import sqlite3
import os
import secrets

cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def get_user_from_token(token):
    # build connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # find user
    users = cursor.execute(
        "SELECT * from User WHERE token = ?", (token,)
    ).fetchone()
    # DEBUG
    # print(users)
    connection.commit()
    # User token does not exists: user not login
    if users == None:
        return None
    # close connection
    connection.close()
    # return result
    user = {}
    user['user_id'] = users[0]
    user['user_name'] = users[1]
    user['password'] = users[2]
    user['email'] = users[3]
    user['token'] = users[4]
    return user


def gen_token():
    return secrets.token_urlsafe(16)


def popularity_caculation(movie_id):
    sqliteConnection = sqlite3.connect(db_file)
    cursor = sqliteConnection.cursor()
    # connect to sqlite3
    count_comment = cursor.execute(
        "SELECT COUNT(review) from Review where movie_id = '{}'".format(movie_id)).fetchone()
    count_add_wishlist = cursor.execute(
        "SELECT COUNT(*) from Wishlist_movies where movie_id = '{}'".format(movie_id)).fetchone()
    comment_all = cursor.execute(
        "SELECT COUNT(review) from Review ").fetchone()
    add_wishlist_all = cursor.execute(
        "SELECT COUNT(*) from Wishlist ").fetchone()

    if comment_all[0] == 0:
        percentage_commet = count_comment[0] / comment_all[0]
    else:
        percentage_commet = 0
    # print(percentage_commet)
    if add_wishlist_all[0] != 0:
        percentage_wishlist = count_add_wishlist[0] / add_wishlist_all[0]
    else:
        percentage_wishlist = 0

    # print(percentage_wishlist)
    popularity = count_comment[0] + count_add_wishlist[0]

    return popularity


def get_banned_list(token):
    if token == 'None':
        return None
    user = get_user_from_token(token)
    if user is None:
        return None
    user_id = user['user_id']
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    banned_user = cursor.execute(
        '''
        SELECT ban_user_id FROM Banlist WHERE user_id = ?''', (user_id,)
    ).fetchall()
    res = []
    for u in banned_user:
        res.append(u[0])
    return res
