import requests
import json

# url = 'http://lagoon3.duckdns.org:20226/mealMenu/getMenu/Menu?date=2023-12-29'
# response = requests.get(url)

url = 'http://lagoon3.duckdns.org:20226/mealMenu/getMenu/Menu'
data = {
    'bot':'',
    'action':{
        'params':
            {'date':'2024-01-02'},
        'clientExtra': 
            {'restaurant' : '한빛식당'}
    },
    'date': '2024-01-02',
    # 'time': '점심',
    # 'restaurant': '한빛식당',
}
response = requests.post(url, data = json.dumps(data))
print(response.json())