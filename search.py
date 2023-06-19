import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# css 불러오기
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

title = st.title('🚍 정류소 위치 검색 🚍')

# jeju.csv 파일을 읽어옵니다.
df = pd.read_csv('jeju.csv')

# 정류소명, 위치정보 열의 데이터를 저장합니다.
bus_stops = df[['정류소명', '위치정보(주변설명)', '경도', '위도']]

# NaN 값을 제거합니다.
bus_stops = bus_stops.dropna(subset=['정류소명'])

# 검색어 입력을 받습니다.
search_term = st.text_input('', placeholder='정류소명 검색')

# 검색어와 정류소명의 첫 번째 글자가 일치하는 결과를 출력합니다.
if search_term:
    filtered_stops = bus_stops[bus_stops['정류소명'].str.startswith(search_term)]
    if len(filtered_stops) == 0:
        st.markdown('<p class="p-result-none">검색 결과가 없습니다.</p>',unsafe_allow_html=True)
    else:
        st.markdown(
            f"""<div class="div-search-row">
                        <p class="p-row1">정류소명<p>
                        <p class="p-row2">위치정보<p>
                        <p class="p-row3">🗺️<p>
                    <div>
                """, unsafe_allow_html=True)
        for index, row in filtered_stops.iterrows():
            st.markdown(
                f"""<div class="div-search-result">
                        <p class="p-search1">{row['정류소명']}</p>
                        <p class="p-search2">|</p>
                        <p class="p-search3">{row['위치정보(주변설명)']}</p>
                    </div>
                """, unsafe_allow_html=True)

            # 클릭 이벤트 처리
            button_clicked = st.button(
                "위치확인", key=f"button_{index}", help=f"{index}번째 정류소")
            if button_clicked:
                # 클릭한 정류소 위치를 지도에 표시
                m = folium.Map(location=[row['위도'], row['경도']], zoom_start=14)
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    popup=row['정류소명'],
                    icon=folium.Icon(icon='bus', prefix='fa')
                ).add_to(m)
                folium_static(m)
                with st.empty():
                    pass