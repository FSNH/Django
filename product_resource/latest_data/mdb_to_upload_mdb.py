import pymongo
import time
import threading
from multiprocessing.dummy import Pool as ThreadPool


class MongoToMongo(object):
    """
    30服务器的mongo产品规格信息，上传归总到本地mongo数据库
    mongo数据库：latest_pinfo
    mongo集合：property
    """
    update_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def __init__(self):
        self.client = pymongo.MongoClient(host="192.168.1.30", port=27017)  # 数据工厂采集的数据

        self.client_local = pymongo.MongoClient(host="192.168.1.30", port=27017)  # 合并到30服务器的latest_pinfo数据库中
        self.db_local = self.client_local["latest_pinfo"]  # save to info database

        self.pool = ThreadPool(10)  # 开启线程数,即一次性抛出的请求数
        self.thread = []  # 线程池
        self.collections = []

        self.db = self.client.db_5fbc6f4de770400d381398b3
        self.db1 = self.client.db_5f9a7ba7e7704003b8757694
        self.db2 = self.client.db_5f97784be7704005e8f0ca7b
        self.db3 = self.client.db_60594642e770400380778139
        self.db4 = self.client.db_605a97b5e770400cac89dc64
        self.db5 = self.client.db_605aeb93e770400a24245863
        self.db6 = self.client.db_60598de105c7042ff8009793
        self.db7 = self.client.db_6062c6bce7704010c0eb1f26
        self.db8 = self.client.db_605bf1f8e770400a2424e422
        self.db9 = self.client.db_606147c7e77040143c7a32f5
        self.db10 = self.client.db_605d3c09e7704011040a8e04
        self.db11 = self.client.db_6078e21fe770400d6072a253
        self.db12 = self.client.db_6079387de7704013fc6c9d7e
        self.db13 = self.client.db_60790145e7704013fc6c9c84
        self.db14 = self.client.db_6077a67c05c7043a3cb3e42b
        self.db15 = self.client.db_605d876de7704011040bafe0
        self.db16 = self.client.db_606d077fe7704012a83a7317

        self.collection = self.db.entity_5fbc6f4de770400d381398b3_productinfo  # 产品规格 mce
        self.collection1 = self.db1.entity_5f9a7ba7e7704003b8757694_detailinfo  # 产品信息 西利生物
        self.collection2 = self.db2.entity_5f97784be7704005e8f0ca7b_propertyproperty  # 罗恩
        self.collection3 = self.db3.entity_60594642e770400380778139_property  # 阿拉丁
        self.collection4 = self.db4.entity_605a97b5e770400cac89dc64_property  # 南京试剂
        self.collection5 = self.db5.entity_605aeb93e770400a24245863_property  # 韶远
        self.collection6 = self.db6.entity_60598de105c7042ff8009793_property  # 麦克林
        self.collection7 = self.db7.entity_6062c6bce7704010c0eb1f26_property  # 南京药石
        self.collection8 = self.db8.entity_605bf1f8e770400a2424e422_property  # tci
        self.collection9 = self.db9.entity_606147c7e77040143c7a32f5_property  # 乐研
        self.collection10 = self.db10.entity_605d3c09e7704011040a8e04_property  # 百灵威

        self.collection11 = self.db11.entity_6078e21fe770400d6072a253_property  # 小辣椒
        self.collection12 = self.db12.entity_6079387de7704013fc6c9d7e_property  # bestfluorodrug
        self.collection13 = self.db13.entity_60790145e7704013fc6c9c84_property  # 杰达维
        self.collection14 = self.db14.entity_6077a67c05c7043a3cb3e42b_property  # 九鼎
        self.collection15 = self.db15.entity_605d876de7704011040bafe0_property  # 毕得
        self.collection16 = self.db16.entity_606d077fe7704012a83a7317_property  # trc

        # self.collections.append(self.collection)
        # self.collections.append(self.collection1)
        # self.collections.append(self.collection2)
        # self.collections.append(self.collection3)
        # self.collections.append(self.collection4)
        # self.collections.append(self.collection5)
        # self.collections.append(self.collection6)
        # self.collections.append(self.collection7)
        # self.collections.append(self.collection8)
        # self.collections.append(self.collection9)
        # self.collections.append(self.collection10)
        # self.collections.append(self.collection11)
        # self.collections.append(self.collection12)
        # self.collections.append(self.collection13)
        # self.collections.append(self.collection14)
        # self.collections.append(self.collection15)
        # self.collections.append(self.collection16)

    def sync_local_pinfo(self):
        """
        localhost主机的本地数据上传到30服务器的latest_pinfo
        :return:
        """
        self.client = pymongo.MongoClient(host="web.test.web960.com", port=32001)
        self.db = self.client["latest_pinfo"]  # save to info database
        self.collections.append(self.db.property)

    def getmongo(self, collection):
        """
        获取规格信息
        :return:
        数据结构字段如下：
            data=[
                {   'goods_id':'HY-U00162-500mg',
                    'productname': '2"-O-Galloylhyperin',
                    'cas': "53209-27-1",
                    'size': "5mg",
                    "stock": "In-stock",
                    'price': "￥1580",
                    "purity": ">98.0%",
                    "url": "https://www.medchemexpress.cn/2-o-galloylhyperin.html",
                }
            ]
        """
        # for collection in self.collections:
        #     print(collection)
        data = collection.find({'sync_state': {"$ne": 2}}, no_cursor_timeout=True).limit(2000)

        for i, content in enumerate(data):
            if content.get('productname', '') and content.get('goods_id', '') and content.get("price",
                                                                                              "") and content.get(
                    'specs', '') and content.get('cas', ''):
                info = {
                    '_id': content.get('_id'),
                    "goods_id": content.get('goods_id').strip(),
                    "productname": content.get('productname', '').strip(),
                    "cas": content.get('cas').strip(),
                    "specs": content.get('specs').strip(),
                    "price": str(content.get('price')).strip(),
                    "purity": content.get("purity", '').strip() if content.get("purity", '') else '',
                    "stock": str(content.get("stock")).strip(),
                    "source_url": content.get('source_url', ''),
                    "source": content.get('source'),
                    "update_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
                self.update_mongodb(info)
                self.update_sync(collect=collection, id=content.get('_id'))
                print(i, info)

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
                'goods_id': content.get('goods_id')

            }, {"$set": {
                "cas": content.get('cas').strip(),  # cas号
                "productname": content.get('productname').strip(),  # 产品名
                "price": content.get('price').strip(),  # 价格
                "specs": content.get('specs').strip(),  # 规格
                "purity": content.get("purity"),  # 纯度
                "stock": content.get("stock", '').strip() if content.get("stock", '') else '',  # 库存
                "source": content.get('source'),  # 来源/品牌
                "source_url": content.get('source_url', ''),  # 产品详情链接
                "update_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'sync_state': 0  # 数据已同步，出现更新数据时，将同步状态更为待同步，下次同步时会一并同步
            }}, upsert=True)
        print('success')

    def update_sync(self, collect, id):
        """
        更新同步状态
        :param collect: 集合
        :param id: id
        :return:
        """
        collect.update_one({'_id': id}, {'$set': {'sync_state': 2}})
        print("状态更新成功")

    def start_pool(self):
        while True:
            self.sync_local_pinfo()
            result = self.pool.map(self.getmongo, self.collections)


if __name__ == "__main__":
    # MongoToMongo().start()
    MongoToMongo().start_pool()
    print("MongoToMongo success")
