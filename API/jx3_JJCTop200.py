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

import pymysql
import requests
import json
import creeper.jxDatas as information

# 请求头

headers = information.headers


async def connect_Mysql(sql):
    try:
        db = pymysql.connect(host="localhost", user="root", password="Qinhao123.", database="farbnamen", charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.fetchall()
        db.close()
    except Exception as e:
        print(e)
        print("连接数据库异常")


async def get_xsk(data=None):
    data = json.dumps(data)
    res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
    return res['data']['ts'], res['data']['sk']


async def get_global_role_id(role_id: str, server_name: str, zone_name: str):
    # 准备请求参数
    try:
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
        if data.get("data").get("person_info") is None:
            return None
        global_role_id = data.get("data").get("role_info").get("global_role_id")
        return global_role_id
    except Exception as e:
        print(e)


async def get_jjc_record(global_role_id: str):
    # 准备请求参数
    param = {'global_role_id': global_role_id, "size": 10, "cursor": 0}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/match/history", data=param, headers=headers).json()
    if data.get("code") != 0:
        print("获取JJC战绩失败，请重试")
        return None
    if not data.get('data'):
        print("没有JJC战绩，请重试")
        return None
    return data


async def get_top200_history(typeName: str, tag: int, heiMaBang: bool):
    # 准备请求参数
    param = {'typeName': typeName, 'tag': tag, "heiMaBang": heiMaBang}
    ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
    param['ts'] = ts  # 给参数字典赋值ts参数
    param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
    headers['X-Sk'] = xsk  # 修改请求中的xsk
    data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/arena/top200", data=param, headers=headers).json()
    school_top = {}
    failure_list = []
    for element in data.get("data"):
        role_id = element.get("personInfo").get("gameRoleId")
        school = element.get("personInfo").get("force")
        server = element.get("personInfo").get("server")
        zone = element.get("personInfo").get("zone")
        if school in information.much_school:
            global_role_id = await get_global_role_id(role_id, server, zone)
            if global_role_id is None:
                print(role_id + " " + school + " " + server + " " + zone + " 不存在")
                failure_list.append(element)
                continue
            jjc_record = await get_jjc_record(global_role_id)
            if jjc_record is None:
                print(role_id + " " + school + " " + server + " " + zone + " 战绩不存在")
                failure_list.append(element)
                continue

            kungfu = jjc_record.get("data")[1].get("kungfu")
            if kungfu in information.school_pinyin:
                value = information.school_pinyin[kungfu]
                school_top[value] = school_top.get(value, 0) + 1
        else:
            school_top[school] = school_top.get(school, 0) + 1
    print(failure_list)
    return school_top


async def main():
    week = 26
    data = await get_top200_history('week', week, False)
    sql = "insert into JJC_rank_weekly (week, 霸刀, 藏剑, 蓬莱, 无方,云裳,花间,少林,惊羽,丐帮,苍云,紫霞,相知,补天,凌雪,明教,毒经,灵素,天策,田螺,胎虚,离经,莫问,衍天,冰心) values ('%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (week,data["霸刀"], data["藏剑"], data["蓬莱"], data["无方"], data["云裳"], data["花间"], data["少林"], data["惊羽"], data["丐帮"], data["苍云"], data["紫霞"], data["相知"], data["补天"], data["凌雪阁"], data["明教"], data["毒经"], data["灵素"], data["天策"], data["田螺"], data["胎虚"], data["离经"], data["莫问"], data["衍天宗"], data["冰心"])
    await connect_Mysql(sql)
    print(data)

if __name__ == '__main__':
    asyncio.run(main())
