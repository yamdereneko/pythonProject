# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs :
"""
import asyncio
import requests
import json
import ymProject.Data.jxDatas as jxdata
import sys

sys.path.append(r'/home/pycharm_project')
sys.path.append(r'/home/pycharm_project/API')

# 请求头

headers = jxdata.headers


class ServerState:
    def __init__(self, server=None):
        self.server = jxdata.mainServer(server)
        self.zone = jxdata.mainZone(self.server)

    async def get_xsk(self, data=None):
        data = json.dumps(data)
        res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
        return res['data']['ts'], res['data']['sk']

    async def get_server_list(self):
        # 准备请求参数
        gameName = "jx3"
        param = {'gameName': gameName}
        ts, xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
        param['ts'] = ts  # 给参数字典赋值ts参数
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/msgr-http/get-jx3-server-list", data=param,
                             headers=headers).json()
        if data.get("code") != 0:
            print("服务器状态有问题")
            return None

        ServerStates = []
        for info in data.get("data"):
            flag = 0
            ServerState = {}
            server = info.get("mainServer")
            for i in ServerStates:
                if i.get("mainServer") == server:
                    flag = 1
                    break
            if flag == 1:
                continue
            ServerState["mainServer"] = server
            ServerState["mainZone"] = info.get("mainZone")
            ServerState["connectState"] = info.get("connectState")
            ServerStates.append(ServerState)
        return ServerStates
