import json
import logging

import redis
from boat.models import SaveSource
import os
import django


class MyRedis(object):
    """
    redis
    """

    def __init__(self, spidername):
        self.spidername = spidername
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        self.client = redis.Redis(connection_pool=self.pool)

    def push_list(self, data):
        """
        push redis list
        :param data: dict
        :return: int
        """
        result = self.client.lpush(f'{self.spidername}:start_urls', json.dumps(data))
        return result

    def push_zset(self, data: dict):
        """
        :param data:
        :return:
        """

        result = self.client.zadd(f'{self.spidername}s:start_urls', mapping={data.get('score'): data.get("url")})
        return result

    def push_set_one(self, priority=10, cas='', url=''):
        """
        导入cas号
        单个导入zset
        :param priority: 优先级数 越大优先级越高
        :param cas:
        :param url:
        :return:
        data_dict = {10: {"url": "http://www.bomeibio.com/goods.php?id=2687"},
                     200: {"url": "http://www.bomeibio.com/goods.php?id=2686"},
                     30: {"url": "http://www.bomeibio.com/goods.php?id=2685"},
                     400: {"url": "http://www.bomeibio.com/goods.php?id=2684"},
                     500: {"url": "http://www.bomeibio.com/goods.php?id=2683"},
                     600: {"url": "http://www.bomeibio.com/goods.php?id=2682"},
                     }
        """

        data_dict = {priority: {"url": f"{url}", "cas": f"{cas}"}, }

        # data_dict = {100: {"url": "http://www.bomeibio.com/goods.php?id=13716"}, }
        for d, x in data_dict.items():
            # print(d, x)
            score = d  # 有序集合的分数，分数越大优先级越高
            member = json.dumps(x)  # 优先级对应的参数url，类型为str
            mapping = {member: score, }  # redis zadd使用字典方式存放参数
            self.client.zadd(f'{self.spidername}s:start_urls', mapping)  # 正确 导入数据到redis队列
            num = self.client.zcard(f'{self.spidername}s:start_urls')  # 查询导入的数据量
            # print(num)
            return num

    def get_zset(self, batchsize: int):
        """
        form score:low to score:high by get data
        reverse score
        :param batchsize:
        :return:
        """
        result = self.client.zrevrange(f'{self.spidername}s:start_urls', start=0, end=batchsize - 1)
        result_num = self.client.zremrangebyrank(f'{self.spidername}s:start_urls', min=-batchsize, max=-1)
        print(result, result_num)


class Test(object):
    """
    rotuer redis_keys
    # 爬虫数据源名：爬虫名称
    spiderproject = {
        "alichem": 'alich',
        "astatechinc": "astate",
        "fluorochem": "fluor",
    }
    """

    def __init__(self):
        self.spiderproject = {}  # 初始化项目
        self.update_spiderproject()  # 初始化加载

    # spiderproject = {
    #     "alichem": 'alich',
    #     "astatechinc": "astate",
    #     "fluorochem": "fluor",
    # }

    def update_spiderproject(self):
        spiders = SaveSource.objects.all()
        for m_spider in spiders:
            # spiderproject.update({m_spider.source_name: m_spider.spider_info.spider_name})  # 更新爬虫项目路由映射表字典
            # 配置爬虫是否可采集
            # print(m_spider.spider_info.monitor)
            if m_spider.spider_info.monitor:
                # print({m_spider.spider_info.spider_name: m_spider.source_name})
                self.spiderproject.update({m_spider.source_name: m_spider.spider_info.spider_name})  # 更新爬虫项目路由映射表字典
            else:
                print(f"爬虫未配置{m_spider.source_name}")
        # print(self.spiderproject)

    def spider_func(self):
        spidername_list = []  # 爬虫名称列表
        spiderfunction = {}  # 爬虫名称：调用的方法名称
        for spider, value in self.spiderproject.items():
            # print(spider, value)
            spidername_list.append(spider)  # 爬虫
            spiderfunction.update({spider: "push_data_redis_zset"})  # 使用爬虫的数据源名称与对应的函数建立联系
        return spidername_list, spiderfunction

    # print(f"爬虫项目：{spidername_list}")
    # print(f"调用函数{spiderfunction}")

    @staticmethod
    def push_data_redis_list(data: dict):
        print(data)
        """
        push data to list_reids_key
        :param data: dict
        :return: int
        """
        result = MyRedis(data.get('source')).push_list(data=data)
        return result

    @staticmethod
    def push_data_redis_zset(data: dict):
        """
        priority :优先级默认为10
        push data to zset_reids_key
        :param data: dict
        :return: int
        """
        result = MyRedis(data.get('source')).push_set_one(priority=data.get('priority'),
                                                          url=data.get("url"),
                                                          cas=data.get("cas")
                                                          )
        return result

    def predict(self, datas: dict):
        # 调度爬虫redis队列的数据分发
        """
        rotuer data to appoint redis_key by check spider_list(Spidername) and spiderfunction(dict {spidername:'push_data_redis'})
        :param datas: dict
        :return: int
        """

        global data
        if isinstance(datas, dict):
            data = datas
        elif isinstance(datas, str):
            data = json.loads(datas)
        else:
            pass
        d = 1
        for state in self.spider_func()[0]:

            # print(state)
            if state == data.get('source'):  # 爬虫数据源（source）匹配查找的爬虫是否存在
                # 更新爬虫项目名为爬虫名
                data.update({"source": self.spiderproject[state]})  # 通过数据源（source）获取对应redis键的名称
                result = eval("Test." + self.spider_func()[1][state])(data)
                data.update({"num": result, 'success': 1})  # 返回提交的数据

                return data
            else:
                d += 1
                try:
                    if d < len(self.spider_func()[0]):
                        continue
                    else:
                        data.update({'msg': "未更新到数据", 'success': 0})
                        return data
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    data = {'source': '11', 'url': 'https://www.tcichemicals.com/CN/zh/p/D3715', 'cas': '', 'priority': 10}
    s = Test().predict(datas=data)
    print(s)
    pass
