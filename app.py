import streamlit as st
import pandas as pd
import time
import hmac
import hashlib
import requests
import os

# 1. 페이지 설정 및 디자인(CSS)
st.set_page_config(page_title="KIMSSINE FRESH", page_icon="🍎", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; text-align: center;
    }
    div.stButton > button { border-radius: 10px; height: 3rem; font-weight: 600; }
    .stButton button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 금고에서 열쇠 가져오기
COUPANG_ACCESS_KEY = os.environ.get('COUPANG_ACCESS_KEY')
COUPANG_SECRET_KEY = os.environ.get('COUPANG_SECRET_KEY')
COUPANG_SELLER_ID = os.environ.get('COUPANG_SELLER_ID')
ADMIN_CLIENT_ID = os.environ.get('ADMINPLUS_CLIENT_ID')
ADMIN_CLIENT_SECRET = os.environ.get('ADMINPLUS_CLIENT_SECRET')

# 3. 쿠팡 주문 수집 함수
def get_coupang_orders():
    path = f"/v2/providers/openapi/apis/api/v4/vendors/{COUPANG_SELLER_ID}/ordersheets"
    method = "GET"
    query_string = "status=ACCEPT"
    timestamp = time.strftime('%y%m%dT%H%M%SZ', time.gmtime())
    message = timestamp + method + path + query_string
    signature = hmac.new(COUPANG_SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization = f"CEA algorithm=HmacSHA256, access-key={COUPANG_ACCESS_KEY}, signed-date={timestamp}, signature={signature}"
    url = f"https://api-gateway.coupang.com{path}?{query_string}"
    headers = {"Content-Type": "application/json", "Authorization": authorization}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json().get('data', [])
    except:
        return []

# --- 화면 구성 ---
st.title("🍎 KIMSSINE FRESH 자동화 시스템")

# 현황판 영역
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-card"><p>수집된 신규 주문</p><h3>' + str(len(st.session_state.get('orders', []))) + ' 건</h3></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><p>오늘 발주 완료</p><h3>0 건</h3></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><p>연동 상태</p><h3 style="color:green;">정상</h3></div>', unsafe_allow_html=True)

st.write("")

# 메인 기능
tab1, tab2, tab3 = st.tabs(["📦 주문 관리 및 발주", "💬 CS 관리", "⚙️ 설정"])

with tab1:
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("🔄 쿠팡 신규 주문 수집", use_container_width=True):
            with st.spinner("쿠팡 서버에서 주문을 긁어오고 있습니다..."):
                orders = get_coupang_orders()
                st.session_state['orders'] = orders
                if orders: st.success(f"{len(orders)}건 수집 완료!")
                else: st.info("새로운 주문이 없습니다.")
    with c2:
        if st.button("🚀 어드민플러스로 일괄 발주", type="primary", use_container_width=True):
            st.warning("도매처 전송 기능 준비 중입니다 (상품 매칭 필요)")

    st.write("")
    if 'orders' in st.session_state and st.session_state['orders']:
        st.subheader("수집된 주문 목록")
        df = pd.DataFrame(st.session_state['orders'])
        st.dataframe(df, use_container_width=True)
    else:
        st.write("표시할 주문이 없습니다. 버튼을 눌러 수집을 시작하세요.")

with tab2:
    st.subheader("AI CS 답변 비서")
    q = st.text_area("문의 내용 입력")
    if st.button("AI 답변 생성"):
        st.success("답변 생성 기능은 추후 OpenAI API 연동 시 활성화됩니다.")

with tab3:
    st.subheader("시스템 연동 정보")
    st.text_input("쿠팡 Seller ID", value=COUPANG_SELLER_ID, disabled=True)
    st.write("※ API Key는 금고(Secrets) 내부에 안전하게 보관 중입니다.")
