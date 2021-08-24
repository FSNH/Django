from django.contrib import admin
from .models import SpiderInfo, SaveSource, LinksSource, User


# Register your models here.
class LinksSourceInline(admin.TabularInline):
    model = LinksSource
    fields = ('id', "host", "port", "database_name", 'collection_name', 'field_name')


class SaveSourceInline(admin.TabularInline):
    model = SaveSource
    fields = ('id', "host", "port", "database_name", 'collection_name', 'source_name')


#
class SpiderInfoAdmin(admin.ModelAdmin):
    # inlines = [LinksSourceInline,SaveSourceInline]
    fields = (
        "project_name", 'spider_name', 'source_name', 'comname', 'priority', 'cas_search', 'monitor', 'create_time',
        'remark')
    list_display = ["id", "project_name", 'spider_name', 'source_name', 'comname', 'priority', 'cas_search', 'monitor',
                    'create_time', 'remark']
    search_fields = ["project_name", 'spider_name', 'source_name', 'comname']


class LinksSourceAdmin(admin.ModelAdmin):
    # inlines = [SpiderInfoInline, ]
    fields = ("host", "port", "database_name", 'collection_name', 'field_name', 'spider_info', 'update_time')  # 可编辑的字段
    list_display = ['id', "host", "port", "database_name", 'collection_name', 'field_name', 'spider_info',
                    'update_time']
    # list_editable = ["database_name"]
    search_fields = ["database_name"]
    readonly_fields = ('update_time',)
    pass


class SaveSourceAdmin(admin.ModelAdmin):
    # inlines = [SpiderInfoInline, ]
    fields = ("host", "port", "database_name", 'collection_name', 'source_name', 'spider_info', 'update_time')  # 可编辑的字段
    list_display = ['id', "host", "port", "database_name", 'collection_name', 'source_name', 'spider_info',
                    'update_time']
    # list_editable = ["database_name"]
    search_fields = ["database_name"]
    readonly_fields = ('update_time',)
    pass


class UserAdmin(admin.ModelAdmin):
    fields = ("user", "pwd", 'create_time')  # 可编辑的字段
    list_display = ['id', "user", "pwd", 'create_time']
    search_fields = ["user"]


admin.site.register(SpiderInfo, SpiderInfoAdmin)
admin.site.register(SaveSource, SaveSourceAdmin)
admin.site.register(LinksSource, LinksSourceAdmin)
admin.site.register(User, UserAdmin)

admin.site.site_title = "Scrapy项目管理"
admin.site.site_header = "爬虫项目管理"
