import pymongo
import pymysql
import time
from multiprocessing import Process
import xlrd
import csv
from pymysql.converters import escape_string  # 字符串转义


# 获取MONGODB数据库数据
class Mongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="192.168.1.30", port=27017)
        self.db = self.client.db_601e31e005c70417bcd24f27  # molbase
        self.db1 = self.client.db_601cb09f05c7041214a15890  # chemicbook
        self.db2 = self.client.db_5fe3e40a05c7040cf8aecda2  # lookchem
        self.db3 = self.client.db_6041f920e770401248654447  # gaide
        self.db4 = self.client.db_5dca18fa05c7040ca4e8fe9c  # 丁香通
        self.collection = self.db.entity_601e31e005c70417bcd24f27_companyinfo  # 联系信息
        self.collection1 = self.db1.entity_601cb09f05c7041214a15890_companyinfo  # 联系信息
        self.collection2 = self.db2.entity_5fe3e40a05c7040cf8aecda2_companyinfo  # 联系信息
        self.collection3 = self.db3.entity_6041f920e770401248654447_detail_info  # 联系信息
        self.collection4 = self.db4.entity_5dca18fa05c7040ca4e8fe9c_companyinfo  # 丁香通

    def name_to_company_name(self):
        """
        将字段名称不符合导入字段的数据进行转换
        pt：丁香通
        :return: dict
        "comname" : "上海雅吉生物科技有限公司",
        "QQ" : "58268971",
        "cell" : "15821073967",
        "comaddress" : "上海闵行区元江路5500号第1幢5658室",
        "comurl" : "https://yaji.biomart.cn",
        "contactname" : "高杰",
        "mail" : "yajikit@163.com",
        "mode" : "生产厂商,代理商",
        "proname" : "玫瑰红三羧酸铵丨铝试剂丨玫红三羧酸铵丨5-[(3-羧基-4-羟基苯基)(3-羧基-4-氧代-2,5-环己二烯-1-亚基)甲基]-2-羟基苯甲酸三铵盐丨金精三羧酸铵丨金红三甲酸铵丨2-(亚水杨基氨基)酚丨水杨叉邻氨基酚丨水杨醛缩邻氨基酚丨Aluminon",
        "scope" : "细胞库 / 细胞培养,试剂,技术服务",
        "tel" : "021-34661275",
        "years" : "5 年",
        """
        data = self.collection4.find(no_cursor_timeout=True)
        for i, content in enumerate(data):
            info = {
                "pt": content.get("source", '') if content.get("source") else '丁香通',
                "company_name": content.get('comname'),
                "years": content.get('years') if content.get('years') is not None else '',
                "person": content.get('contactname') if content.get('contactname') else '',
                "telephone": content.get('tel') if content.get('tel') else '',
                "phone": content.get('cell') if content.get('cell') else '',
                "qq": content.get("QQ") if content.get("QQ") else '',
                "email": content.get("mail") if content.get("mail") else '',
                "company_type": content.get("mode") if content.get("mode") else '',
                "company_scope": content.get("scope") if content.get("scope") else '',
                "product_num": int(content.get("product_num")) if content.get(
                    "product_num") is not None and content.get(
                    "product_num") != '' else 0,
                "address": content.get("comaddress") if content.get("comaddress") is not None else '',
                "source": content.get("source") if content.get("source") else '丁香通',
                "url": content.get('comurl'),
                "pickup_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            # print(info)
            # """平台类型	公司名称	联系人	座机	手机	QQ	邮箱	地址	公司类型	主营产品 合作年限	更新时间"""
            # with open('companyinfo1.csv', 'a+', encoding='utf8', newline='')as f:
            #     headers = ['平台类型', '公司名称', '联系人', '座机', '手机', 'QQ', '邮箱', '地址', '公司类型', '主营产品', '合作年限', '更新时间']
            #     rows = [
            #         (info.get('pt'),
            #          info.get('company_name'),
            #          info.get('person'),
            #          info.get('telephone'),
            #          info.get('phone'),
            #          info.get('qq'),
            #          info.get('email'),
            #          info.get('address'),
            #          info.get('company_type'),
            #          info.get('company_scope'),
            #          info.get('years'),
            #          info.get('pickup_date'),
            #          )]
            #     f_csv = csv.writer(f)
            #     # f_csv.writerow(headers)
            #     f_csv.writerows(rows)
            if info.get('years'):
                Mysql().insert(info)
                Mysql().insert_conpany_name(info)
                print(i, info)
        Mysql().close()

    def get_company_name(self):
        """
        no_cursor_timeout=True  防止数据量太多  报错
        获取公司名信息
        :return:
        """
        print('开始同步公司名称数据---------------------------------------------')
        data = self.collection4.find(no_cursor_timeout=True)
        for i, content in enumerate(data):
            if content.get('company_name', ''):
                print(content)
                info = {
                    "company_name": content.get('company_name'),
                    "pickup_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
                Mysql().insert_conpany_name(info)
                print(i, info)

        Mysql().close()
        pass

    def get_link_info(self):
        """
        no_cursor_timeout=True  防止数据量太多  报错
        获取vip联系信息
        :return:
        """
        print('开始同步公司信息数据---------------------------------------------')
        data = self.collection4.find(no_cursor_timeout=True)
        # 采集的全部数据库的字段
        for i, content in enumerate(data):
            if content.get('company_name', ''):
                info = {
                    "company_name": content.get('company_name'),
                    "years": content.get('years') if content.get('years') != None else '',
                    "person": content.get('person') if content.get('person') else '',
                    "telephone": content.get('telephone') if content.get('telephone') else '',
                    "phone": content.get('phone') if content.get('phone') else '',
                    "qq": content.get("qq") if content.get("qq") else '',
                    "email": content.get("email") if content.get("email") else '',
                    "company_type": content.get("company_type") if content.get("company_type") else '',
                    "company_scope": content.get("company_scope") if content.get("company_scope") else '',
                    "product_num": int(content.get("product_num")) if content.get(
                        "product_num") is not None and content.get(
                        "product_num") != '' else 0,
                    "address": content.get("address") if content.get("address") != None else '',
                    "source": content.get("source"),
                    "url": content.get('url'),
                    "pickup_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
                Mysql().insert(info)
                print(i, info)
        Mysql().close()

    def get_pt_info(self):
        """
        no_cursor_timeout=True  防止数据量太多  报错
        获取vip联系信息
        :return:
        """
        print('开始同步平台数据---------------------------------------------')
        data = self.collection.find(no_cursor_timeout=True)
        for i, content in enumerate(data):
            if content.get('company_name', ''):
                info = {
                    "company_name": content.get('company_name'),
                    "pt_num": int(1),
                    "product_num": int(content.get("product_num")) if content.get(
                        "product_num") is not None and content.get(
                        "product_num") != '' else 0,  # 平台产品数据最大值为整数
                    "source": content.get("source"),
                    "url": content.get('url'),
                }
                Mysql().insert_pt(info)
                print(i, info)
            else:
                print("没有公司名", info)
        Mysql().close()


# 数据同步处理更新到MySQL数据库
class Mysql(object):
    def __init__(self):
        # self.client = pymysql.connect(host='localhost',user='root', password='123456', database='company_search',
        #                               charset='utf8')  # 打开数据库连接,本地测试
        self.client = pymysql.connect(host='192.168.1.26', user='company_search', password='WAaN3AHaDDFHJ6DY',
                                      database='company_search',
                                      charset='utf8')  # 打开数据库连接，线上
        self.cursor = self.client.cursor()  # 获取操作游标

    def select(self):
        """
        查询所有
        :return:
        """
        self.cursor.execute('select * from app_company_info')  # 运行SOL语句
        lists = self.cursor.fetchall()  # 接收返回的结果
        if lists is not None:
            print(lists)
        # for i in lists:
        #     print(i)
        #     print(i[1], i[10], i[11])

    def insert(self, content):
        """
        插入规格信息
        按公司名、源链接、平台联合去重
        :param content:
        :return:
        """

        # content = {
        #     'company_name': '青岛万源山生物科技有限公司',
        #     # 'telephone': '010-67886402',
        #     # 'phone': '18515385101',
        #     # 'qq': '2853399794',
        #     # 'email': 'weipeng@hopelife.cn',
        #     # 'address': '北京经济技术开发区宏达北路12号创新大厦B座1区309室',
        #     # 'company_type': '定制',
        #     'source': 'chemicbook',
        #     'pickup_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        #     'url': 'https://www.chemicalbook.com/supplier/14851902/',
        #     'product_num': '50',
        # }

        if content.get("company_name", ''):
            print(content)
            sql = "INSERT INTO app_company_info (" \
                  "company_name,link_person,telephone,mobile,qq,email,address,company_type,product_num,scope,cooperate_years,source,source_url,update_time) " \
                  "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " \
                  "ON DUPLICATE KEY UPDATE link_person='%s',telephone='%s',mobile='%s',qq='%s',email='%s',address='%s',company_type='%s',product_num='%s',scope='%s',cooperate_years='%s',update_time='%s'" % \
                  (
                      str(content.get("company_name")),
                      str(content.get("person", '')), str(content.get("telephone", '')),
                      str(content.get("phone", '')), str(content.get("qq", '')), str(content.get("email", '')),
                      str(content.get("address", '')),
                      str(content.get("company_type", '')),
                      int(content.get("product_num")) if content.get("product_num") is not None and content.get(
                          "product_num") != '' else 0,
                      str(";".join(content.get("company_scope")) if content.get("company_scope") != "" and content.get(
                          "company_scope") is not None else ''),
                      str(content.get("years", '')), str(content.get("source")), str(content.get("url")),
                      str(content.get("pickup_date")),

                      # 以下为更新字段
                      str(content.get("person", '')), str(content.get("telephone", '')),
                      str(content.get("phone", '')), str(content.get("qq", '')), str(content.get("email", '')),
                      str(content.get("address", '')),
                      str(content.get("company_type", '')),
                      int(content.get("product_num")) if content.get("product_num") is not None and content.get(
                          "product_num") != '' else 0,
                      str(";".join(content.get("company_scope")) if content.get("company_scope") != "" and content.get(
                          "company_scope") is not None else ''),
                      str(content.get("years", '')),
                      str(content.get("pickup_date"))

                  )
            self.cursor.execute(sql)

            self.client.commit()  # 提交mysql语句

    def insert_conpany_name(self, content):
        """
        插入公司名称库
        按公司名去重
        :param content:
        :return:
        """
        # content = {
        #     'company_name': '北京海步医药科技有限公司',
        #     'pickup_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        # }
        if content.get("company_name", ''):
            sql = 'INSERT INTO app_company (company_name,update_time) VALUES ("%s","%s") ON DUPLICATE KEY UPDATE update_time="%s"' % \
                  (
                      str(content.get("company_name")),
                      str(content.get("pickup_date")),
                      # 下面是更新字段值
                      str(content.get("pickup_date")),
                  )
            self.cursor.execute(sql)
            self.client.commit()  # 提交mysql语句
        pass

    def insert_pt(self, content):
        """
        导入数据到ptinfo,计算出pt_num,pt_sources,product_num_max
        :param content:
        :return:
        """
        # content = {
        #
        #     'company_name': '青岛万源山生物科技有限公司',
        #     "source": 'lookchem',
        #     "url": "https://www.chemicalbook.com/supplier/14851902/",
        #     # 'pt_num': '2',
        #     # 'pt_sources': 'chemicbook lookchem',
        #     'product_num': '53',
        # }
        check_sql = "select company_name,pt_sources,product_num_max,pt_num from app_ptinfo where company_name='{0}'".format(
            content.get('company_name'))
        self.cursor.execute(check_sql)
        # 查询待插入公司是否存在pt_info数据库中
        result = self.cursor.fetchall()
        if result:  # 存在；就判断待插入的数据记录的数据源source类型是否已经存在pt_info的数据源类型中，存在就只更新pt_info的最大产品数，否则更新整条记录；
            for res in result:
                print(res[0], res[1], res[2], res[3])
                # print(str(content.get('source')+" "+str(res[1])),int(res[3])+1,max(content.get('product_num'),res[2]))
                # 判断待插入的数据记录的数据源source类型是否已经存在pt_info的数据源类型中，存在就只更新pt_info的最大产品数，否则更新整条记录；
                s1_sql = 'SELECT source FROM app_company_info WHERE company_name="{0}" AND source_url="{1}"'.format(
                    content.get('company_name'), content.get('url'))
                print(s1_sql)
                self.cursor.execute(s1_sql)
                source = self.cursor.fetchone()  # 接收返回的source
                if source:  # 待插入数据记录的源是否存在pt_info平台类型中，存在就只更新最大产品数，否则更新整条记录
                    s_sql = 'SELECT pt_sources FROM app_ptinfo WHERE company_name="{0}"'.format(
                        content.get('company_name'))
                    self.cursor.execute(s_sql)
                    lists = self.cursor.fetchone()  # 接收返回的结果
                    # 获取pt_info
                    if lists:
                        print("插入数据源" + source[0])
                        print("平台已有数据源" + lists[0])
                        if source[0] in lists[0]:
                            print("更新数据最大产品数：", res[0])
                            update_sql = "UPDATE app_ptinfo SET product_num_max='{0}' WHERE company_name='{1}'". \
                                format(str(max(int(content.get('product_num')), int(res[2]))),
                                       content.get('company_name'))
                            self.cursor.execute(update_sql)
                            self.client.commit()  # 提交mysql语句
                        else:
                            print("更新数据：", res[0])
                            update_sql = "UPDATE app_ptinfo SET pt_sources='{0}',pt_num='{1}',product_num_max='{2}' WHERE company_name='{3}'". \
                                format(str(content.get('source') + " " + str(res[1])), int(res[3]) + 1,
                                       str(max(int(content.get('product_num')), int(res[2]))),
                                       content.get('company_name'))
                            self.cursor.execute(update_sql)
                            self.client.commit()  # 提交mysql语句

        else:  # 不能存在就直接插入
            sql = "INSERT IGNORE INTO app_ptinfo (company_name,pt_num,pt_sources,product_num_max) VALUES (%s,%s,%s,%s)"
            self.cursor.execute(sql, (
                str(content.get("company_name")),
                str(content.get("pt_num")),
                str(content.get("source")),
                int(content.get("product_num")) if content.get("product_num") != None and content.get(
                    "product_num") != '' else 0,
            ))
            self.client.commit()  # 提交mysql语句

        pass

    def read_excel(self):
        data = xlrd.open_workbook('付费会员目录.xlsx')  # 使用xlrd模块打开excel表读取数据
        # 根据工作表的索引获取工作表的内容
        table = data.sheet_by_name('Sheet1')
        # 获取第一行所有内容,如果括号中1就是第二行，这点跟列表索引类似
        keys = table.row_values(0)  # hearer
        # 获取工作表的有效行数
        rowNum = table.nrows
        # 获取工作表的有效列数
        colNum = table.ncols
        # 定义一个空列表
        datas = []
        for i in range(1, rowNum):
            # 定义一个空字典
            sheet_data = {}
            for j in range(colNum):
                # 获取单元格数据
                c_cell = table.cell_value(i, j)
                # print(c_cell)
                # sheet_data[self.keys[j]] = c_cell
                # 循环每一个有效的单元格，将字段与值对应存储到字典中
                # 字典的key就是excel表中每列第一行的字段
                sheet_data[keys[j]] = table.row_values(i)[j]
                sheet_data['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            datas.append(sheet_data)
        # print(datas)
        return datas

    def insert_chem960vip(self):
        data = self.read_excel()
        for name in data:
            print(name)
            sql = "INSERT IGNORE INTO app_chem960vipcompany (companyname,create_time) VALUES (%s,%s)"
            self.cursor.execute(sql, (name.get('CompanyName'), name.get('create_time')))
            self.client.commit()  # 提交mysql语句

    def close(self):
        """
        数据库关闭
        :return:
        """
        self.client.close()  # 关闭数据库


if __name__ == '__main__':
    # Mysql().select()
    # Mysql().insert_chem960vip()
    # Mysql().read_excel()

    # p1 = Process(target=Mongo().get_company_name(), args=("进程1",))  # 创建第一个进程  # 公司名称
    # p2 = Process(target=Mongo().get_link_info(), args=("进程2",))  # 创建第二个进程  # 公司联系方式
    # p3 = Process(target=Mongo().get_pt_info(), args=("进程3",))  # 创建第二个进程  # 公司综合信息
    # #
    # p1.start()  # 开启第一个进程
    # p2.start()  # 开启第二个进程
    # p3.start()  # 开启第三个进程

    Mongo().name_to_company_name()  # 同步公司名及公司详情信息

    print("执行完毕")
