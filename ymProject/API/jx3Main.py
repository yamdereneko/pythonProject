#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append("/home/pycharm_project/ymProject/Data")
sys.path.append("/home/pycharm_project/ymProject/API")
from ymProject.Data import jxDatas as JX3Data
from ymProject.API import jx3_GetJJCTopRecord as GetJJCTopRecord, jx3_JJCRecord as JJCRecord, \
    jx3_WanBaoLouInfo as WanBaoLouInfo, jx3_PersonHistory as PersonHistory, jx3_ServerState as ServerState
from pydantic import BaseModel
from typing import Union
import nonebot
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request, status

nonebot.init(_env_file=".env.dev")
app: FastAPI = nonebot.get_app()


class UnicornException(Exception):
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class RoleName(BaseModel):
    Role_name: Union[str, None] = None


class personInfo(BaseModel):
    Role_name: Union[str, None] = None
    Server: Union[str, None] = None
    Zone: Union[str, None] = None


class Transaction(BaseModel):
    Shape: Union[str, None] = None
    School: Union[str, None] = None


class JJCWeekly(BaseModel):
    Week: Union[int, None] = None


# ************************************************
# 代码实现部分 实际代码为异步

def roles(shape, school):
    role = WanBaoLouInfo.main(shape, school)
    return role


def get_jjc_Record(role_name):
    role_JJC_Record = JJCRecord.main(role_name)
    return role_JJC_Record


def get_person_history(role_name, server, zone):
    person_history_res = PersonHistory.main(role_name, server, zone)
    return person_history_res


def get_JJCTop_Record(table, week):
    jjcTopRecord = GetJJCTopRecord.get_JJCWeeklyRecord(table, week)
    return jjcTopRecord


def get_ServerState():
    serverState = ServerState.get_server_list()
    return serverState


# ***************************************
# 接口部分(以下)

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=404,
        content={"code": "404", "msg": f"\'{exc.name}\'{exc.content}，请重新尝试.", "data": {}},
    )


# JJC个人战绩查询
# 入参 { "Role_name": "笋笋" }
@app.get("/jx3/jjc")
async def jjc_record_api(
        *,
        role: Union[RoleName, None] = None
):
    jjc_record = await get_jjc_Record(role.Role_name)
    if jjc_record is None:
        raise UnicornException(name=role.Role_name, content="该用户信息不存在")
    nonebot.logger.info(jjc_record)
    return {"code": 0, "msg": "success", "role_name": role.Role_name, "data": jjc_record}


# 推栏个人查询
# 入参 { "Role_name": "笋笋" }
@app.get("/jx3/person")
async def person_history_api(
        *,
        role: Union[personInfo, None] = None,
        server: Union[personInfo, None] = None,
        zone: Union[personInfo, None] = None,
):
    person_res = await get_person_history(role.Role_name, role.Server, role.Zone)
    if person_res is None:
        raise UnicornException(name=role.Role_name, content="该用户信息不存在")
    nonebot.logger.info(person_res)
    return {"code": 0, "msg": "success", "role_name": role.Role_name, "server": "role.Server", "zone": "role.Zone",
            "data": person_res}


# 万宝楼情况查询
# 入参 { "Shape": "萝莉", School: "蓬莱" }
@app.get("/jx3/role")
async def jx3_Role_Api(
        *,
        transaction: Union[Transaction, None] = None
):
    school_dict = JX3Data.school_number
    shape_dict = JX3Data.bodyType
    if transaction.School not in school_dict:
        raise UnicornException(name="门派", content="该门派不存在，请重试")
    if transaction.Shape not in shape_dict:
        raise UnicornException(name="体型", content="该体型不存在，请重试")
    roleInfo, role_sum = await roles(transaction.Shape, transaction.School)
    if roleInfo == "-11":
        raise UnicornException(name="", content="网站维护中...")
    nonebot.logger.info(roleInfo)
    return {"code": 0, "msg": "success", "school": transaction.School, "shape": transaction.Shape,
            "roles_sum": role_sum,
            "data": roleInfo}


# JJC TOP200查询
# 入参 { "Week": 30 }
@app.get("/jx3/jjcTop200")
async def jjc_TopRecord_api(
        *,
        weekly: Union[JJCWeekly, None] = None
):
    table = "JJC_rank_weekly"
    jjcTopRecord = await get_JJCTop_Record(table, weekly.Week)
    if jjcTopRecord is None:
        raise UnicornException(name=str(weekly.Week), content="该周竞技场信息不存在")
    nonebot.logger.info(jjcTopRecord)
    return {"code": 0, "msg": "success", "Type": "Top200", "weekly": weekly.Week, "data": jjcTopRecord}


# JJC TOP50查询
# 入参 { "Week": 30 }
@app.get("/jx3/jjcTop50")
async def jjc_TopRecord_api(
        *,
        weekly: Union[JJCWeekly, None] = None
):
    table = "JJC_rank50_weekly"
    jjcTopRecord = await get_JJCTop_Record(table, weekly.Week)
    if jjcTopRecord is None:
        raise UnicornException(name=str(weekly.Week), content="该周竞技场信息不存在")
    nonebot.logger.info(jjcTopRecord)
    return {"code": 0, "msg": "success", "Type": "Top50", "weekly": weekly.Week, "data": jjcTopRecord}


# 服务器状态查询
@app.get("/jx3/check")
async def check_ServerState():
    Server_State = await get_ServerState()
    if Server_State is None:
        raise UnicornException(name="", content="服务器校验有误，请重试")
    nonebot.logger.info(Server_State)
    return {"code": 0, "msg": "success", "data": Server_State}
