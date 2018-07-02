# -*- coding: utf-8 -*- 
# @Time : 2018/6/27 10:32 
# @Author : Allen 
# @Site :  导入caleader包，计算当日是否节假日或周末，是返回节假日

import calendar
import requests
import json
import time
import re
from calendar_db import insert_db

def week_day(data):
    data = data.split('-')
    weeks = calendar.monthcalendar(int(data[0]),int(data[1]))
    # print(weeks)
    for week in weeks:
        if int(data[2]) in week:
            return weeked(week.index(int(data[2])) + 1)
    else:
        return 'error'
#调用接口，3s一次 返回农历时间
def get_lunar(data):
    url = "https://www.sojson.com/open/api/lunar/json.shtml?date=%s"%(data)
    time.sleep(3)
    data_lunar = json.loads(requests.get(url).text)
    lunar_year = data_lunar['data']['lunarYear']
    lunar_month = data_lunar['data']['lunarMonth']
    lunar_day = data_lunar['data']['lunarDay']
    # print(data_lunar['data'])
    return lunar_year,lunar_month,lunar_day

def weeked(d):
    if d == 1:
        return "星期一"
    elif d == 2:
        return "星期二"
    elif d == 3:
        return "星期三"
    elif d == 4:
        return "星期四"
    elif d == 5:
        return "星期五"
    elif d == 6:
        return "星期六"
    elif d == 7:
        return "星期日"
    else:
        return "error"

def get_lunar_zw(data):
    url = "http://192.168.150.233:8080/id=" +data
    # print(url)
    # print(type(requests.get(url).text))
    data_string = requests.get(url).text
    data_string = data_string.split(' ')
    # print(data_string)
    lunar_year = data_string[0]
    lunar_month = data_string[1]
    lunar_day = data_string[2]
    holiday = ''.join(re.findall(r'[\u4e00-\u9fa5]',data_string[3]))
    # print(lunar_year+" "+holiday)
    return lunar_year,lunar_month,lunar_day,holiday

def demo():
    import datetime
    start = '2018-06-27'
    end = '2019-01-01'
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    data_list = []
    while datestart < dateend:
        rest = 0
        datestart += datetime.timedelta(days=1)
        day_string = datestart.strftime('%Y-%m-%d')
        days = day_string.split('-')
        # print(days)
        year = days[0]
        month = days[1]
        day = days[2]
        week = week_day(day_string)
        lunar_year, lunar_month, lunar_day,holiday = get_lunar_zw(day_string)
        if '六' in week or '日' in week:
            rest = 1
        elif '无' not in holiday:
            rest = 1
        data_list.append([str(year),str(month),str(day),week,str(lunar_year)+"年",\
                          str(lunar_month)+"月",str(lunar_day)+"日",holiday,str(rest)])

        print("阳历："+year+"-"+month+"-"+day+" "+week+" " +"农历："+str(lunar_year)+"-"+str(lunar_month)\
              +"-"+str(lunar_day)+" "+str(rest)+" holiday:"+holiday)
    print(data_list)
    insert_db(data_list)



if __name__ == '__main__':
    # day = week_day("2018-06-27")
    # print(day)
    # lunar_year,lunar_month,lunar_day = get_lunar("2018-06-27")
    # print("农历："+str(lunar_year)+"-"+str(lunar_month)+"-"+str(lunar_day))
    demo()
    # get_lunar_zw("2018-10-01")