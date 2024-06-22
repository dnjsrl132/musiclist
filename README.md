# musiclist
/add
사용자가 CSV 파일로 제공한 Spotify 데이터를 데이터베이스에 저장하기 위한 url입니다.
def add_new를 통해서 실행되며 upload.html이 열립니다. 
utf-8 형식의 csv 파일을 업로드해야 합니다. 
track_name, release_year, released_month, released_day, track_name, speechiness_%,
liveness_%, acousticness_%, energy_%, valence_%, danceability_%, mode, bpm, key, 
instrumentalness_%, artists(s)_name이 row에 포함되어야 합니다.

/match
artist의 평균을 구하는 url입니다. def match를 통해서 실행됩니다.
따로 페이지가 존재하지 않고 모든 artist의 데이터를 가져와서 평균을 구해 artist.feature에 저장합니다.

/
사용자가 가수/노래를 검색할 수 있는 검색창을 제공하며 home의 기능을 합니다.
class SearchView를 통해서 실행되며 search.html이 열립니다.
검색한 가수/노래를 table형식으로 보여줍니다. 가수인 경우에는 노래 칸이 비워져 있습니다.
가수들의 특징을 퍼센트 바(Percent Bar)로 시각화하여 보여줍니다.

/songs/<str:artist_name>/
사용자가 /search에서 원하는 가수를 선택하면, 선택한 가수의 상세 정보를 보여주는 url입니다.
class SongView를 통해서 실행되며 song_list.html가 열립니다.
가수의 특징을 그래프로 시각화하여 보여주고, 가수의 노래들을 table형식으로 보여줍니다.
가수의 노래들의 특징을 퍼센트 바(Percent Bar)로 시각화하여 보여줍니다.

function sortTable(colIndex): 가수의 노래 목록을 표시하는 테이블의 헤더 컬럼을 선택했을 때, 해당 컬럼의 인덱스를 기준으로 노래들을 정렬하는 함수입니다. 
한 번 클릭하면 오름차순으로, 두 번 클릭하면 내림차순으로 정렬됩니다.
function drawChart(): Google Chart에서 제공하는 JavaScript 함수로, 가수의 특징들(Speechiness, Liveness, Acousticness 등)을 그래프로 나타냅니다. 
특정 컬럼을 클릭하면 해당 특징과 유사한 다른 가수를 추천하는 url(/similar/<str:feature>/<str:name>/)로 이동합니다.

/similar/<str:feature>/<str:name>/
/songs/<str:artist_name>의 시각화 그래프에서 특정 특징을 선택하면 이동하는 url입니다.
class SimilarArtistsView에서 실행되며 similar_artists.html이 열립니다.
클릭한 특징을 기준으로 유사한 가수들을 조회할 수 있습니다. 
각 가수의 이름에 링크가 걸려 있어 클릭 시 해당 가수의 상세 정보 페이지로 이동합니다.

#models
class Feature
노래와 가수의 특징을 저장하는 모델입니다.
노래 혹은 가수의 이름을 pk로 사용합니다. oner가 true이면 가수이고 false이면 노래입니다.
speechiness, liveness, acousticness, energy, valence, danceability, mode, key, bpm, instrumentalness, realease_date가 있습니다.

class Artist
가수의 정보를 저장하는 모델입니다.
각 가수는 생성시에 고유 id를 pk로 가집니다.
해당하는 feature 모델을 fk로 가지고 name을 가지고 있습니다.

class Song
노래의 정보를 저장하는 모델입니다.
각 노래는 생성시에 고유 id를 pk로 가집니다.
해당하는 feature 모델과 artist를 fk로 가지고 name을 가지고 있습니다.