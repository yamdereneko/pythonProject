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
import dufte

# 请求头

headers = jxDatas.headers
matplotlib.rc("font", family='PingFang HK')


class JJCRecord:
    def __init__(self, role):
        self.role = role

    async def connect_Mysql(self, sql):
        try:
            db = pymysql.connect(host="localhost", user="root", password="Qinhao123.", database="farbnamen",
                                 charset="utf8")
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

    async def get_xsk(self, data=None):
        data = json.dumps(data)
        res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
        return res['data']['ts'], res['data']['sk']

    async def get_global_role_id(self, role_id: str, server_name: str, zone_name: str):
        # 准备请求参数
        param = {'role_id': role_id, 'server': server_name, "zone": zone_name}
        ts, xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
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

    async def get_jjc_record(self, global_role_id: str):
        # 准备请求参数
        param = {'global_role_id': global_role_id, "size": 10, "cursor": 0}
        ts, xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
        param['ts'] = ts  # 给参数字典赋值ts参数
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/match/history", data=param, headers=headers).json()
        if data.get("code") != 0:
            print("获取JJC战绩失败，请重试")
        if not data.get('data'):
            print("没有JJC战绩，请重试")
        return data

    async def get_data(self):
        sql = "select id from InfoCache where name='%s'" % self.role
        role_id = await self.connect_Mysql(sql)
        if role_id is None is role_id[0] is None:
            print("获取用户id失败")
            return None
        role_id = role_id[0].get("id")
        global_role_id = await self.get_global_role_id(str(role_id), "斗转星移", "电信五区")
        dataSet = await self.get_jjc_record(global_role_id)
        if dataSet.get("code") != 0:
            print("没有拿到数据")
            return None
        data = dataSet.get("data")
        return data

    async def get_figure(self):
        data = await self.get_data()
        plt.style.use(dufte.style)
        fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
        ax.axis([0, 10, 0, 10])
        ax.set_title("斗转星移  " + self.role + '  近10场JJC战绩', fontsize=19, color='#303030', fontweight="heavy",
                     verticalalignment='top')
        ax.axis('off')
        for x, y in reversed(list(enumerate(data))):
            pvp_type = y.get("pvp_type")
            avg_grade = y.get("avg_grade")
            total_mmr = y.get("total_mmr")
            won = y.get("won") is True and "胜利" or "失败"
            consume_time = time.strftime("%M分%S秒", gmtime(y.get("end_time") - y.get("start_time")))
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time")))
            ax.text(0, x, f'{pvp_type}V{pvp_type}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(1, x, f'{avg_grade}段局 ', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            ax.text(2, x, f'{total_mmr}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            fontColor = won == "胜利" and 'blue' or 'red'
            ax.text(3, x, f'{won}', verticalalignment='bottom', horizontalalignment='left', color=fontColor)
            ax.text(4, x, f'{consume_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            ax.text(6, x, f'{start_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
        plt.savefig(f"/tmp/role{self.role}.png")

# async def get_plot(role: str):
#     TotalData = await main(role)
#     plt.figure()
#     plt.title(role+'近10场JJC战绩')
#     jjc_time = []
#     mmr = []
#     # plt.xlabel('周', fontsize=16)
#     # plt.ylabel('数量', fontsize=16)
#     for y in reversed(TotalData):
#         start_time = time.strftime("%H:%M:%S", time.localtime(y.get("start_time")))
#         jjc_time.append(str(start_time))
#         mmr.append(y.get("total_mmr"))
#         plt.text(jjc_time, mmr, '%.0f' % y.get("total_mmr"), ha="center", va="bottom")
#     containsMmr = mmr[0] // 100 * 100
#     plt.axis([0, 10, containsMmr, containsMmr+100])
#     plt.grid(True)
#     plt.plot(jjc_time, mmr, "o-")
#     plt.show()
