import asyncio
import re
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import ymProject.Data.jxDatas as jx3Data
import ymProject.API.jx3_GetJJCTopRecord as jx3JJCInfo
import ymProject.API.jx3_JJCRecord as JJCRecord
import ymProject.API.jx3_ServerState as ServerState
import ymProject.API.jx3_PersonHistory as PersonHistory

RoleJJCRecord = on_command("RoleJJCRecord", rule=to_me(), aliases={"战绩", "JJC信息"}, priority=5)
JJCTop = on_command("JJCTop", rule=to_me(), aliases={"JJC趋势图"}, priority=5)
ServerCheck = on_command("ServerCheck", rule=to_me(), aliases={"开服", "区服"}, priority=5)
PersonInfo = on_command("PersonInfo", rule=to_me(), aliases={"角色"}, priority=5)


@RoleJJCRecord.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        plain_text = re.sub(r'[ ]+', ' ', plain_text)
        server = plain_text.split(" ")[0]
        roleName = plain_text.split(" ")[1]
        jjcRecord = JJCRecord.GetPersonRecord(roleName, server)
        await jjcRecord.get_person_record()
        msg = MessageSegment.image(f"file:///tmp/role{roleName}.png")
        await JJCTop.finish(msg)
    else:
        await JJCTop.reject("请求错误,请参考: 战绩 区服 用户名")


@JJCTop.handle()
async def handle_second_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        plain_text = await jx3Data.school(plain_text)

        if plain_text in jx3Data.all_school.keys():
            jjcInfo = jx3JJCInfo.GetJJCTopInfo("JJC_rank_weekly", 0, plain_text)
            await jjcInfo.get_JJCWeeklySchoolRecord()
        else:
            jjcInfo = jx3JJCInfo.GetJJCTopInfo("JJC_rank_weekly", plain_text, "")
            await jjcInfo.get_JJCWeeklyRecord()
        msg = MessageSegment.image(f"file:///tmp/top{plain_text}.png")
        await JJCTop.finish(msg)
    else:
        await JJCTop.reject("请求错误,请参考: JJC排名 31或者门派")


@PersonInfo.handle()
async def handle_third_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        plain_text = re.sub(r'[ ]+', ' ', plain_text)
        server = plain_text.split(" ")[0]
        roleName = plain_text.split(" ")[1]
        personInfo = PersonHistory.GetPersonInfo(roleName, server)
        role_name = await personInfo.get_Fig()
        msg = MessageSegment.image(f"file:///tmp/role{role_name}.png")
        await JJCTop.finish(msg)
    else:
        await JJCTop.reject("请求错误,请参考: 角色 区服 用户名")


@ServerCheck.handle()
async def handle_forth_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()
        all_serverState = ServerState.ServerState(plain_text)
        serverState = await all_serverState.get_server_list()
        state = serverState is True and plain_text + "已开服" or plain_text + "未开服"
        await ServerCheck.finish(state)
    else:
        serverState = ServerState.ServerState()
        msg = await serverState.get_server_list()
        await JJCTop.finish(msg)


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
