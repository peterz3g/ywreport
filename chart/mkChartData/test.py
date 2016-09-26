# coding:utf-8
import json

from LineChart import LineChart
from VerBarChart import VerBarChart
from HorBarChart import HorBarChart

# lc = LineChart()
# lc = VerBarChart()
# lc = HorBarChart()
from chart.mkChartData.GeoChart import GeoChart

lc = GeoChart()
# mystr = lc.mk_itoms_by_date('常规变更', '2016-06-28')
mystr = lc.mk_Areaitoms_gby_type_date(u'Xbank事件工单','20160701')
print mystr['series_data_mtop']
# pstr=json.load(mystr)
