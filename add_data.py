import time

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from lostark_api_front import item

# Google API 요청 시 필요한 권한 유형
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# 구글 시트 ID
SPREADSHEET_ID = '1QpKxz3ghKcjthG4j8FvOmpYmVMLaEnTrpEWef58IkF8'

def main():
    name = list()
    cPrice = list()
    for x in item():
        for y in x:
            name.append(y['Name'])
            cPrice.append(y['RecentPrice'])
    body = {
        'values': [
            name,
            cPrice
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
    print("execute")

if __name__ == '__main__':
    while True:
        main()
        time.sleep(1800)