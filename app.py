import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="KIMSSINE FRESH | 관리자",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 세련된 대시보드를 위한 커스텀 디자인(CSS)
st.markdown("""
    <style>
    /* 전체 배경색 및 폰트 */
    .main { background-color: #f8f9fa; font-family: 'Pretendard', sans-serif; }
    
    /* 상단 카드 디자인 */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        text-align: center;
    }
    
    /* 버튼 스타일 커스텀 */
    div.stButton > button {
        border-radius: 10px;
        height: 3.5rem;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }
    
    /* 발주 전송 버튼 (강조) */
    .stButton button[kind="primary"] {
        background-color: #007bff !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0,123,255,0.3);
    }
    
    /* 일반 버튼 */
    .stButton button[kind="secondary"] {
        background-color: white;
        border: 1px solid #ddd;
    }
    
    /* 탭 메뉴 디자인 */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        background-color: #eee;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [aria-selected="true"] { background-color: #007bff !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 상단 헤더 및 현황판
st.title("🍎 KIMSSINE FRESH")
st.markdown("##### 과일 위탁판매 통합 관리 솔루션")

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown('<div class="metric-card"><p style="color:gray;">신규 주문</p><h2>2 건</h2><p style="color:green;">↑ 새 주문</p></div>', unsafe_allow_html=True)
with m_col2:
    st.markdown('<div class="metric-card"><p style="color:gray;">미답변 CS</p><h2>1 건</h2><p style="color:red;">⚠️ 처리필요</p></div>', unsafe_allow_html=True)
with m_col3:
    st.markdown('<div class="metric-card"><p style="color:gray;">발주 대기</p><h2>0 건</h2><p style="color:blue;">정상</p></div>', unsafe_allow_html=True)
with m_col4:
    st.markdown('<div class="metric-card"><p style="color:gray;">정산 예정금액</p><h2>1,240,500원</h2><p style="color:gray;">이번 달 기준</p></div>', unsafe_allow_html=True)

st.write("")

# 메인 탭
tab1, tab2, tab3 = st.tabs(["📦 주문/발주 관리", "💬 AI 고객응대(CS)", "⚙️ 시스템 설정"])

with tab1:
    # 상단 툴바
    t_col1, t_col2, t_col3 = st.columns([1, 1, 2])
    with t_col1:
        st.button("🔄 쿠팡 주문 동기화", key="refresh")
    with t_col2:
        st.button("📥 발주 리스트(Excel)", key="excel")
    with t_col3:
        # 하얀색이라 안보였던 버튼에 색상 강제 부여
        st.button("🚀 어드민플러스 발주 전송 시작", type="primary", use_container_width=True)

    st.write("")
    
    # 주문 데이터 및 표 설정 (글자 안잘리게 조절)
    dummy_data = {
        "주문일시": ["2024-10-10 14:20", "2024-10-10 15:05", "2024-10-10 15:30", "2024-10-10 16:12"],
        "주문번호": ["20231010-001", "20231010-002", "20231010-003", "20231010-004"],
        "상품명": [
            "[산지직송] 경북 고당도 부사 사과 5kg (실속형)", 
            "프리미엄 샤인머스캣 2kg (2-3송이)", 
            "제주도 서귀포 노지 감귤 10kg", 
            "영암 특산물 무화과 2kg (한정수량)"
        ],
        "수량": [1, 2, 1, 5],
        "구매자": ["홍길동", "임꺽정", "장길산", "이몽룡"],
        "연락처": ["010-1234-5678", "010-1111-2222", "010-3333-4444", "010-5555-6666"],
        "배송지 주소": ["서울시 강남구 테헤란로 123길 45 (06123)", "부산시 해운대구 마린시티로 789 (48123)", "강원도 강릉시 경포로 55 (25412)", "전라남도 영암군 영암읍 12 (58412)"],
        "결제액": ["25,000", "48,000", "32,000", "55,000"],
        "상태": ["결제완료", "결제완료", "결제완료", "결제완료"]
    }
    df = pd.DataFrame(dummy_data)
    
    # st.dataframe의 column_config 기능을 사용하여 특정 열 너비를 고정/확장
    st.dataframe(
        df, 
        use_container_width=True, 
        height=450,
        column_config={
            "상품명": st.column_config.TextColumn("상품명", width="large"),
            "배송지 주소": st.column_config.TextColumn("배송지 주소", width="max"),
            "주문일시": st.column_config.TextColumn("주문일시", width="medium"),
        },
        hide_index=True
    )

with tab2:
    c_col1, c_col2 = st.columns([1, 1.2])
    with c_col1:
        st.markdown("### 문의 접수")
        st.text_area("고객 문의 내용을 붙여넣으세요", height=250)
        st.button("✨ AI 답변 추천받기", use_container_width=True, type="primary")
    with c_col2:
        st.markdown("### AI 답변 초안")
        st.success("문의 내용을 입력하면 전문적인 답변이 이곳에 생성됩니다.")

with tab3:
    st.markdown("### ⚙️ 시스템 연동 설정")
    st.info("API 키는 GitHub Secrets에서 안전하게 관리되고 있습니다.")
    sc_col1, sc_col2 = st.columns(2)
    with sc_col1:
        st.text_input("쿠팡 API 상태", value="Connected (정상)", disabled=True)
        st.text_input("도매처 연동 수", value="1 (어드민플러스)", disabled=True)
    with sc_col2:
        st.write("자동화 스케줄")
        st.checkbox("매일 오전 10시 발주", value=True)
        st.checkbox("매일 오후 4시 발주", value=True)

st.write("")
st.caption("KIMSSINE FRESH Automation Tool v1.1 | Developed for Business Efficiency")
