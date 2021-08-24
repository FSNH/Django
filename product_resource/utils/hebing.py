import pymongo
import time
import threading
from multiprocessing.dummy import Pool as ThreadPool


class MongoToMongo(object):
    """
    30服务器的产品规格信息，上传归总到本地mongo数据库
    """

    def __init__(self):
        self.client = pymongo.MongoClient(host="192.168.1.30", port=27017)
        # self.client_local_1 = pymongo.MongoClient(host="127.0.0.1", port=27017)

        self.client_local = pymongo.MongoClient(host="192.168.1.30", port=27017)
        self.db_local = self.client_local["info"]  # save to info database

        self.pool = ThreadPool(10)  # 开启线程数,即一次性抛出的请求数
        self.thread = []  # 线程池
        self.collections = []
        # TODO FROM property_info TO info
        self.db = self.client.property_info
        self.collection = self.db.property
        self.collections.append(self.collection)
        self.update_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def hebingpropertyinfo_info(self, collection):
        data = collection.find({'hebing_sync_state': {"$ne": 2}}, no_cursor_timeout=True) # doing
        # print("*"*100)
        for i, content in enumerate(data):
            print(i)
            info = {
                '_id': content.get('_id'),
                "productname": content.get('productname', '').strip(),
                "cas": content.get('cas', '').strip() if content.get('cas', '') else '',
                "specs": content.get('specs', '').strip() if content.get('specs', '') else '',
                "price": content.get('price', '').strip() if content.get('price', '') else '',
                "purity": content.get("purity", '').strip() if content.get("purity", '') else '',
                "stock": str(content.get("stock", '')).strip() if content.get("stock", '') else '',
                "source_url": content.get('source_url', ''),
                "source": content.get('source'),
                "update_date": self.update_date
            }
            self.update_mongodb(info)
            self.update_sync(info.get("_id"))
            print(info)

    def update_mongodb(self, content):
        """
        多个数据库的字段汇总到办本地数据库
        如果更新的数据条件不存在，就将条件和更新值写入数据库
        :param content: 数据库字段集合
        :return:None
        """
        # TODO:将分散的数据整合到一个数据库
        self.db_local.property.update_many(
            {
                "cas": content.get('cas', '').strip() if content.get('cas', '') else '',
                "productname": content.get('productname', '').strip(),
                "specs": content.get('specs', '').strip() if content.get('specs', '') else '',
                "purity": content.get("purity"),
                "stock": content.get("stock", '').strip() if content.get("stock", '') else '',
                "source": content.get('source'),
                "source_url": content.get('source_url', ''),

            }, {"$set": {
                "price": content.get('price', '').strip() if content.get('price', '') else '',
                "update_date": self.update_date,
                'sync_state': 0  # 数据已同步，出现更新数据时，将同步状态更为待同步，下次同步时会一并同步
            }}, upsert=True)
        # self.db_local.property.insert(content)
        print('success')

    def update_sync(self,id):
        """
        更新同步状态
        :param collect: 集合
        :param id: id
        :return:
        """
        self.collection.update_one({'_id': id}, {'$set': {'hbingsync_state': 2}})
        print("update state success")

    def create(self):
        # 创建十个线程
        for i in range(100):
            t = threading.Thread(target=self.hebingpropertyinfo_info, args=(self.collection,))
            self.thread.append(t)

    def start(self):
        self.create()
        for i, t in enumerate(self.thread):
            print(threading.current_thread().name + '线程**********************************************************:', i)
            t.start()
            # t.join()

    def start_pool(self):
        result = self.pool.map(self.hebingpropertyinfo_info, self.collections)



if __name__ == "__main__":
    # MongoToMongo().start()
    MongoToMongo().start_pool()
    print("MongoToMongo success")

