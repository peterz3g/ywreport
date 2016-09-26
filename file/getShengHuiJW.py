import re
import os
import shutil
import urllib.request
from urllib.request import Request, urlopen
 
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
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    #page = urllib.request.urlopen(url).read()
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
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    #page = urllib.request.urlopen(url).read()
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
            break #只取第一个城市
        else:
            print("    " + ls2[i] + " 已存在")
 
 
if __name__ == "__main__":
    #try:
    url = home
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    #page = urllib.request.urlopen(url).read()
    page = page.decode("gb2312")
     
    page = page.replace("\r\n", "")
    page = page.replace(" ", "")
    #ls = re.findall(re.compile('class="bredbotitle14">(.+?)</a><'), page)
    #ls = re.findall(re.compile('class="bredbotitle14">(.+?)</p>'), page)
    #匹配关键字含换行符
    ls = re.findall(re.compile('class="bredbotitle14">(.*\n.*\n.*)</a>'), page)
    #'山西省</p>\n<pclass="ulink">\n<ahref="kongzi.asp?id=3078">太原市'
    file = "log.txt"
    os.remove(file)
    
    for l in ls:
        i_s = l.find("<")
        s_I = l[:i_s]
        #s_I = l
        print("for 11111")
        print(s_I)
        if find_txt(file, s_I):
            print(">>>in find_txt")
            continue
	
        if s_I.find("?") >= 0:
            print("have ? %s",S_I)
            continue
	
         
        #s2 = l[i_s:] + "<"
        #ls2 = re.findall(re.compile('href="kongzi(.+?)<'), l)
        ls2 = re.findall(re.compile('href="kongzi(.+?)$'), l)
        #'.asp?id=3078">太原市'
        for l2 in ls2:
            print(l2)
            l2 = l2.replace('">', " ")
            ls3 = l2.split(" ")
            print(ls3)
            if l2 == "|" or l2.find(">") > 0:
                continue
            if len(ls3) != 2:
                continue
		
            f_p="kongzi"+ls3[0] 
            print("  " + ls3[1] + " " + f_p)
            s_II = ls3[1]
            
            if s_II.find("?") >= 0:
                print("in ? %s",S_II)
                continue
            dwon_city(s_I, s_II, "kongzi"+ls3[0])
        append_txt(file, s_I + "\n")
    #except:
    #    print("error!")
    print("finished!")
