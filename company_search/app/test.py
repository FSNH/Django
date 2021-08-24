import requests

headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
url=''
data=''
resp = requests.post(url=url, data=json.dumps(data), headers=headers)
# print(resp.text)
total = resp.json().get("totalcount")
result_list = resp.json().get('list')