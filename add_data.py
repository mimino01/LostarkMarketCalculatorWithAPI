import time
import tkinter as tk

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from lostark_api_front import item

# 초기 메시지를 저장할 리스트
MESSAGE = []
# Google API 요청 시 필요한 권한 유형
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# 구글 시트 ID
SPREADSHEET_ID = '1QpKxz3ghKcjthG4j8FvOmpYmVMLaEnTrpEWef58IkF8'
CURRENT_TIME = ""


def main():
    if(item() == list()):
        return "not connect server"
    else:
        name = list()
        cPrice = list()
        c_time = list()
        c_time.append(CURRENT_TIME)
        for x in item():
            for y in x:
                name.append(y['Name'])
                cPrice.append(y['RecentPrice'])
        body = {
            'values': [
                name,
                cPrice,
                c_time
            ]
        }
        # json 파일로 서비스 계정 credential 정의
        credentials = ServiceAccountCredentials.from_json_keyfile_name('lofty-digit-433703-n1-f7e9bc4aa1f1.json', SCOPES)
        http_auth = credentials.authorize(Http())
        service = build('sheets', 'v4', http=http_auth)
        # 업데이트 요청 및 실행
        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                         range='데이터!B1',  # 2
                                                         valueInputOption='RAW',
                                                         body=body)
        request.execute()
        return "connect and execute"

def update_message():
    #시간 갱신
    global CURRENT_TIME
    CURRENT_TIME = time.strftime('%Y-%m-%d %H:%M:%S')

    #서버 데이터 갱신
    response = main()

    # 현재 시간을 기반으로 한 새로운 메시지 생성
    new_message = f"갱신된 시간: {CURRENT_TIME} \n서버 상태: {response} \n"

    # 새로운 메시지를 리스트에 추가
    MESSAGE.insert(0,new_message)

    # 모든 메시지를 라벨에 표시 (이전 메시지 포함)
    message_label.config(text="\n".join(MESSAGE))

    # 1초 후에 다시 메시지 갱신
    root.after(18000, update_message)

if __name__ == '__main__':
    # Tkinter 윈도우 생성
    root = tk.Tk()
    root.title("데이터 갱신")

    # 메시지를 표시할 라벨 생성 (멀티라인 지원을 위해 anchor 설정)
    message_label = tk.Label(root, text="초기 메시지", anchor="w", justify="left", font=("Helvetica", 12))
    message_label.pack(padx=10, pady=10)

    # 메시지 업데이트 함수 호출
    update_message()

    # Tkinter 이벤트 루프 시작
    root.mainloop()