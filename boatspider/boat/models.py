from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class SpiderInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="爬虫编号")
    project_name = models.CharField(max_length=20, verbose_name="scrapy项目名称")
    spider_name = models.CharField(max_length=20, verbose_name="scrapy爬虫名称")
    source_name = models.CharField(max_length=20, verbose_name="项目数据源命名")
    comname = models.CharField(max_length=30, verbose_name="公司网站名称")
    priority = models.BooleanField(max_length=20, verbose_name="是否支持优先级")
    cas_search = models.BooleanField(max_length=20, verbose_name="是否支持cas搜索")
    monitor = models.BooleanField(max_length=20, verbose_name="是否配置爬虫")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="项目第一次创建时间")
    remark = models.CharField(max_length=100, verbose_name="网站备注")
    link_source = models.ForeignKey('LinksSource', on_delete=models.CASCADE, verbose_name="链接数据源", blank=True,
                                    null=True)
    save_source = models.ForeignKey('SaveSource', on_delete=models.CASCADE, verbose_name="数据保存信息", blank=True,
                                    null=True)

    def __str__(self):
        return self.project_name

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        verbose_name_plural = u'Scrapy项目信息'
        indexes = [models.Index(fields=['project_name', 'spider_name', 'source_name'])]


class LinksSource(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="数据链接源编号")
    host = models.CharField(max_length=50, verbose_name="主机", default='127.0.0.1')
    port = models.CharField(max_length=10, verbose_name="端口号", default='27017')
    database_name = models.CharField(max_length=50, verbose_name="数据库名称", default='自定义')
    collection_name = models.CharField(max_length=50, verbose_name="数据库集合名称", default='自定义')
    field_name = models.CharField(max_length=50, verbose_name="链接字段名称", default='自定义')
    update_time = models.DateTimeField(auto_now=True, verbose_name="链接最后更新时间")
    spider_info = models.ForeignKey('SpiderInfo', on_delete=models.CASCADE, verbose_name="爬虫基本信息", blank=True,
                                    null=True)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        verbose_name_plural = u'Scrapy导入链接配置信息'
        indexes = [models.Index(fields=['database_name', 'collection_name', 'field_name'])]

    def __str__(self):
        return self.database_name


class SaveSource(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="数据链接源编号")
    host = models.CharField(max_length=50, verbose_name="主机", default='127.0.0.1')
    port = models.CharField(max_length=10, verbose_name="端口号", default='27017')
    database_name = models.CharField(max_length=50, verbose_name="数据库名称")
    collection_name = models.CharField(max_length=50, verbose_name="数据库集合名称")
    source_name = models.CharField(max_length=50, verbose_name="项目数据源命名")
    update_time = models.DateTimeField(auto_now=True, verbose_name="链接最后更新时间")
    spider_info = models.ForeignKey('SpiderInfo', on_delete=models.CASCADE, verbose_name="爬虫基本信息", blank=True,
                                    null=True)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        verbose_name_plural = u'Scrapy监控配置信息'
        indexes = [models.Index(fields=['database_name', 'collection_name', 'source_name'])]

    def __str__(self):
        return self.database_name


class DatabaseSource(models.Model):
    """
    部署数据库信息并关联爬虫
    """
    id = models.AutoField(primary_key=True, verbose_name="数据链接源编号")
    host = models.CharField(max_length=50, verbose_name="主机", default='127.0.0.1')
    port = models.CharField(max_length=10, verbose_name="端口号", default='27017')
    database_name = models.CharField(max_length=50, verbose_name="数据库名称", default='自定义')
    collection_name = models.CharField(max_length=50, verbose_name="数据库集合名称", default='自定义')
    create_time = models.DateTimeField(default=timezone.now, verbose_name="项目第一次创建时间")

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        verbose_name_plural = u'Scrapy数据库配置信息'
        indexes = [models.Index(fields=['host', 'database_name', 'collection_name'])]

    def __str__(self):
        return self.host


class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="用户编号")
    user = models.CharField(max_length=50, verbose_name="用户名", default='admin')
    pwd = models.CharField(max_length=10, verbose_name="密码", default='admin')
    create_time = models.DateTimeField(default=timezone.now, verbose_name="项目第一次创建时间")

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        verbose_name_plural = u'用户信息'
        indexes = [models.Index(fields=['user', 'pwd', ])]

    def __str__(self):
        return self.user
