from parsel import Selector
import json
from save import Update
import download
from utils.db import RedisClient


def xlsw_detail(response):
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
        print(product_info)
        # 调用保存方法
        Update().save(product_info)
        return json.dumps(product_info)
    else:
        result = {"message": "数据不存在"}
        return json.dumps(result)


def start_xlsw():
    while True:
        data = json.loads(RedisClient().sub_info())
        print("接收到数据：",data)
        if data.get('source') == 'xlsw':
            try:
                print(data.get('url'))
                response = download.downloader(data.get('url'))
                # print(response)

                xlsw_detail(response)
            except Exception:
                continue
        pass


if __name__ == '__main__':
    start_xlsw()
