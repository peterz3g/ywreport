# coding:utf-8
import re
import os
import shutil
#import urllib2.request
import urllib, urllib2
 
home = "http://jingwei.supfree.net"
 
def find_txt(file, s):
    b_find = False
    if os.path.exists(file):
        f = open(file, "r")
        ls_txt = f.readlines()
        f.close()     
         
        for l in ls_txt:
            if l.find(s) >= 0:
                b_find = True
                break
    return b_find
 
def append_txt(file, s):
    f = open(file, "a")
    f.write(s)
    f.close()    
 
def getjw(p2):
    url = home + "/" + p2
    #page = urllib.request.urlopen(url).read()
    page = urllib.urlopen(url).read()
    try:
        page = page.decode("gb2312")   
    except:
        try:
            page = page.decode("gbk")
        except:
            page = page.decode("utf-8")
    ls = re.findall(re.compile('botitle18">(.+?)<'), page)
    if len(ls) == 2:
        return ls[0].strip(" "), ls[1].strip(" ")
 
 
def dwon_city(s_I, s_II, p):
    file = "jingwei.txt"
    url = home + "/" + p
    #page = urllib.request.urlopen(url).read()
    page = urllib.urlopen(url).read()
    try:
        page = page.decode("gb2312")   
    except:
        try:
            page = page.decode("gbk")
        except:
            page = page.decode("utf-8")
     
    ls1 = re.findall(re.compile('href="(mengzi\.asp.+?)"'), page)
    ls2 = re.findall(re.compile('经纬度">(.+?)</a'), page)
    #print(len(ls1))
    #print(len(ls2))
    for i in range(len(ls1)):
        #print("        " + ls2[i] + " " + ls1[i])
        if not find_txt(file, s_I + " " + s_II + " " + ls2[i]):
            (j, w) = getjw(ls1[i])
            print("    " + ls2[i] + " " + j + " " + w)
            s3 = s_I + " " + s_II + " " + ls2[i] + " " + j + " " + w + "\n"
            append_txt(file, s3)
        else:
            print("    " + ls2[i] + " 已存在")
 
 
if __name__ == "__main__":
    #try:
    url = home
    #page = urllib.request.urlopen(url).read()
    page = urllib.urlopen(url).read()
    #page = page.decode("gb2312")
    page = page.decode("utf-8")
     
    page = page.replace("\r\n", "")
    page = page.replace(" ", "")
    ls = re.findall(re.compile('class="bredbotitle14">(.+?)</a><'), page)
    print(len(ls))
    file = "log.txt"
     
    for l in ls:
        i_s = l.find("<")
        s_I = l[:i_s]
        print(s_I)
        if find_txt(file, s_I):
            continue
         
        s2 = l[i_s:] + "<"
        ls2 = re.findall(re.compile('href="(.+?)<'), s2)
        for l2 in ls2:
            l2 = l2.replace('">', " ")
            ls3 = l2.split(" ")
            #if l2 == "|" or l2.find(">") > 0:
            #    continue
            if len(ls3) != 2:
                continue
            print("  " + ls3[1] + " " + ls3[0])
            s_II = ls3[1]
            if s_II.find("?") >= 0:
                continue
             
            dwon_city(s_I, s_II, ls3[0])
        append_txt(file, s_I + "\n")
    #except:
    #    print("error!")
    print("finished!")
