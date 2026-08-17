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

# 페이지 기본 설정 (와이드 모드)
st.set_page_config(page_title="김씨네 프레시 관리", page_icon="🍎", layout="centered")

# 헤더 디자인
st.markdown("""
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 25px; text-align: center; border: 1px solid #e9ecef;">
    <h1 style="color: #d32f2f; margin-bottom: 5px;">🍎 김씨네 프레시 오토메이션</h1>
    <p style="color: #6c757d; font-size: 1.1em; margin: 0;">발주부터 CS까지 알아서 척척! 스마트 대시보드</p>
</div>
""", unsafe_allow_html=True)

client = get_gspread_client()

if client:
    try:
        sheet_name = "김씨네 프레시" 
        doc = client.open(sheet_name)
        worksheet = doc.get_worksheet(0) # 첫 번째 탭 선택

        # 2. 현재 설정값 읽어오기 (B2: 도매처, C2: Q&A 상태, D2: CS 상태)
        # 빈 칸일 경우를 대비해 기본값 설정
        current_wh = worksheet.acell('B2').value or "도매처A"
        current_qa = worksheet.acell('C2').value or "OFF"
        current_cs = worksheet.acell('D2').value or "OFF"

        # --- [1] 메인 발주 관리 ---
        st.markdown("### 📦 메인 발주 관리")
        with st.container(border=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                options = ["도매처A", "도매처B", "도매처C", "도매처D", "도매처E"]
                default_index = options.index(current_wh) if current_wh in options else 0
                selected_wh = st.selectbox("오늘 발주할 도매처를 선택하세요:", options, index=default_index)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(f"현재: **{current_wh}**")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- [2] 부가 자동화 스위치 ---
        st.markdown("### 🤖 부가 기능 자동화 스위치")
        with st.container(border=True):
            st.markdown("로봇이 매일 정해진 시간에 아래 기능들을 수행할지 여부를 결정합니다.")
            
            c1, c2 = st.columns(2)
            with c1:
                # 쿠팡 Q&A 토글
                qa_toggle = st.toggle("💬 쿠팡 Q&A 자동 답변", value=(current_qa == "ON"))
                st.caption("키워드 분석을 통해 똑똑하게 답변을 남깁니다.")
                
            with c2:
                # CS 문자 토글
                cs_toggle = st.toggle("💌 CS 문자 자동 발송", value=(current_cs == "ON"))
                st.caption("고객에게 배송 출발 알림을 보냅니다.")
                
        # 상태 변환 (토글 값 -> 문자열)
        new_qa_status = "ON" if qa_toggle else "OFF"
        new_cs_status = "ON" if cs_toggle else "OFF"

        st.markdown("<br>", unsafe_allow_html=True)

        # --- [3] 저장 버튼 ---
        if st.button("💾 모든 설정 저장하기", type="primary", use_container_width=True):
            with st.spinner('구글 시트에 설정을 안전하게 기록하는 중...'):
                # 변경된 내용 시트에 업데이트
                worksheet.update_acell('B2', selected_wh)
                worksheet.update_acell('C2', new_qa_status)
                worksheet.update_acell('D2', new_cs_status)
                
                st.success("✨ 성공적으로 저장되었습니다! 로봇이 이 설정대로 움직입니다.")
                st.balloons()
                st.rerun()

    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"구글 시트를 찾을 수 없습니다. 시트 이름이 '{sheet_name}'이 맞는지 확인해주세요.")
    except Exception as e:
        if "200" not in str(e):
            st.error(f"알 수 없는 오류 발생: {e}")
