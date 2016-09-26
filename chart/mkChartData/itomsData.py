#coding:utf-8
import sys
sys.path.append("../../")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ywreport.settings")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
import django
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


from chart.models import itoms_count
from django.db import connection

'''
获取itoms工单近一段时间的所有工单总量数据
'''
def impItomsHaveSys():
    #首先清空表中的内容，每次重新加载，不留历史记录，提高计算速度
    # itoms_count.objects.all().delete()
    # use below for the autoincrement not reset, but consider usefull at anywhere
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE `chart_itoms_count`")


    myfile=open('%s/file/itoms_testdatas.csv' % BASE_DIR)
    rowhead=myfile.readline()
    print rowhead
    for line in myfile:
        crt_date,itoms_type,sys_name,itoms_status,count=line.split('|+|')
        itoms_count.objects.create(
            crt_date=crt_date,
            itoms_type=itoms_type,
            sys_name=sys_name,
            itoms_status=itoms_status,
            count=int(count)
        )
    myfile.close()



