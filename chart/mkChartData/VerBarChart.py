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


class VerBarChart:
    """
    echart 垂直分布的柱状图, 数据集合与数据生成
    类变量命名规范：从echart配置项开始，逐级append参数名称，并用下划线相连．
    如：series_data; series_data_label_normal_show 等．
    """
    PERIOD_DAYS = 30  # 展示两周１４天的数据

    def __init__(self):
        self.title_text = ''
        self.legend_data = []
        self.yAxis_data = []  # 垂直柱状图的坐标是反的
        self.yAxis_count = 0  # 垂直柱状图的坐标,展示多少数据
        self.series = []
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.today_n_ago = (datetime.datetime.now() - datetime.timedelta(days=self.PERIOD_DAYS)).strftime("%Y%m%d")
        self.selected_date = ''

    def mk_itoms_by_date(self, itoms_type, date):
        '''
        由于查询涉及到具体的工单字段，因此图类的方法需要按名称区分不同数据源的处理,而不是统一函数名称
        查询生成某类工单，某天的统计数据
        :param itoms_type: 由上一级传递进来的工单类型
        :param date: 由上一级传递进来的查询日期
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s按系统排名' % itoms_type

        # 查询当前要处理的数据集合，不做加工
        query_set = itoms_count.objects \
            .filter(crt_date=self.selected_date, itoms_type=itoms_type) \
            .exclude(sys_name='(null)')

        # 根据当前数据集，找到所有工单状态,作为legend分类数据
        query_itoms_status = query_set.values('itoms_status').distinct().order_by('itoms_status')

        # 根据当前数据集，生成对工单的统计数据
        query_count_by_sys_stat = query_set.values('sys_name', 'itoms_status') \
            .annotate(count_grp=Sum('count')).order_by('sys_name', 'itoms_status')

        # 根据当前数据集，生成对工单的统计数据; 单独按系统排名是为了得到从高到低的顺序
        query_count_total = query_set.values('sys_name') \
            .annotate(count_grp=Sum('count')).order_by('count_grp')

        # 根据系统总量排名，遍历数据集，生成展示数据．
        for q in query_count_total:
            self.yAxis_data.append(q['sys_name'])

        # 数据集确定后，状态维度的长度固定，系统类型维度的长度固定．即每一个系统都要有这几个状态，没有时补０．
        # 可以先按维度初始化，然后遍历系统，有则＋１计数．
        sys_count = query_count_total.count()
        self.yAxis_count = sys_count

        for q in query_itoms_status:
            self.legend_data.append(q['itoms_status'])

            # 每个状态维度都初始化固定系统长度值
            sys_list = [0] * sys_count
            for index in range(sys_count):
                # 遍历系统，并填充Ｙ坐标的数据.
                for sys in query_count_by_sys_stat:
                    if sys['sys_name'] == query_count_total[index]['sys_name'] and sys['itoms_status'] == q[
                        'itoms_status']:
                        # index代表的系统属于当前的状态，则＋１
                        sys_list[index] += sys['count_grp']

            sery_dict = {
                'name': q['itoms_status'],
                'type': 'bar',
                'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': sys_list
            }
            self.series.append(sery_dict)

        return self.get_dict_data()

    def mk_itoms_chg_by_date(self, itoms_type, date):
        '''
        由于查询涉及到具体的工单字段，因此图类的方法需要按名称区分不同数据源的处理,而不是统一函数名称
        查询生成某类工单，某天的统计数据
        :param itoms_type: 由上一级传递进来的工单类型
        :param date: 由上一级传递进来的查询日期
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s按系统排名' % itoms_type

        # 查询当前要处理的数据集合，不做加工
        query_set = itoms_count.objects \
            .filter(crt_date=self.selected_date, itoms_type=itoms_type) \
            .exclude(sys_name='(null)')

        # 根据当前数据集，找到所有工单状态,作为legend分类数据
        query_itoms_status = query_set.values('itoms_status').distinct().order_by('itoms_status')

        # 根据当前数据集，生成对工单的统计数据
        query_count_by_sys_stat = query_set.values('sys_name', 'itoms_status') \
            .annotate(count_grp=Sum('count')).order_by('sys_name', 'itoms_status')

        # 根据当前数据集，生成对工单的统计数据; 单独按系统排名是为了得到从高到低的顺序
        query_count_total = query_set.values('sys_name') \
            .annotate(count_grp=Sum('count')).order_by('count_grp')

        # 根据系统总量排名，遍历数据集，生成展示数据．
        for q in query_count_total:
            self.yAxis_data.append(q['sys_name'])

        # 数据集确定后，状态维度的长度固定，系统类型维度的长度固定．即每一个系统都要有这几个状态，没有时补０．
        # 可以先按维度初始化，然后遍历系统，有则＋１计数．
        sys_count = query_count_total.count()
        self.yAxis_count = sys_count

        for q in query_itoms_status:
            self.legend_data.append(q['itoms_status'])

            # 每个状态维度都初始化固定系统长度值
            sys_list = [0] * sys_count
            for index in range(sys_count):
                # 遍历系统，并填充Ｙ坐标的数据.
                for sys in query_count_by_sys_stat:
                    if sys['sys_name'] == query_count_total[index]['sys_name'] and sys['itoms_status'] == q[
                        'itoms_status']:
                        # index代表的系统属于当前的状态，则＋１
                        sys_list[index] += sys['count_grp']

            sery_dict = {
                'name': q['itoms_status'],
                'type': 'bar',
                'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': sys_list
            }
            self.series.append(sery_dict)

        return self.get_dict_data()

    def mk_itoms_chg_Ysys_Lstatus_by_date_reason(self, itoms_type, date, emergency_reason):
        '''
        变更工单，Ｙ轴为ＳＹＳ，ｌｅｇｅｎｄ为状态，过滤日期和紧急变更原因
        :param itoms_type: 由上一级传递进来的工单类型
        :param date: 由上一级传递进来的查询日期
        :param date: 由上一级传递进来的变更原因
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s按系统排名' % itoms_type

        # 查询当前要处理的数据集合，不做加工
        query_set = itoms_chg.objects \
            .filter(crt_date=self.selected_date,
                    itoms_type=itoms_type,
                    emergency_reason=emergency_reason)
            # .exclude(sys_name='(null)')

        # 根据当前数据集，找到所有工单状态,作为legend分类数据
        query_itoms_status = query_set.values('itoms_status').distinct().order_by('itoms_status')

        # 根据当前数据集，生成对工单的统计数据
        query_count_by_sys_stat = query_set.values('sys_name', 'itoms_status') \
            .annotate(count_grp=Sum('count')).order_by('sys_name', 'itoms_status')

        # 根据当前数据集，生成对工单的统计数据; 单独按系统排名是为了得到从高到低的顺序
        query_count_total = query_set.values('sys_name') \
            .annotate(count_grp=Sum('count')).order_by('count_grp')

        # 根据系统总量排名，遍历数据集，生成展示数据．
        for q in query_count_total:
            self.yAxis_data.append(q['sys_name'])

        # 数据集确定后，状态维度的长度固定，系统类型维度的长度固定．即每一个系统都要有这几个状态，没有时补０．
        # 可以先按维度初始化，然后遍历系统，有则＋１计数．
        sys_count = query_count_total.count()
        self.yAxis_count = sys_count

        for q in query_itoms_status:
            self.legend_data.append(q['itoms_status'])

            # 每个状态维度都初始化固定系统长度值
            sys_list = [0] * sys_count
            for index in range(sys_count):
                # 遍历系统，并填充Ｙ坐标的数据.
                for sys in query_count_by_sys_stat:
                    if sys['sys_name'] == query_count_total[index]['sys_name'] and sys['itoms_status'] == q[
                        'itoms_status']:
                        # index代表的系统属于当前的状态，则＋１
                        sys_list[index] += sys['count_grp']

            sery_dict = {
                'name': q['itoms_status'],
                'type': 'bar',
                'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': sys_list
            }
            self.series.append(sery_dict)

        return self.get_dict_data()

    # 20161015 created by zhangyang32
    def mk_itoms_para_mod_w_date_type_reason_Lstatus_Ysys_server(self, date, itoms_type, reason):
        '''
        变更工单，Ｙ轴为ＳＹＳ，ｌｅｇｅｎｄ为状态，过滤日期和紧急变更原因
        :param itoms_type: 由上一级传递进来的工单类型
        :param date: 由上一级传递进来的查询日期
        :param date: 由上一级传递进来的变更原因
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s按系统排名' % itoms_type
        legend = 'itoms_status'
        yaxis = 'sys_name'

        # 查询当前要处理的数据集合，不做加工
        query_set = itoms_para_mod.objects \
            .filter(crt_date=self.selected_date,
                    itoms_type=itoms_type,
                    mod_reason=reason)
            # .exclude(sys_name='(null)')

        # 根据当前数据集，找到所有工单状态,作为legend分类数据
        query_itoms_status = query_set.values(legend).distinct().order_by(legend)

        # 根据当前数据集，生成对工单的统计数据
        query_count_by_sys_stat = query_set.values(yaxis, legend) \
            .annotate(count_grp=Sum('count')).order_by(yaxis, legend)

        # 根据当前数据集，生成对工单的统计数据; 单独按系统排名是为了得到从高到低的顺序
        query_count_total = query_set.values(yaxis) \
            .annotate(count_grp=Sum('count')).order_by('count_grp')

        # 根据系统总量排名，遍历数据集，生成展示数据．
        for q in query_count_total:
            self.yAxis_data.append(q[yaxis])

        # 数据集确定后，状态维度的长度固定，系统类型维度的长度固定．即每一个系统都要有这几个状态，没有时补０．
        # 可以先按维度初始化，然后遍历系统，有则＋１计数．
        sys_count = query_count_total.count()
        self.yAxis_count = sys_count

        for q in query_itoms_status:
            self.legend_data.append(q[legend])

            # 每个状态维度都初始化固定系统长度值
            sys_list = [0] * sys_count
            for index in range(sys_count):
                # 遍历系统，并填充Ｙ坐标的数据.
                for sys in query_count_by_sys_stat:
                    if sys[yaxis] == query_count_total[index][yaxis] and sys[legend] == q[legend]:
                        # index代表的系统属于当前的状态，则＋１
                        sys_list[index] += sys['count_grp']

            sery_dict = {
                'name': q[legend],
                'type': 'bar',
                'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': sys_list
            }
            self.series.append(sery_dict)

        return self.get_dict_data()

    def mk_itoms_chg_Ysys_Lstatus_by_date(self, itoms_type, date):
        '''
        变更工单，Ｙ轴为ＳＹＳ，ｌｅｇｅｎｄ为状态，过滤日期和紧急变更原因
        :param itoms_type: 由上一级传递进来的工单类型
        :param date: 由上一级传递进来的查询日期
        :return:返回python字典，由外部进行返回前端时的json转换
        '''

        self.selected_date = date  # 当前选中日期,格式同源数据库，字符串保存
        # self.title_text = '%s按系统排名' % itoms_type
        self.title_text = u'%s按系统排名' % itoms_type

        # 查询当前要处理的数据集合，不做加工
        query_set = itoms_chg.objects \
            .filter(crt_date=self.selected_date,
                    itoms_type=itoms_type) \
            .exclude(sys_name='(null)')

        # 根据当前数据集，找到所有工单状态,作为legend分类数据
        query_itoms_status = query_set.values('itoms_status').distinct().order_by('itoms_status')

        # 根据当前数据集，生成对工单的统计数据
        query_count_by_sys_stat = query_set.values('sys_name', 'itoms_status') \
            .annotate(count_grp=Sum('count')).order_by('sys_name', 'itoms_status')

        # 根据当前数据集，生成对工单的统计数据; 单独按系统排名是为了得到从高到低的顺序
        query_count_total = query_set.values('sys_name') \
            .annotate(count_grp=Sum('count')).order_by('count_grp')

        # 根据系统总量排名，遍历数据集，生成展示数据．
        for q in query_count_total:
            self.yAxis_data.append(q['sys_name'])

        # 数据集确定后，状态维度的长度固定，系统类型维度的长度固定．即每一个系统都要有这几个状态，没有时补０．
        # 可以先按维度初始化，然后遍历系统，有则＋１计数．
        sys_count = query_count_total.count()
        self.yAxis_count = sys_count

        for q in query_itoms_status:
            self.legend_data.append(q['itoms_status'])

            # 每个状态维度都初始化固定系统长度值
            sys_list = [0] * sys_count
            for index in range(sys_count):
                # 遍历系统，并填充Ｙ坐标的数据.
                for sys in query_count_by_sys_stat:
                    if sys['sys_name'] == query_count_total[index]['sys_name'] and sys['itoms_status'] == q[
                        'itoms_status']:
                        # index代表的系统属于当前的状态，则＋１
                        sys_list[index] += sys['count_grp']

            sery_dict = {
                'name': q['itoms_status'],
                'type': 'bar',
                'stack': '总量',
                'label': {
                    'normal': {
                        # 'show': 'true',
                        'position': 'insideRight'
                    }
                },
                'data': sys_list
            }
            self.series.append(sery_dict)

        return self.get_dict_data()

    def get_dict_data(self):
        result = {
            'title_text': self.title_text,
            'legend_data': self.legend_data,
            'yAxis_data': self.yAxis_data,
            'yAxis_count': self.yAxis_count,
            'series': self.series,
        }
        return result
