import pymysql
import requests
import json

class api_manager():
    __base_url = "https://api.themoviedb.org/3/"
    __conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', db='mr', password='0000', charset='utf8')
    __cursor = __conn.cursor()

    def __init__(self, key):
        self.__headers = {
            "accept": "application/json",
            "Authorization": key
        }
    
    def __del__(self):
        self.__conn.close()
        pass

    # 최대 14일 간격으로 수집 가능
    # date 문자열 형태 --> YYYY-MM-DD
    def get_movie_ids(self, start_date, end_date):
        url = self.__base_url + "movie/changes?end_date=" + end_date + "&page=1&start_date=" + start_date
        
        response = requests.get(url, headers=self.__headers)
        response = json.loads(response.text)
        total_pages = int(response['total_pages'])
        movie_ids = [[int(info['id']) for info in response['results']]]

        for page in range(2, total_pages+1):
            url = self.__base_url + "movie/changes?end_date=" + end_date + "&page=" + page + "&start_date=" + start_date
            response = requests.get(url, headers=self.__headers)
            response = json.loads(response.text)

            movie_ids.append([info['id'] for info in response['results']])

        return movie_ids

    def get_movie_detail(self, id: int):
        url = self.__base_url + "movie/" + str(id) + "?language=ko-KR"
        response = requests.get(url, headers=self.__headers)
        response = json.loads(response.text)

        details = {
            "id": id,
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
    
    def wirte_movie_detail(self, details: json):
        sql = """
            INSERT INTO home_movieinfo(id, title, adult, backdrop_path, poster_path, genres, popularity, overview, release_date, runtime, vote_average, vote_count) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)   
        """

        self.__cursor.execute(sql, details, )
        self.__conn.commit()