import time
import tkinter as tk
import os
import sys

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from lostark_api_front import item

MESSAGE = []
ERROR = []
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1QpKxz3ghKcjthG4j8FvOmpYmVMLaEnTrpEWef58IkF8'
CURRENT_TIME = ""

def get_keyfile_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)

def main():
    retry_count = 3  # 최대 3번 재시도
    retry_delay = 60  # 재시도 간격 (초)

    for attempt in range(retry_count):
        try:
            item()
            item_data = item()
            if item_data[0] == -1:
                print("오류")
                return item_data[1]
            else:
                name = []
                cPrice = []
                c_time = []
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
                keyfile_path = get_keyfile_path('lofty-digit-433703-n1-f7e9bc4aa1f1.json')
                credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile_path, SCOPES)
                http_auth = credentials.authorize(Http(timeout=30))
                service = build('sheets', 'v4', http=http_auth)
                request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                                 range='데이터!B1',
                                                                 valueInputOption='RAW',
                                                                 body=body)
                request.execute()
                return "connect and execute"

        except Exception as e:
            if attempt < retry_count - 1:
                time.sleep(retry_delay)  # 재시도 전 대기 시간
                continue  # 다시 시도
            else:
                return f"Error after {retry_count} attempts: {e}"

def update_message():
    global CURRENT_TIME
    CURRENT_TIME = time.strftime('%Y-%m-%d %H:%M:%S')
    response = main()
    new_message = f"갱신된 시간: {CURRENT_TIME} \n서버 상태: {response} \n"
    MESSAGE.insert(0, new_message)

    # Text 위젯에 메시지 업데이트
    message_text.delete(1.0, tk.END)  # 기존 내용 삭제
    message_text.insert(tk.END, "\n".join(MESSAGE))  # 새로운 내용 추가

    if response != "connect and execute":
        new_error = f"갱신된 시간: {CURRENT_TIME} \n서버 상태: {response} \n"
        ERROR.insert(0, new_error)
        error_text.delete(1.0, tk.END)
        error_text.insert(tk.END, "\n".join(ERROR))

    root.after(10000, update_message)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("데이터 갱신")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # 수직 스크롤바 생성
    scrollbar_y = tk.Scrollbar(frame, orient="vertical")
    scrollbar_y.grid(row = 0, column = 1, sticky="ns")

    # 메시지를 표시할 Text 위젯 생성
    message_text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar_y.set, height=15, width=50)
    message_text.grid(row = 0, column = 0)

    # 스크롤바와 Text 위젯 연동
    scrollbar_y.config(command=message_text.yview)

    scrollbar_error = tk.Scrollbar(frame, orient="vertical")
    scrollbar_error.grid(row = 1, column = 1, sticky="ns")

    error_text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar_error.set, height=10, width=50)
    error_text.grid(row = 1, column = 0)

    scrollbar_error.config(command=error_text.yview)

    update_message()
    root.mainloop()