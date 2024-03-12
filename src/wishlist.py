from helper import get_user_from_token
import os
import sqlite3

cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def get_wishlists(token):
    user = get_user_from_token(token)
    user_id = user['user_id']
    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # check the wishlist in list
    wishlists = cursor.execute(
        '''
        SELECT DISTINCT wishlist_id from Wishlist WHERE user_id = ?
        ''', (user_id,)
    ).fetchall()
    connection.commit()
    # get the list id as result
    result = []
    for wishlist in wishlists:
        result.append(wishlist[0])
    connection.close()
    return {'list_id': result}


def get_wishlists_by_user_id(user_id):
    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # check if user_id exists
    try:
        cursor.execute('''SELECT * from User WHERE user_id = ?''',
                       (user_id, )).fetchone()
        connection.commit()
    except:
        connection.close()
        return {'400': 'No user_id exist in database'}
    # get wishlist by user_id
    wishlists = cursor.execute(
        '''
        SELECT wishlist_id FROM Wishlist WHERE user_id = ? AND status = 0
        ''', (user_id, )
    ).fetchall()
    # extract wishlists
    result = []
    for wishlist in wishlists:
        result.append(wishlist[0])
    # return wishlists
    connection.close()
    return {'list_id': result}


def get_wishlist_by_id(list_id, token):
    user = get_user_from_token(token)
    user_id = user['user_id']
    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # check if user have access
    status = cursor.execute(
        '''
        SELECT status, user_id FROM Wishlist WHERE wishlist_id = ?
        ''', (list_id, )
    ).fetchone()
    if int(status[0]) == 1 and int(user_id) != status[0]:
        return {'400': 'No access to this wishlist.'}
    # get wishlist
    wishlists = cursor.execute(
        '''SELECT movie_id, added_on FROM Wishlist_movies WHERE wishlist_id = ?''',
        (list_id, )).fetchall()
    connection.commit()
    # build result
    movies = []
    for wishlist in wishlists:
        movies.append(wishlist[0])
    list_info = cursor.execute(
        '''
        SELECT list_name, user_id FROM Wishlist WHERE wishlist_id = ?
        ''', (list_id, )
    ).fetchone()
    connection.commit()
    if list_info is None:
        return {'400': 'No such wishlist exist'}
    result = {
        'list_name': list_info[0],
        'movies': movies,
        'user_id': list_info[1],
    }
    return result


def build_wishlist(list_name, token, status):
    # Check if token valid
    user = get_user_from_token(token)
    user_id = user['user_id']

    # Check if the name duplicated
    # if check_list_exists_by_list_name(list_name, user_id):
    #     return {'400': "List name already exists"}

    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Build the list for user
    cursor.execute(
        '''
        INSERT INTO Wishlist(user_id, list_name, status, likes)
        VALUES (?,?,?, ?)
        ''', (user_id, list_name, status, 0)
    )
    connection.commit()

    # get the new list id
    list_id = cursor.execute(
        '''SELECT wishlist_id FROM Wishlist WHERE user_id = ? AND list_name = ?
        ''', (user_id, list_name,)
    ).fetchone()
    connection.close()
    return {'list_id': list_id[0]}


def destroy_wishlist(list_id, token):
    # Check if user logged in
    user = get_user_from_token(token)
    user_id = user['user_id']
    # Check if list exists
    if not check_list_exists_by_list_id(list_id):
        return {'400': "Wishlist does not exists"}
    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Check if user have access
    wishlist = cursor.execute(
        '''
        SELECT user_id, list_name FROM Wishlist WHERE wishlist_id = ?
        ''', (list_id,)
    ).fetchone()
    connection.commit()
    if wishlist is None:
        return {'400': 'No such wishlist exist'}
    if int(wishlist[0]) != int(user_id):
        return {'400': "No access to delete wishlist."}
    if wishlist[1] == 'fav movies':
        print(wishlist[1])
        return {'400': "You cannot delete the 'fav movies'"}

    # Delete the wishlist
    try:
        cursor.execute(
            '''
            DELETE FROM Wishlist_movies WHERE wishlist_id = ?
            ''', (list_id,)
        )
        connection.commit()
        cursor.execute(
            '''
            DELETE FROM Wishlist WHERE wishlist_id = ?
            ''', (list_id,)
        )
        connection.commit()
        return {'200': 'success'}
    except:
        return {'400': 'Deletion failed.'}


