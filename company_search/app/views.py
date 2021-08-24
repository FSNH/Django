# encoding=utf-8
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger
from .models import Company, Company_info, Ptinfo, User, UserMonitor, Chem960VipCompany
from .form import LoginForm
from .check_login import check_login
import json
import os
from .verify_cas import IsCas
import requests
from .baidupm import BaiduPm
from .chemical_cas import CasVerifyGet
from django.http import StreamingHttpResponse
import time
import pandas as pd

# 当前文件目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
            if User.objects.filter(uname=username).exists():
                user = User.objects.get(uname=username)
                if user.pwd == pwd:
                    request.session['is_login'] = True
                    request.session['user_name'] = user.uname
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


@check_login
def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.method == "GET":
        get_ip(request)
        name = request.GET.get("company_name", '')
        try:
            pindex = request.GET.get('page', 1)
        except PageNotAnInteger:
            pindex = 1
        global queryset
        if name:
            kwargs = {"company_name": name}
            queryset = Ptinfo.objects.filter(**kwargs)
        else:
            queryset = Ptinfo.objects.all().order_by('-pt_num', '-product_num_max')
        paginator = Paginator(queryset, 20)  # 创建每页显示的数量实列
        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        page_nums = paginator.num_pages
        return render(request, "index.html", {"page": page, "page_nums": page_nums})


@check_login
def search(request):
    """
    模糊查找
    :param request:
    :return:
    """
    get_ip(request)
    return render(request, "search.html")


@check_login
def getcompanyname(request):
    if request.method == "GET":
        get_ip(request)
        name = request.GET.get("company_name", '')
        try:
            pindex = request.GET.get('page', 1)
        except PageNotAnInteger:
            pindex = 1
        global queryset
        if name:
            kwargs = {'company_name': name}
            queryset = Company.objects.filter(**kwargs)
        else:
            queryset = Company.objects.all().order_by("-update_time")
        paginator = Paginator(queryset, 20)  # 创建每页显示的数量实列
        page = paginator.page(pindex)  # 传递当前页的实例对象到前端
        page_nums = paginator.num_pages
        return render(request, "company.html", {"page": page, "page_nums": page_nums})


@check_login
def getdetail(request):
    """
    平台公司详情
    :param request:
    :return:
    """
    if request.method == "GET":
        get_ip(request)
        name = request.GET.get("name", "")
        sources = request.GET.get("source", "")
        # print(sources)
        # 相同公司数据源去重处理
        sourcelist = list(set(sources.split()))
        # print(sourcelist)
        results = []
        for source in sourcelist:
            # print(source)
            kwargs = {
                "company_name": name,
                "source": source
            }
            # print(name)
            result = Company_info.objects.filter(**kwargs)
            results.append(result)
        # print(results)
    return render(request, "detail.html", {"results": results})


@check_login
def company_detail(request):
    """
    企业详细信息
    :param request:
    :return:
    """
    get_ip(request)
    name = request.GET.get("name", '')
    results = []
    if name:
        kwargs = {'company_name': name}
        result = Company_info.objects.filter(**kwargs)
        results.append(result)
    return render(request, 'company_detail.html', {'results': results})


@check_login
def searchapi(request):
    """
    模糊查询接口
    :param request:
    :return:
    """
    if request.method == "POST":
        get_ip(request)
        data = request.POST.get('name', "")
        kwargs = {
            "company_name__icontains": data
        }
        queryset = Ptinfo.objects.filter(**kwargs)[:100]
        if queryset:
            d = []
            for q in queryset:
                tmp = {}
                vip_c = {'companyname': q.company_name}
                vip = Chem960VipCompany.objects.filter(**vip_c).first()  # 判断是都是vip
                if vip is not None:
                    # print(vip)
                    tmp["vip"] = "是"
                else:
                    tmp["vip"] = "否"
                tmp["company_name"] = q.company_name
                tmp['num'] = q.pt_num
                tmp['sourcelist'] = q.pt_sources
                tmp['product_num_max'] = q.product_num_max
                tmp["message"] = 'success'
                d.append(tmp)
            # print(d)
        else:
            tmp = {
                "status": "fail",
                "message": "没有查询到，请更换关键词重试！"
            }
        return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})


