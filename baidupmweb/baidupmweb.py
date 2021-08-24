from flask import Flask
from flask import Flask, render_template, request,jsonify,redirect
from pm import BaiduPm
from gevent import pywsgi
import configparser
import requests
import logging
import os
import time
# 在创建 app 之前将 log 级别重置为debug，让其线上 info 日志级别
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def hello_world():
    return render_template("top.html")

@app.route('/getpm/',methods=["GET","POST"])
def getkeywords():
    global info
    info = []
    if request.method=="POST":
        data = request.form.get("data")
        datas = []
        for i in data.split("\n"):
            if i.strip()!='':
                datas.append(i.strip())
            else:
                pass
        app.logger.info(datas)
        info = BaiduPm().pool(datas)
        app.logger.info(info)
        if info:  # 反回数据不为空，数据就返回
            return {"code": "success", "data": info}
        else:
            return {"code": "false", "data": info}

    else:
        return render_template('index.html')

@app.route('/changeip/',methods=["GET","POST"])
def changeip():
    # 实例化configParser对象
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('./config.ini', encoding='utf-8-sig')

    acount = config.get('vps', 'acount')
    pwd = config.get('vps', 'pwd')
    """
    切换vps ip地址，成功就返回IP地址；失败就返回错误信息
    :return:
    """
    app.logger.info(acount)
    app.logger.info(pwd)
    os.system('rasdial /disconnect')
    time.sleep(1)
    # os.system('rasdial 宽带连接 05629694968 111222')
    os.system('rasdial 宽带连接'+' '+ acount+' '+ pwd)
    try:
        ip = requests.get("http://httpbin.org/ip").json().get("origin")
    except Exception as e:
        return {"code": "failed", "error": e,"vps":{"acount":acount,"pwd":pwd}}
    else:
        return {"code": "success","IP":ip,"vps":{"acount":acount,"pwd":pwd}}

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=6001)
if __name__ == '__main__':
    handler = logging.FileHandler('flask.log', encoding='UTF-8')  # 设置日志字符集和存储路径名字
    logging_format = logging.Formatter(  # 设置日志格式
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    server = pywsgi.WSGIServer(('0.0.0.0', 6001), app)
    server.serve_forever()
    app.run()