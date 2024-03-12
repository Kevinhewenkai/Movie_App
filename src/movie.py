from helper import popularity_caculation, get_user_from_token
import sqlite3
import json
import os
cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")
# this will add the movie for user


def add_Movie(token, name, country, language, description, genre):
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}
    try:
        user = get_user_from_token()
        if user is None:
            return {'400': "Please login."}
    except:
        return {'400': "Please login."}
    try:
        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        # connect to sqlite3
        cursor.execute('SELECT COUNT(*) from Movie')
        cur_result = cursor.fetchone()[0]
        generate_movieId = cur_result + 1
        # check the number row and generate a movie id by order
        cursor.execute("insert into Movie (id, name, country, language, description, genre) values (?, ?, ?, ?, ?, ?)",
                       (generate_movieId, name, country, language, description, genre))
        # insert a new movie with new generate id
        sqliteConnection.commit()
        print("Movie inserted successfully into Movie table ", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert movie into movie table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return generate_movieId


def add_MoviePhoto(token, id, photo):
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}
    try:
        user = get_user_from_token()
        if user is None:
            return {'400': "Please login."}
    except:
        return {'400': "Please login."}

    try:
        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        # connect to sqlite3
        cursor.execute('SELECT COUNT(*) from Movie_Photo')
        cur_result = cursor.fetchone()[0]
        generate_movieId = cur_result + 1
        cursor.execute("insert into Movie_Photo (id, photo) values (?, ?) where movie_id values (?)",
                       (generate_movieId, photo, id))
        # insert a new movie with new generate id
        sqliteConnection.commit()
        print("photo inserted successfully into Movie_photo table ", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert photo into Movie_pthoto table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return generate_movieId

# this will delete the  movie for user


def delete_Movie(token, movie_id):
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}
    try:
        user = get_user_from_token()
        if user is None:
            return {'400': "Please login."}
    except:
        return {'400': "Please login."}
    status = False
    try:
        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        # connect to sqlite3
        sql_update_query = """DELETE from Movie where id = ?"""
        cursor.execute(sql_update_query, (movie_id,))
        sqliteConnection.commit()
        status = True
        print("movie deleted successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete movie from a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")
    return status


def delete_MoviePhoto(token, photo_id):
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}
    try:
        user = get_user_from_token()
        if user is None:
            return {'400': "Please login."}
    except:
        return {'400': "Please login."}
    status = False
    try:
        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        # connect to sqlite3
        sql_update_query = """DELETE from Movie_Photo where id = ?"""
        cursor.execute(sql_update_query, (photo_id,))
        sqliteConnection.commit()
        status = True
        print("MoviePhoto deleted successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete MoviePhoto from MoviePhoto table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")
    return status


def update_Movie(token, id, name, country, language, description, genre):
    # check if user is logged in
    if token is None:
        return {'400': "Please login."}
    try:
        user = get_user_from_token()
        if user is None:
            return {'400': "Please login."}
    except:
        return {'400': "Please login."}
    status = False

    try:
        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        # connect to sqlite3
        sql_update_query = """Update Movies set name = ?, country = ?, language = ?, description = ?, genre = ? where id = ?"""
        data = (name, country, language, description, genre, id)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        status = True
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return status


def get_AllMovie_id():
    conn = sqlite3.connect(db_file)
    # conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    cursor = conn.cursor()

    Movies = cursor.execute('''SELECT movie_id from Movie''').fetchall()
    movie_ids = {}
    movie_ids["movie_ids"] = []
    for movie_id in Movies:
        movie_ids["movie_ids"].append(movie_id[0])
    conn.commit()
    conn.close()
    # DEBUG
    # print(movie_ids)
    return movie_ids  # CREATE JSON


def get_AllMovie():
    conn = sqlite3.connect(db_file)
    # conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    cursor = conn.cursor()

    Moives = cursor.execute('''SELECT * from Movie''').fetchall()
    for movie in Moives:
        Movie_photo = cursor.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie[0]))
        movie['Movie_photo'] = Movie_photo
    conn.commit()
    conn.close()

    return Moives  # CREATE JSON


