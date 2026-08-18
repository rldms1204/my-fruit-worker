import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import requests
import time
import hmac
import hashlib
import pandas as pd

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

        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- [4] 쿠팡 실시간 주문 조회 ---
        st.markdown("### 🛒 오늘의 신규 발주 조회")
        with st.container(border=True):
            st.markdown("쿠팡에 들어온 최신 '결제완료/상품준비중' 주문을 실시간으로 확인합니다.")
            if st.button("🔄 주문 목록 가져오기", use_container_width=True):
                # 웹 환경(Streamlit)에서 쿠팡 키 확인
                if "COUPANG_ACCESS_KEY" not in st.secrets:
                    st.warning("⚠️ Streamlit 설정에 쿠팡 API 키가 등록되지 않았습니다. 가이드를 참고해 키를 등록해주세요.")
                else:
                    with st.spinner('쿠팡에서 주문을 가져오는 중...'):
                        ACCESS_KEY = st.secrets["COUPANG_ACCESS_KEY"]
                        SECRET_KEY = st.secrets["COUPANG_SECRET_KEY"]
                        SELLER_ID = st.secrets["COUPANG_SELLER_ID"]
                        
                        # 쿠팡 API 호출 (status=ACCEPT)
                        now = time.gmtime()
                        from_time = time.strftime('%Y-%m-%d', time.gmtime(time.time() - 86400))
                        to_time = time.strftime('%Y-%m-%d', time.gmtime(time.time() + 86400))
                        
                        path = f"/v2/providers/openapi/apis/api/v4/vendors/{SELLER_ID}/ordersheets"
                        method = "GET"
                        query_string = f"createdAtFrom={from_time}&createdAtTo={to_time}&status=ACCEPT"
                        
                        timestamp = time.strftime('%y%m%dT%H%M%SZ', now)
                        message = timestamp + method + path + query_string
                        signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
                        
                        authorization = f"CEA algorithm=HmacSHA256, access-key={ACCESS_KEY}, signed-date={timestamp}, signature={signature}"
                        url = f"https://api-gateway.coupang.com{path}?{query_string}"
                        headers = {"Content-Type": "application/json", "Authorization": authorization}
                        
                        # 프록시(고정 IP) 설정 확인
                        fixie_url = st.secrets.get("FIXIE_URL", None)
                        proxies = {"http": fixie_url, "https": fixie_url} if fixie_url else None
                        
                        if fixie_url:
                            res = requests.get(url, headers=headers, proxies=proxies)
                        else:
                            res = requests.get(url, headers=headers)
                            
                        if res.status_code == 200:
                            orders = res.json().get('data', [])
                            if not orders:
                                st.info("👍 현재 수집된 신규 주문이 없습니다.")
                            else:
                                st.success(f"총 {len(orders)}건의 신규 주문을 불러왔습니다!")
                                
                                # 주문 데이터를 표 형태로 정리
                                table_data = []
                                for order in orders:
                                    items = order.get('orderItems', [])
                                    for item in items:
                                        table_data.append({
                                            "주문일시": order.get('orderedAt', '')[:16],
                                            "주문번호": order.get('orderId', ''),
                                            "상품명": item.get('vendorItemName', ''),
                                            "수량": item.get('shippingCount', 0),
                                            "수취인": order.get('receiver', {}).get('name', ''),
                                            "연락처": order.get('receiver', {}).get('safeNumber', '')
                                        })
                                
                                df = pd.DataFrame(table_data)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.error(f"주문 수집 실패: {res.status_code}")

    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"구글 시트를 찾을 수 없습니다. 시트 이름이 '{sheet_name}'이 맞는지 확인해주세요.")
    except Exception as e:
        if "200" not in str(e):
            st.error(f"알 수 없는 오류 발생: {e}")
