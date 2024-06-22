# musiclist
/add
사용자가 CSV 파일로 제공한 Spotify 데이터를 데이터베이스에 저장하기 위한 url입니다.
def add_new를 통해서 실행되며 add_feature.html이 열립니다. 
UI를 통해 사용자는 서버로 데이터를 전송할 수 있습니다.
전송된 데이터를 

search.html
사용자가 가수/노래를 검색할 수 있는 검색창을 제공합니다. 
검색한 가수/노래를 table형식으로 보여줍니다.
가수들의 특징을 퍼센트 바(Percent Bar)로 시각화하여 보여줍니다.

song_list.html
사용자가 search.html에서 원하는 가수를 선택하면, 선택한 가수의 상세 정보를 보여주는 페이지입니다.
가수의 특징을 그래프로 시각화하여 보여주고, 가수의 노래들을 table형식으로 보여줍니다.
가수의 노래들의 특징을 퍼센트 바(Percent Bar)로 시각화하여 보여줍니다.

function drawChart(): Google Chart에서 제공하는 JavaScript 함수로, 가수의 특징들(Speechiness, Liveness, Acousticness 등)을 그래프로 나타냅니다. 
특정 컬럼을 클릭하면 해당 특징과 유사한 다른 가수를 추천하는 페이지(similar_artists.html)로 이동합니다.
function sortTable(colIndex): 가수의 노래 목록을 표시하는 테이블의 헤더 컬럼을 선택했을 때, 해당 컬럼의 인덱스를 기준으로 노래들을 정렬하는 함수입니다. 
한 번 클릭하면 오름차순으로, 두 번 클릭하면 내림차순으로 정렬됩니다.

similar_artists.html
song_list.html에서 특정 특징 컬럼을 클릭했을 때 이동하는 페이지입니다.
 클릭한 특징을 기준으로 유사한 가수들을 조회할 수 있습니다. 
각 가수의 이름에 링크가 걸려 있어 클릭 시 해당 가수의 상세 정보 페이지로 이동합니다.