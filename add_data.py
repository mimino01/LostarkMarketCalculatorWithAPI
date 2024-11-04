import time
import tkinter as tk
import os
import sys
from pickle import GLOBAL
from tokenize import Double
from xmlrpc.client import Boolean

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from lostark_api_front import item
from datetime import date, datetime

MESSAGE = []
ERROR = []
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1QpKxz3ghKcjthG4j8FvOmpYmVMLaEnTrpEWef58IkF8'
CURRENT_TIME = ""
DATA_LIMIT = True
MINUTE_LIMIT = [True, 0]

def set_ten_minute_union_values():
    global CURRENT_TIME
    data = get_data('데이터!AE2:AH2')
    lens = get_data('통계!S:T')
    body = {
        'values': [
            [
                CURRENT_TIME,
                data[0][0],
                data[0][2],
                data[0][3],
                data[0][1]
            ]
        ]
    }
    insert_data(f'통계!S{len(lens)+1}',body)

def set_today_stuff_values():
    values = get_data('통계!A:E')
    today = date.today().strftime("%m/%d")
    if not values:
        print('No data found.')
    else:
        # for row in values:
        #     print(row)
        body = {
            'values': [
                [
                    today,
                    float(values[0][3]),
                    float(values[0][4])
                ]
            ]
        }
        insert_data(f'통계!A{len(values)+1}',body)

def set_life_earn_values():
    values = get_data('생활계산기!BL:BN')
    # for a in values:
    #     print(a)
    # values = get_data('생활계산기!BN6:BN8')
    today = date.today().strftime("%m/%d")
    if not values:
        print('No data found.')
    else:
        body = {
            'values': [
                [
                    today,
                    values[5][0],
                    values[7][0]
                ]
            ]
        }
        insert_data(f'생활계산기!BL{len(values)+1}',body)

def set_today_union_values():
    data = get_data('데이터!AE3:AH3')
    lens = get_data('통계!Y:Z')
    today = date.today().strftime("%m/%d")
    body = {
        'values': [
            [
                today,
                data[0][0],
                data[0][2],
                data[0][3],
                data[0][1]
            ]
        ]
    }
    insert_data(f'통계!Y{len(lens)+1}',body)

def set_today_data_recoding():
    set_today_stuff_values()
    set_life_earn_values()
    set_today_union_values()

def set_ten_minute_data_recoding():
    set_ten_minute_union_values()

def get_keyfile_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)

def get_service():
    keyfile_path = get_keyfile_path('lofty-digit-433703-n1-f7e9bc4aa1f1.json')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile_path, SCOPES)
    http_auth = credentials.authorize(Http(timeout=30))
    return build('sheets', 'v4', http=http_auth)

def insert_data(path, body):
    service = get_service()
    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                     range=path,
                                                     valueInputOption='USER_ENTERED',
                                                     body=body)
    request.execute()

def get_data(path):
    service = get_service()
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=path).execute()
    values = result.get('values', [])
    return values

def main():
    global DATA_LIMIT
    global MINUTE_LIMIT
    retry_count = 3
    retry_delay = 60

    for attempt in range(retry_count):
        try:
            hour = datetime.now().hour
            minute = datetime.now().minute
            if (hour == 2) & DATA_LIMIT:
                DATA_LIMIT = False
                set_today_data_recoding()
            elif (hour == 3) & (not DATA_LIMIT):
                DATA_LIMIT = True

            if MINUTE_LIMIT[0]:
                set_ten_minute_data_recoding()
                MINUTE_LIMIT = [False,minute]
                # print(f'run{MINUTE_LIMIT}')
            elif MINUTE_LIMIT[0] == False and (minute % 10 == 0) and (not (minute / 10 == MINUTE_LIMIT[1] / 10)):
                MINUTE_LIMIT[0] = True
                # print(f"cold time is back{MINUTE_LIMIT}")

            item_data = item()
            if item_data[0] == -1:
                ERROR.append(item_data[1])
                return item_data[1]
            else:
                data_body = prepare_data_body(item_data)
                insert_data('데이터!B1', data_body)
                return "connect and execute"

        except Exception as e:
            if attempt < retry_count - 1:
                time.sleep(retry_delay)
                continue
            else:
                return f"Error after {retry_count} attempts: {e}"

def prepare_data_body(item_data):
    name = []
    cPrice = []
    yPrice = []
    pdProfit = []
    for category in item_data:
        for entry in category:
            name.append(entry.get('Name', 'N/A'))
            cPrice.append(entry.get('RecentPrice', 0))
            pdProfit.append(entry.get('RecentPrice', 0) / max(entry.get('YDayAvgPrice', 1), 1) * 100)
            if entry.get('YDayAvgPrice') == 0:
                yPrice.append(entry.get('RecentPrice', 0))
            else:
                yPrice.append(entry.get('YDayAvgPrice', 0))

    return {
        'values': [
            name,
            cPrice,
            yPrice,
            pdProfit,
            [CURRENT_TIME]
        ]
    }

def app():
    return main()
    # return testMain()

def testMain():
    set_today_union_values()


def update_message():
    global CURRENT_TIME
    CURRENT_TIME = time.strftime('%Y-%m-%d %H:%M:%S')
    response = app()
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