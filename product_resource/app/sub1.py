# 消息订阅
import json

import redis


def redis_listen():
    r = redis.StrictRedis(host="127.0.0.1", port=6379)
    p = r.pubsub()
    p.subscribe("first channel")
    while True:
        message = p.listen()
        for i in message:
            if i["type"] == 'message':
                print(json.loads(i["data"]))