import requests
from lostark_api_token import Token

headers = {
    'accept': 'application/json',
    'authorization': Token,
    'Content-Type': 'application/json',
}

url = 'https://developer-lostark.game.onstove.com/markets/items'

def fetch_items(json_data):
    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        jsonObject = response.json()
        return jsonObject.get("Items", [])  # 'Items'가 없을 때 빈 리스트 반환
    except requests.RequestException as err:
        return [-1, f"요청 오류 발생: {err}"]
    except ValueError as json_err:
        return [-1, f"JSON 파싱 오류 발생: {json_err}"]
    except Exception as err:
        return [-1, f"알 수 없는 오류 발생: {err}"]

def item():
    items = []
    categoryCord = [90200, 90300, 90400, 90500, 90600, 90700]

    for temp in categoryCord:
        json_data = {
            'Sort': 'GRADE',
            'CategoryCode': temp,
            'SortCondition': 'ASC',
        }
        result = fetch_items(json_data)
        if result[0] == -1:
            return result
        items.append(result)

    additional_data = {
        'Sort': 'GRADE',
        'CategoryCode': 50010,
        'ItemName': '융화',
        'SortCondition': 'ASC',
    }
    additional_result = fetch_items(additional_data)
    if additional_result[0] == -1:
        return additional_result
    items.append(additional_result)

    return items  # 최종 데이터 반환
