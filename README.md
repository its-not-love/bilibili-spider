# bilibili-spider
用爬虫在b站上找寻共同关注最多的基友，筛选同时关注ABCDup的用户。


# 同时关注ABCD的用户
打开一个视频右键检查，点击NETWORK，在FILTER中输入list.so获取视频oid,
在check_follow.py中把oid和up_id替换掉,
python check_follow.py即可。


# 找寻共同关注
在com_follow.py中把oid和yourid替换掉，
python com_follow.py即可。


# 生成词云
把record.txt清空，
python cloud.py即可。
