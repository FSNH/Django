from django.test import TestCase

# Create your tests here.

import pymysql


class Mysql():
    def __init__(self):
        self.client = pymysql.connect(host='localhost', user='root', password='123456', database='company_search',
                                      charset='utf8')  # 打开数据库连接,本地测试

        self.cursor = self.client.cursor()  # 获取操作游标

    def insert(self):
        """
        插入平台数据时，如果插入数据的平台类型已经存在pt_info平台字段中，就不更新该条数据的平台类型以及平台数据只更新平台产品数量，
        :return:
        """
        s1_sql = 'SELECT source FROM app_company_info WHERE company_name="{0}" AND source_url="{1}"'.format(
            '武汉鼎信通药业有限公司', 'https://www.chemicalbook.com/supplier/15595671/')
        self.cursor.execute(s1_sql)
        source = self.cursor.fetchone()  # 接收返回的source
        if source:
            s_sql = 'SELECT pt_sources FROM app_ptinfo WHERE company_name="{}"'.format('武汉鼎信通药业有限公司')
            self.cursor.execute(s_sql)
            lists = self.cursor.fetchone()  # 接收返回的结果
            if source[0] in lists[0]:
                print('存在')
            else:
                print('不存在')
            print(lists[0])
            pass


if __name__ == '__main__':
    import pandas as pd
    import time
    import os
    from openpyxl.workbook import Workbook

    time_stamp = time_stamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    info = [{'status': 200, 'result_list': '淮安德邦化工有限公司', 'keyword': '544'}]
    df = pd.DataFrame(info)
    print(pd)
    print(time_stamp)
    file_path = os.path.join('F:\pythongit\company_search\media', time_stamp + ".xlsx")
    df.to_excel(file_path, index=False)
    # Mysql().insert()
    # kwargs = {'company_name': 1, 'company_name': 2}
    # print(kwargs)
