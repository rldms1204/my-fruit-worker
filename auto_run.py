import os
import requests
import time
import hmac
import hashlib
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

import cs_messenger
import coupang_qa

# 1. 금고에서 기본 열쇠들 꺼내기
COUPANG_ACCESS_KEY = os.environ.get('COUPANG_ACCESS_KEY')
COUPANG_SECRET_KEY = os.environ.get('COUPANG_SECRET_KEY')
COUPANG_SELLER_ID = os.environ.get('COUPANG_SELLER_ID')
GOOGLE_SHEETS_JSON = os.environ.get('GOOGLE_SHEETS_JSON')

# 2. 구글 시트에서 오늘의 도매처와 스위치 상태를 읽어오는 함수
def get_today_settings():
    try:
        key_dict = json.loads(GOOGLE_SHEETS_JSON)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
        client = gspread.authorize(creds)
        
        # 시트 이름이 '김씨네 프레시'인지 확인하세요!
        sheet = client.open("김씨네 프레시").sheet1
        
        wholesaler = sheet.acell('B2').value or "도매처A"
        qa_status = sheet.acell('C2').value or "OFF"
        cs_status = sheet.acell('D2').value or "OFF"
        
        return wholesaler, qa_status, cs_status
    except Exception as e:
        print(f"❌ 구글 시트를 읽는 중 오류 발생: {e}")
        return "도매처A", "OFF", "OFF" # 오류 나면 전부 기본값/OFF 처리

# 3. 쿠팡 주문 수집 함수 (기존 코드 유지)
def get_orders():
    print("🚀 로봇 비서: 쿠팡에서 신규 주문을 수집합니다...")
    path = f"/v2/providers/openapi/apis/api/v4/vendors/{COUPANG_SELLER_ID}/ordersheets"
    method = "GET"
    query_string = "status=ACCEPT"
    timestamp = time.strftime('%y%m%dT%H%M%SZ', time.gmtime())
    message = timestamp + method + path + query_string
    signature = hmac.new(COUPANG_SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization = f"CEA algorithm=HmacSHA256, access-key={COUPANG_ACCESS_KEY}, signed-date={timestamp}, signature={signature}"
    url = f"https://api-gateway.coupang.com{path}?{query_string}"
    headers = {"Content-Type": "application/json", "Authorization": authorization}
    
    res = requests.get(url, headers=headers)
    orders = res.json().get('data', [])
    print(f"📦 수집 완료: 총 {len(orders)}건의 주문을 찾았습니다.")
    return orders

# 4. 메인 실행부
if __name__ == "__main__":
    # [단계 1] 구글 시트에서 설정 읽어오기
    selected_wh, qa_status, cs_status = get_today_settings()
    print(f"📍 오늘의 타겟 도매처: {selected_wh}")
    print(f"📍 Q&A 자동화: {qa_status}, CS 자동화: {cs_status}")

    # [단계 2] 선택된 도매처에 맞는 열쇠 세팅
    if selected_wh == "도매처B":
        ADMIN_ID = os.environ.get('ADMINPLUS_B_ID')
        ADMIN_SECRET = os.environ.get('ADMINPLUS_B_SECRET')
        print("🔗 도매처 B(ADMINPLUS_B) 열쇠를 장착했습니다.")
    else:
        ADMIN_ID = os.environ.get('ADMINPLUS_A_ID')
        ADMIN_SECRET = os.environ.get('ADMINPLUS_A_SECRET')
        print("🔗 도매처 A(ADMINPLUS_A) 열쇠를 장착했습니다.")

    # [단계 3] 쿠팡 주문 가져오기
    orders = get_orders()

    if orders:
        print(f"💡 {selected_wh}로 발주 전송을 시도합니다... (ID: {ADMIN_ID})")
        # 여기에 사장님의 실제 발주 전송 로직(requests.post 등)을 넣으면 끝!
        
    print("\n==============================================")
    if cs_status == "ON":
        print("💌 [부가기능 1] CS 문자 자동 발송 시작")
        print("==============================================")
        cs_messenger.send_cs_message("010-1234-5678", "고객님, 사과가 오늘 싱싱하게 출발했습니다!")
    else:
        print("💌 [부가기능 1] CS 문자 자동 발송 (OFF 상태라 건너뜁니다)")
        print("==============================================")
        
    print("\n==============================================")
    if qa_status == "ON":
        print("💬 [부가기능 2] 쿠팡 Q&A 자동 확인 시작")
        print("==============================================")
        qas = coupang_qa.check_new_qa()
        for qa in qas:
            qa_id = qa.get('inquiryId', '알수없음')
            question_text = qa.get('content', '')
            coupang_qa.reply_to_qa(qa_id, question_text)
    else:
        print("💬 [부가기능 2] 쿠팡 Q&A 자동 확인 (OFF 상태라 건너뜁니다)")
        print("==============================================")
        
    print("\n✅ 오늘의 발주, CS 문자, Q&A 업무가 모두 완료되었습니다.")

