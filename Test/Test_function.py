# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import sys
import requests
import json
import creeper.jxDatas

# 请求头

headers = creeper.jxDatas.headers


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


async def get_friend_data(global_role_id: str):
    # 准备请求参数
    param = {'gameGlobalRoleId': global_role_id, "zone": "电信一区", "server": "龙争虎斗", "centerId": "15"}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/role/get-fellow-list-by-globalId", data=param,
                         headers=headers).json()
    print(data)
    if data.get("code") != 0:
        print("获取JJC战绩失败，请重试")
    if not data.get('data'):
        print("没有JJC战绩，请重试")
    return data

asyncio.run(get_friend_data("378302368709802699"))