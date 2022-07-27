# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import sys
import SQLITE
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
    "User-Agent": "SeasunGame/193 CFNetwork/1333.0.4 Darwin/21.5.0",
    "X-Sk": None
}


def get_xsk(data=None):
    data = json.dumps(data)
    res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
    return res['data']['ts'], res['data']['sk']


def get_global_role_id(role_id: str, server_name: str, zone_name: str):
    # 准备请求参数
    param = {'role_id': role_id, 'server': server_name, "zone": zone_name}
    ts, xsk = get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
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


def get_jjc_record(global_role_id: str):
    # 准备请求参数
    param = {'global_role_id': global_role_id, "size": 6, "cursor": 0}
    ts, xsk = get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/match/history", data=param, headers=headers).json()
    if data.get("code") != 0:
        print("获取JJC战绩失败，请重试")
        sys.exit(1)
    if not data.get('data'):
        print("没有JJC战绩，请重试")
        sys.exit(1)
    return data


def main(role: str):
    role_id = SQLITE.sqlite(role)
    print(role_id)
    if role_id is None:
        print("获取用户id失败")
        sys.exit(1)
    global_role_id = get_global_role_id(str(role_id), "斗转星移", "电信五区")
    dataSet = get_jjc_record(global_role_id)
    if dataSet.get("code") != 0:
        print("没有拿到数据")
        sys.exit(1)
    for data in dataSet.get("data"):
        print(data)


if __name__ == '__main__':
    main("时岁岁")
