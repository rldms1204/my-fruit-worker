import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# 1. 구글 시트 연결 설정
def get_gspread_client():
    try:
        secret_json = st.secrets["GOOGLE_SHEETS_JSON"]
        key_dict = json.loads(secret_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"열쇠(Secrets) 설정에 문제가 있습니다: {e}")
        return None

st.set_page_config(page_title="김씨네 프레시 관리", page_icon="🍎")
st.title("🍎 김씨네 프레시 발주 관리")

client = get_gspread_client()

if client:
    try:
        # ⚠️ 주의: 구글 시트 이름이 '김씨네 프레시'와 정확히 일치해야 합니다.
        sheet_name = "김씨네 프레시" 
        doc = client.open(sheet_name)
        worksheet = doc.get_worksheet(0) # 첫 번째 탭 선택

        st.subheader("오늘의 도매처 설정")

        # 2. 현재 설정값 읽어오기 (B2 셀 하나만 딱 읽어옵니다)
        current_wh = worksheet.acell('B2').value
        st.info(f"현재 설정된 도매처: **{current_wh}**")

        # 3. 도매처 선택 메뉴
        options = ["도매처A", "도매처B", "도매처C", "도매처D", "도매처E"]
        
        # 현재 값이 리스트에 없으면 첫 번째 선택
        default_index = options.index(current_wh) if current_wh in options else 0
        selected_wh = st.selectbox("오늘 발주할 도매처를 선택하세요:", options, index=default_index)

        if st.button("설정 저장하기"):
            with st.spinner('구글 시트에 기록 중...'):
                # B2 셀에 값 업데이트
                worksheet.update_acell('B2', selected_wh)
                st.success(f"성공! 이제부터 주문은 '{selected_wh}'로 들어갑니다.")
                st.balloons()
                st.rerun() # 화면 새로고침

    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"구글 시트를 찾을 수 없습니다. 시트 이름이 '{sheet_name}'이 맞는지 확인해주세요.")
    except Exception as e:
        # Response [200]은 성공이므로 무시하도록 설정
        if "200" not in str(e):
            st.error(f"알 수 없는 오류 발생: {e}")
