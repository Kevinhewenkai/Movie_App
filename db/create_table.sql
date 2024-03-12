-- Table User
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    token TEXT
)


-- Table Banlist
CREATE TABLE IF NOT EXISTS Banlist (
    user_id INTEGER NOT NULL,
    ban_user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (ban_user_id) REFERENCES User(user_id)
)


-- Table Movie
CREATE TABLE IF NOT EXISTS Movie (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    country TEXT,
    language TEXT,
    description TEXT,
    genre TEXT,
    year INTEGER
)


-- Table Movie_Photo
CREATE TABLE IF NOT EXISTS Movie_Photo (
    photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    photo TEXT,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
)


-- Table Review
CREATE TABLE IF NOT EXISTS Review (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    review TEXT,
    rating REAL,
    added_on INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
)


-- Table Wishlist
CREATE TABLE IF NOT EXISTS Wishlist (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    added_on INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
)


-- Table Actor
CREATE TABLE IF NOT EXISTS Actor (
    actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    country TEXT,
    birthyear INTEGER,
    deathyear INTEGER,
    photo TEXT
)


-- Table Cast_Movie
CREATE TABLE IF NOT EXISTS Cast_Movie (
    movie_id INTEGER NOT NULL,
    actor_id INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (actor_id) REFERENCES Actor(actor_id)
)


-- Table Director
CREATE TABLE IF NOT EXISTS Director (
    director_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    country TEXT,
    birthyear INTEGER,
    deathyear INTEGER,
    photo TEXT
)


-- Table Direct_Movie
CREATE TABLE IF NOT EXISTS Direct_Movie (
    movie_id INTEGER NOT NULL,
    director_id INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (director_id) REFERENCES Director(director_id)
)

