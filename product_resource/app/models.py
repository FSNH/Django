from django.db import models

# Create your models here.

s_choice = (
    ('Mce', "Mce"),
    ('xlsw', '西利生物')
)


class Property(models.Model):
    ID = models.AutoField(primary_key=True)  # 产品id
    pname = models.CharField(max_length=500, verbose_name="产品名称", db_index=True)  # 产品名称
    cas = models.CharField(max_length=100, verbose_name="cas号", db_index=True)  # 产品cas号
    specs = models.CharField(max_length=100, verbose_name="产品规格", null=True, db_index=True)  # 产品规格
    status = models.CharField(max_length=800, verbose_name="产品状态", null=True, db_index=True)  # 产品状态
    price = models.CharField(max_length=100, verbose_name="产品价格", null=True, db_index=True)  # 产品价格
    purity = models.CharField(max_length=100, verbose_name="产品纯度", null=True, db_index=True)  # 产品纯度
    source_url = models.CharField(max_length=400, verbose_name="产品链接", db_index=True)  # 产品链接
    source = models.CharField(max_length=100, verbose_name="产品来源", choices=s_choice, db_index=True)  # 产品来源
    pickup_date = models.DateTimeField(auto_now_add=True, verbose_name="采集时间", db_index=True)  # 产品采集时间

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误u
        verbose_name_plural = u'产品规格'
        indexes = [models.Index(fields=['pname', 'cas', 'source']),models.Index(fields=['cas', 'source', 'specs', 'source_url', 'purity'])]


    def __str__(self):
        return self.pname


class Alias(models.Model):
    ID = models.AutoField(primary_key=True)  # 产品id
    pname = models.CharField(max_length=100, verbose_name="产品名称")  # 产品名称
    cas = models.CharField(max_length=100, verbose_name="cas号")  # 产品cas号
    falias = models.CharField(max_length=100, verbose_name="英文别名")
    calias = models.CharField(max_length=100, verbose_name="中文别名")
    pickup_date = models.DateTimeField(auto_now_add=True, verbose_name="采集时间")  # 产品采集时间

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误
        verbose_name_plural = u'产品别名'
        indexes = [models.Index(fields=['pname', 'cas', 'falias', 'calias'])]

    def __str__(self):
        return self.pname


class User(models.Model):
    """
    用户库
    """
    ID = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=20, unique=True, db_index=True)
    pwd = models.CharField(max_length=20)

    class Meta:
        # 末尾不加s
        # 中文前加u进行编码否则报编码错误u

        verbose_name_plural = u'用户'
        indexes = [models.Index(fields=['uname'])]

    def __str__(self):
        return self.uname

    pass
