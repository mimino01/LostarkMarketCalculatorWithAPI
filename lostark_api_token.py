from dotenv import load_dotenv
import os
# lostark_api_token.py
# 복사한 토큰을 아래와 같이 입력
# bearer 문구를 지우게 되면 에러코드가 발생하므로 지우지 않도록 한다.
load_dotenv()
Token = os.getenv("API_KEY")