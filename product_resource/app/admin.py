from django.contrib import admin
from .models import Property,Alias,User
# Register your models here.


class PropertyAdmin(admin.ModelAdmin):
    fields = ("pname","cas","specs","status","price","purity","source")  # 字段名
    list_display = ["ID","pname","cas","specs","status","price","purity","source",'source_url',"pickup_date"]  # 可显示字段名
    search_fields = ["pname","cas",'source']  # 可搜索字段名
    list_filter = ('source',)  # 筛选字段名
    pass

class AliasAdmin(admin.ModelAdmin):
    fields = ("pname","cas","falias","calias")
    list_display = ["ID","pname","cas","falias","calias","pickup_date"]
    search_fields = ["pname", "cas","falias","calias"]
    pass


class UserAdmin(admin.ModelAdmin):
    fields = ("uname", "pwd")
    list_display = ["uname", "pwd"]
    search_fields = ['uname']
    pass
admin.site.register(Property,PropertyAdmin)
admin.site.register(Alias,AliasAdmin)
admin.site.register(User, UserAdmin)

#修改网页title和站点header。
admin.site.site_title = "960化工网 产品信息管理"
admin.site.site_header = "产品信息管理"