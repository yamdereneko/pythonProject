import asyncio
import os

from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import ymProject.API.jx3Main as jx3API
import ymProject.API.jx3_GetJJCTopRecord as jx3Top100

roleJJCRecord = on_command("roleJJCRecord", rule=to_me(), aliases={"角色", "JJC信息"}, priority=5)
JJCTop = on_command("JJCTop", rule=to_me(), aliases={"JJC排名"}, priority=5)


@roleJJCRecord.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("role", args)
    roleJJCInfo = await get_roleJJCInfo(role=plain_text)
    await roleJJCRecord.finish(roleJJCInfo)

@JJCTop.handle()
async def handle_second_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        print(plain_text)
        await jx3Top100.get_Figure("JJC_rank_weekly", plain_text)
        msg = MessageSegment.image(f"file:///home/pycharm_project/ymProject/ym_bot/plugins/top{plain_text}.png")
        await JJCTop.finish(msg)
    else:
        await JJCTop.reject("请求错误,请参考: JJC排名 31")
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
async def get_roleJJCInfo(role: str) -> str:
    # params = {'Role_name': role}
    # JJCInfo = httpx.get('https://localhost:8080/jjc', params=params).json()
    data = await jx3API.get_jjc_Record(role)
    if data is None:
        await roleJJCRecord.reject(f"你想查询的角色{role}不存在")
    for i in data:
        match_id = i.get("match_id")
        print(i)
    return f"{data}"


