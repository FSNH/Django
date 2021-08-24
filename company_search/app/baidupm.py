import requests
from fake_useragent import UserAgent
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor
import time, random
from urllib.request import quote
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
excutor = ThreadPoolExecutor(max_workers=3)  # 开启3个线程


class BaiduPm(object):

    def get_parse(self, word):
        """
        :param word:
        :param page:
        :return:
        """
        infolist = []
        flag = True
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.114 Safari/537.36',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec - Fetch - User": "?1",
            "Upgrade - Insecure - Requests": "1"

        }
        for href in ["https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={0}".format(quote(word))]:
            print(href)
            try:
                response = requests.get(url=href, headers=headers, verify=False)
                # print(response.text)
                time.sleep(random.randint(1, 3))
            except Exception as e:
                print(e)
            else:
                items = Selector(response.text)
                divs = items.xpath('//div[contains(@class,"c-container")]')
                ban = items.xpath('//div[@class="timeout-feedback hide"]')
                if divs:
                    for div in divs:
                        title = div.xpath('./h3/a').xpath('string(.)').get()
                        score = div.xpath('./@id').get()
                        url = div.css('.c-showurl::text').get()

                        if title and score and url:
                            # print(title.strip(),score.strip(),url.strip(),word)
                            if "chem960" in url:
                                info = {
                                    "keyword": word,
                                    "title": title.strip(),
                                    "score": score.strip(),
                                    "url": url.strip()
                                }
                                yield info
                            else:
                                pass

                        # infolist.append(info)
                elif ban:  # 网站出现被封
                    flag = False
                else:
                    pass
        if not flag:  # 如果存在被禁返回failed
            return flag

    def pool(self, urls):
        """
        :param urls:
        :return: datalist
        """
        datas = []
        for data in excutor.map(self.get_parse, urls):
            # print(data)
            if isinstance(data, list):  # 如果返回的数据是列表
                for i in data:
                    datas.append(i)
            else:  # 如果返回的是字符串failed,就将字符串返回
                return data
        # print(datas)
        return datas
        pass

    def start(self,keyword):
        d = []
        for s in self.get_parse(keyword):
            d.append(s)
        return d


if __name__ == '__main__':
    # f = BaiduPm().get_parse("阿哌沙班杂质")
    # print(f)
    f = BaiduPm()
    """
    Lactoyl-CoA 
    阿哌沙班杂质 
    白叶藤碱 
    利伐沙班杂质 s
    新白叶藤碱
    """
    # s = f.pool(["Lactoyl-CoA", "阿哌沙班杂质", "白叶藤碱", "利伐沙班杂质"])
    # s = f.pool(["50-00-0"])
    s = f.start('Lactoyl-CoA')
    print(s)
    pass
