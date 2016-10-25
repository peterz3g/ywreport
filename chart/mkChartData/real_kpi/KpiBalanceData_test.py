# coding:utf-8
'''
折线图类，生成折线展现时需要的数据
'''

import datetime
import random
import sys
import math

from django.db.models import Sum

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ywreport.settings")
# base_dir/chart/mkChartDate/real_kpi = 4 dirname
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
import django

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


class KpiBalanceData:
    """
    20161009:此类主要在于生成水平系列图，bar,line,其实都是可以相互转化的．
    echart 水平分布图, 数据集合与数据生成
    类变量命名规范：从echart配置项开始，逐级append参数名称，并用下划线相连．
    如：series_data; series_data_label_normal_show 等．

    """
    PERIOD_DAYS = 30  # 展示两周１４天的数据

    def __init__(self):
        self.title_text = ''
        self.legend_data = []
        self.xAxis_data = []  # 水平柱状图的坐标是反的
        self.xAxis_count = 0  # 水平柱状图的坐标,展示多少数据
        self.series = []
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.today_n_ago = (datetime.datetime.now() - datetime.timedelta(days=self.PERIOD_DAYS)).strftime("%Y%m%d")
        self.selected_date = ''

    def mk_data_today_by_random(self, start=0):
        '''
        --date 作为x轴.
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        now_h = int(datetime.datetime.now().strftime("%H"))
        now_m = int(datetime.datetime.now().strftime("%M"))
        print "%s:%s" % (now_h, now_m)

        start = now_h * 60 + now_m

        # self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'分时图'
        # 设置横坐标的值,已在前端实现,不再传递
        # for i in range(24):
        #     hour = "%d" % i
        #     for j in range(60):
        #         min = "%d" % j
        #         time = "%s:%s" % (hour, min)
        #         self.xAxis_data.append(time)

        series_data_by_legend = []
        # series_data_by_legend.append({'name': '00:00', 'value': 100})
        # series_data_by_legend.append({'name': '00:30', 'value': 200})
        # series_data_by_legend.append({'name': '12:30', 'value': 500})
        # series_data_by_legend.append({'name': '23:30', 'value': 0})

        # 读取现有数据
        for i in range(start-1):
            series_data_by_legend.append(250 * math.sin(0.01 * i))

        series_data_by_legend.append(250 * math.sin(0.01 * i))

        nowlen = len(series_data_by_legend)
        for i in range(1440 - nowlen):
            series_data_by_legend.append('-')

        sery_dict = {
            'name': 'balance',
            # 'type': 'bar',
            'type': 'line',
            # 'stack': '总量',
            'label': {
                'normal': {
                    # 'show': 'true',
                    'position': 'insideRight'
                }
            },
            'data': series_data_by_legend
        }
        self.series.append(sery_dict)

        return self.get_dict_data()


    def mk_data_day_by_random(self, ndays=0):
        '''
        --date 作为x轴.
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        now_h = int(datetime.datetime.now().strftime("%H"))
        now_m = int(datetime.datetime.now().strftime("%M"))
        print "%s:%s" % (now_h, now_m)

        start = now_h * 60 + now_m

        # self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'按日历史'
        # 设置横坐标的值,已在前端实现,不再传递
        # for i in range(24):
        #     hour = "%d" % i
        #     for j in range(60):
        #         min = "%d" % j
        #         time = "%s:%s" % (hour, min)
        #         self.xAxis_data.append(time)

        series_data_by_legend = []
        # series_data_by_legend.append({'name': '00:00', 'value': 100})
        # series_data_by_legend.append({'name': '00:30', 'value': 200})
        # series_data_by_legend.append({'name': '12:30', 'value': 500})
        # series_data_by_legend.append({'name': '23:30', 'value': 0})

        # 读取现有数据
        ndays=int(ndays)
        for i in range(ndays):
            series_data_by_legend.append(250 * math.sin(0.01 * i))

        sery_dict = {
            'name': 'balance',
            # 'type': 'bar',
            'type': 'line',
            # 'stack': '总量',
            'label': {
                'normal': {
                    # 'show': 'true',
                    'position': 'insideRight'
                }
            },
            'data': series_data_by_legend
        }
        self.series.append(sery_dict)

        return self.get_dict_data()

    def get_dict_data(self):
        result = {
            'title_text': self.title_text,
            'legend_data': self.legend_data,
            'xAxis_data': self.xAxis_data,
            'xAxis_count': self.xAxis_count,
            'series': self.series,
        }

        return result
