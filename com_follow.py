# -*- coding: utf-8 -*-
"""
Created on Thur Feb 27 17:34:20 2020
@author: wanghao
"""
import requests
import time
from bs4 import BeautifulSoup

CRCPOLYNOMIAL = 0xEDB88320
crctable = [0 for x in range(256)]

oid=152715431 #视频oid
yourid=103761777 #你的id

up_id=[]
user_hash =[]
user_hash1=[]
user_id=[]
result=[]

def get_hash():
    start_time = time.time()
    url="https://api.bilibili.com/x/v1/dm/list.so?oid="+str(oid)
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'api.bilibili.com',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    res = requests.get(url,head).content
    soup = BeautifulSoup(res, "html.parser")
    i=0
    for comment in soup.find_all('d'):
        user_hash.append(comment.attrs['p'].split(',')[6])
        i+=1
    end_time = time.time()
    user_hash1= set(user_hash)
    print("查询到" + str(i) + "条弹幕,"+str(len(user_hash1))+"个用户,"+f"耗时{round(end_time - start_time, 2)}秒")

def parse_id():
    user_hash1 = set(user_hash)
    print("正在解析hashcode")
    create_table()
    start_time = time.time()
    i=1
    size=len(user_hash1)
    for user in user_hash1:
        user_id.append(main(user))
        print("\r已解析到hashcode为".format(user) + str(user) + "的用户id,进度".format(i) + str(i)+"/".format(size) + str(size),end="")
        i+=1
    end_time = time.time()
    print("\n"+f"解析完成,耗时{round(end_time - start_time, 2)}秒")
def get_follow(mid=0,set=0):
    list=[]
    sum=0
    i = 0
    global user
    ref_url = "https://space.bilibili.com/"+str(mid)+"/#/fans/follow"
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'api.bilibili.com',
        'Pragma': 'no-cache',
        'Referer': ref_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    while 1:
        i += 1
        if i >= 6:
            break
        url = "https://api.bilibili.com/x/relation/followings?vmid=" + \
            str(mid)+"&pn="+str(i) + \
            "&ps=20&order=desc&jsonp=jsonp&callback=__jp5"
        try:
            r = requests.get(url, headers=head, timeout=10).text
            r2 = eval(r[6:-1].replace('null', 'None'))
            list1 = r2['data']['list']
            if list1 == []:
                break
            else:
                for user1 in list1:
                    if set==1:
                        up_id.append(user1["mid"])
                    elif user1["mid"] in up_id:
                        sum+=1
                        list.append(user1["uname"])
        except Exception as e:
            print(e)
    if set==0:
        temp=(mid,sum,list)
        result.append(temp)

def get_res():
    i = 1
    size = len(user_id)
    start_time = time.time()
    for mid in user_id:
        print("\r正在检查用户".format(mid) + str(mid) + "的关注列表,进度".format(i) + str(i) + "/".format(size)+ str(size),end="")
        get_follow(mid, 0)
        i += 1
    end_time = time.time()

    print("\n" + f"检查完成,耗时{round(end_time - start_time, 2)}秒")
    res = sorted(result, key=lambda x: (x[1]),reverse=True)
    file_handle = open('record.txt', mode='w')
    for r in res:
        print("------------------------------------------------------------------------------------------------------------------------------------------------")
        url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(r[0])
        zhuye = 'https://space.bilibili.com/' + str(r[0])
        jsondata = requests.get(url).json()['data']
        file_handle.write(jsondata['name']+' '+str(r[1])+'\n')
        print("你与[{}]有{}个共同关注:".format(jsondata['name'], r[1]),end="")
        for per in r[2]:
            print(per+'、',end="")
        print("\n主页:{}".format(zhuye))
#以下是解码部分
def create_table():
    for i in range(256):
        crcreg = i
        for _ in range(8):
            if (crcreg & 1) != 0:
                crcreg = CRCPOLYNOMIAL ^ (crcreg >> 1)
            else:
                crcreg = crcreg >> 1
        crctable[i] = crcreg

def crc32(string):
    crcstart = 0xFFFFFFFF
    for i in range(len(str(string))):
        index = (crcstart ^ ord(str(string)[i])) & 255
        crcstart = (crcstart >> 8) ^ crctable[index]
    return crcstart

def crc32_last_index(string):
    crcstart = 0xFFFFFFFF
    for i in range(len(str(string))):
        index = (crcstart ^ ord(str(string)[i])) & 255
        crcstart = (crcstart >> 8) ^ crctable[index]
    return index

def get_crc_index(t):
    for i in range(256):
        if crctable[i] >> 24 == t:
            return i
    return -1

def deep_check(i, index):
    string = ""
    tc=0x00
    hashcode = crc32(i)
    tc = hashcode & 0xff ^ index[2]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[2]] ^ (hashcode >>8)
    tc = hashcode & 0xff ^ index[1]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[1]] ^ (hashcode >> 8)
    tc = hashcode & 0xff ^ index[0]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[0]] ^ (hashcode >> 8)
    return [1, string]

def main(string):
    index = [0 for x in range(4)]
    i = 0
    ht = int(f"0x{string}", 16) ^ 0xffffffff
    for i in range(3,-1,-1):
        index[3-i] = get_crc_index(ht >> (i*8))
        snum = crctable[index[3-i]]
        ht ^= snum >> ((3-i)*8)
    for i in range(100000000):
        lastindex = crc32_last_index(i)
        if lastindex == index[3]:
            deepCheckData = deep_check(i, index)
            if deepCheckData[0]:
                break
    if i == 100000000:
        return -1
    return f"{i}{deepCheckData[1]}"
#以上是解码部分
if __name__ == "__main__":
    get_follow(yourid,1)
    get_hash()
    parse_id()
    get_res()
