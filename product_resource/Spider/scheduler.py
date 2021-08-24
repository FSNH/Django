from mce_spider import start_mce
from xlsw_spider import start_xlsw
from multiprocessing import Process

def start():
    start_xlsw()
    start_mce()
if __name__ == '__main__':
    start()


