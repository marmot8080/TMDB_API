# TMDB_API
TMDB API를 통해 영화 데이터를 수집하여 MySQL을 활용한 DB 구축

## 목차
1. [실행](#실행)
2. [테이블 정의](#테이블-정의)

## 실행
1. github에서 프로젝트 복사
```
git clone https://github.com/marmot8080/TMDB_API.git
```
2. TMDB_API 폴더 내에 API_key.txt 파일 생성
3. 본인의 TMDB api key를 API_key.txt에 복사 후 저장
4. API_manager.py에서 환경에 맞춰 DB 연결정보 수정
5. state.json에서 page 및 recent_date 수정(page는 최소 1, recent_date는 최소 2012-10-05 부터 가능)
6. API_call.py 실행
```
python API_call.py
```

## 테이블 정의
| 컬럼 명      | 컬럼 영문명 | 타입 | 길이 | 널 허용 | 키 구분 | 초기값 | 비고|
|-------------|------------|------|------|--------|---------|-------|-----|
| 아이디  | movie_id | MUDIUMINT | 5 | N | PK |  |  |
| 제목 | title | VARCHAR | 100 | N |  |  |  |
| 개봉일 | release_date | DATE |  | N |  |  |  |
| 상영시간 | runtime | SMALLINT | 5 | Y |  |  |  |
| 