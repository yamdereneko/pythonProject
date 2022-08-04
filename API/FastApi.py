#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import Union
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import uvicorn
import jx3_WanBaoLouInfo
import jxDatas as JX3Data
import jx3_JJCRecord
import jx3_PersonHistory
import jx3_GetJJCTopRecord
import jx3_ServerState

sys.path.append(r'/home/pycharm_project')
sys.path.append(r'/home/pycharm_project/API')

app = FastAPI()


# ************************************************
# 定义类型部分

class UnicornException(Exception):
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class RoleName(BaseModel):
    Role_name: Union[str, None] = None


class Transaction(BaseModel):
    Shape: Union[str, None] = None
    School: Union[str, None] = None


class JJCWeekly(BaseModel):
    Week: Union[int, None] = None


# ************************************************
# 代码实现部分 实际代码为异步

def roles(shape, school):
    role = jx3_WanBaoLouInfo.main(shape, school)
    return role


def get_jjc_Record(role_name):
    role_JJC_Record = jx3_JJCRecord.main(role_name)
    print(role_JJC_Record)
    return role_JJC_Record


def get_person_history(role_name):
    person_history_res = jx3_PersonHistory.main(role_name)
    print(person_history_res)
    return person_history_res


def get_JJCTop_Record(week):
    jjcTopRecord = jx3_GetJJCTopRecord.get_JJCWeeklyRecord(week)
    print(jjcTopRecord)
    return jjcTopRecord


def get_ServerState():
    serverState = jx3_ServerState.get_server_list()
    print(serverState)
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
    print(jjc_record)
    return {"code": 0, "msg": "success", "role_name": role.Role_name, "data": jjc_record}


# 推栏个人查询
# 入参 { "Role_name": "笋笋" }
@app.get("/jx3/person")
async def person_history_api(
        *,
        role: Union[RoleName, None] = None
):
    person_res = await get_person_history(role.Role_name)
    if person_res is None:
        raise UnicornException(name=role.Role_name, content="该用户信息不存在")
    print(person_res)
    return {"code": 0, "msg": "success", "role_name": role.Role_name, "data": person_res}


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
    return {"code": 0, "msg": "success", "school": transaction.School, "shape": transaction.Shape,
            "roles_sum": role_sum,
            "data": roleInfo}


# JJC TOP200查询
# 入参 { "Week": 30 }
@app.get("/jx3/jjcTop")
async def jjc_TopRecord_api(
        *,
        weekly: Union[JJCWeekly, None] = None
):
    jjcTopRecord = await get_JJCTop_Record(weekly.Week)
    if jjcTopRecord is None:
        raise UnicornException(name=str(weekly.Week), content="该周竞技场信息不存在")
    print(jjcTopRecord)
    return {"code": 0, "msg": "success", "weekly": weekly.Week, "data": jjcTopRecord}


# 服务器状态查询
@app.get("/jx3/check")
async def check_ServerState():
    Server_State = await get_ServerState()
    if Server_State is None:
        raise UnicornException(name="", content="服务器校验有误，请重试")
    print(Server_State)
    return {"code": 0, "msg": "success", "data": Server_State}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