def change_list_name(list_id, token, new_list_name):
    # Check if user exist
    user = get_user_from_token(token)
    user_id = user['user_id']
    # Check if list exists
    if not check_list_exists_by_list_id(list_id):
        return {'400': "Wishlist does not exists"}

    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Check if user has correct identity
    res = cursor.execute('''
        SELECT user_id, list_name from Wishlist WHERE wishlist_id = ?
    ''', (list_id,)).fetchone()
    connection.commit()
    if int(res[0]) != int(user_id):
        return {'400': "User have no access to change the list name"}
    if res[1] == 'fav movies':
        return {'400': "You cannot change the name of fav movies"}
    # Change the name for user
    cursor.execute('''
        UPDATE Wishlist SET list_name=? WHERE wishlist_id=?
    ''', (new_list_name, list_id,))
    connection.commit()
    connection.close()

    return {'200': 'success'}


def add_to_wishlist(list_id, token, movie_id):
    # Check if wishlist is exist
    if not check_user_availbility(token, list_id):
        return {'400': 'User has no access'}

    # Check if movie already exists
    if movie_in_wishlist_by_id(token, list_id, movie_id):
        return {'400': "Movie already in wishlist"}

    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Add to wishlist
    cursor.execute('''
    INSERT INTO Wishlist_movies(wishlist_id, movie_id, added_on) VALUES (?, ?, ?)
    ''', (list_id, movie_id, 0,))
    connection.commit()
    connection.close()
    return {'200': 'success'}


def delete_from_wishlist(token, list_id, movie_id):
    # Check if wishlist is exist
    if not check_user_availbility(token, list_id):
        return {'400': 'User has no access'}

    # Check if wishlist is exist
    if not check_list_exists_by_list_id(list_id):
        return {'400': "Wishlist does not exists"}

    # Check if movie in list
    if not movie_in_wishlist_by_id(token, list_id, movie_id):
        return {'400': "Movie does not exist in wishlist"}

    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Remove movie from list
    cursor.execute(''' DELETE FROM Wishlist_movies WHERE wishlist_id = ? AND movie_id = ?
    ''', (list_id, movie_id,))
    connection.commit()
    connection.close()
    return {'200': 'success'}


def change_wishlist_private(token, list_id, status):
    # Check if wishlist is exist
    if not check_user_availbility(token, list_id):
        return {'400': 'User has no access'}

    # Connect to database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    res = cursor.execute('''
        SELECT list_name from Wishlist WHERE wishlist_id = ?
    ''', (list_id,)).fetchone()
    connection.commit()
    if res[0] == 'fav movies':
        return {'400': "You cannot change the permission of fav movies"}
    # Change wishlist status
    cursor.execute(
        '''
        UPDATE Wishlist SET status=? WHERE wishlist_id = ?
        ''', (status, list_id))
    connection.commit()
    connection.close()
    return {'200': 'success'}


def get_wishlist_status(token, list_id):
    # Check if wishlist is exist
    if not check_user_availbility(token, list_id):
        return 1
    # Connect to database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Check wishlist status
    status = cursor.execute(
        '''
        SELECT status FROM Wishlist WHERE wishlist_id = ?
        ''', (list_id,)).fetchone()
    connection.commit()
    connection.close()
    return status[0]


######## helper function ########


def movie_in_wishlist_by_id(token, list_id, movie_id):
    # Check if movie is duplicated
    wishlist = get_wishlist_by_id(list_id, token)
    if movie_id in wishlist['movies']:
        return True
    return False


def movie_in_wishlist_by_name(token, list_id, movie_name):
    # Check if movie is duplicated
    wishlist = get_wishlist_by_id(list_id, token)
    for movie in wishlist['movies']:
        if movie_name is movie['movie_name']:
            return True
    return False


def check_list_exists_by_list_id(list_id):
    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # check if list_id exist
    try:
        cursor.execute(
            '''
            SELECT * FROM Wishlist WHERE wishlist_id = ?
            ''', (list_id,)
        )
    except:
        connection.close()
        return False
    connection.close()
    return True


def check_list_exists_by_list_name(list_name, user_id):
    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # get all the wishlist name
    try:
        cursor.execute(
            '''
            SELECT * FROM Wishlist WHERE list_name = ? AND user_id = ?
            ''', (list_name, user_id)
        ).fetchall()
    except:
        connection.close()
        return False
    connection.close()
    return True


def check_user_availbility(token, list_id):
    # Check if user exist
    user = get_user_from_token(token)
    user_id = user['user_id']
    # Check if list exists
    if not check_list_exists_by_list_id(list_id):
        return {'400': "Wishlist does not exists"}

    # connect to databse
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Check if user has correct identity
    res = cursor.execute('''
        SELECT user_id from Wishlist WHERE wishlist_id = ?
    ''', (list_id,)).fetchone()
    connection.commit()
    if int(res[0]) != int(user_id):
        return False
    return True
