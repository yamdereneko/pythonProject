import asyncio
import os

import matplotlib
import matplotlib.pyplot as plt
import nonebot
import pymysql
import pymysql.cursors
import dufte

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
        return None


async def get_JJCWeeklyRecord(table, weekly):
    sql = "select * from %s where week='%s'" % (table, weekly)
    res = await connect_Mysql(sql)
    res_dict = res[0]
    tuples = sorted(res_dict.items(), key=lambda x: x[1], reverse=True)
    res_total = dict(tuples)
    del res_total["week"]
    return res_total


async def get_JJCWeeklySchoolRecord(table: str, school: str):
    sql = "select week,%s from %s " % (school, table)
    res = await connect_Mysql(sql)
    return res


async def get_Figure(table, weekly):
    res = await get_JJCWeeklyRecord(table, weekly)
    if res is None:
        return None
    plt.style.use(dufte.style)
    fig, ax = plt.subplots(figsize=(18, 10), facecolor='white', edgecolor='white')
    ax.set_title("推栏" + str(weekly) + "周JJC前200排名", fontsize=18)
    for x, y in res.items():
        plt.text(x, y, '%.0f' % y, ha="center", va="bottom")
    bar_width = 0.3
    ax.bar(res.keys(), res.values(), width=bar_width)
    plt.savefig(f"/tmp/top{weekly}.png")


async def get_plot(table, school):
    if os.path.exists(f"/tmp/top{school}.png"):
        nonebot.logger.info(school + "JJC趋势图已经存在")
    else:
        res = await get_JJCWeeklySchoolRecord(table, school)
        plt.style.use(dufte.style)
        fig, ax = plt.subplots(figsize=(20, 10), facecolor='white', edgecolor='white')
        # plt.title("推栏" + str(school) + "JJC前200趋势图")
        if res is None:
            return None
        x = []
        y = []
        # plt.xlabel('周', fontsize=16)
        # plt.ylabel('数量', fontsize=16)
        ax.set_xlabel('周', fontsize=16)
        ax.set_ylabel('数量', fontsize=16)
        ax.set_title("推栏" + str(school) + "JJC前200趋势图", fontsize=18)
        for data in res:
            x.append(data["week"])
            y.append(data[school])
            plt.text(data["week"], data[school], '%.0f' % data[school], ha="center", va="bottom")
        ax.plot(x, y, "o-", color='#607d8b')
        plt.savefig(f"/tmp/top{school}.png")
        nonebot.logger.info(school + "JJC趋势图重新创建")
