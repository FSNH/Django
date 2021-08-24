import requests
import base64
import time
import execjs
import json


post_obj = {
    "timestamp": str(time.time() * 1000).split('.')[0],
    "bd": "BD675023"}
print(post_obj)
with open('./sign.js', 'r', encoding='utf-8')as f:
    js = execjs.compile(f.read())
    d = js.call('getSign', post_obj, 1)

    print(d)


exit()

post_obj = {
    "timestamp": str(time.time() * 1000).split('.')[0],
    "bd": "BD675023",
    "_": "NDFmOGU5YTMyZjZjNDMxZWIyMTViNWFlNmZkMDM2NjI=",
    "__": ['timestamp', 'bd']
}

# with open('./sign.js', 'r', encoding='utf-8')as f:
#     js = execjs.compile(f.read())
#     d = js.call('getSign', post_obj, 1)
#     post_obj['__'] = "['timestamp', 'bd']"
#     post_obj['_'] = str(d)
#     print(d)
#
# headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
# data = {
#     "params": "eyJ0aW1lc3RhbXAiOjE2MTc4NzE5MTQ1MTIsImJkIjoiQkQ2NzUwMjMiLCJfIjoiTXpFek1HWXdZbVZoWmpOaE1EUmlNbVZoTTJKaVl6UTRaV1F3T1RJMU5EYz0iLCJfXyI6WyJ0aW1lc3RhbXAiLCJiZCJdfQ====",
#
# }
# url = 'https://www.bidepharm.com/webapi/v1/getproductstocklocal'
# response = requests.post(url=url, data=data, headers=headers)
# info = response.json().get('value')[2:]
# print(info)
# for i in info:
#     dict = {}
#     dict['quantity_cd'] = i.get('quantity_cd')
#     dict['quantity_sz'] = i.get('quantity_sz')
#     dict['quantity_sh'] = i.get('quantity_sh')
#     dict['quantity_tj'] = i.get('quantity_tj')
#     dict['quantity_wh'] = i.get('quantity_wh')
#
#
#     print(dict)
#
# print(post_obj)
