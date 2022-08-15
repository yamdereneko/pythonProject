# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import datetime
import matplotlib
import matplotlib.pyplot as plt
import nonebot
import ymProject.Data.database as database
import requests
import json
import ymProject.Data.jxDatas as jxData
import dufte

# 请求头
headers = jxData.headers
matplotlib.rc("font", family='PingFang HK')


class GetDaily:
    def __init__(self, server: str = None, next: int = 0):
        config = jxData.config
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.next = next
        self.Pool = "jx3_Daily"
        self.database = database.DataBase(config)
        self.day = (datetime.datetime.now() + datetime.timedelta(days=+self.next)).strftime("%Y-%m-%d")

    async def Get_Daily(self):
        param = {'server': self.server, 'next': self.next}
        daily_info = requests.get(url="https://www.jx3api.com/app/daily", data=json.dumps(param)).json()
        if daily_info.get("code") != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return daily_info

    async def SyncDateConnectPool(self):
        try:
            daily_info = await self.Get_Daily()
            await self.database.connect()
            if daily_info is None:
                nonebot.logger.error("同步数据至连接池异常:" + self.Pool)
                return None
            date = daily_info.get("data").get("date")
            week = daily_info.get("data").get("week")
            war = daily_info.get("data").get("war")
            battle = daily_info.get("data").get("battle")
            camp = daily_info.get("data").get("camp")
            prestige = ":".join(daily_info.get("data").get("prestige"))
            relief = daily_info.get("data").get("relief")
            team = ":".join(daily_info.get("data").get("team"))
            draw = daily_info.get("data").get("draw")
            sql = "insert into jx3_Daily values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                date, week, war, battle, camp, prestige, relief, team, draw)
            res = await self.database.execute(sql)
            return True if res else None
        except Exception as e:
            nonebot.logger.error(e)
            return None

    async def QueryTodayDaily(self):
            sql = "select * from jx3_Daily where date='%s'" % self.day
            await self.database.connect()
            res = await self.database.fetchone(sql)
            if res is None:
                nonebot.logger.warning("连接池中不存在该数据，将进行数据同步...")
                syncResult = await self.SyncDateConnectPool()
                if syncResult is None:
                    nonebot.logger.error("连接池同步失败...")
                    return None
                res = await self.database.fetchone(sql)
            return res


daily = GetDaily()
data_daily = asyncio.run(daily.QueryTodayDaily())
print(data_daily)