def get_ThisMovie(Movie_id, token):
    user = get_user_from_token(token)
    if user is not None:
        user_id = user['user_id']
    else:
        user_id = None
    conn = sqlite3.connect(db_file)
    # conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    cursor = conn.cursor()

    Movie = cursor.execute(
        "SELECT * from Movie where movie_id = '{}' ".format(Movie_id)).fetchone()
    Movie_photo = cursor.execute(
        "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(Movie_id)).fetchone()
    Movie_Director_id_list = cursor.execute(
        "SELECT director_id FROM Direct_Movie where movie_id = '{}' ".format(Movie_id)).fetchall()
    Movie_Director_list = []
    Movie_Actor_list = []
    for Movie_Drector_id in Movie_Director_id_list:
        Movie_Director_list.append(cursor.execute(
            "SELECT name FROM Director where director_id = '{}' ".format(Movie_Drector_id[0])).fetchone()[0])
    Movie_Actor_id_list = cursor.execute(
        "SELECT actor_id FROM Cast_Movie where movie_id = '{}' ".format(Movie_id)).fetchall()
    for Movie_Actor_id in Movie_Actor_id_list:
        Movie_Actor_list.append(cursor.execute(
            "SELECT name FROM Actor where actor_id = '{}' ".format(Movie_Actor_id[0])).fetchone()[0])
    Movie_Popularity = popularity_caculation(Movie_id)
    #Moive['Movie_photo'] = Movie_photo
    result = {}
    result["id"] = Movie[0]
    result["name"] = Movie[6]
    result["country"] = Movie[1]
    result["language"] = Movie[2]
    result["description"] = Movie[3]
    result["genre"] = (Movie[4]).split(',')
    print(result["genre"])
    result["year"] = int(Movie[5])
    result["popularity"] = Movie_Popularity
    result["movie_photo"] = Movie_photo[0] if Movie_photo is not None else []
    result["Director"] = Movie_Director_list
    result["Actor"] = Movie_Actor_list

    if user_id is not None:
        cursor.execute('''
            INSERT INTO ReviewHistory(user_id, movie_id) VALUES (?,?)
        ''', (user_id, Movie_id,))

    conn.commit()
    conn.close()
    # DEBUG
    # print(result)
    # print(Movie_photo)
    return result  # CREATE JSON


def get_Movie_By_Actor(Actor_id):
    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()

    Movies = cursor.execute("SELECT Movie_id from Cast_Movie where actor_id = '{}' ".format(
        Actor_id)).fetchall()  # find out this actor and take out the movie list
    list = {}
    for Movie in Movies:
        tmp = {}
        tmp['movie_id'] = []
        tmp["movie_id"] = Movie[0]
        tmp["photo"] = []
        Movie_photo = cursor.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(Movie[0])).fetchone()
        tmp["photo"].append(Movie_photo[0])
        list[Movie[0]] = tmp

    conn.commit()
    conn.close()
    return json.dumps(list)  # CREATE JSON


def get_Movie_By_Director(Director_id):
    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()

    Movies = cursor.execute("SELECT Movie_id from Direct_Movie where director_id = '{}' ".format(
        Director_id)).fetchall()  # find out this director and take out the movie list
    list = {}
    for Movie in Movies:
        tmp = {}
        tmp['movie_id'] = []
        tmp["movie_id"] = Movie[0]
        tmp["photo"] = []
        Movie_photo = cursor.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(Movie[0])).fetchone()
        tmp["photo"].append(Movie_photo[0])
        list[Movie[0]] = tmp

    print(list)
    conn.commit()
    conn.close()
    return list  # CREATE JSON


def get_Movie_By_Genre(Genre):
    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()

    Movies = cursor.execute("SELECT Movie_id from Movie where Genre = '{}' ".format(
        Genre)).fetchall()  # find out this director and take out the movie list
    list = {}
    for Movie in Movies:
        tmp = {}
        tmp['movie_id'] = []
        tmp["movie_id"] = Movie[0]
        tmp["photo"] = []
        Movie_photo = cursor.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(Movie[0])).fetchone()
        tmp["photo"].append(Movie_photo[0])
        list[Movie[0]] = tmp
    # take movies from each movie_id and add the movie photo to the list

    conn.commit()
    conn.close()
    return json.dumps(list)  # CREATE JSON


def get_lastestsix_id():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    list = {}
    Movies = cursor.execute(
        '''SELECT movie_id from Movie ORDER BY year DESC''').fetchall()
    # print(Movies)
    i = 0
    while i < 6:
        # print(Movies[i][0])
        tmp = {}
        tmp['movie_id'] = []
        tmp["movie_id"] = Movies[i][0]
        tmp["photo"] = []

        Movie_photo = cursor.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(Movies[i][0])).fetchone()
        tmp["photo"].append(Movie_photo[0])
        # print(tmp)
        list[i] = tmp
        i = i + 1

    conn.commit()
    conn.close()

    return list  # CREATE JSON
