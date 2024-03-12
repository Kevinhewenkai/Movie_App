# This is using the api TMDB to build the database
import requests

class TMDB():
    def __init__(self):
        self.key = '8b63ded63660b4842b8c80e32243379b'
        self.url = 'https://api.themoviedb.org'
    
    def search_by_movie_name(self, keywards):
        r = requests.get(f"{self.url}/3/search/movie?api_key={self.key}", params={
        "query" : keywards,
        })
        assert r.status_code == 200
        payload = r.json()
        print(payload)
    
    def search_movie_details(self, movie_id):
        r = requests.get(f"{self.url}/3/movie/{movie_id}?api_key={self.key}")
        assert r.status_code == 200
        payload = r.json()
        print(payload)

if __name__ == "__main__":
    api = TMDB()
    api.search_by_movie_name("Wolf Warriors")
    # api.search_movie_details(335462)