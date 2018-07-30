# -*- coding: utf-8 -*- 
# @Time : 2018/6/27 13:13 
# @Author : Allen 
# @Site :  将数据插入数据库，阳历年月日，农历年月日，星期几，节假日，休息日

import pymysql

def connection():
    conn = pymysql.connect(host='localhost', port=3306,
                                  user='root', passwd='gzxiaoi', db='GZXIAOI', charset='utf8')
    return conn

def insert_db(data):
    conn = connection()
    cursor = conn.cursor()
    sql = '''
        INSERT INTO CALENDAR(YEAR,MONTH,DAY,LUNAR_YEAR,LUNAR_MONTH,LUNAR_DAY,WEEK,HOLIDAY,REST)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    try:
        cursor.executemany(sql,data)
        conn.commit()
    except Exception as e:
        print(e)
    else:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insert_db()
