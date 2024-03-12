# simple search
from re import A
import sqlite3
import os
import helper
cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def search(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where name like '%{}%'".format(keyword)).fetchall()

    movie_all_list = []

    for movie_id in Movie_ids:
        movie_list = {}
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        # print(Movie_name[0])
        movie_list["movie_name"] = Movie_name[0]
        movie_list["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_list["photo"] = Movie_photo[0]
        movie_all_list.append(movie_list)

    print(movie_all_list)
    if(movie_all_list is not None):
        #All_sorted = dict(sorted(All.items()))

        conn.commit()
        conn.close()
        # DEBUG
        # print(movie_ids)
    return movie_all_list  # CREATE JSON
# def get_movie_SortByName(keyword):
#     conn = sqlite3.connect(db_file)
#     c = conn.cursor()
#     Movie_ids = c.execute("SELECT movie_id from Movie where name like '%{}%' order by name".format(keyword)).fetchall()
#     movie_list = {}
#     for movie_id in Movie_ids:
#         Movie_name = c.execute("SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
#         #print(Movie_name[0])
#         movie_list[Movie_name[0]] = {}
#         movie_list[Movie_name[0]]["movie_id"] = movie_id[0]
#         Movie_photo = c.execute("SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
#         movie_list[Movie_name[0]]["photo"] = Movie_photo[0]
#     movie_sorted = dict(sorted(movie_list.items()))
#     conn.commit()
#     conn.close()
#     return movie_sorted


def get_movie_Reviews(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    Reviews = c.execute(
        "SELECT review from Review where review like '%{}%' ".format(keyword)).fetchall()

    Review_list = {}

    for review in Reviews:
        review_id = c.execute("SELECT review_id from Review where review = '{}'".format(
            review[0])).fetchone()[0]
        Review_list[review_id] = {}
        movie_id = c.execute(
            "SELECT movie_id from Review where review = '{}'".format(review[0])).fetchone()
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        Review_list[review_id]["movie_name"] = []
        Review_list[review_id]["movie_name"].append(Movie_name[0])
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        Review_list[review_id]["movie_photo"] = []
        Review_list[review_id]["movie_photo"].append(Movie_photo[0])

    conn.commit()
    conn.close()
    return Review_list


def get_movie_SortByGenre(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    movie_list = {}
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where genre like '%{}%' order by genre".format(keyword)).fetchall()
    for movie_id in Movie_ids:
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        # print(Movie_name[0])
        movie_list[Movie_name[0]] = {}
        movie_list[Movie_name[0]]["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_list[Movie_name[0]]["photo"] = Movie_photo[0]
    movie_sorted = dict(sorted(movie_list.items()))
    conn.commit()
    conn.close()
    return movie_sorted


def get_movie_SortByCountry(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    movie_list = {}
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where country like '%{}%' order by country".format(keyword)).fetchall()
    for movie_id in Movie_ids:
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        # print(Movie_name[0])
        movie_list[Movie_name[0]] = {}
        movie_list[Movie_name[0]]["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_list[Movie_name[0]]["photo"] = Movie_photo[0]
    movie_sorted = dict(sorted(movie_list.items()))
    conn.commit()
    conn.close()
    return movie_sorted


def get_movie_SortByLanguage(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    movie_list = {}
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where language like '%{}%' order by language".format(keyword)).fetchall()
    for movie_id in Movie_ids:
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        # print(Movie_name[0])
        movie_list[Movie_name[0]] = {}
        movie_list[Movie_name[0]]["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_list[Movie_name[0]]["photo"] = Movie_photo[0]
    movie_sorted = dict(sorted(movie_list.items()))
    conn.commit()
    conn.close()
    return movie_sorted


def get_movie_SortByName(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    movie_list = []
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where name like '%{}%' order by name".format(keyword)).fetchall()
    for movie_id in Movie_ids:
        movie_dic = {}
        film_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_dic["movie_name"] = film_name[0]
        movie_dic["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_dic["photo"] = Movie_photo[0]
        movie_list.append(movie_dic)

    conn.commit()
    conn.close()
    # print(movie_sorted)
    return movie_list


def get_movie_SortByYear(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    movie_list = []
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where name like '%{}%' order by year DESC".format(keyword)).fetchall()
    for movie_id in Movie_ids:
        movie_dic = {}

        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_dic["movie_name"] = Movie_name[0]
        # print(Movie_name[0])

        movie_dic["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_dic["photo"] = Movie_photo[0]
        movie_list.append(movie_dic)

    conn.commit()
    conn.close()
    return movie_list


def get_movie_SortByPpularity(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    movie_list = []
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where name like '%{}%'".format(keyword)).fetchall()
    for movie_id in Movie_ids:
        movie_dic = {}
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        # print(Movie_name[0])
        movie_dic["movie_name"] = Movie_name[0]
        popularity = helper.popularity_caculation(movie_id[0])
        movie_dic["popularity"] = popularity
        movie_dic["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_dic["photo"] = Movie_photo[0]
        movie_list.append(movie_dic)
    movie_sorted = sorted(
        movie_list, key=lambda x: x['popularity'], reverse=True)
    conn.commit()
    conn.close()
    return movie_sorted


def get_movie_SortByRate(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    Movie_ids_1 = c.execute(
        "SELECT movie_id from Movie where name like '%{}%'".format(keyword)).fetchall()
    Movie_ids_2 = c.execute(
        "SELECT movie_id from Review order by rating".format(keyword)).fetchall()
    Movie_1 = []
    Movie_2 = []
    for e in Movie_ids_1:
        Movie_1.append(e[0])
    for a in Movie_ids_2:
        Movie_2.append(a[0])
    Movie_ids = sorted(set(Movie_1) & set(Movie_2), key=Movie_2.index)
    print(Movie_ids)
    movie_list = []
    for movie_id in Movie_ids:
        movie_dic = {}
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id)).fetchone()
        # print(Movie_name[0])
        # movie_list[Movie_name[0]] = {}
        movie_dic["movie_name"] = Movie_name[0]
        # movie_list[Movie_name[0]]["movie_id"] = movie_id
        movie_dic["movie_id"] = movie_id
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id)).fetchone()
        # movie_list[Movie_name[0]]["photo"] = Movie_photo[0]
        movie_dic["photo"] = Movie_photo[0]
        movie_list.append(movie_dic)
    # movie_sorted = dict(sorted(movie_list,reverse = True))
    # movie_sorted = sorted(movie_list,reverse = True)
    conn.commit()
    conn.close()
    return movie_list


def get_movie_SortByDescription(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    movie_list = {}
    Movie_ids = c.execute(
        "SELECT movie_id from Movie where description like '%{}%' order by description".format(keyword)).fetchall()
    for movie_id in Movie_ids:
        Movie_name = c.execute(
            "SELECT name FROM Movie where movie_id = '{}' ".format(movie_id[0])).fetchone()
        # print(Movie_name[0])
        movie_list[Movie_name[0]] = {}
        movie_list[Movie_name[0]]["movie_id"] = movie_id[0]
        Movie_photo = c.execute(
            "SELECT photo FROM Movie_Photo where movie_id = '{}' ".format(movie_id[0])).fetchone()
        movie_list[Movie_name[0]]["photo"] = Movie_photo[0]
    movie_sorted = dict(sorted(movie_list.items(), reverse=True))
    conn.commit()
    conn.close()
    return movie_sorted


def get_Director_SortByDirector(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    director_list = {}
    Director_ids = c.execute(
        "SELECT director_id from Director where name like '%{}%' order by name".format(keyword)).fetchall()
    for director_id in Director_ids:
        director_name = c.execute(
            "SELECT name FROM Director where director_id = '{}' ".format(director_id[0])).fetchone()
        director_list[director_name[0]] = {}
        director_list[director_name[0]]["director_id"] = director_id[0]
        director_photo = c.execute(
            "SELECT photo FROM Director where director_id = '{}' ".format(director_id[0])).fetchone()
        director_list[director_name[0]]["photo"] = director_photo[0]
    director_sorted = dict(sorted(director_list.items()))
    conn.commit()
    conn.close()
    return director_sorted


def get_Actor_SortByActor(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    actor_list = {}
    Actor_ids = c.execute(
        "SELECT actor_id from Actor where name like '%{}%' order by name".format(keyword)).fetchall()
    for actor_id in Actor_ids:
        actor_name = c.execute(
            "SELECT name FROM Actor where actor_id = '{}' ".format(actor_id[0])).fetchone()
        actor_list[actor_name[0]] = {}
        actor_list[actor_name[0]]["actor_id"] = actor_id[0]
        actor_photo = c.execute(
            "SELECT photo FROM Actor where actor_id = '{}' ".format(actor_id[0])).fetchone()
        actor_list[actor_name[0]]["photo"] = actor_photo[0]
    actor_sorted_sorted = dict(sorted(actor_list.items()))
    conn.commit()
    conn.close()
    return actor_sorted_sorted


def get_Movie_Wishlist(keyword):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    wishlist_list = []

    Wishlist_id_list = c.execute(
        "SELECT wishlist_id from Wishlist where list_name like '%{}%' order by list_name".format(keyword)).fetchall()

    for wishlist_id in Wishlist_id_list:
        #movie_list = {}
        #user_id = c.execute("SELECT user_id from Wishlist where wishlist_id = '{}'".format(wishlist_id[0])).fetchone()
        #Movie_id = c.execute("SELECT movie_id from Wishlist_movies where wishlist_id = '{}'".format(wishlist_id[0])).fetchone()
        #movie_name = c.execute("SELECT name FROM Movie where movie_id = '{}' ".format(Movie_id[0])).fetchone()
        #movie_list[movie_name[0]] = {}
        #movie_list[movie_name[0]]["movie_id"] = Movie_id[0]
        #movie_photo = c.execute("SELECT photo FROM Movie where movie_id = '{}' ".format(Movie_id[0])).fetchone()
        #movie_list[movie_name[0]]["photo"] = movie_photo[0]
        #wishlist_list[user_id[0]] = movie_list
        wishlist_list.append(wishlist_id)
    conn.commit()
    conn.close()
    return wishlist_list
