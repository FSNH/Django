import pymssql
import redis
# 连接池
# 并发的话，把他做成单例，写在一个文件里面，import它
import redis
import json
from pymongo import MongoClient
from influxdb import InfluxDBClient
from datetime import datetime
import requests
import time
from boat.models import SpiderInfo, SaveSource
import logging
import pandas as pd
import datetime


class SqlConnect(object):
    def __init__(self):
        # self.connect = pymssql.connect('192.168.1.26', 'chem960-2018', 'chem960-2018@', 'ChemPrice-2021')  # 建立连接
        self.connect = pymssql.connect(server='web.test.web960.com', port='14326', user='chem960-2018',
                                       password='chem960-2018@',
                                       database='ChemPrice-2021')  # 建立连接
        if self.connect:
            print("连接成功!")
        self.cursor = self.connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行

    def select(self, url):
        sql = f"select * from ChemPriceList where SourceUrl={repr(url)}"  # SQL语句
        self.cursor.execute(sql)  # 执行sql语句
        results = self.cursor.fetchall()
        data = []
        for result in results:
            p_data = {
                "ProductNo": result[1],
                "ProductName": result[2],
                "CasNo": result[3],
                "Purity": result[4],
                "Specification": result[5],
                "Price": result[6],
                "InStock": result[7],
                "CompanyName": result[8],
                "Souce": result[9],
                "SourceUrl": result[10],
                "LastModificationTime": str(result[17]).replace('T', ' ')
            }

            data.append(p_data)
            # print(result)
        # data = pd.DataFrame(self.cursor.fetchall())  # 读取查询结果
        print(data)
        return data

    def close(self):
        self.cursor.close()  # 关闭游标
        self.connect.close()  # 关闭连接


class RedisClient(object):
    # redis 连接池
    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)  # 本地
        self.queue = 'url_data'

    @property
    def conn(self):
        # 判断实例对象是否连接，没有连接就调用连接方法，并返回连接对象，否之直接父返回已经连接的对象
        if not hasattr(self, '_conn'):
            self.getConnection()
        return self._conn

    def getConnection(self):
        # 创建连接池，从中获取一个连接
        self._conn = redis.Redis(connection_pool=self.pool)

    def put(self, data):
        """
        put data to redis
        :param data:
        :return:
        """
        self.conn.lpush(self.queue, data)

    def listen_task(self):
        """
        get data by redis
        监听的方式获取（阻塞）
        :return:
        """
        while True:
            task = self.conn.blpop(self.queue, 0)[1]
            print("Task get", task)
            return task

    def pub_info(self, info):
        """
        redis发布
        :param info:
        :return:
        """
        self.conn.publish(self.queue, json.dumps(info))

    def sub_info(self):
        """
        redis订阅
        :param info:
        :return:
        """
        p = self.conn.pubsub()
        p.subscribe(self.queue)
        while True:
            message = p.listen()
            for i in message:
                if i["type"] == 'message':
                    print(json.loads(i["data"]))
                    return json.loads(i["data"])


class InfluxClient(object):
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.client = InfluxDBClient(host='192.168.1.180', port=8080)  # 初始化时间序列数据库
        self.mongo_client = MongoClient(host=self.host, port=self.port)  # 初始化监控的数据库

    def insert_data(self):
        data = SaveSource.objects.all()
        for info in data:
            # for is_monitor in SpiderInfo.objects.filter(save_source__source_name=info.source_name):
            #     if is_monitor:
            db = self.mongo_client[info.database_name]  # 设置要监控的数据库
            collection = db[info.collection_name]
            # 获取总的数据量
            current_count = collection.find({"source": info.source_name}).count()
            # 已经同步价格词数
            sync_price_nums = collection.find({"sync_state": 2}).count()
            # 待同步关键词数
            wait_sync_count = collection.find({"sync_state": 0}).count()
            current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            # 构建
            json_body = [
                {
                    "measurement": info.source_name,
                    "time": current_time,
                    "tags": {
                        "spidername": info.collection_name
                    },
                    "fields": {
                        "total": current_count,
                        "sync_price_nums": sync_price_nums,
                        "wait_sync_count": wait_sync_count,

                    }
                }
            ]
            #  将获取到的数据写入influxdb
            if self.client.write_points(json_body):
                print("成功写入influxdb!", json_body)
            # else:
            #     logging.info("没有配置监控")

    def start(self):
        while True:
            self.insert_data()
            time.sleep(15)  # 设置监控频率


if __name__ == '__main__':
    InfluxClient().start()
