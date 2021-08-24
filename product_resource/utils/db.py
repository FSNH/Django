import redis
# 连接池
# 并发的话，把他做成单例，写在一个文件里面，import它
import redis
import json


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
