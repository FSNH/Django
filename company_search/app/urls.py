from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login.html', views.login, name='login'),  # 登录
    path('logout.html', views.logout, name='logout'),  # 退出
    path('index.html', views.index, name='index'),  # 首页，平台统计信息
    path('search.html', views.search, name='search'),  # 检索信息
    path('detail.html', views.getdetail, name='getdetail'),  # 平台企业联系信息
    path('company.html', views.getcompanyname, name='getcompanyname'),  # 企业名称库
    path('cdetail.html', views.company_detail, name='company_detail'),  # 企业详细信息
    # path('api/getcomany/', views.getcompany, name='getcompany'),
    path('api/searchapi/', views.searchapi, name='searchapi'),  # 模糊搜索api
    path('api/m_searchAip/', views.m_searchAip, name='m_searchAip'),  # 批量搜索api
    # path('api/getcalcua_data/', views.getcalcu_data, name='getcalcu_data'),
    path('api/get_ip/', views.get_ip, name='getip'),  # 用户访问记录
    path('api/check_chem960vip/', views.check_chem960vip, name='check_chem960vip'),  # 用户访问记录
    path('api/totals/', views.chem960_click_nums, name='chem960_click_nums'),  # 平台点击量接口获取一个cas号
    path('total.html', views.chem960, name='chem960'),  # cas号点击量获取
    path('api/m_totals/', views.m_chem960_click_nums, name='m_chem960_click_nums'),  # 平台点击量接口获取多个cas号
    path('api/pm_totals/', views.pm_chem960_nums, name="pm_chem960_nums"),
    path('api/verify/', views.cas_verify_get, name='cas_verify_get'),  # 校验cas号并且返回chemicalbook结果
    path('verify.html', views.verify, name='verify'),
    # 公司点击路由
    path('api/c_totals/', views.comid_chem960_nums, name='comid_chem960_nums'),  # 公司id获取点击量
    path('cid_total.html', views.company_search, name='company_search'),  # 公司搜索
    path('api/ajax_download/', views.download_booking_API, name="download_booking_API"),  # 下载接口
    path('api/ajax_cas_download/', views.download_casinfoing_API, name="download_casinfoing_API"),  # 下载cas接口
]
