import pymysql
import requests
import json

class api_manager():
    # TMDB api 및 MySQL 연결 정보 설정
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

    # 요청한 날짜 범위에서 movie id들의 총 페이지 수 반환
    def get_total_pages(self, start_date, end_date):
        url = self.__base_url + "movie/changes?end_date=" + end_date + "&page=1&start_date=" + start_date
        
        response = requests.get(url, headers=self.__headers)
        response = json.loads(response.text)
        total_pages = int(response['total_pages'])

        return total_pages

    # date 문자열 형태 --> YYYY-MM-DD
    def get_movie_ids(self, start_date, end_date, page):
        url = self.__base_url + "movie/changes?end_date=" + end_date + "&page=" + str(page) + "&start_date=" + start_date
        response = requests.get(url, headers=self.__headers)
        response = json.loads(response.text)

        movie_ids = [info['id'] for info in response['results']]

        return movie_ids

    # 영화 정보 반환
    def get_movie_detail(self, id: int):
        url = self.__base_url + "movie/" + str(id) + "?language=ko-KR"
        response = requests.get(url, headers=self.__headers)
        response = json.loads(response.text)

        if "success" in response and response['success'] == False:
            return None

        details = {
            "movie_id": id,
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
    
    # 영화 정보를 DB에 저장
    def wirte_movie_detail(self, details: json):
        sql = """
            INSERT IGNORE INTO home_movieinfo(movie_id, title, adult, backdrop_path, poster_path, genres, popularity, overview, release_date, runtime, vote_average, vote_count) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        genres_json = json.dumps(details.get('genres', []))

        data = (
            details['movie_id'],
            details['title'],
            details['adult'],
            details['backdrop_path'],
            details['poster_path'],
            genres_json,
            details['popularity'],
            details['overview'],
            details['release_date'],
            details['runtime'],
            details['vote_average'],
            details['vote_count']
        )

        self.__cursor.execute(sql, data, )
        self.__conn.commit()