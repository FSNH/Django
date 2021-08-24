import json
from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Count
from django.db.models import Q
from django.http.response import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from pyecharts.charts import Bar
from utils.db import RedisClient
from .check_login import check_login
from .form import LoginForm
from .models import Property, Alias, User
from pytz import timezone
from pyecharts.globals import CurrentConfig
# cdn加速pyecharts渲染加速
CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"


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


def logout(request):
    if not request.session.get('is_login', False):
        # 如果本来就未登录，也就没有登出一说
        return redirect("login.html")
    request.session.flush()
    return redirect("login.html")


@check_login
def index(request):
    """
    首页的规格信息
    :param request:
    :return:
    """
    # chart_count(request)
    if request.method == "GET":
        global queryset, pindex
        name = request.GET.get("pname", '')
        cas = request.GET.get("cas", '')
        source = request.GET.get("source", '')
        try:
            pindex = request.GET.get('page', 1)
        except PageNotAnInteger:
            pindex = 1
        if name or cas or source:
            s_field = [name, cas, source]
            s_filter = ["pname", "cas", "source"]
            s_data = []
            for i in zip(s_filter, s_field):
                s_data.append(i)
            kwargs = {u[0]: u[1] for u in s_data if u[1] != ''}
            # print(kwargs)
            # TODO:翻页带查询参数
            queryset = Property.objects.filter(**kwargs).order_by('-ID')
            k_sources = Property.objects.values('source').distinct()
            # print(k_sources )
            # print(queryset)
        else:
            queryset = Property.objects.all().order_by('-ID')
            k_sources = Property.objects.values('source').distinct()  # 去重获取产品来源
            # print(k_sources)

    paginator = Paginator(queryset, 20)  # 创建每页显示的数量实列
    page = paginator.page(pindex)  # 传递当前页的实例对象到前端
    page_nums = paginator.num_pages
    # print(page_nums)
    # return render(request, "index.html", {"page": page, "page_nums": page_nums,"k_source":k_sources})
    return render(request, "index.html", locals())


@check_login
def search(request):
    """
    支持名称cas号别名查询
    :param request:
    :return:
    """
    return render(request, "search.html")


@check_login
def m_search(request):
    """
    根据cas号批量采集
    :param request:
    :return:
    """
    data = request.POST.get('data', '')
    d = []
    if data:
        cass = data.split('\n')
        global queryset
        for name in cass:
            kwargs = {"cas": name.strip()}
            queryset = Property.objects.filter(**kwargs)
            if queryset:
                for i in queryset:
                    tmp = {}
                    tmp["id"] = i.ID
                    tmp["pname"] = i.pname
                    tmp["cas"] = i.cas
                    tmp["specs"] = i.specs
                    tmp["status"] = i.status
                    tmp["price"] = i.price
                    tmp["purity"] = i.purity
                    tmp["source"] = i.source
                    tmp["source_url"] = i.source_url
                    tmp["pickup_date"] = datetime_to_str(i.pickup_date)
                    tmp["message"] = "success"
                    d.append(tmp)
                    # print(d)
            else:
                tmp = {
                    "status": "fail",
                    "message": "没有查询到，请更换关键词重试！"
                }
    return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})


def datetime_as_timezone(date_time, time_zone):
    tz = timezone(time_zone)
    utc = timezone('UTC')
    return date_time.replace(tzinfo=utc).astimezone(tz)


def datetime_to_str(date_time):
    date_time_tzone = datetime_as_timezone(date_time, 'Asia/Shanghai')
    return '{0:%Y-%m-%d %H:%M}'.format(date_time_tzone)


