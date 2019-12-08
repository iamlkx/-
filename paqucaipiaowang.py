import urllib.request
import re
import pandas as pd

# 定义一个爬虫函数
def jokeClawer(url):
    # 模拟一个请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }
    # 设置一个请求体
    req = urllib.request.Request(url, headers=headers)
    # 发起请求
    response = urllib.request.urlopen(req)
    # 保存数据
    data = response.read().decode("utf-8")
    # 返回得到的网页数据
    return data

# 分析爬取下来的网页，得到日期，前五位和后两位中奖数
def findValue(data):
    # 找日期
    pat1 = '<td class="Issue">(.*?)</td>'
    allDate = re.compile(pat1).findall(data)
    # 找前五位
    pat2 = '<td class="B_1(.*?)</td>'
    allAheadValue = re.compile(pat2).findall(data)
    # 找后两位
    pat3 = '<td class="B_5(.*?)</td>'
    allBehindValue = re.compile(pat3).findall(data)
    #print(len(allAheadValue))
    return allDate, allAheadValue, allBehindValue

# 定义一个函数，用于整合数据并写入文件
def writeTofile(allDate, allAheadValue, allBehindValue):
    # 建立一个空字符储存每一期的前五位中奖数
    list = []
    # 遍历整个正则表达式匹配出来的所有前五位中奖数
    for i in allAheadValue:
        # i为字符加数字，数字在后两位，所以用i[-2:]把数字提取出来
        # 利用append函数添加进列表中
        list.append(i[-2:])
    # 对后两位中奖数做相同操作
    list2 = []
    for i in allBehindValue:
        list2.append(i[-2:])
    # 下面步骤为整合数据，即每一期的期数、前五位号码、后两位号码，全部整合在一起形成：期数+号码
    # 设置一个空列表，用于存储数据
    list3 = []
    # 每次从allDate中拿出一个日期，直到拿完所有（即allDate为空）
    # 利用pop函数可以从列表中删除下标所对应的元素，并返回这个元素
    while allDate != []:
        # 把拿出的日期添加进list3中存储
        list3.append(allDate.pop(0))
        # list列表中的前五位为第一期的前五位号码，所以遍历五次
        for j in range(5):
            list3.append(list.pop(0))
        # list2列表中的前两位为第一期的前两位号码，所以遍历两次
        for k in range(2):
            list3.append(list2.pop(0))
    # 将所得全部期数+号码，写进dataFrame中，便于写入csv文件
    # 定义一个空的dataFrame
    test1 = pd.DataFrame()
    # 定义一个空的列表，用于存储数据作过渡作用
    list4 = []
    # 从list3列表中拿出一期又一期的数据，直到拿完为止
    while list3 != []:
        # list3每8位数据为每一期完整的数据：期数+号码
        for i in range(8):
            list4.append(list3.pop(0))
        # 上面得到的list4，为一期的完整数据：期数+号码
        name = [list4.pop(0)]
        test = pd.DataFrame(columns=name, data=list4)
        # 上面得到的test为一期数据的dataFrame形式
        # 接下来用test1接受每一期的完整的数据，从而形成一个包含所有期的数据的dataFrame
        test1[name] = test[name]
        # 将列表设置为空，再做过渡使用
        list4 = []
    # 将所有期的完美数据写入文件
    test1.to_csv(r"C:\Users\lkx\Desktop\daletou.csv", index=False)

# 定义主函数
def main():
    number = input("请输入你要查找的期数：")
    # 创建网页
    url = "https://chart.lottery.gov.cn//dltBasicKaiJiangHaoMa.do?typ=1&issueTop={}".format(number)
    # 爬取网页
    data = jokeClawer(url)
    # 解析数据
    allDate, allAheadValue, allBehindValue = findValue(data)
    # 写入文件
    writeTofile(allDate, allAheadValue, allBehindValue)

main()










