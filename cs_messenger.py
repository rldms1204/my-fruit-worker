import os
import json
import requests
import time
import hmac
import hashlib

# 💡 문자/알림톡 발송용 뼈대 코드
# 사장님이 '솔라피(Solapi)' 등에 가입하시면 API 키를 넣어서 완성합니다.

def send_cs_message(phone_number, message_text):
    """
    고객에게 문자를 발송하는 함수입니다.
    현재는 안전을 위해 실제로 발송되지 않고 화면에 출력만 됩니다.
    """
    print(f"📱 [가상 발송 테스트] 수신번호: {phone_number}")
    print(f"   내용: {message_text}")
    
    # --------------------------------------------------------
    # [차후 추가될 실제 솔라피 API 발송 코드 영역]
    # API_KEY = os.environ.get('SOLAPI_API_KEY')
    # API_SECRET = os.environ.get('SOLAPI_SECRET_KEY')
    # --------------------------------------------------------
    
    print("✅ (테스트) 문자 발송이 완료된 것처럼 처리되었습니다.\n")
    return True
