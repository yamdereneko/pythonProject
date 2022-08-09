# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import time
from time import gmtime
import matplotlib
import matplotlib.pyplot as plt
import asyncio
import sys
import pymysql
import pymysql.cursors
import requests
import json
import ymProject.Data.jxDatas as jxDatas

# 请求头

headers = jxDatas.headers
matplotlib.rc("font", family='PingFang HK')


async def connect_Mysql(sql):
    try:
        db = pymysql.connect(host="localhost", user="root", password="Qinhao123.", database="farbnamen", charset="utf8")
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        res = cursor.execute(sql)
        if res is None:
            print("登陆失败")
            return None
        cursor.close()
        result = cursor.fetchall()
        db.close()
        return result
    except Exception as e:
        print(e)
        print("连接数据库异常")


async def get_xsk(data=None):
    data = json.dumps(data)
    res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
    return res['data']['ts'], res['data']['sk']


async def get_global_role_id(role_id: str, server_name: str, zone_name: str):
    # 准备请求参数
    param = {'role_id': role_id, 'server': server_name, "zone": zone_name}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/role/indicator", data=param, headers=headers).json()
    if data.get("code") != 0:
        print("获取全局role_id失败，请重试")
        sys.exit(1)
    if data.get('data').get('role_info') is None:
        print("获取角色失败，请重试")
        sys.exit(1)
    global_role_id = data.get("data").get("role_info").get("global_role_id")
    return global_role_id


async def get_jjc_record(global_role_id: str):
    # 准备请求参数
    param = {'global_role_id': global_role_id, "size": 10, "cursor": 0}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/match/history", data=param, headers=headers).json()
    if data.get("code") != 0:
        print("获取JJC战绩失败，请重试")
    if not data.get('data'):
        print("没有JJC战绩，请重试")
    return data


async def main(role: str):
    sql = "select id from InfoCache where name='%s'" % role
    role_id = await connect_Mysql(sql)
    if role_id is None is role_id[0] is None:
        print("获取用户id失败")
        return None
    role_id = role_id[0].get("id")
    global_role_id = await get_global_role_id(str(role_id), "斗转星移", "电信五区")
    dataSet = await get_jjc_record(global_role_id)
    if dataSet.get("code") != 0:
        print("没有拿到数据")
        return None
    data = dataSet.get("data")
    return data


async def get_figure(role: str):
    data = await main(role)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(role+'近10场JJC战绩')
    ax.axis([0, 10, 0, 10])
    ax.axis('off')
    for x, y in reversed(list(enumerate(data))):
        pvp_type = y.get("pvp_type")
        avg_grade = y.get("avg_grade")
        total_mmr = y.get("total_mmr")
        won = y.get("won") is True and "胜利" or "失败"
        consume_time = time.strftime("%M分%S秒", gmtime(y.get("end_time") - y.get("start_time")))
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time")))
        ax.text(0, x, f'{pvp_type}V{pvp_type}    {avg_grade}段     {total_mmr}    {won}   {consume_time}   {start_time}',
                fontweight='bold'
                )
    plt.show()

    # Set titles for the figure and the subplot respectively
    # fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')


    # ax.set_xlabel('xlabel')
    # ax.set_ylabel('ylabel')

    # Set both x- and y-axis limits to [0, 10] instead of default [0, 1]


async def get_plot(role: str):
    TotalData = await main(role)
    plt.figure(figsize=(20, 6))
    plt.title(role+'近10场JJC战绩')
    jjc_time = []
    mmr = []
    # plt.xlabel('周', fontsize=16)
    # plt.ylabel('数量', fontsize=16)
    for y in reversed(TotalData):
        start_time = time.strftime("%H:%M:%S", time.localtime(y.get("start_time")))
        jjc_time.append(str(start_time))
        mmr.append(y.get("total_mmr"))
        plt.text(jjc_time, mmr, '%.0f' % y.get("total_mmr"), ha="center", va="bottom")
    print(jjc_time)
    print(mmr)
    plt.plot(jjc_time, mmr, "o-")
    plt.show()


asyncio.run(get_plot("小疏竹"))
