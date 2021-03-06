# coding:utf-8
from django.db import models
import os

os.environ.update({"DJANGO_SETTINGS_MODULE": "ywreport.settings"})


# Create your models here.
class itoms_count(models.Model):
    crt_date = models.CharField(max_length=16, default="20160101")
    itoms_type = models.CharField(max_length=256, default="itoms")
    sys_name = models.CharField(max_length=256, null=True)
    area_name = models.CharField(max_length=256, null=True)
    itoms_status = models.CharField(max_length=256, default="itoms")
    count = models.IntegerField(default=1)

    class Meta:
        index_together = [
            ["crt_date", "itoms_type"],
        ]

    def __unicode__(self):
        return 'crt_date=[%s], itoms_type=[%s], sys_name=[%s].' % (self.crt_date, self.itoms_type, self.sys_name)

#　变更工单定义
class itoms_chg(models.Model):
    crt_date = models.CharField(max_length=16, default="20160101")
    itoms_type = models.CharField(max_length=256, default="itoms")
    sys_name = models.CharField(max_length=256, null=True)
    itoms_status = models.CharField(max_length=256, default="itoms")
    emergency_reason = models.CharField(max_length=256, default="")
    count = models.IntegerField(default=1)

    class Meta:
        index_together = [
            ["crt_date"],
        ]

    def __unicode__(self):
        return 'crt_date=[%s], itoms_type=[%s], sys_name=[%s].' % (self.crt_date, self.itoms_type, self.sys_name)

#　参数修改工单定义
class itoms_para_mod(models.Model):
    crt_date = models.CharField(max_length=16, default="20160101")
    itoms_type = models.CharField(max_length=256, default="itoms")
    sys_name = models.CharField(max_length=256, null=True)
    mod_type = models.CharField(max_length=256, null=True)
    itoms_status = models.CharField(max_length=256, default="itoms")
    mod_reason = models.CharField(max_length=256, default="")
    count = models.IntegerField(default=1)

    class Meta:
        index_together = [
            ["crt_date"],
        ]

    def __unicode__(self):
        return 'crt_date=[%s], itoms_type=[%s], sys_name=[%s].' % (self.crt_date, self.itoms_type, self.sys_name)






