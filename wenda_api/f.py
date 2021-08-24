import requests
from parsel import Selector
import csv
from openpyxl import Workbook
import pymongo
client = pymongo.MongoClient(host='192.168.1.30', port=27017)
db = client.f
collection = db.e
url= "http://www.jacschem.com/scroll.asp"
headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'Host': 'www.jacschem.com',
    'Cookie': 'ASPSESSIONIDSSSDSCBS=PGGBEOBACOPLKMIAFOCNLBKC'

}
res = requests.get(url=url,headers=headers)
res.encoding='gbk'
# print(res.text)
items = Selector(res.text)
data = items.xpath('//p//a//text()').getall()
print(len(data))

for info in data:
    cas = info.split('-')[-3:]
    print(cas)
    name = info.split('-')[0:-3]
    print(name)
    print('-'.join(name))
    print("-".join(cas))
    k=["-".join(cas),'-'.join(name)]
    print(k)
    data ={'cas':"-".join(cas),'name':'-'.join(name)}

    # collection.insert(g)
    # with open('info3.csv','a+',encoding='utf-8',newline="")as f:
    # 写入csv
    #     writer = csv.writer(f)
    #     writer.writerow(k)  #单行写入

    with open('123.csv', 'a+',encoding='utf-8', newline='')as f:
        # 写入字典
        fieldnames = {'cas', 'name'}
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)

print(data)

def save_to_excel(mongoDB_data):
    # 写入excel
    outwb = Workbook()
    outws = outwb.worksheets[0]
    # 遍历外层列表
    for new_dict in mongoDB_data:
        a_list = []
        # 遍历内层每一个字典dict，把dict每一个值存入list
        for item in new_dict.values():
            a_list.append(item)
        # sheet直接append list即可
        outws.append(a_list)

    outwb.save(r'inf01.xlsx')
    print('数据存入excel成功')

# save_to_excel(o)