import os
import requests
import time
import hmac
import hashlib

# 1. 금고에서 열쇠 꺼내기
COUPANG_ACCESS_KEY = os.environ.get('COUPANG_ACCESS_KEY')
COUPANG_SECRET_KEY = os.environ.get('COUPANG_SECRET_KEY')
COUPANG_SELLER_ID = os.environ.get('COUPANG_SELLER_ID')

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

# 실행
if __name__ == "__main__":
    orders = get_orders()
    if orders:
        print("💡 도매처(어드민플러스)로 발주 전송을 시도합니다...")
        # 여기에 실제 어드민플러스 전송 코드가 들어갑니다.
    print("✅ 오늘의 자동 업무가 완료되었습니다.")
