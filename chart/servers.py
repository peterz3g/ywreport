# coding:utf-8
'''
for web services like ajax request
html page is responsed by views.py
'''

from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

# Create your servers here.
from chart.mkChartData.GeoChart import GeoChart
from chart.mkChartData.LineChart import LineChart
from chart.mkChartData.PieChart import PieChart
from chart.mkChartData.VerBarChart import VerBarChart
from chart.mkChartData.HorBarChart import HorBarChart
from chart.mkChartData.real_kpi.KpiBalanceData_test import KpiBalanceData
from django.core.serializers import json

from chart.models import itoms_count
from chart.models import itoms_chg
from chart.models import itoms_para_mod

'''
ajax请求统一接口
工单相关请求,接受两个参数：
１，chart_type：说明图表类型，决定有哪些参数
２，params：说明请求参数
'''


def server_itoms(request):
    # 函数路由表，取代switch case的方法
    # 路由命名规范: 图类型_表名_where_条件字段_附属说明,如:pie_itoms_chg_where_data_type_sys_Lstatus
    # 路由关键字:ver_itoms_para_mod_w_date_type_reason_Lstatus_Ysys
    # 路由服务:ver_itoms_para_mod_w_date_type_reason_Lstatus_Ysys_server
    # make方法:图表类.mk_itoms_chg_Ysys_Lstatus_by_date_reason
    # 路由注释提供数据格式说明
    func_route = {
        'ver_bar': ver_bar_chart_server,
        'hor_bar': hor_bar_chart_server,
        'geo': geo_chart_server,
        'pie': pie_chart_server,
        'pie_test': pie_test_server,
        # none
        'hor_balance_today': hor_balance_today_server,
        # itoms_type
        'hor_Xdate_Litype': hor_chart_server,
        # selected_date|itoms_type|emergency_reason
        'ver_Ysys_Lstatus_by_date': ver_Ysys_Lstatus_by_date_server,
        # selected_date|itoms_type|emergency_reason
        'ver_Ysys_Lstatus_by_date_reason': ver_chart_server,
        # selected_date|itoms_type|mod_reason
        'ver_itoms_para_mod_w_date_type_reason_Lstatus_Ysys': ver_itoms_para_mod_w_date_type_reason_Lstatus_Ysys_server,
        # selected_date|itoms_type
        'pie_LemgcReasons_by_date': pie_chart_server,
        # selected_date|itoms_type|sys_name
        'pie_itoms_chg_where_data_type_sys_Lstatus': pie_itoms_chg_where_data_type_sys_Lstatus_server,
        # selected_date|itoms_type
        'pie_itoms_para_mod_w_date_type_Lreason': pie_itoms_para_mod_w_date_type_Lreason_server,
    }
    # return func_route[request.GET['chart_type']](request.GET['itoms_type'])
    # print request.GET['chart_type']
    return func_route.get(request.GET['chart_type'], pie_test_server(request))(request)


def hor_chart_server(request):
    params = request.GET['params']
    itoms_type = params.split('|')
    chart = HorBarChart()
    if u"变更" in itoms_type[0]:
        result = chart.mk_table_w_type_g_date(itoms_chg, itoms_type[0])
    elif u"修改" in itoms_type[0]:
        result = chart.mk_table_w_type_g_date(itoms_para_mod, itoms_type[0])
    else:
        result = chart.mk_sysitoms_gby_date(itoms_type[0])
    return JsonResponse(result)


def hor_balance_today_server(request):
    # print "hor_balance_today_server..."
    params = request.GET['params']
    values = params.split('|')
    chart = KpiBalanceData()
    if "test" in values[0]:
        print "test:hor_balance_today_server..."
        result = chart.mk_data_today_by_random(values[1])
    else:
        result = chart.mk_data_today_by_random(values[1])
    return JsonResponse(result)


def ver_chart_server(request):
    chart_type = request.GET['chart_type']
    params = request.GET['params']
    selected_date, itoms_type, emergency_reason = params.split('|')
    chart = VerBarChart()
    result = chart.mk_itoms_chg_Ysys_Lstatus_by_date_reason(itoms_type, selected_date, emergency_reason)
    return JsonResponse(result)


