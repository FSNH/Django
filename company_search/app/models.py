from django.db import models

# Create your models here.


class Company(models.Model):
    """
    企业名称库
    """
    ID = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200, verbose_name="公司名称")
    update_time = models.DateField(auto_created=True)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        verbose_name_plural = u'公司名称库'
        indexes = [models.Index(fields=['company_name'])]

    pass

class Company_info(models.Model):
    """
    企业信息库
    """
    ID = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, verbose_name="公司名称")
    link_person = models.CharField(max_length=100, verbose_name="联系人", blank=True)
    telephone = models.CharField(max_length=100, verbose_name="固话", blank=True)
    mobile = models.CharField(max_length=100, verbose_name="手机", blank=True)
    qq = models.CharField(max_length=100, verbose_name="qq号", blank=True)
    email = models.CharField(max_length=100, verbose_name="邮箱", blank=True)
    address = models.CharField(max_length=255, verbose_name="公司地址", blank=True)
    product_num = models.CharField(max_length=100, verbose_name="产品数量", blank=True)
    company_type = models.CharField(max_length=100, verbose_name="公司类型", blank=True)
    scope = models.CharField(max_length=500, verbose_name="主营产品", blank=True)
    cooperate_years = models.CharField(max_length=50, verbose_name="合作年限", blank=True)
    source = models.CharField(max_length=100, verbose_name="数据源网站")
    source_url = models.CharField(max_length=100, verbose_name="数据源网站链接")
    update_time = models.DateField(auto_now=True)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        ordering = ("-product_num",)
        verbose_name_plural = u'公司信息详情'
        indexes = [models.Index(fields=['company_name', 'source'])]

    pass

class User(models.Model):
    """
    用户库
    """
    ID = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=20, unique=True)
    pwd = models.CharField(max_length=20)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误

        verbose_name_plural = u'用户'
        indexes = [models.Index(fields=['uname'])]

    pass

class Ptinfo(models.Model):
    """
    平台数据信息库
    """
    ID = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, verbose_name="公司名称")
    pt_num = models.CharField(max_length=100, verbose_name="平台数据源数量", blank=True)
    pt_sources = models.CharField(max_length=255, verbose_name="平台数据源")
    product_num_max = models.CharField(max_length=100, verbose_name="最大产品数", blank=True)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        ordering = ["-pt_num"]
        verbose_name_plural = u'平台统计信息'
        indexes = [models.Index(fields=['company_name'])]

    pass

class UserMonitor(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="用户名", blank=True)
    IP=models.CharField(max_length=100, verbose_name="IP地址", blank=True)
    localtime = models.CharField(max_length=100, verbose_name="访问时间", blank=True)
    address = models.CharField(max_length=100, verbose_name="访问地址", blank=True)
    views = models.IntegerField(verbose_name='次数',blank=True,default=0)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        ordering = ["-localtime"]
        verbose_name_plural = u'平台访问信息'
        indexes = [models.Index(fields=['name'])]
    def __str__(self):
        return self.IP

    def viewed(self):
        self.views += 1 # 访问量
        self.save(update_fields=['views'])

class Chem960VipCompany(models.Model):
    ID = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=100, verbose_name="公司名称", blank=True)
    create_time= models.DateTimeField(auto_now_add=True)  # 创建时间
    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        ordering = ["-create_time"]
        verbose_name_plural = u'Chem960Vip'
        indexes = [models.Index(fields=['companyname'])]
    def __str__(self):
        return self.companyname