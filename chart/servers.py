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
from django.core.serializers import json

'''
ajax请求统一接口
工单相关请求,接受两个参数：
１，chart_type：说明图表类型，决定有哪些参数
２，itoms_type：说明工单类型，决定如何初始化参数
'''


def server_itoms(request):
    # 函数路由表，取代switch case的方法
    func_route = {
        'line': line_chart_server,
        'ver_bar': ver_bar_chart_server,
        'hor_bar': hor_bar_chart_server,
        'geo': geo_chart_server,
        'pie': pie_chart_server,
        # 'pie': pie_chart_server,
    }
    # return func_route[request.GET['chart_type']](request.GET['itoms_type'])
    return func_route.get(request.GET['chart_type'], line_chart_server(request))(request)


def line_chart_server(request):
    itoms_type = request.GET['itoms_type']
    chg_line = LineChart()
    result = chg_line.mk_itoms_chg_data()
    return JsonResponse(result)


def ver_bar_chart_server(request):
    itoms_type = request.GET['itoms_type']
    itoms_date = request.GET['itoms_date']
    chart = VerBarChart()
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


def pie_chart_server(request):
    # print "geo_chart_server...."
    itoms_type = request.GET['itoms_type']
    itoms_date = request.GET['itoms_date']
    chart = PieChart()
    result = chart.mk_itoms_chg_by_date_gby_reason(itoms_type, itoms_date)
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
