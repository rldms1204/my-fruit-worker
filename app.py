import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# 1. 구글 시트 연결 설정
def get_gspread_client():
    # GitHub Secrets에 저장한 열쇠를 가져옵니다.
    secret_json = os.environ.get("GOOGLE_SHEETS_JSON")
    key_dict = json.loads(secret_json)
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    return gspread.authorize(creds)

st.title("🍎 김씨네 프레시 발주 관리")

try:
    # 2. 구글 시트 열기
    client = get_gspread_client()
    # 아까 만드신 시트 이름과 정확히 일치해야 합니다.
    sheet = client.open("김씨네 프레시").sheet1 

    st.subheader("오늘의 도매처 설정")

    # 3. 현재 설정된 값 읽어오기
    current_data = sheet.get_all_records()
    # 예: 첫 번째 품목(사과)의 도매처 확인
    current_wh = current_data[0]['도매처'] if current_data else "미설정"
    
    st.write(f"현재 설정된 도매처: **{current_wh}**")

    # 4. 도매처 선택 드롭다운
    options = ["도매처A", "도매처B", "도매처C", "도매처D", "도매처E"]
    selected_wh = st.selectbox("오늘 발주할 도매처를 선택하세요:", options)

    if st.button("설정 저장하기"):
        # 시트의 2행 2열(B2)에 선택한 도매처 이름을 씁니다.
        sheet.update_cell(2, 2, selected_wh)
        st.success(f"성공! 이제부터 주문은 '{selected_wh}'로 들어갑니다.")
        st.balloons()

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.info("GitHub Secrets에 GOOGLE_SHEETS_JSON이 잘 저장되었는지, 시트 이름이 '김씨네 프레시'가 맞는지 확인해주세요.")