@check_login
def getproperty(request):
    """
    规格信息接口
    :param request:
    :return:
    """
    if request.method == "POST":
        name = request.POST.get("data")
        # print(name)
        # 查询名称与cas号
        queryset = Property.objects.filter(Q(pname__contains=name) | Q(cas__contains=name))
        aliasqueryset = Alias.objects.filter(
            Q(falias__icontains=name) | Q(calias__icontains=name) | Q(calias__icontains=name))
        d = []
        if queryset:
            for i in queryset:
                tmp = {}
                tmp["id"] = i.ID
                tmp["pname"] = i.pname
                tmp["cas"] = i.cas
                tmp["specs"] = i.specs
                tmp["status"] = i.status
                tmp["price"] = i.price
                tmp["purity"] = i.purity
                tmp["source"] = i.source
                tmp["source_url"] = i.source_url
                tmp["pickup_date"] = datetime_to_str(i.pickup_date)
                tmp["message"] = "success"
                d.append(tmp)
            # print(d)
            return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})
        elif aliasqueryset:
            # print([i.pname for i in aliasqueryset])
            name = [i.pname for i in aliasqueryset][0]
            queryset = Property.objects.filter(Q(pname__contains=name) | Q(cas__contains=name))
            d = []
            if queryset:
                for i in queryset:
                    tmp = {}
                    tmp["id"] = i.ID
                    tmp["pname"] = i.pname
                    tmp["cas"] = i.cas
                    tmp["specs"] = i.specs
                    tmp["status"] = i.status
                    tmp["price"] = i.price
                    tmp["purity"] = i.purity
                    tmp["source"] = i.source
                    tmp["source_url"] = i.source_url
                    tmp["pickup_date"] = datetime_to_str(i.pickup_date)
                    tmp["message"] = "success"
                    d.append(tmp)
                # print(d)
                return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                tmp = {
                    "status": "failed",
                    "message": "请检查参数"
                }
                d.append(tmp)
                return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            tmp = {
                "status": "failed",
                "message": "请检查参数"
            }
            d.append(tmp)
            return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})


@check_login
def getalias(request):
    """
    别名信息接口
    :param request:
    :return:
    """
    if request.method == "GET":
        queryset = Alias.objects.all()
        d = []
        for i in queryset:
            tmp = {}
            tmp["id"] = i.ID
            tmp["pname"] = i.pname
            tmp["cas"] = i.cas
            tmp["falias"] = i.falias
            tmp["calias"] = i.calias
            tmp["code"] = "success"
            d.append(tmp)
        # print(d)
        return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        alia = request.POST.get("data")
        queryset = Alias.objects.filter(Q(falias__icontains=alia) | Q(calias__icontains=alia))
        d = []
        for i in queryset:
            tmp = {}
            tmp["id"] = i.ID
            tmp["pname"] = i.pname
            tmp["cas"] = i.cas
            tmp["falias"] = i.falias
            tmp["calias"] = i.calias
            tmp["code"] = "success"
            d.append(tmp)
        # print(d)
        return JsonResponse(d, safe=False, json_dumps_params={'ensure_ascii': False})


@check_login
def analysis(request):
    """
    数据展示页面
    :param request:
    :return:
    """
    chart_count(request)
    return render(request, 'analysis.html')


# @check_login
def chart_count(request):
    """
    聚合查询来源的数据量
    :param request:
    :return:
    """
    source = Property.objects.values_list('source').distinct()  # 去重获取数据源
    x_data = []
    y_data = []
    for s in source:
        x_data.append(s[0])
        s_types = Property.objects.filter(source=s[0]).aggregate(Count('cas'))  # 聚合查询每个来源的数据量
        y_data.append(s_types.get('cas__count'))
    # print(x_data,y_data)
    bar = Bar()
    bar.add_xaxis(x_data)
    bar.add_yaxis("产品总量", y_data, category_gap='80%', bar_width=30)
    bar.render(r"F:\pythongit\product_resource\templates\charts.html")
    return render(request, "charts.html")

@check_login
def save_url_redis(request):
    # TODO:前端通过ajax将待采集的数据存入redis队列
    if request.method == "POST":
        data = request.POST.get('data', '')
        result = data.split(';')  # 获取ajax传输的数据
        info = {
            'cas': result[0].strip(),
            'source': result[1].strip(),
            'url': result[2].strip()
        }
        client = RedisClient()
        client.pub_info(json.dumps(info))  # 存入redis
        # print(info)
        return JsonResponse(info)
        pass

