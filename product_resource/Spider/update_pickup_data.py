# encoding:utf-8
import requests
from parsel import Selector
from fake_useragent import UserAgent
from retrying import retry
import time
import json
import os
import sys
import re

print(sys.path)
sys.path.append('F:\\pythongit\\product_resource\\Spider')
sys.path.append('F:\\pythongit\\product_resource')
import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product_resource.settings")# project_name 项目名称
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utils.settings_local")  # 本地设置文件project_name 项目名称
django.setup()
from app.models import Property

from utils.db import RedisClient


class Update(object):
    _url = ''

    def save(self, data):
        """
        :param data:  更新参数字典
        :return:
        """
        # TODO:采集到的数据保存到mysql数据库,这里存在更新一个产品多个规格是随机更新的情况，就存在与联合索引冲突的问题；
        # TODO:解决方法就是，两个数据库，一号同步数据的设置联合索引为唯一，二号设置为正常，数据从一号同步到二号数据库
        # TODO:使用orm update_or_create数据存在则更新不存在就新增
        for info in data:
            Property.objects.update_or_create(cas=info.get('cas'), specs=info.get('specs'), source=info.get('source'),
                                              source_url=info.get('source_url'),
                                              defaults={
                                                  "pname": info.get('productname'),
                                                  'purity': info.get('purity', ''),
                                                  'price': info.get('price'),
                                                  'status': info.get('status'),
                                                  'source_url': info.get('source_url'),
                                                  'pickup_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                              })
            print("success")

    @retry(stop_max_attempt_number=3, stop_max_delay=2)
    def download(self, url):
        # TODO: 添加一个三次重试异常
        """
        获取源代码
        :return:
        """
        ua = UserAgent()
        headers = {
            "user-agent": str(ua)
        }
        try:
            response = requests.get(url=url, headers=headers)
            response.encoding = response.apparent_encoding
        except requests.ConnectionError as e:
            print(e)
        else:
            # print(type(response.url))
            return response, url

    def mce_detail(self, response):
        """
        Mce数据解析
        :param response: 返回的网页源代码
        :return:
        """
        print(response[1])
        items = Selector(response[0].text)
        cas = items.xpath('//div[@id="detail_img_pro"]//p/span/text()').extract_first()
        productname = items.xpath('//div[@id="pro_detail_hd"]//h1[@itemprop="name"]//strong//text()').extract_first()
        print(cas)
        if cas is not None:  # 产品是否存在cas
            cas = cas.strip()
            purity = items.xpath('//div[@id="pro_detail_hd"]//span[@class="ml_90"]/text()').extract_first()
            purity = purity.split(':')[1].strip() if purity else ""
            info = items.xpath('//table[@id="con_one_1"]//tr')[1:]
            product_info = []
            for p in info:
                result = {}
                specs = p.xpath('./td[@class="pro_price_1"]/text()').extract_first()
                specs = specs.strip().replace('\n', '').replace(' ', '').replace('\xa0', '') if specs else ''
                price = p.xpath('./td[@class="pro_price_2"]/text()').extract_first()
                price = price.strip() if price else ''
                status = p.xpath('./td[@class="pro_price_3"]/span/text()').extract_first()
                status = status.strip() if status else p.xpath(
                    './td[@class="pro_price_3"]/a/text()').extract_first().strip()
                result['cas'] = cas
                result['productname'] = productname
                result['purity'] = purity
                result['specs'] = specs
                result['price'] = price
                result['status'] = status
                result["source_url"] = response[1],
                result['source'] = 'Mce'
                product_info.append(result)

            print(product_info)
            # TODO:采集到的数据保存到mysql数据库
            self.save(product_info)
            pass
            return json.dumps(product_info)
        else:
            result = {"message": "数据不存在"}
            return json.dumps(result)

    def xlsw_detail(self, response):
        """
        西利生物
        :param response: 返回的源代码
        :return:
        """
        items = Selector(response[0].text)
        cas = items.xpath('//div[@class="txt wow fadeInUp"]/div[@style="overflow:hidden"][2]/text()').extract_first()
        productname = items.xpath('//div[@class="divT wow fadeInUp"]/text()').extract_first()
        if cas is not None:
            product_info = []
            _cas = cas.strip()
            price_specs = items.xpath('//div[@class="txt wow fadeInUp"]/span//text()').extract_first()
            _price, _specs = price_specs.split('/')[0], price_specs.split('/')[1] if price_specs is not None else ""
            # print(_price)
            # print(_specs)
            purity = items.xpath(
                '//div[@class="txt wow fadeInUp"]/div[@style="overflow:hidden"][7]/text()').extract_first()
            _purity = purity.strip() if purity else ""
            # print(_purity)
            _status = ""
            _source = "xlsw"

            result = {
                "productname": productname,
                "cas": _cas,
                "price": _price,
                "specs": _specs,
                "purity": _purity,
                "status": _status,
                "source_url": response[1],
                "source": _source
            }
            product_info.append(result)
            # 调用保存方法
            self.save(product_info)
            return json.dumps(product_info)
        else:
            result = {"message": "数据不存在"}
            return json.dumps(result)

    def start(self):
        """
        主函数
        :return:
        """
        while True:
            data = RedisClient().listen_task()
            data = data if data else ''
            # print(data)
            _mce_source = json.loads(data).get('source') == "Mce" if data else ''
            _xlsw_source = json.loads(data).get('source') == "xlsw" if data else ''
            if _mce_source:
                _url = json.loads(data).get('url') if data else ''
                if _url:
                    try:
                        response = self.download(_url)
                        result = self.mce_detail(response)
                        print(result)
                    except:
                        continue

            elif _xlsw_source:
                _url = json.loads(data).get('url') if data else ''
                if _url:
                    response = self.download(_url)
                    result = self.xlsw_detail(response)
                    print(result)
                pass


if __name__ == '__main__':
    Update().start()
    # Update().download('https://www.medchemexpress.cn/Rapamycin.html')
