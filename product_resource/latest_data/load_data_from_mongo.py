import pymongo
import pymysql
from pymysql.converters import escape_string  # 字符串转义
import time
from multiprocessing import Process


class MongoToMysql(object):
    """
    产品主要信息：产品名称；
    mongo数据库：latest_pinfo
    mongo集合：property
    mysql数据库：product_sources
    mysql表：property
    """

    def __init__(self):
        self.client = pymongo.MongoClient(host="192.168.1.30", port=27017)
        self.db = self.client['latest_pinfo']
        self.collection = self.db['property']
        # TODO:合并后的规格信息，导入mysql
        self.update_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def getmongo(self,name):
        """
        获取规格信息
        :return:
        """
        data = self.collection.find({'sync_state': {"$ne": 2}}, no_cursor_timeout=True).limit(2000)
        """"
        数据结构字段如下：
         data = [
            {'goods_id': "HY-U00162-100mg",
             'productname': '2"-O-Galloylhyperin',
             'cas': "53209-27-1",
             'specs': "100mg",
             "stock": "In-stock",
             'price': "￥10",
             "purity": ">98.0%",
             "source_url": "https://www.medchemexpress.cn/2-o-galloylhyperin.html",
             "source":'mce',
             "update_date":self.update_date
             }
        ]
        """

        for i, content in enumerate(data):
            info = {
                "_id": content.get('_id'),
                "goods_id": content.get('goods_id').strip(),
                "productname": content.get('productname').strip(),
                "cas": content.get('cas').strip(),
                "specs": content.get('specs').strip(),
                "price": content.get('price').strip(),
                "purity": content.get("purity", '').strip() if content.get("purity", '') else '',
                "stock": content.get("stock", '').strip() if content.get("stock", '') else '',
                "source_url": content.get('source_url', ''),
                "source": content.get('source'),
                "update_date": content.get('update_date')
            }
            Mysql().insert(info)
            self.update_sync(self.collection, info.get('_id'))
            print(name,i, info)
        Mysql().close()
        pass

    def update_sync(self, collect, id):
        """
        更新同步状态
        :param collect: 集合
        :param id: id
        :return:
        """
        collect.update_one({'_id': id}, {'$set': {'sync_state': 2}})
        print("状态更新成功")


class Mysql(object):
    def __init__(self):
        # self.client = pymysql.connect(user='root', password='123456', database='product_sources', charset='utf8')
        # 打开数据库连接
        self.client = pymysql.connect(host='192.168.1.26',
                                      user='product_sources',
                                      password='JPCkXkZMhHeMM8YC',
                                      database='product_sources',
                                      charset='utf8')  # 打开数据库连接

        self.cursor = self.client.cursor()  # 获取操作游标

    def select(self):
        """
        查询所有
        :return:
        """
        demo = self.cursor.execute('select * from property')  # 运行SOL语句
        lists = self.cursor.fetchall()  # 接收返回的结果
        for i in lists:
            print(i)

    def insert(self, content):
        """
        ON DUPLICATE KEY UPDATE: 先执行前面的Insert,如果主键重复，则执行后面的UPDATE
        插入规格信息,根据联合索引goods_id,source,数据一样即视为相同产品数据，就执行更新他们的产品：状态、价格、纯度、采集时间，否则就全量插入数据
        :param content:
        :return:
        """

        update_insert_sql = "INSERT INTO property(productid,pname,cas,specs,status,price,purity,source_url,source,pickup_date)" \
                            "VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE status='%s',price='%s',purity='%s',pickup_date='%s'" % \
                            (
                                escape_string(content.get('goods_id')),
                                escape_string(str(content.get("productname"))),
                                escape_string(str(content.get("cas"))),
                                escape_string(str(content.get("specs"))),
                                escape_string(str(content.get("stock", ''))),
                                escape_string(str(content.get("price"))),
                                escape_string(str(content.get("purity", ''))),
                                escape_string(str(content.get("source_url"))),
                                escape_string(str(content.get('source'))),
                                content.get("update_date"),
                                # 去重更新的字段
                                escape_string(str(content.get("stock", ''))),
                                escape_string(str(content.get("price", ''))),
                                escape_string(str(content.get("purity", ''))),
                                content.get("update_date"),
                            )
        # print(update_insert_sql)
        self.cursor.execute(update_insert_sql)
        self.client.commit()  # 提交mysql语句

    def close(self):
        """
        数据库关闭
        :return:
        """
        self.client.close()  # 关闭数据库


if __name__ == '__main__':
    while True:
        # p1 = Process(target=Mongo().getalias(), args=("进程1",))  # 创建第一个进程
        p1 = Process(target=MongoToMysql().getmongo(), args=("进程1",))  # 创建第一个进程
        p2 = Process(target=MongoToMysql().getmongo(), args=("进程2",))  # 创建第一个进程
        p1.start()  # 开启第一个进程
        p2.start()  # 开启第二个进程

        print("执行完毕,等待。。。。。。。。。。。。。。。。。")
