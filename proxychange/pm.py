import requests
from fake_useragent import UserAgent
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor
import time,random
from urllib.request import quote
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
excutor = ThreadPoolExecutor(max_workers=3)  # 开启3个线程

class BaiduPm(object):
    def next_url(self,word):
        """
        :param word:
        :return:
        """
        for page in range(3):
            if page==0:
                url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={0}".format(quote(word))
            else:
                url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={0}&pn={1}&oq={2}".format(quote(word),(page) * 10,quote(word))

            yield url

    def get_parse(self,word):
        """
        :param word:
        :param page:
        :return:
        """
        infolist = []
        failed = []
        headers = {
            "User-Agent":str(UserAgent().random),
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec - Fetch - User": "?1",
            "Upgrade - Insecure - Requests": "1"

        }
        for href in self.next_url(word):
            print(href)
            try:
                response = requests.get(url=href,headers=headers,verify=False)
                # print(response.text)
                time.sleep(random.randint(2,3))
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
                                info={
                                    "keyword":word,
                                    "title":title.strip(),
                                    "score":score.strip(),
                                    "url":url.strip()
                                }
                                # yield info
                                infolist.append(info)
                elif ban:  # 网站出现被封
                    failed.append('failed')
                else:
                    pass
        if failed:  # 如果存在被禁返回failed
            return "failed"
        else:
            return infolist  # 返回采集到的数据

    def pool(self,urls):
        """
        :param urls:
        :return: datalist
        """
        datas = []
        for data in excutor.map(self.get_parse,urls):
            # print(data)
            if isinstance(data,list):  # 如果返回的数据是列表
                for i in data:
                    datas.append(i)
            else:  # 如果返回的是字符串failed,就将字符串返回
                return data
        # print(datas)
        return datas
        pass
if __name__ == '__main__':
    # f = BaiduPm().get_parse("阿哌沙班杂质")
    # print(f)
    f=BaiduPm()
    """
    Lactoyl-CoA 
    阿哌沙班杂质 
    白叶藤碱 
    利伐沙班杂质 
    新白叶藤碱
    """
    f.pool(["Lactoyl-CoA","阿哌沙班杂质","白叶藤碱","利伐沙班杂质"])
    pass
