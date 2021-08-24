# 消息订阅
import json

import redis

r = redis.StrictRedis(host="127.0.0.1", port=6379)
p = r.pubsub()
p.subscribe("first channel")
while True:
    message = p.listen()
    for i in message:
        if i["type"] == 'message':
            d = json.loads(i["data"])
            print(json.loads(i["data"]))
            if d['source'] == 'xlsw':
                print(d['source_url'])
            else:
                print('xsxxxxxxxxxxxxxxxxxxxxx')
