from multiprocessing import Process
from utils.load_data_from_mongo import MongoToMysql
from utils.mdb_to_upload_mdb import MongoToMongo

while True:
    p1 = Process(target=MongoToMongo().start_pool(), args=("进程1",))  # 创建第一个进程
    p2 = Process(target=MongoToMysql().getmongo(), args=("进程2",))  # 创建第一个进程
    p1.start()
    p2.start()