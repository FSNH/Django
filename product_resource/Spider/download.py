import requests
from fake_useragent import UserAgent
from retrying import retry

# @retry(stop_max_attempt_number=3, stop_max_delay=2)
def downloader(url):
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
        # print(response)
        # print(type(response.url))
        return response, url
if __name__ == '__main__':
    s = downloader('http://www.biobiopha.com/view/xlswPC/1/49/view/7576.html')
    print(s)