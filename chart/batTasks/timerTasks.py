#coding:utf-8
'''
这是一个批量调用的主程序，在ｓｅｔｔｉｎｇ中配置触发
'''

import time
import os
import dbImport
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def impFiles2DB():
    todayNow=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print '>>>today is: %s' % todayNow
    print '>>>__file__: %s' % __file__
    print '>>>__name__: %s' % __name__
    print '>>>path: %s' % BASE_DIR

def dbImpFromFiles():
    todayNow=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print '>>>today is: %s' % todayNow
    print '>>exec impItomsHaveSys...'
    dbImport.impItomsHaveSys()
    print '>>exec impItomsHaveSys finished!'




