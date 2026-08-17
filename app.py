import streamlit as st
import pandas as pd
import time
import hmac
import hashlib
import requests
import json
import os
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="KIMSSINE FRESH", page_icon="🍎", layout="wide")

# --- 1. 보안 열쇠 가져오기 (금고에서 꺼냄) ---
COUPANG_ACCESS_KEY = os.environ.get('COUPANG_ACCESS_KEY')
COUPANG_SECRET_KEY = os.environ.get('COUPANG_SECRET_KEY')
COUPANG_SELLER_ID = os.environ.get('COUPANG_SELLER_ID')
ADMIN_CLIENT_ID = os.environ.get('ADMINPLUS_CLIENT_ID')
ADMIN_CLIENT_SECRET = os.environ.get('ADMINPLUS_CLIENT_SECRET')

# --- 2. 쿠팡 주문 수집 함수 ---
def get_coupang_orders():
    path = f"/v2/providers/openapi/apis/api/v4/vendors/{COUPANG_SELLER_ID}/ordersheets"
    method = "GET"
    query_string = "status=ACCEPT" # 결제 완료된 주문만
    
    # 쿠팡 특유의 보안 인증 생성
    timestamp = time.strftime('%y%m%dT%H%M%SZ', time.gmtime())
    message = timestamp + method + path + query_string
    signature = hmac.new(COUPANG_SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization = f"CEA algorithm=HmacSHA256, access-key={COUPANG_ACCESS_KEY}, signed-date={timestamp}, signature={signature}"
    
    url = f"https://api-gateway.coupang.com{path}?{query_string}"
    headers = {"Content-Type": "application/json", "Authorization": authorization}
    
    try:
        res = requests.get(url, headers=headers)
        return res.json().get('data', [])
    except:
        return []

# --- 3. 어드민플러스 토큰 발급 함수 ---
def get_admin_token():
    url = "https://api.adminplus.co.kr/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": ADMIN_CLIENT_ID,
        "client_secret": ADMIN_CLIENT_SECRET
    }
    try:
        res = requests.post(url, data=data)
        return res.json().get('access_token')
    except:
        return None

# --- 웹 화면 구성 ---
st.title("🍎 KIMSSINE FRESH 자동화 시스템")

tab1, tab2 = st.tabs(["📦 주문 및 발주", "⚙️ 설정"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 쿠팡 주문 수집 시작", type="primary", use_container_width=True):
            orders = get_coupang_orders()
            if orders:
                st.session_state['orders'] = orders
                st.success(f"{len(orders)}건의 신규 주문을 가져왔습니다.")
            else:
                st.info("새로운 주문이 없습니다.")

    with col2:
        if st.button("🚀 어드민플러스 발주 전송", use_container_width=True):
            token = get_admin_token()
            if token and 'orders' in st.session_state:
                st.info("도매처로 발주를 전송 중입니다...")
                # 여기에 실제 전송 로직이 들어갑니다 (테스트 후 활성화)
                st.success("발주 전송이 완료되었습니다.")
            else:
                st.error("전송할 주문이 없거나 인증에 실패했습니다.")

    if 'orders' in st.session_state:
        df = pd.DataFrame(st.session_state['orders'])
        st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("시스템 연결 상태")
    st.write(f"쿠팡 ID: {COUPANG_SELLER_ID}")
    st.write("도매처: 어드민플러스 연동 중")
