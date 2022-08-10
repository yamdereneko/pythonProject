import asyncio
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

roleJJCRecord = on_command("roleJJCRecord", rule=to_me(), aliases={"角色", "JJC信息"}, priority=5)
JJCTop = on_command("JJCTop", rule=to_me(), aliases={"JJC排名"}, priority=5)
ServerCheck = on_command("ServerCheck", rule=to_me(), aliases={"开服"}, priority=5)


@roleJJCRecord.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        await JJCRecord.get_figure(plain_text)
        msg = MessageSegment.image(f"file:///tmp/role{plain_text}.png")
        await JJCTop.finish(msg)
    else:
        await JJCTop.reject("请求错误,请参考: 角色 用户名")


@JJCTop.handle()
async def handle_second_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        plain_text = await jx3Data.school(plain_text)

        if plain_text in jx3Data.all_school.keys():
            jjcInfo = jx3JJCInfo.get_JJCTopInfo("JJC_rank_weekly", 0, plain_text)
            await jjcInfo.get_JJCWeeklySchoolRecord()
        else:
            jjcInfo = jx3JJCInfo.get_JJCTopInfo("JJC_rank_weekly", plain_text, "")
            await jjcInfo.get_JJCWeeklyRecord()
        msg = MessageSegment.image(f"file:///tmp/top{plain_text}.png")
        await JJCTop.finish(msg)
    else:
        await JJCTop.reject("请求错误,请参考: JJC排名 31或者门派")


@ServerCheck.handle()
async def handle_second_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()
        all_serverState = await ServerState.get_server_list()
        for serverState in all_serverState:
            if serverState.get("mainServer") == plain_text:
                state = serverState.get("connectState") is True and plain_text + "已开服" or plain_text + "未开服"
                await ServerCheck.finish(state)
        msg = plain_text + "大区信息不对"
        await ServerCheck.reject(msg)
    else:
        msg = await ServerState.get_server_list()
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
