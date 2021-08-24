import json
import time

from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import SpiderInfo, LinksSource, SaveSource, User
from router_data_redis.db import Test
from utils.db import SqlConnect
from .form import LoginForm
from .check_login import check_login


# Create your views here.

def login(request):
    error_msg1 = ""
    error_msg = ""
    form_obj = LoginForm()
    if request.method == "POST":
        form_obj = LoginForm(request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            pwd = form_obj.cleaned_data.get("pwd")
            # print(username, pwd)
            # 查询用户是否在数据库中
            if User.objects.filter(user=username).exists():
                users = User.objects.get(user=username)
                if users.pwd == pwd:
                    request.session['is_login'] = True
                    request.session['user_name'] = users.user
                    return redirect('index.html')
                else:
                    error_msg = '用户密码错误'
            else:
                error_msg = '用户名不存在'

    return render(request, 'login.html', {"form_obj": form_obj, "error_msg": error_msg})


@check_login
def logout(request):
    if not request.session.get('is_login', False):
        # 如果本来就未登录，也就没有登出一说
        return redirect("login.html")
    request.session.flush()
    return redirect("login.html")


def scrapy_info(request):
    spiders = SpiderInfo.objects.all()

    data = []
    for spider in spiders:
        info = {
            "id": spider.id,
            "project": spider.project_name,
            "spider_name": spider.spider_name,
            "source_name": spider.source_name,
            "company_name": spider.comname,
            "is_cas": "是" if spider.cas_search else "否",
            "is_priority": "是" if spider.priority else "否",
            "is_monitor": "是" if spider.monitor else "否",
            "create": spider.create_time,
            'status': 200
        }
        data.append(info)
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    pass


def monitor_info(request):
    monitors = SaveSource.objects.all()
    data = []
    for monitor in monitors:
        info = {
            "host": monitor.host,
            "port": monitor.port,
            "db": monitor.database_name,
            "collection": monitor.collection_name,
            "source_name": monitor.source_name,
            "spider_name": monitor.spider_info.project_name,
            "update": monitor.update_time,
            'status': 200
        }
        data.append(info)
    return JsonResponse(data, safe=False)


def load_data(reqyest):
    converts = LinksSource.objects.all()
    data = []
    for convert in converts:
        info = {
            "host": convert.host,
            "port": convert.port,
            "db": convert.database_name,
            "collection": convert.collection_name,
            "field_name": convert.field_name,
            "spider_name": convert.spider_info.spider_name,
            "update": convert.update_time,
            'status': 200
        }
        data.append(info)
    return JsonResponse(data, safe=False)

@check_login
def project_detail(request, pk):
    spider = SpiderInfo.objects.get(id=int(pk))
    spider_monitor = SaveSource.objects.get(spider_info__spider_name=spider.spider_name)
    print(spider_monitor)
    try:
        link_convert = LinksSource.objects.get(spider_info__spider_name=spider.spider_name)
        print(link_convert)
    except Exception as e:
        pass
    else:
        data = []
        info = {
            "project": spider.project_name,
            "spider_name": spider.spider_name,
            "company_name": spider.comname,
            "is_cas": "是" if spider.cas_search else "否",
            "is_priority": "是" if spider.priority else "否",
            "is_monitor": "是" if spider.monitor else "否",
            "save_db_name": spider_monitor.database_name if spider_monitor.database_name else '',
            "save_collection_name": spider_monitor.collection_name if spider_monitor.collection_name else '',
            "source_name": spider_monitor.source_name,
            "load_db_name": link_convert.database_name if link_convert.database_name else '',
            "load_collection_name": link_convert.collection_name if link_convert.collection_name else '',
            "field_name": link_convert.field_name,
            "create": spider.create_time,
            'status': 200
        }
        data.append(info)
    # return JsonResponse(data, safe=False)
    return render(request, 'detail.html', locals())

@check_login
def index(request):
    # InfluxClient().start()
    return render(request, 'index.html')

@check_login
def monitor(request):
    return render(request, 'monitor.html')

@check_login
def convert(request):
    return render(request, 'convert.html')


def search(request):
    global result
    if request.method == "POST":
        datas = request.POST.get('data', '')
        # TODO:传入参数
        """ 
        data = "[{'source': 'Bestfluorodrug',
                 'url': 'http://product.bestfluorodrug.com/product/282.html',
                 'cas': '',
                 'priority': 100},
                {'source': 'Bestfluorodrug',
                 'url': 'http://product.bestfluorodrug.com/product/283.html',
                 'cas': '',
                 'priority': 100}]"
        """
        if datas:
            results = []  # 获取到的数据列表
            c_urls = []  # 更新数据的url列表
            sources = []  # 更新数据源source列表
            for data in json.loads(datas):
                # print(data)
                if data.get("source"):  # 参数不为空且必填字段不为空
                    if data.get("cas") or data.get('url'):  # cas号和url二选一必填
                        try:
                            result = Test().predict(datas=data)  # 返回提交的数据
                        except Exception as e:
                            print(e)
                        else:
                            if result.get('success'):
                                time.sleep(3)
                                p_data = SqlConnect().select(data.get('url'))
                                results.extend(p_data)
                                c_urls.append(data.get("url"))
                                sources.append(data.get("source"))
                            else:
                                c_urls.append(data.get("url"))
                                sources.append(data.get("source"))
                                continue
                    else:
                        return JsonResponse([{"result": "0", "message": "cas和url参数二选一必填"}])
                else:
                    return JsonResponse([{"result": "0", "message": "数据不完整"}])
            # print(results)
            if results:
                result.update(
                    {"source": list(set(sources)), "url": c_urls, "total": len(c_urls), "msg": "",
                     "datas": results, "success": 1})
                return JsonResponse([result], safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                result.update({"source": list(set(sources)), "url": c_urls, "failure": len(c_urls), "msg": "未更新到数据",
                               "datas": results})
                return JsonResponse([result], safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse([{"result": "0", "message": "数据为空"}])
    elif request.method == "GET":
        source = request.GET.get("source", '')
        url = request.GET.get("url", '')
        cas = request.GET.get("cas", '')
        priority = request.GET.get("priority", 10)
        if source:
            if cas or url:
                data = {'source': source, 'url': url, 'cas': cas, 'priority': priority}
                if data.get("source"):  # 参数不为空且必填字段不为空
                    if data.get("cas") or data.get('url'):  # cas号和url二选一必填

                        try:
                            result = Test().predict(datas=data)  # 返回提交的数据
                            # print(result)
                        except Exception as e:
                            print(e)
                        else:
                            if result.get('success'):
                                time.sleep(3)
                                p_data = SqlConnect().select(data.get('url'))
                                # 判断返回数据是否有更新，检查LastModificationTime字段不为空，为空等待两秒再获取返回数据
                                # TODO:根据返回时间检查数据是否更新，检查LastModificationTime的时间与当前时间大小，正确返回更新数据为LastModificationTime字段时间大于当前时间

                                if p_data[0].get('LastModificationTime',
                                                 '') == "None":  # 获取更新时间，为空则重新获取数据，原因在于爬虫采集时间（慢）与操作存在时间差（快）
                                    print('等待两秒，重新获取。。。')
                                    time.sleep(2)
                                    p_data = SqlConnect().select(data.get('url'))
                                    if p_data[0].get('LastModificationTime', '') == "None":
                                        result.update({"flag": 0})
                                    print(f'返回数据：{p_data}')
                                result.update({"flag": 1, "msg": "", "datas": p_data})
                                return JsonResponse([result], safe=False, json_dumps_params={'ensure_ascii': False})
                            else:
                                result.update({"msg": "未更新到数据", "datas": []})
                                return JsonResponse([result], safe=False, json_dumps_params={'ensure_ascii': False})

                    else:
                        return JsonResponse([{"result": "0", "message": "cas和url参数二选一必填"}])
            else:
                return JsonResponse([{"result": "0", "message": "数据不完整"}])
        else:
            return JsonResponse([{"result": "0", "message": "数据源为空"}])


def istrue(request, pk):
    """配置爬虫可用"""
    # print(pk)
    SpiderInfo.objects.filter(id=int(pk)).update(monitor=True)
    return redirect('/index.html')


def isdelete(request, pk):
    """配置爬虫不可用"""
    SpiderInfo.objects.filter(id=int(pk)).update(monitor=False)
    return redirect('/index.html')


def all_cas(request):
    """
    data = "[{'source': 'Bestfluorodrug',
                 'url': 'http://product.bestfluorodrug.com/product/282.html',
                 'cas': '',
                 'priority': 100},
                {'source': 'Bestfluorodrug',
                 'url': 'http://product.bestfluorodrug.com/product/283.html',
                 'cas': '',
                 'priority': 100}]"
    """
    global result
    if request.method == 'POST':
        datas = request.POST.get('data', '')
        if datas:
            sources = []
            for data in json.loads(datas):
                if data.get('cas', ''):
                    # 构造cas对应每一个爬虫
                    for spider in SpiderInfo.objects.all():
                        if spider.monitor and spider.cas_search:
                            sources.append(spider.source_name)
                            cas_data = {"source": spider.source_name, "cas": data.get('cas'), "url": "",
                                        'priority': 100}
                            try:
                                result = Test().predict(datas=cas_data)  # 返回提交的数据
                            except Exception as e:
                                print(e)
                        else:
                            continue
                else:
                    return JsonResponse([{"result": "0", "message": "cas数据为空"}])
            if sources:
                result.update(
                    {"source": sources, "totals": len(sources), "flag": 1, "msg": "", "success": 1, "datas": []})
                return JsonResponse([result], safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                result.update({"source": sources, "totals": len(sources), "flag": 1, "msg": "", "datas": []})
                return JsonResponse([result], safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse([{"result": "0", "message": "数据为空"}])
    else:
        pass
