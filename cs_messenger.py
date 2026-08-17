import os
import time
import uuid
import hmac
import hashlib
import requests

def get_solapi_signature(api_secret, data):
    return hmac.new(api_secret.encode(), data.encode(), hashlib.sha256).hexdigest()

def send_cs_message(phone_number, message_text):
    """
    솔라피(Solapi)를 통해 고객에게 실제 문자를 발송합니다.
    """
    print(f"📱 [CS 문자 발송 시도] 수신번호: {phone_number}")
    
    API_KEY = os.environ.get('SOLAPI_API_KEY')
    API_SECRET = os.environ.get('SOLAPI_API_SECRET')
    
    if not API_KEY or not API_SECRET:
        print("❌ 솔라피 API 키가 설정되지 않아 발송을 건너뜁니다.")
        return False
        
    date = time.strftime('%Y-%m-%dT%H:%M:%S%Z')
    salt = str(uuid.uuid1().hex)
    data = date + salt
    signature = get_solapi_signature(API_SECRET, data)
    
    auth = f'HMAC-SHA256 apiKey={API_KEY}, date={date}, salt={salt}, signature={signature}'
    
    # ⚠️ 주의: 반드시 솔라피 사이트에서 발신번호를 먼저 등록해야 합니다!
    SENDER_NUMBER = "01000000000" # 추후 사장님 폰번호로 변경 필요
    
    payload = {
        "message": {
            "to": phone_number.replace("-", ""),
            "from": SENDER_NUMBER,
            "text": message_text
        }
    }
    
    url = "https://api.solapi.com/messages/v4/send"
    headers = {
        "Authorization": auth,
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            print(f"✅ 문자 발송 완료! (내용: {message_text})")
            return True
        else:
            print(f"❌ 문자 발송 실패: {res.text}")
            return False
    except Exception as e:
        print(f"❌ 문자 발송 중 오류: {e}")
        return False

