import pymongo
import redis
from bson import ObjectId
# mongo = pymongo.MongoClient(host='127.0.0.1',port=27017)  # 开启数据库实例
# db = mongo.keyword
# collection = db.baidukeyword
#
# count = collection.find().count()
# print(count)
# data = ["5fb1d2f2c037275a19e8d973","5fb1d2f5c037275a19e8d974","5fb1d2f5c037275a19e8d975","5fb1d2f7c037275a19e8d976"]
# for i in data:
# 	print(i)
# 	data = collection.update({"_id": ObjectId(i)}, {'$set': {'checkstate': 0}})
# 	print(data)

# client = redis.Redis(host='127.0.0.1',port=6379,db=0)
# v = client.get("f")
# client.incr("f")
# client.incr("f")
#
#
# print(v)
import pymongo
import math
client = pymongo.MongoClient(host="192.168.1.30",port=27017)  # 开启数据库实例
db = client["db_5bc68c19f7000afcb87c0a4b"]
nums = 134
page_nums = 50
count = math.ceil(int(db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find(
    {"_360longtailkeywordurl_pickstatus": 0}).count()) // page_nums) +1
print(count)
# results = db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find({"_360longtailkeywordurl_pickstatus": 0}).sort( '_id', 1).skip((int(nums) - 1) * page_nums).limit(page_nums)
# for i ,result in enumerate(results,1):
#     print(i,result)
