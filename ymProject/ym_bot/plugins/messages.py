import asyncio

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import ymProject.API.jx3Main as jx3API

roleJJCRecord = on_command("roleJJCRecord", rule=to_me(), aliases={"角色", "JJC信息"}, priority=5)


@roleJJCRecord.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("role", args)
    roleJJCInfo = await get_roleJJCInfo(role=plain_text)
    await roleJJCRecord.finish(roleJJCInfo)


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

# 在这里编写获取天气信息的函数
async def get_roleJJCInfo(role: str) -> str:
    # params = {'Role_name': role}
    # JJCInfo = httpx.get('https://localhost:8080/jjc', params=params).json()
    data = await jx3API.get_jjc_Record(role)
    for i in data:
        print(i)
    return f"{data}"


asyncio.run(get_roleJJCInfo("笋笋"))
