import requests
from collections import defaultdict

# nowcoder: 在rank页找一下编号cookie
class node:
    rk = 0
    ac = 0
    time = 0

    def __init__(self, rk, ac, time):
        self.rk = rk
        self.ac = ac
        self.time = time

dict = defaultdict(list) #队伍映射

tot = 10  #比赛次数

url = r"" #设定爬取链接

for i in range(0, tot):
    response = requests.get(url.format(33186 + i))
    jsondata = response.json()
    name_list = []
    ac_list = []
    time_list = []
    rk_list = []
    for var in jsondata['data']['rankData']:
        name_list.append(var['userName'])
        ac_list.append(var['acceptedCount'])
        time_list.append(var['penaltyTime'])
        rk_list.append(var['ranking'])
    cnt = len(name_list)  #队伍人数
    for j in range(cnt):
        dict[name_list[j]].append(node(rk_list[j], ac_list[j],
                                       time_list[j]))  #添加队伍信息
    for key in dict.keys():
        if len(dict[key]) < i:
            dict[key].append(node(0, 0, 0))

# hdu: 登录才能查看rank页且有反爬虫需要用requests.session()