import requests
from lostark_api_token import Token

headers = {
    'accept': 'application/json',
    'authorization': Token,
    'Content-Type': 'application/json',
}

categoryCord = [90200, 90300, 90400, 90500, 90600, 90700]
items = list()
url = 'https://developer-lostark.game.onstove.com/markets/items'

# 예외 처리를 추가한 코드
for temp in categoryCord:
    json_data = {
        'Sort': 'GRADE',
        'CategoryCode': temp,
        'SortCondition': 'ASC',
    }
    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()  # HTTP 에러가 발생했는지 확인
        jsonObject = response.json()
        items.append(jsonObject.get("Items", []))  # 'Items'가 없을 때 빈 리스트를 반환
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 오류 발생: {req_err}")
    except ValueError as json_err:
        print(f"JSON 파싱 오류 발생: {json_err}")
    except Exception as err:
        print(f"알 수 없는 오류 발생: {err}")

# 추가 요청에 대한 예외 처리
json_data = {
    'Sort': 'GRADE',
    'CategoryCode': 50010,
    'ItemName': '융화',
    'SortCondition': 'ASC',
}
try:
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    jsonObject = response.json()
    items.append(jsonObject.get("Items", []))
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP 오류 발생: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"요청 오류 발생: {req_err}")
except ValueError as json_err:
    print(f"JSON 파싱 오류 발생: {json_err}")
except Exception as err:
    print(f"알 수 없는 오류 발생: {err}")
    items = list()  # 오류 발생 시 빈 리스트로 초기화

def item():
    return items
