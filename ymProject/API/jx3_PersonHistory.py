# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio

import pymysql
import pymysql.cursors
import jx3_SearchRoleID
import requests
import json
import ymProject.Data.jxDatas as jxData

# 请求头

headers = jxData.headers


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


async def get_person_id(role_id: str, server_name: str, zone_name: str):
    # 准备请求参数
    param = {'role_id': role_id, 'server': server_name, "zone": zone_name}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/role/indicator", data=param, headers=headers).json()
    person_id = data.get("data").get("person_info").get("person_id")
    return person_id


async def get_person_history(person_id: str):
    # 准备请求参数
    param = {'person_id': person_id, "size": 10, "cursor": 0}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/mine/match/person-history", data=param, headers=headers).json()
    return data


asyncio.run(get_person_history(""))


async def main(role: str):
    sql = "select id from InfoCache where name='%s'" % role
    role_id = await connect_Mysql(sql)
    if role_id is None is role_id[0] is None:
        print("获取用户id失败")
        return None
    role_id = role_id[0].get("id")
    person_id = await get_person_id(str(role_id), "斗转星移", "电信五区")
    dataSet = await get_person_history(person_id)
    data = dataSet.get("data")
    return data
