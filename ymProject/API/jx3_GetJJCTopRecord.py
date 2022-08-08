import asyncio

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

import pymysql

matplotlib.rc("font", family='PingFang HK')


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
    res_dict = res[0]
    res_total = dict(sorted(res_dict.items(), key=lambda x: x[1], reverse=True))
    del res_total["week"]
    return res_total


async def get_Figure(table, weekly):
    res = await get_JJCWeeklyRecord(table, weekly)
    if res is None:
        return None
    plt.figure(figsize=(20, 6))
    plt.title("推栏"+str(weekly) + "周JJC前200排名")
    for x, y in res.items():
        plt.text(x, y, '%.0f' % y, ha="center", va="bottom")
    bar_width = 0.3
    plt.bar(res.keys(), res.values(), width=bar_width)
    plt.savefig("/home/pycharm_project/ymProject/ym_bot/plugins/top.png")

