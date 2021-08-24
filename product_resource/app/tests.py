# Create your tests here
import redis
# 消息推送
import time
import json
r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

i = 0
while True:
    i += 1
    info = {
        'source': "xlsw",
        'source_url': 'http://www.biobiopha.com/view/xlswPC/1/49/view/7574.html',
        "num": i
    }
    r.publish("first channel", json.dumps(info))
    print("the info " + json.dumps(info))
    time.sleep(1)




