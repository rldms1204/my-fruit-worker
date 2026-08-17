import os
import time
import hmac
import hashlib
import requests

# 💡 쿠팡 Q&A 관리용 뼈대 코드
# 사장님이 어떤 방식으로 답변을 달지 결정하시면 내용을 채워넣습니다.

COUPANG_ACCESS_KEY = os.environ.get('COUPANG_ACCESS_KEY')
COUPANG_SECRET_KEY = os.environ.get('COUPANG_SECRET_KEY')
COUPANG_SELLER_ID = os.environ.get('COUPANG_SELLER_ID')

def generate_signature(method, path, query_string=""):
    timestamp = time.strftime('%y%m%dT%H%M%SZ', time.gmtime())
    message = timestamp + method + path + query_string
    signature = hmac.new(COUPANG_SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"CEA algorithm=HmacSHA256, access-key={COUPANG_ACCESS_KEY}, signed-date={timestamp}, signature={signature}"

def check_new_qa():
    """
    쿠팡에서 '답변 대기 중'인 문의를 실제로 수집합니다.
    """
    print("🔎 로봇 비서: 쿠팡 고객 문의(Q&A)를 확인합니다...")
    
    if not COUPANG_SELLER_ID:
        print("❌ 쿠팡 API 키가 설정되지 않았습니다.")
        return []

    from datetime import datetime, timedelta
    now = datetime.now()
    past = now - timedelta(days=7) # 최근 7일치 문의 검색
    from_date = past.strftime('%Y-%m-%d')
    to_date = now.strftime('%Y-%m-%d')

    path = f"/v2/providers/openapi/apis/api/v4/vendors/{COUPANG_SELLER_ID}/customerInquiries"
    method = "GET"
    query_string = f"answeredType=NO_ANSWER&createdAtFrom={from_date}&createdAtTo={to_date}"
    
    authorization = generate_signature(method, path, query_string)
    url = f"https://api-gateway.coupang.com{path}?{query_string}"
    headers = {"Content-Type": "application/json", "Authorization": authorization}
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json().get('data', {})
            qas = data.get('content', [])
            print(f"💬 답변 대기 중인 문의: {len(qas)}건 발견!")
            return qas
        else:
            print(f"❌ Q&A 수집 실패: {res.status_code}")
            return []
    except Exception as e:
        print(f"❌ Q&A 수집 중 오류: {e}")
        return []

def get_smart_answer(question_text):
    """B안: 키워드 기반 맞춤형 답변 생성"""
    q = question_text.replace(" ", "") # 공백 제거 후 검색
    
    if "배송" in q or "언제" in q or "출발" in q:
        return "고객님, 저희 과일은 평일 오전 10시 이전 주문 건에 한해 당일 산지 직송으로 출고됩니다. 신선하고 맛있는 과일로 꼼꼼히 포장하여 보내드리겠습니다! 조금만 기다려주세요."
    elif "반품" in q or "환불" in q or "취소" in q or "파손" in q or "썩" in q:
        return "불편을 드려 죄송합니다. 상품에 문제가 있으실 경우, 쿠팡 시스템에서 반품 접수를 해주시거나 불량 부분 사진을 고객센터로 보내주시면 담당자가 확인 후 빠르게 처리해 드리겠습니다."
    elif "유통기한" in q or "보관" in q or "숙성" in q:
        return "신선 식품이므로 가급적 수령 후 빠르게 드시는 것을 권장하며, 서늘한 곳이나 냉장 보관을 부탁드립니다. (후숙 과일의 경우 상온에서 1~2일 후숙 후 드시면 더욱 맛있습니다.)"
    else:
        return "과일 산지 직송 '김씨네 프레시'입니다! 문의하신 내용을 확인 중이며, 순차적으로 상세히 안내해 드리겠습니다. 감사합니다."

def reply_to_qa(qa_id, question_text):
    """
    쿠팡 문의에 답변을 작성합니다.
    (안전 모드: 실제 전송은 막아두고 화면에만 출력)
    """
    # 1. 스마트 답변 생성
    answer_text = get_smart_answer(question_text)
    
    print(f"\n======================================")
    print(f"✍️ [답변 시뮬레이션] 문의 ID: {qa_id}")
    print(f"❓ 고객 질문: {question_text}")
    print(f"💡 자동 답변: {answer_text}")
    print(f"======================================\n")
    
    # [차후 주석 해제 시 실제 답변이 등록되는 코드]
    '''
    path = f"/v2/providers/openapi/apis/api/v4/vendors/{COUPANG_SELLER_ID}/customerInquiries/{qa_id}/replies"
    method = "POST"
    authorization = generate_signature(method, path)
    url = f"https://api-gateway.coupang.com{path}"
    headers = {"Content-Type": "application/json", "Authorization": authorization}
    payload = {"content": answer_text}
    
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        print(f"✅ {qa_id} 문의에 답변이 등록되었습니다.")
    else:
        print(f"❌ 답변 등록 실패: {res.text}")
    '''
    
    return True
