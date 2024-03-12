import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
from helper import get_user_from_token

cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")

movie_data = pd.read_excel('../db/movie.xlsx', sheet_name='movie')
director_data = pd.read_excel('../db/movie.xlsx', sheet_name="director")
actor_data = pd.read_excel('../db/movie.xlsx', sheet_name="actor")

feature = ['country', 'language', 'description']


def get_similarity_by_history(movie_id, token):
    global feature
    # get user_id
    user_id = get_user_from_token(token)
    if user_id is None:
        return {'400': 'No such user'}
    user_id = user_id['user_id']
    # build the connection
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # get the recent viewed list
    rv = cursor.execute(
        '''
        SELECT movie_id FROM ReviewHistory where user_id = ?
        ''', (user_id,)
    ).fetchall()
    recent_viewed = []
    for m in rv:
        recent_viewed.append(m[0])
    # Calculate the similarities
    # combine the features
    combined_features = movie_data[feature[0]]
    for n in range(1, len(feature)):
        combined_features = combined_features + ' '
        combined_features += movie_data[feature[n]]
    # converting the text to feature vectors
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)
    # replace all 1
    for index in range(0, len(similarity)):
        similarity[index][index] = 0
    # calculate the total score of the review history
    total_similarity = [0] * len(similarity)
    # similarity_board = list(enumerate(similarity[movie_id-1]))
    # print(similarity_board)
    for movie_id in recent_viewed:
        for idx, amount in enumerate(similarity[movie_id]):
            total_similarity[idx] += amount
    similarity_board = sorted(
        list(enumerate(similarity[movie_id-1])), key=lambda x: x[1], reverse=True)

    # grab the most similar 6 movies
    similar_movies = []
    count = 0
    for movie in range(1, len(similarity_board)):
        if similarity_board[movie][0] in recent_viewed:
            similar_movies.append(similarity_board[movie][0])
            count += 1
        if len(similar_movies) == 6:
            break
    if len(similar_movies) < 6:
        for movie in range(1, len(similarity_board)):
            if similarity_board[movie][0] not in similar_movies:
                similar_movies.append(similarity_board[movie][0])
            if len(similar_movies) == 6:
                break
    return {'similar movies': similar_movies}


def get_similarity_by_genre(movie_id):
    global feature
    selected_feature = feature + ['genre']
    # combine the features
    combined_features = movie_data[selected_feature[0]]
    for n in range(1, len(selected_feature)):
        combined_features = combined_features + ' '
        combined_features += movie_data[selected_feature[n]]
    # converting the text to feature vectors
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)
    similarity_board = sorted(
        list(enumerate(similarity[movie_id-1])), key=lambda x: x[1], reverse=True)
    # grab the most similar 6 movies
    similar_movies = []
    for movie in range(1, 7):
        similar_movies.append(similarity_board[movie][0])
    return {'similar movies': similar_movies}


def get_similarity_by_director(movie_id):
    global feature
    # combine the features
    combined_features = movie_data[feature[0]]
    for n in range(1, len(feature)):
        combined_features = combined_features + ' '
        combined_features += movie_data[feature[n]]
    combined_features += ' ' + director_data['name']
    combined_features += ' ' + director_data['country']
    combined_features += ' ' + str(director_data['birthyear'])
    # converting the text to feature vectors
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)
    similarity_board = sorted(
        list(enumerate(similarity[movie_id-1])), key=lambda x: x[1], reverse=True)
    # grab the most similar 6 movies
    similar_movies = []
    for movie in range(1, 7):
        similar_movies.append(similarity_board[movie][0])
    return {'similar movies': similar_movies}