@check_login
def m_searchAip(request):
    """
    批量搜索接口
    :param request:
    :return:
    """
    if request.method == "POST":
        get_ip(request)
        data = request.POST.get('data', '')
        d = []
        if data:
            names = data.split('\n')
            global queryset
            for name in names:
                kwargs = {"company_name": name.strip()}
                queryset = Ptinfo.objects.filter(**kwargs)
                if queryset:
                    for q in queryset:
                        tmp = {}
                        vip_c = {'companyname': q.company_name}
                        vip = Chem960VipCompany.objects.filter(**vip_c).first()  # 判断是都是vip
                        if vip is not None:
                            print(vip)
                            tmp["vip"] = "是"
                        else:
                            tmp["vip"] = "否"
                        tmp["company_name"] = q.company_name
                        tmp['num'] = q.pt_num
                        tmp['sourcelist'] = q.pt_sources
                        tmp['product_num_max'] = q.product_num_max
                        tmp["message"] = 'success'
                        d.append(tmp)
                        # print(d)
                else:
                    tmp = {
                        "status": "fail",
                        "message": "没有查询到，请更换关键词重试！"
                    }
        return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})


def get_ip(request):
    """
    获取用户访问的ip信息
    :param request:
    :return:
    """
    address = request.path
    name = request.session['user_name']
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {'name': name, 'IP': ip, 'localtime': local, 'address': address}
    print(data)
    kwargs = {'name': name, 'address': address}
    M = UserMonitor.objects.filter(**kwargs).first()  # 获取第一条数据，如果数据根据用户及地址已经存在就更新访问次数加一，否则新建
    if M is not None:
        count = M.views
        M = UserMonitor.objects.filter(**kwargs).update(localtime=local, views=count + 1)
    else:
        M = UserMonitor.objects.create(**data)
        M.viewed()
    # return json.dumps(data)
    # return JsonResponse(data,safe=False, json_dumps_params={'ensure_ascii': False})


