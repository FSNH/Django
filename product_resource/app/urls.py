from django.urls import path, re_path

from . import views

urlpatterns = [
    path('login.html', views.login, name='login'),  # 登录
    path('logout.html', views.logout, name='logout'),  # 退出
    path('index.html', views.index, name="index"),  # 首页
    path('search.html', views.search, name="search"),  # 搜索
    path('analysis.html', views.analysis, name='analysis'),  # 数据统计
    path('api/getproperty/', views.getproperty, name="property"),  # 查询接口
    path('api/getalias/', views.getalias, name="alias"),  # 查询别名接口
    path('api/m_search/', views.m_search, name="m_search"),  # 批量查询接口
    path('api/chart_count/', views.chart_count, name="chart_count"),  # 数据统计柱状图接口
    path('api/save_url_redis/', views.save_url_redis, name='save_url_redis'),  # 更新数据接口
]
