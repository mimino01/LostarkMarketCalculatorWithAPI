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


for temp in categoryCord:
    json_data = {
        'Sort': 'GRADE',
        'CategoryCode': temp,
        # 'CharacterClass': 'string',
        # 'ItemTier': 0,
        # 'ItemGrade': 'string',
        # 'ItemName': 'string',
        # 'PageNo': 1,
        'SortCondition': 'ASC',
    }
    response = requests.post(url , headers=headers, json=json_data)
    jsonObject = response.json()
    items.append(jsonObject.get("Items"))
json_data = {
    'Sort': 'GRADE',
    'CategoryCode': 50010,
    # 'CharacterClass': 'string',
    # 'ItemTier': 0,
    # 'ItemGrade': 'string',
    'ItemName': '융화',
    # 'PageNo': 1,
    'SortCondition': 'ASC',
}
response = requests.post(url , headers=headers, json=json_data)
jsonObject = response.json()
items.append(jsonObject.get("Items"))

def item():
    return items

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n  "Sort": "GRADE",\n  "CategoryCode": 0,\n  "CharacterClass": "string",\n  "ItemTier": 3,\n  "ItemGrade": "string",\n  "ItemName": "string",\n  "PageNo": 0,\n  "SortCondition": "ASC"\n}'
#response = requests.post('https://developer-lostark.game.onstove.com/markets/items', headers=headers, data=data)