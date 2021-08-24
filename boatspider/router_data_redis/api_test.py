import requests
import json


class PriceApiTest(object):
    """价格接口测试案例：
    参数 source:数据源（必填）  参数类型 str:字符串
    参数 url:详情链接  参数类型 str:字符串
    参数 cas:化合物cas号  参数类型 str:字符串
    参数 priority:优先级 默认10  参数类型 int:整型
    参数 url和cas二选一必填
    """

    def post(self):
        data = {
            'data': json.dumps([{'source': 'Bestfluorodrug',
                                 'url': 'http://product.bestfluorodrug.com/product/282.html',
                                 'cas': '',
                                 'priority': 100},
                                {'source': 'Bestfluorodrug',
                                 'url': 'http://product.bestfluorodrug.com/product/283.html',
                                 'cas': '',
                                 'priority': 100}])}
        # print(data)
        try:
            resp = requests.post(url='https://api.prices.chem960.com/api/search/', data=data)
        except Exception as e:
            print(e)
        else:
            print(resp.text)

    def get(self):
        # url = 'https://api.prices.chem960.com/api/search/'
        param = {'source': 'Bestfluorodrug',
                 'url': 'http://product.bestfluorodrug.com/product/282.html',
                 'cas': '',
                 'priority': 100}
        url = 'http://127.0.0.1:8001/api/search/'
        # param = {'source': 'Mce',
        #          'url': 'https://www.medchemexpress.cn/Oxiconazole_nitrate.html',
        #          'cas': '',
        #          'priority': 100}
        resp = requests.get(url=url, params=param)
        print(resp.url)
        print(resp.text)

    def get_list(self):
        url = 'https://api.prices.chem960.com/api/search/'
        param = {"urllist": json.dumps([{'source': 'Bestfluorodrug',
                                         'url': 'http://product.bestfluorodrug.com/product/282.html', 'cas': '',
                                         'priority': 100}])}
        resp = requests.get(url=url, params=param)
        print(resp.url)
        print(resp.text)

    def get_cas(self):
        # url = 'http://127.0.0.1:8001/api/search_cas/'
        url = 'https://api.prices.chem960.com/api/search_cas/'
        data = {
            'data': json.dumps([{
                'url': '',
                'cas': '77-91-8',
                'priority': 100}
            ])}
        # print(data)
        try:
            resp = requests.post(url=url, data=data)
        except Exception as e:
            print(e)
        else:
            print(resp.text)


if __name__ == '__main__':
    PriceApiTest().get()
