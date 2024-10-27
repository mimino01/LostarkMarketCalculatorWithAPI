import requests
from lostark_api_token import Token

headers = {
    'accept': 'application/json',
    'authorization': Token,
    'Content-Type': 'application/json',
}

url = 'https://developer-lostark.game.onstove.com/markets/items'

# 요청을 처리하는 함수
def fetch_items(json_data):
    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()  # HTTP 에러가 발생했는지 확인
        jsonObject = response.json()
        return jsonObject.get("Items", [])  # 'Items'가 없을 때 빈 리스트 반환
    except requests.exceptions.HTTPError as http_err:
        # print(f"HTTP 오류 발생: {http_err}")
        return [-1,f"HTTP 오류 발생: {http_err}"]  # 오류 발생 시 오류 메시지 반환
    except requests.exceptions.RequestException as req_err:
        # print(f"요청 오류 발생: {req_err}")
        return [-1,f"요청 오류 발생: {req_err}"]  # 오류 발생 시 오류 메시지 반환
    except ValueError as json_err:
        # print(f"JSON 파싱 오류 발생: {json_err}")
        return [-1,f"파싱 오류 발생: {json_err}"]  # 오류 발생 시 오류 메시지 반환
    except Exception as err:
        # print(f"알 수 없는 오류 발생: {err}")
        return [-1,f"알 수 없는 오류 발생: {err}"]  # 오류 발생 시 오류 메시지 반환

# 생활 데이터 받아오기 함수
def item():
    items = []  # 매번 호출 시 리스트 초기화
    categoryCord = [90200, 90300, 90400, 90500, 90600, 90700]

    for temp in categoryCord:
        json_data = {
            'Sort': 'GRADE',
            'CategoryCode': temp,
            'SortCondition': 'ASC',
        }
        result = fetch_items(json_data)  # 요청 함수 호출
        if result[0] == -1:  # 오류 발생 시 즉시 반환
            print(result[0],result[1])
            return result
        items.append(result)

    # 추가 요청 처리
    json_data = {
        'Sort': 'GRADE',
        'CategoryCode': 50010,
        'ItemName': '융화',
        'SortCondition': 'ASC',
    }
    result = fetch_items(json_data)
    if result[0] == 0:  # 오류 발생 시 즉시 반환
        return result
    items.append(result)

    return items  # 최종 데이터 반환
