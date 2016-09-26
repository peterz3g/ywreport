#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def chart_main(request):
    # return render(request, 'home.html')
    # return render(request, 'home_bs_demo.html')
    return render(request, 'chart_main.html')
    # return render(request, 'home_weui.html')

def weui_tabbar(request):
    return render(request, 'weui_tabbar.html')

def chart_itoms(request):
    return render(request, 'chart_itoms.html')

def chart_patrol(request):
    return render(request, 'chart_patrol.html')

def test1(request):
    return render(request, 'test_itoms_chart.html')

def test2(request):
    return render(request, 'test_itoms_patrol.html')

def test_a(request):
    a=request.GET['a']
    b=request.GET['b']
    c = int(a) + int(b)
    # return HttpResponse({c:str(c)})
    a = range(100)
    return JsonResponse({'a':a})
    # return JsonResponse({'c':str(c)})

def home(request):
    # return render(request, 'home.html')
    # return render(request, 'home_bs_demo.html')
    # return render(request, 'wsgi.py')
    return HttpResponse(u"欢迎光临 自强学堂!")
    # return "<p>text</p>"
    # return render(request, 'mouti_pages.html')
