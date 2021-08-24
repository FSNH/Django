import requests
from parsel import Selector
from app.verify_cas import IsCas
import time
import random


class CasVerifyGet(object):
    """
    检测cas号是否正确，不正确则返回chemicalbook正确的结果
    """

    def chemical(self, cas):
        """"
        获取chemicalbook的查询结果
        """
        global url
        try:
            url = f'https://www.chemicalbook.com/Search.aspx?_s=&keyword={cas.strip()}'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                'referer': url,

            }
            resp = requests.get(url=url, headers=headers, verify=False)
            time.sleep(random.randint(2, 4))
        except Exception as e:
            print(f"请求链接url:{url}:错误原因{e}")
        else:
            # return Selector(resp.text)
            print(resp.text)

    def get_cas(self, cas):
        """
        检测cas号是否正确，不正确则返回chemicalbook正确的结果
        :param cas:
        :return:
        """
        if IsCas.iscas(cas.strip()):
            return {"message": "CAS号格式正确"}
        else:
            items = self.chemical(cas)
            info = []
            tds = items.xpath('//table[@id="mbox"]//tr//td')
            for td in tds:
                value = td.xpath('string(.)').get()
                # print(value)
                info.append(value.replace("：", "").strip())
            info_dict = {}
            # print(info)
            for i in range(0, len(info), 2):
                info_dict[info[i]] = info[i + 1]
            # print(info_dict)
            info_dict.update({"result": "正确Cas号"})
            return info_dict


if __name__ == '__main__':
    # print(CasVerifyGet().get_cas('7732-18-1'))
        CasVerifyGet().chemical("7732-18-1")