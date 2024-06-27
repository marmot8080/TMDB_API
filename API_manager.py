import requests
import json

class api_manager():
    __base_url = "https://api.themoviedb.org/3/"

    def __init__(self, key):
        self.__headers = {
            "accept": "application/json",
            "Authorization": key
        }

    def get_movie_ids(self, start_date, end_date):
        url = self.__base_url + "movie/changes?end_date=" + end_date + "&page=1&start_date=" + start_date
        
        response = requests.get(url, headers=self.__headers)
        response = json.loads(response.text)
        total_pages = int(response['total_pages'])
        movie_ids = [int(info['id']) for info in response['results']]

        for page in range(2, total_pages+1):
            url = self.__base_url + "movie/changes?end_date=" + end_date + "&page=" + page + "&start_date=" + start_date
            response = requests.get(url, headers=self.__headers)
            response = json.loads(response.text)

            movie_ids.append(info['id'] for info in response['results'])

        return movie_ids

    def get_movie_detail(self, id):
        url = self.__base_url + "movie/" + id + "?language=ko-KR"
        response = requests.get(url, headers=self.__headers)
        response = json.loads(response.text)

        details = {
            "title": response['title'],
            "adult": bool(response['adult']),
            "backdrop_path": response['backdrop_path'],
            "poster_path": response['poster_path'],
            "genres": [int(genre['id']) for genre in response['genres']],
            "popularity": float(response['popularity']),
            "overview": response['overview'],
            "release_date": response['release_date'],
            "runtime": int(response['runtime']),
            "vote_average": float(response['vote_average']),
            "vote_count": int(response['vote_count'])
        }

        return details