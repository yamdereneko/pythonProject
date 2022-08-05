"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import pymysql


# 请求头
async def connect_Mysql(sql):
    try:
        db = pymysql.connect(host="localhost", user="root", password="Qinhao123.", database="farbnamen", charset="utf8")
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        db.commit()
        res = cursor.fetchall()
        db.close()
        return res
    except Exception as e:
        print(e)
        print("连接数据库异常")


async def get_JJCWeeklyRecord(table, weekly):
    sql = "select * from %s where week='%s'" % (table, weekly)
    res = await connect_Mysql(sql)
    return res
