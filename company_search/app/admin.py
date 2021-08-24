import datetime
from django.contrib import admin
from utils import export_excel
from .models import Company, Company_info, User, Ptinfo, UserMonitor, Chem960VipCompany
import os

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    fields = ("company_name",)
    list_display = ["ID", "company_name", "update_time"]
    search_fields = ["company_name"]

    def save_execl(self, request, queryset):

        filename = r'media/{0}_{1}.xls'.format('CompanyNameInfo', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        headers = [
            'ID', '公司名', '更新时间']
        columns = ['ID', "company_name", "update_time"]
        return export_excel.export_excel(queryset, headers, columns, filename)

    save_execl.short_description = "导出Excel"
    actions = [save_execl]
    pass


class CompanyinfoAdmin(admin.ModelAdmin):
    fields = (
        "company_name", "link_person", "telephone", "mobile", "qq", "email", "address", "company_type", "product_num",
        "scope", "cooperate_years", "source",)
    list_display = ["ID", "company_name", "link_person", "telephone", "mobile", "qq", "email", "address",
                    "company_type", "product_num", "scope", "cooperate_years", "source", "update_time"]
    search_fields = ["company_name", "link_person", "company_type", "product_num", "source"]
    list_filter = ('source',)  # 筛选字段名

    def save_execl(self, request, queryset):

        filename = r'media/{0}_{1}.xls'.format('CompanyInfo', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        headers = [
            'ID', '公司名', '联系人', '电话', '手机', 'qq', '邮箱', '地址', '贸易类型', '产品总数', '经营范围', '合作年限', '平台名']
        columns = ["ID", "company_name", "link_person", "telephone", "mobile", "qq", "email", "address",
                   "company_type", "product_num", "scope", "cooperate_years", "source"]
        return export_excel.export_excel(queryset, headers, columns, filename)

    save_execl.short_description = "导出Excel"
    actions = [save_execl]
    pass


class UserAdmin(admin.ModelAdmin):
    fields = ("uname", "pwd")
    list_display = ["uname", "pwd"]
    search_fields = ['uname']
    pass


class PtinfoAdmin(admin.ModelAdmin):
    fields = ("company_name", "pt_num", "product_num_max", "pt_sources")
    list_display = ["company_name", "pt_num", "product_num_max", "pt_sources"]
    list_display_links = ["company_name"]
    search_fields = ['company_name']

    def save_execl(self, request, queryset):
        filename = r'media/{0}_{1}.xls'.format('PtInfo', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        headers = [
            'ID', '公司名', '合作平台数', '最大产品数', '合作平台']
        columns = ["company_name", "pt_num", "product_num_max", "pt_sources"]
        return export_excel.export_excel(queryset, headers, columns, filename)

    save_execl.short_description = "导出Excel"
    actions = [save_execl]
    pass


class UserMonitorAdmin(admin.ModelAdmin):
    fields = ("ID", "name", "IP", "address", "localtime", "views")
    list_display = ["ID", "name", "IP", "address", "localtime", "views"]
    list_display_links = ["name"]
    search_fields = ['name']

    def save_execl(self, request, queryset):
        filename = r'media/{0}_{1}.xls'.format('UserMonInfo', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        headers = [
            'ID', '用户名', 'IP地址', '访问地址', '访问时间', '总访问量']
        columns = ["ID", "name", "IP", "address", "localtime", "views"]
        return export_excel.export_excel(queryset, headers, columns, filename)

    save_execl.short_description = "导出Excel"
    actions = [save_execl]
    pass


class Chem960VipCompanyAdmin(admin.ModelAdmin):
    fields = ("companyname",)
    list_display = ["ID", "companyname", "create_time"]
    list_display_links = ["ID", "companyname"]
    search_fields = ['companyname']

    def save_execl(self, request, queryset):
        filename = r'media/{0}_{1}.xls'.format('ChemVipInfo', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        headers = [
            'ID', '公司名', "更新时间"]
        columns = ["ID", "companyname", "create_time"]
        return export_excel.export_excel(queryset, headers, columns, filename)

    save_execl.short_description = "导出Excel"
    actions = [save_execl]
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Company_info, CompanyinfoAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Ptinfo, PtinfoAdmin)
admin.site.register(UserMonitor, UserMonitorAdmin)
admin.site.register(Chem960VipCompany, Chem960VipCompanyAdmin)

# 修改网页title和站点header。
admin.site.site_title = "960化工网 企业信息管理"
admin.site.site_header = "企业信息管理"
