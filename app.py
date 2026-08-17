import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="김씨네 프레시 비서", page_icon="🍎", layout="wide")

# 제목
st.title("🍎 김씨네 프레시 자동화 관리 시스템")

# 사이드바
st.sidebar.header("🛠️ 시스템 상태")
st.sidebar.success("서버 가동 중")
st.sidebar.info("연동 계정: kimssine.fresh")

# 메뉴 구성 (CS 메뉴 추가!)
tab1, tab2, tab3 = st.tabs(["📦 발주 관리", "💬 CS 관리(AI)", "⚙️ 설정"])

with tab1:
    st.subheader("오늘의 신규 주문")
    dummy_data = {
        "주문번호": ["20231010-001", "20231010-002"],
        "상품명": ["[산지직송] 고당도 꿀사과 5kg", "프리미엄 샤인머스캣 2kg"],
        "수량": [1, 2],
        "받는분": ["홍길동", "임꺽정"],
        "주소": ["서울시 강남구...", "부산시 해운대구..."],
        "상태": ["결제완료", "결제완료"]
    }
    df = pd.DataFrame(dummy_data)
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 쿠팡 주문 새로고침", use_container_width=True):
            st.toast("주문을 확인하고 있습니다...")
    with col2:
        if st.button("🚀 어드민플러스 발주 전송", use_container_width=True):
            st.error("현재 테스트 모드입니다. API 연동이 필요합니다.")

with tab2:
    st.subheader("🤖 AI CS 답변 비서")
    st.write("고객의 문의 내용을 입력하면 AI가 답변 초안을 만들어줍니다.")
    
    user_query = st.text_area("고객 문의 내용 입력", placeholder="예: 사과가 깨져서 왔어요. 환불해주세요.")
    
    if st.button("AI 답변 생성"):
        if user_query:
            st.info("AI가 답변을 생성 중입니다...")
            # 나중에 여기에 진짜 AI 기능을 넣을 거예요. 지금은 예시입니다.
            if "배송" in user_query:
                st.success("**[AI 추천 답변]**\n\n안녕하세요 고객님! 김씨네 프레시입니다. 주문하신 상품은 현재 산지에서 포장 완료되어 택배사로 인계되었습니다. 내일 중으로는 수령 가능하실 것으로 보입니다. 조금만 기다려주세요!")
            elif "파손" in user_query or "깨져" in user_query or "터져" in user_query:
                st.success("**[AI 추천 답변]**\n\n안녕하세요 고객님, 불편을 드려 정말 죄송합니다. 과일 특성상 배송 중 충격이 발생한 것 같습니다. 사진을 찍어 보내주시면 확인 즉시 새 상품으로 재발송 혹은 환불 처리를 도와드리겠습니다.")
            else:
                st.success("**[AI 추천 답변]**\n\n안녕하세요 고객님! 문의하신 내용 확인하였습니다. 담당 부서에 전달하여 빠르게 확인 후 안내해 드리겠습니다. 감사합니다.")
        else:
            st.warning("문의 내용을 입력해주세요.")

with tab3:
    st.subheader("⚙️ 시스템 설정")
    st.write("등록된 API 키 정보 (보안을 위해 일부 숨김)")
    st.text_input("쿠팡 API 상태", value="연결 대기 중", disabled=True)
    st.text_input("도매처 API 상태", value="연결 대기 중", disabled=True)
