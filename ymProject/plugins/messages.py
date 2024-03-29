# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : message.py
@Author : 喵
@Time : 2022/08/11 22:39:29
@Docs : 回复插件开发
"""

import asyncio
import re
import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.rule import to_me, keyword, command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger, default_format
import ymProject.Data.jxDatas as jx3Data
import ymProject.API.jx3_GetJJCTopRecord as jx3JJCInfo
import ymProject.API.jx3_JJCRecord as JJCRecord
import ymProject.API.jx3_ServerState as ServerState
import ymProject.API.jx3_PersonHistory as PersonHistory
import ymProject.API.jx3_Daily as DailyInfo

logger.add("logs/error.log",
           rotation="00:00",
           diagnose=False,
           level="ERROR",
           format=default_format)

RoleJJCRecord = on_command("RoleJJCRecord", rule=keyword("战绩", "JJC信息"), aliases={"战绩", "JJC信息"}, priority=5)
JJCTop = on_command("JJCTop", rule=keyword("JJC趋势图"), aliases={"JJC趋势图"}, priority=5)
ServerCheck = on_command("ServerCheck", rule=keyword("开服"), aliases={"开服"}, priority=5)
AllServerState = on_command("AllServerState", rule=keyword("区服"), aliases={"区服"}, priority=5)
PersonInfo = on_command("PersonInfo", rule=keyword("角色"), aliases={"角色"}, priority=5)
Daily = on_command("Daily", rule=keyword("日常"), aliases={"日常"}, priority=5)


@RoleJJCRecord.handle()
async def onMessage_RoleJJCRecord(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            plain_text = re.sub(r'[ ]+', ' ', plain_text)
            server = plain_text.split(" ")[0]
            serverRight = jx3Data.mainServer(server)
            if serverRight is not None:
                roleName = plain_text.split(" ")[1]
                jjcRecord = JJCRecord.GetPersonRecord(roleName, server)
                res = await jjcRecord.get_person_record()
                if res is not None:
                    msg = MessageSegment.image(f"file:///tmp/role{roleName}.png")
                    await JJCTop.finish(msg)
                else:
                    nonebot.logger.error(f"{roleName} JJC战绩查询不存在,请重试")
                    await JJCTop.reject(f"{server} {roleName} JJC战绩查询不存在,请重试")
            else:
                nonebot.logger.error(f"{server} 大区不存在,请重试")
    else:
        nonebot.logger.error("请求错误,请参考: 战绩 区服 用户名")
        await JJCTop.reject("请求错误,请参考: 战绩 区服 用户名")


# 接收 JJC趋势图
# JJC趋势图 31或者门派 ==> 调用存储在/tmp目录下得图片
# 图片形式发送
@JJCTop.handle()
async def onMessage_JJCTop(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        plain_text = jx3Data.school(plain_text)
        if plain_text is not None:
            if plain_text in jx3Data.all_school.keys():
                jjcInfo = jx3JJCInfo.GetJJCTopInfo("JJC_rank_weekly", 0, plain_text)
                record_figure = await jjcInfo.get_JJCWeeklySchoolRecord()
            else:
                jjcInfo = jx3JJCInfo.GetJJCTopInfo("JJC_rank_weekly", plain_text, "")
                record_figure = await jjcInfo.get_JJCWeeklyRecord()
            if record_figure is not None:
                msg = MessageSegment.image(f"file:///tmp/top{plain_text}.png")
                await JJCTop.finish(msg)
            else:
                nonebot.logger.error("创建趋势图失败，请检查报错")
        else:
            nonebot.logger.error("参数错误，请重新输入正确参数")
            await JJCTop.reject("参数错误，请重新输入正确参数")
    else:
        nonebot.logger.error("请求错误,请参考: JJC趋势图 31或者门派")
        await JJCTop.reject("请求错误,请参考: JJC趋势图 31或者门派")


# 接收 角色信息 查询本地角色最近游玩的角色的JJC战绩
# 角色 区服 用户名 ==> 目前的角色JJC战绩
# 图片形式发送
@PersonInfo.handle()
async def onMessage_PersonInfo(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            plain_text = re.sub(r'[ ]+', ' ', plain_text)
            server = plain_text.split(" ")[0]
            serverRight = jx3Data.mainServer(server)
            if serverRight is not None:
                roleName = plain_text.split(" ")[1]
                personInfo = PersonHistory.GetPersonInfo(roleName, server)
                role_name = await personInfo.get_Fig()
                if role_name is not None:
                    msg = MessageSegment.image(f"file:///tmp/role{role_name}.png")
                    await JJCTop.finish(msg)
                else:
                    nonebot.logger.error("用户信息未成功获取，请重试")
                    await JJCTop.reject("用户信息未成功获取，请重试")
            else:
                nonebot.logger.error("区服输入错误，请重试")
                await JJCTop.reject("区服输入错误，请重试")
    else:
        nonebot.logger.error("请求错误,请参考: 角色 区服 用户名")
        await JJCTop.reject("请求错误,请参考: 角色 区服 用户名")


@ServerCheck.handle()
async def onMessage_ServerCheck(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text().replace(" ", "")
        all_serverState = ServerState.ServerState(plain_text)
        serverState = await all_serverState.get_server_list()
        serverName = jx3Data.mainServer(plain_text)
        if serverName is not None:
            for info in serverState:
                if info.get("mainServer") == serverName:
                    server_state = info.get("connectState")
                    state = server_state is True and serverName + "已开服" or serverName + "未开服"
                    await ServerCheck.finish(state)
            nonebot.logger.info("开服数据未得到，请检查")
            await ServerCheck.reject("未找到区服,请重新输入")
        else:
            nonebot.logger.error("开服数据未得到，请检查")
    else:
        nonebot.logger.error("请求错误,请参考:区服 ")
        await JJCTop.reject("请求错误,请参考:区服 ")


@AllServerState.handle()
async def onMessage_AllServerState(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() == "":
        plain_text = args.extract_plain_text()
        all_serverState = ServerState.ServerState(plain_text)
        if await all_serverState.get_figure() is True:
            msg = MessageSegment.image(f"file:///tmp/serverState.png")
            await AllServerState.finish(msg)
        else:
            nonebot.logger.error("全区服图未正常创建，请查看")
            await ServerCheck.reject("未找到区服,请重新输入")
    else:
        await JJCTop.reject("请求错误,请参考:区服")


@Daily.handle()
async def onMessage_Daily(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()
        if plain_text.find(" ") != -1:
            plain_text = re.sub(r'[ ]+', ' ', plain_text)
            server = jx3Data.mainServer(plain_text.split(" ")[0])
            if server is not None:
                dailyDate = plain_text.split(" ")[1]
                day = 0
                match dailyDate:
                    case "明天":
                        day = 1
                    case "后天" | "第二天":
                        day = 2
                    case "大后天" | "第三天":
                        day = 3
                daily = DailyInfo.GetDaily(server, day)
                state = await daily.QueryDailyFigure()
                if state is True:
                    msg = MessageSegment.image(f"file:///tmp/daily{server}{day}.png")
                    await Daily.finish(msg)
        else:
            nonebot.logger.error("请求错误,请参考:日常 大区 明天")
            await Daily.reject("请求错误,请参考:日常 大区 明天  ")
    else:
        daily = DailyInfo.GetDaily()
        await daily.QueryDailyFigure()
        msg = MessageSegment.image(f"file:///tmp/daily斗转星移0.png")
        await Daily.finish(msg)

#
# @roleJJCRecord.got("role", prompt="你想查询哪个角色信息呢？")
# async def handle_city(role: Message = Arg(), roleName: str = ArgPlainText("role")):
#     await roleJJCRecord.reject(role.template("你想查询的角色 {role} 暂不支持，请重新输入！"))


#
# @roleJJCRecord.got("role", prompt="你想查询哪个角色信息呢？")
# async def handle_city(role: Message = Arg(), roleName: str = ArgPlainText("role")):
#     nonebot.logger.info(role)
#     if roleName not in ["笋笋"]:  # 如果参数不符合要求，则提示用户重新输入
#         # 可以使用平台的 Message 类直接构造模板消息
#         await roleJJCRecord.reject(role.template("你想查询的角色 {role} 暂不支持，请重新输入！"))
#     role_info = await get_roleInfo(roleName)
#     await roleJJCRecord.finish(role_info)
#

# 在这里编写获取JJC信息的函数
# async def get_roleJJCInfo(role: str) -> str:
#     # params = {'Role_name': role}
#     # JJCInfo = httpx.get('https://localhost:8080/jjc', params=params).json()
#     data = await jx3API.get_jjc_Record(role)
#     if data is None:
#         await roleJJCRecord.reject(f"你想查询的角色{role}不存在")
#     for i in data:
#         match_id = i.get("match_id")
#         print(i)
#     return f"{data}"
