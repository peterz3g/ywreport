# coding:utf-8
'''
折线图类，生成折线展现时需要的数据
'''

import datetime
import sys

from django.db.models import Sum

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


class LineChart:
    """
    echart 折线图数据集合与数据生成
    类变量命名规范：从echart配置项开始，逐级append参数名称，并用下划线相连．
    如：series_data; series_data_label_normal_show 等．
    """
    PERIOD_DAYS = 1000  # 展示两周１４天的数据

    def __init__(self):
        self.title_text = ''
        self.legend_data = []
        self.xAxis_data = []
        self.series_data = []
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.today_n_ago = (datetime.datetime.now() - datetime.timedelta(days=self.PERIOD_DAYS)).strftime("%Y%m%d")

    def mk_itoms_chg_data(self):
        self.title_text='变更工单统计'
        self.legend_data=['常规变更']
        query_set = itoms_count.objects.filter(crt_date__gte=self.today_n_ago,
                                               crt_date__lte=self.today,
                                               itoms_type='常规变更') \
            .values('crt_date').order_by('crt_date') \
            .annotate(count_by_date=Sum('count'))

        for q in query_set:
            self.xAxis_data.append(q['crt_date'])
            self.series_data.append(q['count_by_date'])

        return self.get_dict_data()

    def get_dict_data(self):
        result = {
            'title_text': self.title_text,
            'legend_data': self.legend_data,
            'xAxis_data': self.xAxis_data,
            'series_data': self.series_data,
        }
        return result


