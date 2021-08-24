from parsel import Selector
import json
from save import Update
import download
from utils.db import RedisClient


def mce_detail(response):
    """
    Mce数据解析
    :param response: 返回的网页源代码
    :return:
    """
    items = Selector(response[0].text)
    cas = items.xpath('//div[@id="detail_img_pro"]//p/span/text()').extract_first()
    productname = items.xpath('//div[@id="pro_detail_hd"]//h1[@itemprop="name"]//strong//text()').extract_first()
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
            result["source_url"] = [response[1]][0]
            result['source'] = 'Mce'
            product_info.append(result)

        # TODO:采集到的数据保存到mysql数据库
        Update().save(product_info)
        print(product_info)
        return json.dumps(product_info)
    else:
        result = {"message": "数据不存在"}
        return json.dumps(result)


def start_mce():
    while True:
        data = json.loads(RedisClient().sub_info())
        print("接收到数据：",data)
        if data.get('source') == 'Mce':
            try:
                response = download.downloader(data.get('url'))
                print(response)
                mce_detail(response)
            except Exception:
                continue
        pass


if __name__ == '__main__':
    start_mce()