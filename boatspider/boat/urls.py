from django.urls import path, re_path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('login.html', views.login, name='login'),  # 登录
    path('logout.html', views.logout, name='logout'),  # 退出
    # re_path(r'^$', views.index),  # 首页
    path('index.html', views.index, name='index'),  # 首页
    path('monitor.html', views.monitor, name='monitor'),  # 监控配置
    path('convert.html', views.convert, name='convert'),  # 监控配置
    url(r'scrapyinfo/(\w+).html', views.project_detail, name='project_detail'),  # 爬虫详情
    path('api/spiders/', views.scrapy_info, name="scrapy_info"),  # 爬虫项目基本信息查询接口
    path('api/monitors/', views.monitor_info, name="monitor_info"),  # 爬虫监控信息查询接口
    path('api/links/', views.load_data, name='load_data'),  # 爬虫待采集数据源查询接口
    path('api/search/', views.search, name="search"),  # 分布式爬虫调度接口
    url(r'istrue/(\w+)', views.istrue, name='istrue'),  # 配置爬虫可用
    url(r'isdelete/(\w+)', views.isdelete, name='isdelete'),  # 配置爬虫不可用
    url(r'api/search_cas/', views.all_cas, name='cas_search')  # cas号采集
]
