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
from chart.models import itoms_chg
from chart.models import itoms_para_mod


class HorBarChart:
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

    # 由于查询涉及到具体的工单字段，因此图类的方法需要按名称区分不同数据源的处理,而不是统一函数名称
    # 系统类工单数据, group by date
    def mk_sysitoms_gby_date(self, p_itoms_type):
        '''
        可以按系统区分的工单,group by date, itoms_type(if have more than one type such as 变更工单分为常规和紧急)
        也可以在函数内部对itoms_type进行重新映射,例如传入 sys,则把所有可以按系统区分的工单都包括进来.

        --date 作为x轴.
        --itoms_type 作为lengend
        :param itoms_type: 工单类型,可以是表里面具体的,也可以是组合抽象的,由代码决定
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        # self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s统计' % p_itoms_type

        # 查询当前要处理的数据集合，不做加工
        from django.db.models import Q
        if p_itoms_type == u'变更工单':
            query_set = itoms_count.objects \
                .filter(crt_date__gte=self.today_n_ago, crt_date__lte=self.today) \
                .filter(Q(itoms_type='常规变更') | Q(itoms_type='紧急变更'))
        else:
            query_set = itoms_count.objects \
                .filter(crt_date__gte=self.today_n_ago, crt_date__lte=self.today, itoms_type=p_itoms_type)

        # 根据当前数据集，找到所有legend分类数据
        query_legend = query_set.values('itoms_type').distinct().order_by('itoms_type')

        # 根据当前数据集，找到所有axis分类数据
        query_axis = query_set.values('crt_date').distinct().order_by('crt_date')

        # 根据当前数据集，生成group by 统计数据的所有集合
        query_group_by = query_set.values('crt_date', 'itoms_type') \
            .annotate(count_grp=Sum('count')).order_by('crt_date', 'itoms_type')

        for q in query_axis:
            self.xAxis_data.append(q['crt_date'])

        # 坐标维度长度确定,并以此作为legend数据第二维的长度
        axis_count = query_axis.count()
        self.xAxis_count = axis_count

        for legend_itom in query_legend:
            # 从legend开始遍历,填充数据
            self.legend_data.append(legend_itom['itoms_type'])

            # legend的第二维数组长度固定为坐标的维度长
            legend_axis = [0] * axis_count
            for index in range(axis_count):
                # 遍历每一个坐标值,并填入数据
                for grpby_itom in query_group_by:
                    if grpby_itom['crt_date'] == query_axis[index]['crt_date'] \
                            and grpby_itom['itoms_type'] == legend_itom['itoms_type']:
                        # index代表的系统属于当前的状态，则＋１
                        legend_axis[index] += grpby_itom['count_grp']

            sery_dict = {
                'name': legend_itom['itoms_type'],
                # 'type': 'bar',
                'type': 'line',
                # 'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': legend_axis
            }
            self.series.append(sery_dict)

        return self.get_dict_data()

    def mk_itoms_chg_gby_date(self, p_itoms_type):
        '''
        变更工单数据处理
        group by date, itoms_type(if have more than one type such as 变更工单分为常规和紧急)
        也可以在函数内部对itoms_type进行重新映射,例如传入 sys,则把所有可以按系统区分的工单都包括进来.

        --date 作为x轴.
        --itoms_type 作为lengend
        :param itoms_type: 工单类型,可以是表里面具体的,也可以是组合抽象的,由代码决定
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        # self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s统计' % p_itoms_type

        # 查询当前要处理的数据集合，不做加工
        from django.db.models import Q
        if p_itoms_type == u'变更工单':
            query_set = itoms_chg.objects \
                .filter(crt_date__gte=self.today_n_ago, crt_date__lte=self.today) \
                .filter(Q(itoms_type='常规变更') | Q(itoms_type='紧急变更'))
        else:
            query_set = itoms_chg.objects \
                .filter(crt_date__gte=self.today_n_ago, crt_date__lte=self.today, itoms_type=p_itoms_type)

        print query_set
        # 根据当前数据集，找到所有legend分类数据
        query_legend = query_set.values('itoms_type').distinct().order_by('itoms_type')

        # 根据当前数据集，找到所有axis分类数据
        query_axis = query_set.values('crt_date').distinct().order_by('crt_date')

        # 根据当前数据集，生成group by 统计数据的所有集合
        query_group_by = query_set.values('crt_date', 'itoms_type') \
            .annotate(count_grp=Sum('count')).order_by('crt_date', 'itoms_type')

        for q in query_axis:
            self.xAxis_data.append(q['crt_date'])

        # 坐标维度长度确定,并以此作为legend数据第二维的长度
        axis_count = query_axis.count()
        self.xAxis_count = axis_count

        for legend_itom in query_legend:
            # 从legend开始遍历,填充数据
            self.legend_data.append(legend_itom['itoms_type'])

            # legend的第二维数组长度固定为坐标的维度长
            legend_axis = [0] * axis_count
            for index in range(axis_count):
                # 遍历每一个坐标值,并填入数据
                for grpby_itom in query_group_by:
                    if grpby_itom['crt_date'] == query_axis[index]['crt_date'] \
                            and grpby_itom['itoms_type'] == legend_itom['itoms_type']:
                        # index代表的系统属于当前的状态，则＋１
                        legend_axis[index] += grpby_itom['count_grp']

            sery_dict = {
                'name': legend_itom['itoms_type'],
                # 'type': 'bar',
                'type': 'line',
                # 'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': legend_axis
            }
            self.series.append(sery_dict)

        return self.get_dict_data()

    def mk_table_w_type_g_date(self, table, p_itoms_type):
        '''
        变更工单数据处理
        group by date, itoms_type(if have more than one type such as 变更工单分为常规和紧急)
        也可以在函数内部对itoms_type进行重新映射,例如传入 sys,则把所有可以按系统区分的工单都包括进来.

        --date 作为x轴.
        --itoms_type 作为lengend
        :param itoms_type: 工单类型,可以是表里面具体的,也可以是组合抽象的,由代码决定
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        # self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s统计' % p_itoms_type

        # 查询当前要处理的数据集合，不做加工
        from django.db.models import Q
        if p_itoms_type == u'变更工单':
            query_set = table.objects \
                .filter(crt_date__gte=self.today_n_ago, crt_date__lte=self.today) \
                .filter(Q(itoms_type='常规变更') | Q(itoms_type='紧急变更'))
        elif p_itoms_type == u'参数修改':
            query_set = table.objects \
                .filter(crt_date__gte=self.today_n_ago, crt_date__lte=self.today) \
                .filter(Q(itoms_type='常规修改') | Q(itoms_type='紧急修改'))
        else:
            query_set = table.objects \
                .filter(crt_date__gte=self.today_n_ago, crt_date__lte=self.today, itoms_type=p_itoms_type)

        # print query_set
        # 根据当前数据集，找到所有legend分类数据
        query_legend = query_set.values('itoms_type').distinct().order_by('itoms_type')

        # 根据当前数据集，找到所有axis分类数据
        query_axis = query_set.values('crt_date').distinct().order_by('crt_date')

        # 根据当前数据集，生成group by 统计数据的所有集合
        query_group_by = query_set.values('crt_date', 'itoms_type') \
            .annotate(count_grp=Sum('count')).order_by('crt_date', 'itoms_type')

        for q in query_axis:
            self.xAxis_data.append(q['crt_date'])

        # 坐标维度长度确定,并以此作为legend数据第二维的长度
        axis_count = query_axis.count()
        self.xAxis_count = axis_count

        for legend_itom in query_legend:
            # 从legend开始遍历,填充数据
            self.legend_data.append(legend_itom['itoms_type'])

            # legend的第二维数组长度固定为坐标的维度长
            legend_axis = [0] * axis_count
            for index in range(axis_count):
                # 遍历每一个坐标值,并填入数据
                for grpby_itom in query_group_by:
                    if grpby_itom['crt_date'] == query_axis[index]['crt_date'] \
                            and grpby_itom['itoms_type'] == legend_itom['itoms_type']:
                        # index代表的系统属于当前的状态，则＋１
                        legend_axis[index] += grpby_itom['count_grp']

            sery_dict = {
                'name': legend_itom['itoms_type'],
                # 'type': 'bar',
                'type': 'line',
                # 'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': legend_axis
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
