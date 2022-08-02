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
import jx3Data.jxDatas as JX3Data
import jx3_JJCRecord
import jx3_PersonHistory
import jx3_ServerState

sys.path.append(r'/home/pycharm_project')
sys.path.append(r'/home/pycharm_project/API')

app = FastAPI()


class UnicornException(Exception):
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class RoleName(BaseModel):
    Role_name: Union[str, None] = None


class Transaction(BaseModel):
    Shape: Union[str, None] = None
    School: Union[str, None] = None


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


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=404,
        content={"code": "404", "msg": f"\'{exc.name}\'{exc.content}，请重新尝试.", "data": {}},
    )


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


@app.get("/jx3/role")
async def role_api(
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