def ver_Ysys_Lstatus_by_date_server(request):
    params = request.GET['params']
    selected_date, itoms_type = params.split('|')
    chart = VerBarChart()
    result = chart.mk_itoms_chg_Ysys_Lstatus_by_date(itoms_type, selected_date)
    return JsonResponse(result)


def ver_itoms_para_mod_w_date_type_reason_Lstatus_Ysys_server(request):
    params = request.GET['params']
    # print params
    selected_date, itoms_type, mod_reason = params.split('|')
    chart = VerBarChart()
    result = chart.mk_itoms_para_mod_w_date_type_reason_Lstatus_Ysys_server(selected_date, itoms_type, mod_reason)
    return JsonResponse(result)


def pie_chart_server(request):
    print "pie_chart_server...."

    chart_type = request.GET['chart_type']
    params = request.GET['params']
    selected_date, itoms_type = params.split('|')
    chart = PieChart()
    result = chart.mk_itoms_chg_LemgcReasons_by_date(itoms_type, selected_date)
    print result
    # f = open('/static/json/china.json')
    # result = json.load(f)
    return JsonResponse(result)
    # return HttpResponse('hello')
    # return JsonResponse('/static/json/china.json')


def pie_itoms_chg_where_data_type_sys_Lstatus_server(request):
    params = request.GET['params']
    selected_date, itoms_type, sys_name = params.split('|')
    chart = PieChart()
    result = chart.mk_itoms_chg_where_data_type_sys(itoms_type, selected_date, sys_name, "itoms_status")
    return JsonResponse(result)


def pie_itoms_para_mod_w_date_type_Lreason_server(request):
    params = request.GET['params']
    selected_date, itoms_type = params.split('|')
    chart = PieChart()
    result = chart.mk_pie_itoms_para_mod_w_date_type_Lreason(itoms_type, selected_date)
    return JsonResponse(result)


def pie_test_server(request):
    # params = request.GET['params']
    # print type(params)
    # print params
    result = {'retparams': "this is test"}
    return JsonResponse(result)


def ver_bar_chart_server(request):
    itoms_type = request.GET['itoms_type']
    itoms_date = request.GET['itoms_date']
    chart = VerBarChart()
    if u"变更" in itoms_type:
        result = chart.mk_itoms_chg_by_date(itoms_type, itoms_date)
        # print "1111111111111"
    else:
        result = chart.mk_itoms_by_date(itoms_type, itoms_date)
    return JsonResponse(result)


def hor_bar_chart_server(request):
    itoms_type = request.GET['itoms_type']
    chart = HorBarChart()
    # if itoms_type==u"变更工单" or itoms_type==u""
    # print type(itoms_type)
    if u"变更" in itoms_type:
        result = chart.mk_itoms_chg_gby_date(itoms_type)
        # print "1111111111111"
    else:
        result = chart.mk_sysitoms_gby_date(itoms_type)
    return JsonResponse(result)


def geo_chart_server(request):
    # print "geo_chart_server...."
    itoms_type = request.GET['itoms_type']
    itoms_date = request.GET['itoms_date']
    chart = GeoChart()
    result = chart.mk_Areaitoms_gby_type_date(itoms_type, itoms_date)
    # f = open('/static/json/china.json')
    # result = json.load(f)
    return JsonResponse(result)
    # return HttpResponse('hello')
    # return JsonResponse('/static/json/china.json')


def server_itoms_test(request):
    a = request.GET.get('a', 0)
    b = request.GET.get('b', 0)
    c = int(a) + int(b)
    # return HttpResponse({c:str(c)})
    a = range(100)
    return JsonResponse({'a': a})
    # return JsonResponse({'c':str(c)})


def test_a(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    # return HttpResponse({c:str(c)})
    a = range(100)
    return JsonResponse({'a': a})
    # return JsonResponse({'c':str(c)})


def home(request):
    return render(request, 'mouti_pages.html')
