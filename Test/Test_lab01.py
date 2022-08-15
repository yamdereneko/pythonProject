# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import time
from time import gmtime
import matplotlib
import matplotlib.pyplot as plt
import nonebot
import requests
import json
import dufte
import requests
import json
import ymProject.Data.jxDatas as jxData
import ymProject.Data.database as database

# 请求头
headers = jxData.headers
matplotlib.rc("font", family='PingFang HK')


class GetJJCTop200Record:
    def __init__(self, weekly: int):
        config = jxData.config
        self.weekly = weekly
        self.server = None
        self.zone = jxData.mainZone(self.server)
        self.database = database.DataBase(config)
        self.role_id = None
        self.ts = None
        self.xsk = None
        self.global_role_id = None

    # {'霸刀': 7, '少林': 10, '补天': 5, '蓬莱': 8, '紫霞': 13, '藏剑': 7, '明教': 4, '云裳': 17, '花间': 15, '丐帮': 8, '凌雪阁': 6, '田螺': 6, '惊羽': 4, '相知': 12, '胎虚': 8, '苍云': 5, '天策': 9, '无方': 21, '灵素': 11, '冰心': 3, '毒经': 8, '衍天宗': 5, '莫问': 3, '离经': 5}
    async def main(self):
        # 获取所有的数据进行处理
        data = {'霸刀': 7, '少林': 10, '补天': 5, '蓬莱': 8, '紫霞': 13, '藏剑': 7, '明教': 4, '云裳': 17, '花间': 15, '丐帮': 8, '凌雪阁': 6,
                '田螺': 6, '惊羽': 4, '相知': 12, '胎虚': 8, '苍云': 5, '天策': 9, '无方': 21, '灵素': 11, '冰心': 3, '毒经': 8, '衍天宗': 5,
                '莫问': 3, '离经': 5}
        print(data)
        # 判断连接池数据是否冲突
        sql = "select week from JJC_rank_weekly"
        await self.database.connect()
        weekly = await self.database.fetchall(sql)
        for week in weekly:
            if week.get("week") == self.weekly:
                print("该周数据已存在...")
                return None

        sql = "insert into JJC_rank_weekly (week, 霸刀, 藏剑, 蓬莱, 无方,云裳,花间,少林,惊羽,丐帮,苍云,紫霞,相知,补天,凌雪,明教,毒经,灵素,天策,田螺,胎虚,离经,莫问,衍天,冰心) values ('%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            self.weekly, data["霸刀"], data["藏剑"], data["蓬莱"], data["无方"], data["云裳"], data["花间"], data["少林"], data["惊羽"],
            data["丐帮"], data["苍云"], data["紫霞"], data["相知"], data["补天"], data["凌雪阁"], data["明教"], data["毒经"], data["灵素"],
            data["天策"], data["田螺"], data["胎虚"], data["离经"], data["莫问"], data["衍天宗"], data["冰心"])
        print(sql)
        if sum(data.values()) == 200:
            await self.database.execute(sql)
        else:
            print("门派汇总的人数不到正确值，请人工处理错误信息...")


getRecord = GetJJCTop200Record(32)
asyncio.run(getRecord.main())
