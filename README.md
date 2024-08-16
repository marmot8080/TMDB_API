# TMDB_API
TMDB API를 통해 영화 데이터를 수집하여 MySQL을 활용한 DB 구축

# 실행
1. github에서 프로젝트 복사
```
git clone https://github.com/marmot8080/TMDB_API.git
```
2. TMDB_API 폴더 내에 API_key.txt 파일 생성
3. 본인의 TMDB api key를 API_key.txt에 복사 후 저장
4. API_manager.py에서 각자 환경에 맞춰 DB 연결정보 수정
5. state.json에서 page 및 recent_date 수정(page는 최소 1, recent_date는 최소 2012-10-05 부터 가능)
6. API_call.py 실행
```
python API_call.py
```