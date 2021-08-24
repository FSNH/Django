from selenium import webdriver
from parsel import Selector
from time import sleep
from random import randint
def getpage(url):
    browser= webdriver.Chrome("D:\software\chromedriver.exe")
    browser.get(url)
    # print(browser.page_source)
    sleep(randint(0,2))
    return browser.page_source
    browser.close()
    browser.quit()

def parse_info():
    words = ["Lactoyl-CoA", "阿哌沙班杂质", "白叶藤碱", "利伐沙班杂质", "新白叶藤碱"]
    infolist = []
    for word in words:
        response = getpage(word)
        # print(response)
        items = Selector(response)
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
    print(infolist)
    print(len(infolist))

if __name__ == '__main__':

    parse_info()