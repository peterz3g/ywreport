# coding:utf-8
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
from chart.models import itoms_chg
from chart.models import itoms_para_mod
from django.db import connection
from django.http import HttpResponse


def impMysqlData(request):
    # 首先清空表中的内容，每次重新加载，不留历史记录，提高计算速度
    itoms_count.objects.all().delete()
    impItomsHaveSys()
    impItomsHaveArea()
    reload_itoms_chg()
    reload_itoms_para_mod()
    return HttpResponse("ok, finished.....")


'''
导入可以按系统区分的工单数据
如：变更工单，问题工单
'''


def impItomsHaveSys():
    # itoms_count.objects.all().delete()
    # use below for the autoincrement not reset, but consider usefull at anywhere
    # cursor = connection.cursor()
    # cursor.execute("TRUNCATE TABLE `chart_itoms_count`")


    myfile = open('%s/file/itom_chg20161002.csv' % BASE_DIR)
    # rowhead = myfile.readline()
    # print rowhead
    for line in myfile:
        crt_date, itoms_type, sys_name, itoms_status, count = line.split('|+|')
        itoms_count.objects.create(
            crt_date=crt_date.replace('-', ''),  # 保证日期为8位
            itoms_type=itoms_type,
            sys_name=sys_name,
            itoms_status=itoms_status,
            count=int(count)
        )
    myfile.close()


def impItomsHaveArea():
    # 首先清空表中的内容，每次重新加载，不留历史记录，提高计算速度
    # itoms_count.objects.all().delete()
    # use below for the autoincrement not reset, but consider usefull at anywhere
    # cursor = connection.cursor()
    # cursor.execute("TRUNCATE TABLE `chart_itoms_count`")


    myfile = open('%s/file/itom_xbankevent20161002.csv' % BASE_DIR)
    # rowhead = myfile.readline()
    # print rowhead
    for line in myfile:
        crt_date, itoms_type, brch_no, brch_name, sys_name, itoms_status, count = line.split('|+|')
        city_name = getBrchByNo(brch_no)
        itoms_count.objects.create(
            crt_date=crt_date.replace('-', ''),  # 保证日期为8位
            itoms_type=itoms_type,
            sys_name=sys_name,
            itoms_status=itoms_status,
            count=int(count),
            area_name=city_name
        )
    myfile.close()


def reload_itoms_chg():
    # itoms_count.objects.all().delete()
    # use below for the autoincrement not reset, but consider usefull at anywhere
    # cursor = connection.cursor()
    # cursor.execute("TRUNCATE TABLE `chart_itoms_count`")


    myfile = open('%s/file/itom_chg_new20161002.csv' % BASE_DIR)
    # rowhead = myfile.readline()
    # print rowhead
    itoms_chg.objects.all().delete()
    for line in myfile:
        crt_date, itoms_type, sys_name, itoms_status, emergency_reason, count = line.split('|+|')
        itoms_chg.objects.create(
            crt_date=crt_date.replace('-', ''),  # 保证日期为8位
            itoms_type=itoms_type,
            sys_name=sys_name,
            itoms_status=itoms_status,
            emergency_reason=emergency_reason,
            count=int(count)
        )
    myfile.close()


def reload_itoms_para_mod():
    # itoms_count.objects.all().delete()
    # use below for the autoincrement not reset, but consider usefull at anywhere
    # cursor = connection.cursor()
    # cursor.execute("TRUNCATE TABLE `chart_itoms_count`")


    myfile = open('%s/file/itom_para_mod20161002.csv' % BASE_DIR)
    # rowhead = myfile.readline()
    # print rowhead

    itoms_para_mod.objects.all().delete()
    for line in myfile:
        crt_date, itoms_type, sys_name, mod_type, itoms_status, mod_reason, count = line.split('|+|')
        itoms_para_mod.objects.create(
            crt_date=crt_date.replace('-', ''),  # 保证日期为8位
            itoms_type=itoms_type,
            sys_name=sys_name,
            mod_type=mod_type,
            itoms_status=itoms_status,
            mod_reason=mod_reason,
            count=int(count)
        )
    myfile.close()


def getBrchByNo(_brch_no):
    '''
    :param brch_no: 输入的4位机构号
    :return: 返回上级分行所在的城市名称
    '''
    brch_map = {
        '00': '总行',
        '01': '北京',
        '02': '上海',
        '03': '广州',
        '04': '烟台',
        '05': '武汉',
        '06': '大连',
        '07': '杭州',
        '08': '南京',
        '09': '太原',
        '10': '石家庄',
        '11': '重庆',
        '12': '西安',
        '13': '贵阳',
        '14': '常德',
        '15': '福州',
        '16': '济南',
        '17': '汕头',
        '18': '深圳',
        '19': '宁波',
        '20': '成都',
        '21': '天津',
        '22': '昆明',
        '23': '泉州',
        '24': '三亚',
        '25': '绍兴',
        '26': '苏州',
        '27': '青岛',
        '28': '温州',
        '29': '厦门',
        '30': '郑州',
        '31': '长沙',
        '32': '无锡',
        '33': '长春',
        '34': '合肥',
        '35': '南昌',
        '36': '邯郸',
        '37': '常州',
        '38': '镇江',
        '39': '吕梁',
        '40': '沧州',
        '41': '潍坊',
        '42': '曲靖',
        '43': '洛阳',
        '44': '衡阳',
        '45': '江门',
        '46': '中山',
        '47': '南阳',
        '48': '衡水',
        '49': '南通',
        '50': '襄阳',
        '51': '秦皇岛',
        '52': '大同',
        '53': '唐山',
        '54': '泰州',
        '55': '南宁',
        '56': '莆田',
        '57': '嘉兴',
        '58': '德阳',
        '59': '东营',
        '60': '红河',
        '61': '宜昌',
        '62': '株洲',
        '63': '宝鸡',
        '64': '呼和浩特',
        '65': '沈阳',
        '66': '总行',
        '67': '珠海',
        '68': '总行',
        '69': '总行',
        '70': '许昌',
        '71': '盐城',
        '72': '湘潭',
        '73': '淮安',
        '74': '吉林',
        '75': '台州',
        '76': '龙岩',
        '77': '马鞍山',
        '78': '上饶',
        '79': '临沂',
        '80': '徐州',
        '81': '赣州',
        '82': '威海',
        '83': '济宁',
        '84': '柳州',
        '85': '总行',
        '86': '金华',
        '87': '鄂尔多斯',
        '88': '总行',
        '89': '东莞',
        '98': '香港',
        '99': '总行',
        'A0': '拉萨',
        'A1': '揭阳',
        'A2': '舟山',
        'A3': '盘锦',
        'A4': '张家口',
        'A5': '浏阳',
        'A6': '哈尔滨',
        'A7': '上海',
        'A8': '兰州',
        'A9': '上海',
        'B1': '运城',
        'B2': '遵义',
        'B3': '宜宾',
        'B4': '宁德',
        'B5': '泰安',
        'B6': '新乡',
        'B7': '惠州',
        'B8': '乌鲁木齐',
        'B9': '总行',
        'C0': '银川',
        'C1': '葫芦岛',
        'C2': '宿迁',
        'C4': '漯河',
        'C6': '大庆',
        'C7': '西宁',
        'C8': '淄博',
        'C9': '日照',
    }
    f_city_id = _brch_no[0:2]
    return brch_map.get(f_city_id, '总行')
