import requests
from fake_useragent import UserAgent
from parsel import Selector
import asyncio
import aiohttp
from aiohttp import TCPConnector

tasks = []
start_urls = ['叔丁氧羰基肼','阿哌沙班杂质']
sem = asyncio.Semaphore(3)

async def fetch(word):
    async with sem:
        headers = {
            "user-agent": str(UserAgent().random)
        }
        try:
            url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}".format(word)
            async with aiohttp.ClientSession().get(url,headers=headers) as resp:
                print('url status: {}'.format(resp.status))
                await asyncio.sleep(1)
                if resp.status in [200, 201]:
                    data = await resp.text()
                    return data
        except Exception as e:
           print(e)

def parse_info(task):
    html =task.result()
    items = Selector(html)
    # print(future.result())
    divs = items.xpath('//div[contains(@class,"c-container")]')
    for div in divs:

        title = div.xpath('./h3/a').xpath('string(.)').get()
        score = div.xpath('./@id').get()
        url = div.css('.c-showurl::text').get()
        if title and score and url:
            if "chem960" in url:
                info={
                    "title":title.strip(),
                    "score":score.strip(),
                    "url":url.strip()
                }
                print(info)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(fetch("阿哌沙班杂质"))
    # task.add_done_callback(parse_info)
    loop.run_until_complete(task)
    loop.close()