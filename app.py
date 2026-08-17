import streamlit as st
import pandas as pd

# 1. 페이지 설정: 화면을 넓게(wide) 쓰고, 사이드바를 기본으로 닫아둡니다.
st.set_page_config(
    page_title="김씨네 프레시 관리자",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 스타일 커스텀: 여백 줄이기
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# 상단 헤더 영역
col_title, col_stat1, col_stat2, col_stat3 = st.columns([2, 1, 1, 1])
with col_title:
    st.title("🍎 김씨네 프레시")

# 요약 지표 (실시간 현황판)
with col_stat1:
    st.metric(label="신규 주문", value="2건", delta="신규")
with col_stat2:
    st.metric(label="미답변 CS", value="1건", delta="주의", delta_color="inverse")
with col_stat3:
    st.metric(label="오늘 발주완료", value="15건")

st.divider()

# 메인 업무 영역
tab1, tab2, tab3 = st.tabs(["📦 주문 및 발주 관리", "💬 AI CS 응대", "⚙️ 시스템 설정"])

with tab1:
    # 기능 버튼을 상단에 가로로 배치
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    with btn_col1:
        if st.button("🔄 쿠팡 주문 새로고침"):
            st.toast("최신 주문을 가져오는 중...")
    with btn_col2:
        st.button("📄 발주 엑셀 다운로드")
    with btn_col3:
        st.button("📤 송장 번호 일괄 업로드")
    with btn_col4:
        if st.button("🚀 어드민플러스 발주 전송", type="primary"):
            st.error("API 연동 대기 중")

    st.write("") # 간격
    
    # 주문 표 (공간을 넓게 사용)
    st.subheader("실시간 주문 목록")
    dummy_data = {
        "주문번호": ["20231010-001", "20231010-002", "20231010-003", "20231010-004"],
        "상품명": ["[산지직송] 고당도 꿀사과 5kg", "프리미엄 샤인머스캣 2kg", "제주 황금향 3kg", "영암 무화과 2kg"],
        "수량": [1, 2, 1, 5],
        "구매자": ["홍길동", "임꺽정", "장길산", "이몽룡"],
        "연락처": ["010-1234-5678", "010-1111-2222", "010-3333-4444", "010-5555-6666"],
        "배송지": ["서울시 강남구...", "부산시 해운대구...", "강원도 강릉시...", "전라남도 영암군..."],
        "결제금액": ["25,000원", "48,000원", "32,000원", "55,000원"],
        "상태": ["결제완료", "결제완료", "결제완료", "결제완료"]
    }
    df = pd.DataFrame(dummy_data)
    st.dataframe(df, use_container_width=True, height=400)

with tab2:
    col_cs_in, col_cs_out = st.columns([1, 1])
    with col_cs_in:
        st.subheader("문의 내용")
        user_query = st.text_area("고객 문의를 입력하세요", height=200, placeholder="배송 문의, 파손 접수 등...")
        st.button("✨ AI 답변 생성")
    with col_cs_out:
        st.subheader("AI 추천 답변")
        st.info("여기에 답변이 생성됩니다.")

with tab3:
    st.subheader("시스템 및 API 설정")
    col_conf1, col_conf2 = st.columns(2)
    with col_conf1:
        st.text_input("쿠팡 Seller ID", value="A00XXXXX", disabled=True)
        st.text_input("어드민플러스 연동 업체수", value="1곳", disabled=True)
    with col_conf2:
        st.write("자동 발주 예약 설정")
        st.toggle("오전 10시 자동 발주", value=False)
        st.toggle("오후 4시 자동 발주", value=False)

# 하단 푸터
st.caption("© 2024 Kimssine Fresh Automation System")
