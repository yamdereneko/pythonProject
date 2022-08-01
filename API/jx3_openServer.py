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
import SQLITE
import requests
import json
import jx3Data.jxDatas

# 请求头

headers = jx3Data.jxDatas.headers


async def get_xsk(data=None):
    data = json.dumps(data)
    res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
    return res['data']['ts'], res['data']['sk']


async def get_server_list(gameName: str):
    # 准备请求参数
    param = {'gameName':gameName}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/msgr-http/get-jx3-server-list", data=param, headers=headers).json()
    data = data.get('data')
    print(data)
    return data

asyncio.run(get_server_list('jx3'))