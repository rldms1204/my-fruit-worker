import streamlit as st
import pandas as pd

st.set_page_config(page_title="과일 위탁판매 비서", page_icon="🍎")
st.title("🍎 과일 위탁판매 자동 발주 시스템")
st.info("현재는 테스트 모드입니다. 실제 발주는 연동 후 가능합니다.")

st.sidebar.header("연동 상태")
st.sidebar.success("비밀 금고(Secrets) 연결됨")

tab1, tab2 = st.tabs(["📦 발주 관리", "⚙️ 설정"])

with tab1:
    st.subheader("오늘의 신규 주문")
    dummy_data = {
        "주문번호": ["20231010-001", "20231010-002"],
        "상품명": ["꿀사과 5kg", "샤인머스캣 2kg"],
        "수량": [1, 2],
        "받는분": ["홍길동", "임꺽정"],
        "주소": ["서울시 강남구...", "부산시 해운대구..."]
    }
    df = pd.DataFrame(dummy_data)
    st.dataframe(df, use_container_width=True)
    if st.button("쿠팡 주문 새로고침"):
        st.write("주문을 수집하는 중...")
    if st.button("어드민플러스로 발주 전송"):
        st.warning("실제 API 연결 준비 중입니다.")
