# -*- encoding="utf8"-*-
import math
from gevent import pywsgi
from bson import ObjectId
from flask import Flask, render_template, jsonify, redirect, url_for, request, session
from flask_pymongo import PyMongo
import redis

app = Flask(__name__)
app.config['DEBUG'] = True  # 开启 debug
client = redis.Redis(host="127.0.0.1", port=6379, db=0)
mongo = PyMongo(app, uri="mongodb://192.168.1.30:27017/db_5bc68c19f7000afcb87c0a4b")  # 开启数据库实例
# mongo = PyMongo(app, uri="mongodb://127.0.0.1:27017/keyword")  # 开启数据库实例

from urllib.parse import urlparse, urljoin

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# 函数功能，传入当前url 跳转回当前url的前一个url
def redirect_back(backurl, **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(backurl, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def setcountbyredis():
    client.set("passcount", 2170)
    client.set("delcount", 2170)
    pass


@app.route('/getall_waitpick/', methods=['GET'])
def getall_waitpick():
    # setpasscountbyredis() 设置redis数据值
    global count, results, wait_count
    keyword = request.args.get('keyword', '')
    # print(keyword)
    nums = request.args.get('page', 1)  # 默认第一页
    page_nums = int(request.args.get('per_nums', 100))
    if keyword:
        """
        关键词搜索
        """
        count = math.ceil(int(mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find(
            {"$and": [{"_360longtailkeywordurl_pickstatus": {"$nin": [1, 2]}},
                      {"longtailkeyword": {"$regex": keyword}}]}).count()) // page_nums) + 1
        # print(count)
        results = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find(
            {"$and": [{"_360longtailkeywordurl_pickstatus": {"$nin": [1, 2]}},
                      {"longtailkeyword": {'$regex': keyword}}]}).sort('_id', 1).skip(
            (int(nums) - 1) * page_nums).limit(page_nums)
        wait_count = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find(
            {"$and": [{"_360longtailkeywordurl_pickstatus": {"$in": [0, 1]}}, {"checkstate": 1},
                      {"longtailkeyword": {'$regex': keyword}}]}).count()

    else:
        count = math.ceil(int(mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find(
            {"$and": [{"_360longtailkeywordurl_pickstatus": {"$nin": [1, 2]}}]}).count()) // page_nums) + 1
        results = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find(
            {"$and": [{"_360longtailkeywordurl_pickstatus": {"$nin": [1, 2]}}]}).sort('_id', 1).skip(
            (int(nums) - 1) * page_nums).limit(page_nums)
        wait_count = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find(
            {"$and": [{"_360longtailkeywordurl_pickstatus": {"$in": [0, 1]}}, {"checkstate": 1}]}).count()
        print("待采集", wait_count)
    if int(nums) <= 0:
        nums = 1
    elif int(nums) >= count:
        nums = count
    data = []
    for result in results:
        data.append(result)
    # print(data.__len__())
    # print(data)
    check_count = client.get("passcount").decode()
    del_count = client.get("delcount").decode()
    if results:
        # print(results)
        return render_template('index.html', users=data, count=count, pages=nums, check_count=check_count,
                               wait_count=wait_count, page_nums=page_nums)
    else:
        return 'No user found!'


# 审核通过就修改状态
@app.route('/check_pass_state/', methods=['POST', 'GET'])
def check_pass_state():
    if request.method == "GET":
        id = request.args.get('id')
        if id:
            result = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.update_one({'_id': ObjectId(id)},
                                                                                         {'$set': {'checkstate': 1}})
            if result:
                client.incr("passcount")
                # print(result)
                return redirect_back('/check_pass_state/')
    else:
        data = request.form.get("data")
        global check
        if data:
            # print(data.split(';'))
            ids = []
            # 可以在此处累加审核通过的数据量
            for id in data.split(';'):
                # print(id)
                client.incr("passcount")
                check = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.update({'_id': ObjectId(id)},
                                                                                        {'$set': {'checkstate': 1}})
                ids.append(id)
            if check:
                return {'code': 'success', 'data': ids}
    pass


@app.route('/check_no_state/<id>', methods=['GET', 'POST'])
def check_no_state(id):
    if request.method == "POST":
        id = request.form.get("id")
        result = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.update_one({'_id': ObjectId(id)},
                                                                                     {'$set': {'checkstate': 0}})
        return {"code": "success", "id": id}
    else:
        result = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.update_one({'_id': ObjectId(id)},
                                                                                     {'$set': {'checkstate': 0}})
        if result:
            return redirect_back('/check_no_state/')
    pass


# 删除为id的数据
@app.route('/delete_id/', methods=['GET', 'POST'])
def delete_id():
    global de_result
    if request.method == "GET":
        id = request.args.get('id')
        result = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.delete_one({'_id': ObjectId(id)})
        if result:
            client.incr("delcount")
            return redirect_back('/delete_id/')
    else:
        ids = []
        data = request.form.get('data')
        if data:
            for id in data.split(";"):
                ids.append(id)
                client.incr("delcount")
                de_result = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.delete_one({'_id': ObjectId(id)})
            if de_result:
                return {'data': ids}
    pass


# 获取单条信息
@app.route('/getonebyid/<id>', methods=['GET', 'POST'])
def get_id(id):
    result = mongo.db.entity_5bc68c19f7000afcb87c0a4b_longtailkeyword.find({'_id': ObjectId(id)})
    if result:
        print(result)
        # for res in result:
        #     print(type(res))
        #     print(res['cas'])
        #     print(res['_id'])
        return {'code': "success"}
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# if __name__ == '__main__':
#     server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
#     server.serve_forever()
#     app.run()

