import os
import sys
import time

print(sys.path)
sys.path.append('F:\\pythongit\\product_resource\\Spider')
sys.path.append('F:\\pythongit\\product_resource')
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product_resource.settings")# project_name 项目名称
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utils.settings_local")  # 本地设置文件project_name 项目名称
django.setup()
from app.models import Property
from pymysql.converters import escape_string  # 字符串转义
import pymysql
class Update(object):


    def save(self, data):
        print("开始保存数据：",data)
        """
        :param data:  更新参数字典
        :return:
        """
        # TODO:采集到的数据保存到mysql数据库,这里存在更新一个产品多个规格是随机更新的情况，就存在与联合索引冲突的问题；
        # TODO:解决方法就是，两个数据库，一号同步数据的设置联合索引为唯一，二号设置为正常，数据从一号同步到二号数据库
        # TODO:使用orm update_or_create数据存在则更新不存在就新增
        for info in data:
            print(info)
            Property.objects.update_or_create(cas=info.get('cas'),
                                              specs=info.get('specs'),
                                              source=info.get('source'),
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
