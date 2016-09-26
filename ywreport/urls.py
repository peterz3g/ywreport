"""ywreport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # http views here
    url(r'^$', 'chart.views.chart_main', name='chart_main'),  # new
    url(r'^ec/$', 'chart.views.chart_main', name='chart_main'),  # new
    url(r'^chart_itoms.html/$', 'chart.views.chart_itoms', name='chart_itoms'),  # new
    url(r'^chart_patrol.html/$', 'chart.views.chart_patrol', name='chart_patrol'),  # new

    # http servers here like ajax
    url(r'^server_itoms/$', 'chart.servers.server_itoms', name='server_itoms'),  # new



    # test below---------------------------------------------------------------------------
    url(r'^weui_tabbar.html/$', 'chart.views.weui_tabbar', name='weui_tabbar'),  # new
    # url(r'^chart_itomstoms.html$', 'chart.views.chart_main', name='chart_main'),  # new

    url(r'^test1.html/$', 'chart.views.test1', name='test1'),  # new
    url(r'^test_a.html/$', 'chart.views.test_a', name='test_a'),  # new
    url(r'^impdb/$', 'chart.batTasks.dbImport.impMysqlData', name='impdb'),  # new

    url(r'^home.html/$', 'chart.views.home', name='home'),  # new
    # url(r'^staticnew/(?P<path>.*)$', 'django.views.staticnew.serve',{ 'document_root': settings.STATIC_URL }),
    url(r'^admin/', include(admin.site.urls)),
]