@check_login
def check_chem960vip(request):
    """
    检测公司是否是chem960会员
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST.get('data', '')
        global result
        results = []
        if data is not None:
            for name in data.split(';'):
                kwargs = {'companyname': name}
                vip = Chem960VipCompany.objects.filter(**kwargs).first()
                if vip is not None:
                    result = {"status": '是'}
                    results.append(result)
                else:
                    result = {"status": '否'}
                    results.append(result)
            return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})


@check_login
def chem960(request):
    return render(request, "cas_click_search.html")


@check_login
def chem960_click_nums(request):
    global info
    if request.method == 'POST':
        get_ip(request)
        year = request.POST.get('year', '')
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')
        cas = request.POST.get('cas', '')
        if cas and IsCas.iscas(cas.strip()):
            if not year:
                total, _ = clicknums(cas.strip())  # 获取cas号排名
                if total:
                    info = [
                        {"status": 200,
                         "total": total,
                         "keyword": cas.strip()}
                    ]
                    print(info)

            else:
                total, _ = clicknums(cas=cas.strip(), year=year, start=start, end=end)  # 获取公司id排名
                if total:
                    info = [
                        {"status": 200,
                         "total": total,
                         "keyword": cas.strip()}
                    ]
                    print(info)
        else:
            info = [
                {"status": "fail",
                 "message": "CAS号不正确"
                 }
            ]

    return JsonResponse(info, safe=False, json_dumps_params={'ensure_ascii': False})


def clicknums(cas='', year='', start='', end=''):
    url = 'http://work.kuujia.web960.com:8090/api/data/getdata'
    data = {"entityname": "chem960click", "page": 1, "psize": 100000}
    # s = {"CasNo": cas}
    # data.update({"fliter": json.dumps(s)})
    if year:  # 如果年存在，按月时间段查询
        s_data = [{"CasNo": cas}, {"Year": int(year)}, {"Month": {"$gte": int(start), "$lte": int(end)}}]
        f_data = {"$and": s_data}
        data.update({"fliter": json.dumps(f_data)})
    else:  # 否则就直接按cas查询
        s = {"CasNo": cas}
        data.update({"fliter": json.dumps(s)})
    # print(data)
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    # print(data)
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    total = resp.json().get("totalcount")
    result_list = resp.json().get("list")
    # print(total, result_list)
    if total:
        return total, result_list
    else:
        return None


@check_login
def m_chem960_click_nums(request):
    global d
    if request.method == 'POST':
        get_ip(request)
        data = request.POST.get('data', '')
        print(data)
        d = []
        for cas in data.split("\n"):
            if cas and IsCas.iscas(cas.strip()):
                total = clicknums(cas=cas.strip())
                if total:
                    # print(total)
                    info = {
                        "status": 200,
                        "total": total,
                        "cas": cas.strip()
                    }
                    d.append(info)
                else:
                    info = {
                        "status": 200,
                        "message": "CAS号不存在",
                        "cas": cas.strip()
                    }
                    d.append(info)
            else:
                continue

    return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})


@check_login
def pm_chem960_nums(request):
    global info
    if request.method == 'POST':
        get_ip(request)
        cas = request.POST.get('cas', '')
        if cas and IsCas.iscas(cas.strip()):
            total = clicknums(cas=cas.strip())  # 获取cas号排名
            if total:
                info = []
                pms = BaiduPm().start(str(cas.strip()))
                for s in pms:
                    d = {"status": 200,
                         "total": total,
                         "keyword": cas.strip()
                         }
                    s.update(d)
                    info.append(s)
                # print(info)
            else:
                info = [
                    {"status": 200,
                     "total": total,
                     "keyword": cas.strip()}
                ]
                # print(info)
        else:
            info = [
                {"status": "fail",
                 "message": "CAS号不正确"
                 }
            ]

    return JsonResponse(info, safe=False, json_dumps_params={'ensure_ascii': False})


def verify(request):
    return render(request, 'verify.html')


def cas_verify_get(request):
    global info_list
    if request.method == 'POST':
        get_ip(request)
        cas = request.POST.get('cas', '')
        info_list = []
        if cas:
            data = CasVerifyGet().get_cas(cas=cas)
            if not data.get("message", ''):
                data.update({"status": 200})
                info_list.append(data)
            else:
                info_list.append(data)
        else:
            data = {"status": "fail", "message": "请移步chemicalbook!"}
            info_list.append(data)
    return JsonResponse(info_list, safe=False, json_dumps_params={'ensure_ascii': False})


def company_clicknums(cid='', start='', end='', year=''):
    url = 'http://work.kuujia.web960.com:8090/api/data/getdata'
    data = {"entityname": "chem960click", "page": 1, "psize": 70000}
    if year:  # 如果年存在，按月时间段查询
        s_data = [{"CompanyId": cid}, {"Year": int(year)}, {"Month": {"$gte": int(start), "$lte": int(end)}}]
        f_data = {"$and": s_data}
        data.update({"fliter": json.dumps(f_data)})
    else:  # 否则就直接按公司id查询
        s = {"CompanyId": cid}
        data.update({"fliter": json.dumps(s)})
    # print(data)
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    # print(resp.text)
    total = resp.json().get("totalcount")
    result_list = resp.json().get('list')
    # print(result_list)
    if total:
        return total, result_list
    else:
        return None


def comid_chem960_nums(request):
    """
    公司点击情况
    :param request:
    :return:
    """
    global info
    if request.method == 'POST':
        get_ip(request)
        cid = request.POST.get('cid', '')
        year = request.POST.get('year', '')
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')
        if cid:
            # print(cid)
            if not year:  # 没有设置年和月份开始结束
                total, _ = company_clicknums(cid=cid.strip())  # 获取公司id排名
                if total:
                    info = [
                        {"status": 200,
                         "total": total,
                         "keyword": cid.strip()}
                    ]
                    # print(info)
            else:
                total, _ = company_clicknums(cid=cid.strip(), year=year, start=start, end=end)  # 获取公司id排名
                if total:
                    info = [
                        {"status": 200,
                         "total": total,
                         "keyword": cid.strip()}
                    ]
                    print(info)
        else:
            info = [
                {"status": "fail",
                 "message": "公司id不存在"
                 }
            ]
    # print(info)
    return JsonResponse(info, safe=False, json_dumps_params={'ensure_ascii': False})


def company_search(request):
    # get_ip(request)
    return render(request, 'cid_click_search.html')


def file_iterator(file_name, chunk_size=512):  # 用于形成二进制数据
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def download_booking_API(request):
    time_stamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    response = ""
    if request.method == "POST":
        # print("download_booking_API")
        global info
        info = []
        cid = request.POST.get('cid', '')
        year = request.POST.get('year', '')
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')
        if cid:
            if not year:  # 没有设置年和月份开始结束
                _, result_list = company_clicknums(cid=cid.strip())  # 获取公司id排名
                # print(result_list)
                if result_list:
                    for res in result_list:
                        info.append({
                            "公司名称": res.get("CompanyName"),
                            "keyword": cid.strip(),
                            "CasNo": res.get('CasNo'),
                            "点击对象": res.get('ClickObject'),
                            '点击位置': res.get('ClickFrom'),
                            '点击时间': res.get('CreationTime')
                        })

            else:
                _, result_list = company_clicknums(cid=cid.strip(), year=year, start=start, end=end)  # 获取公司id排名
                if result_list:
                    for res in result_list:
                        info.append({
                            "公司名称": res.get("CompanyName"),
                            # "keyword": cid.strip(),
                            "CasNo": res.get('CasNo'),
                            "点击对象": res.get('ClickObject'),
                            '点击位置': res.get('ClickFrom'),
                            '点击时间': res.get('CreationTime')
                        })
                    # save data by excel file
        # print(info)
        df = pd.DataFrame(info)
        file_path = os.path.join(BASE_DIR, 'media', time_stamp + ".xlsx")
        # print(file_path)
        df.to_excel(file_path, index=False)

        # 返回时间戳（文件名）
        # print(time_stamp)
        return HttpResponse(time_stamp)

    else:
        file_name = request.GET.get('file_name')
        # print('file_name')
        # print(file_name)
        file_path = os.path.join(BASE_DIR, 'media', file_name + ".xlsx")
        response = StreamingHttpResponse(file_iterator(file_path))  # 这里创建返回
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        response['Content-Disposition'] = 'attachment;filename="company_%s.xlsx"' % file_name
        # 注意filename 这个是下载后的名字
        # print(response)
        return response


def download_casinfoing_API(request):
    time_stamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    response = ""
    if request.method == "POST":
        # print("download_booking_API")
        global info
        info = []
        cas = request.POST.get('cas', '')
        year = request.POST.get('year', '')
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')
        if cas:
            if not year:  # 没有设置年和月份开始结束
                _, result_list = clicknums(cas=cas.strip())  # 获取公司id排名
                # print(result_list)
                if result_list:
                    for res in result_list:
                        # print("---------------------------")
                        # print(res)
                        info.append({
                            "公司名称": res.get("CompanyName"),
                            # "keyword": cas.strip(),
                            "CasNo": res.get('CasNo'),
                            "点击对象": res.get('ClickObject'),
                            '点击位置': res.get('ClickFrom'),
                            '点击时间': res.get('CreationTime')
                        })

            else:
                _, result_list = clicknums(cas=cas.strip(), year=year, start=start, end=end)  # 获取公司id排名
                if result_list:
                    for res in result_list:
                        info.append({
                            "公司名称": res.get("CompanyName"),
                            # "keyword": cid.strip(),
                            "CasNo": res.get('CasNo'),
                            "点击对象": res.get('ClickObject'),
                            '点击位置': res.get('ClickFrom'),
                            '点击时间': res.get('CreationTime')
                        })
                    # save data by excel file
        # print(info)
        df = pd.DataFrame(info)
        file_path = os.path.join(BASE_DIR, 'media', time_stamp + ".xlsx")
        # print(file_path)
        df.to_excel(file_path, index=False)

        # 返回时间戳（文件名）
        # print(time_stamp)
        return HttpResponse(time_stamp)

    else:
        file_name = request.GET.get('file_name')
        # print('file_name')
        # print(file_name)
        file_path = os.path.join(BASE_DIR, 'media', file_name + ".xlsx")
        response = StreamingHttpResponse(file_iterator(file_path))  # 这里创建返回
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        response['Content-Disposition'] = 'attachment;filename="company_%s.xlsx"' % file_name
        # 注意filename 这个是下载后的名字
        # print(response)
        return response
