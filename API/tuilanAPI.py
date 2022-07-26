# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 梦影
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""

import requests
import json

# 请求头
headers = {
    "accept": "application/json",
    "platform": "ios",
    "gamename": "jx3",
    "clientkey": "1",
    "cache-control": "no-cache",
    "apiversion": "1",
    "sign": "true",
    "Content-Type": "application/json",
    "Host": "m.pvp.xoyo.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "token": "02da79f83c4f4da5984519e6c1cb29f9:xiaomianyang1619:kingsoft::qo3e/LCoXnb1XovF7VxHGg==",  # 自行抓包获取，每个人的不一样
    "User-Agent": "okhttp/3.12.2",
    "X-Sk": None
}


def get_xsk(data=None):
    data = json.dumps(data)
    print(data)
    res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
    print(res)
    return res['data']['ts'], res['data']['sk']


def get_server_list(role_id: str, server_name: str, zone_name: str):
    # 准备请求参数
    param = {'role_id': role_id, 'server': server_name, "zone": zone_name}
    ts, xsk = get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    print("ts:", ts)
    print("xsk:", xsk)
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    print("param:"+param)
    data = requests.post(url="https://m.pvp.xoyo.com/role/indicator", data=param, headers=headers)
    print(data.text)


if __name__ == '__main__':
    get_server_list("16624814", "斗转星移", "电信五区")
