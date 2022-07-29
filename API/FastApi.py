#!/usr/bin/python
# -*- coding: UTF-8 -*-
import uvicorn
import wanbaolou
import jx3Data.jxDatas as JX3Data
import JJCRecordAPI
import person_history
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException

app = FastAPI()


class UnicornException(Exception):
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


def roles(shape, school):
    role = wanbaolou.main(shape, school)
    return role


def get_jjc_Record(role_name):
    role_JJC_Record = JJCRecordAPI.main(role_name)
    print(role_JJC_Record)
    return role_JJC_Record


def get_person_history(role_name):
    person_history_res = person_history.main(role_name)
    print(person_history_res)
    return person_history_res


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=404,
        content={"code": "404", "msg": f"\'{exc.name}\'{exc.content}，请重新尝试.", "data": {}},
    )


@app.get("/jjc/")
async def jjc_record_api(Role_name: str):
    jjc_record = await get_jjc_Record(Role_name)
    if jjc_record is None:
        raise UnicornException(name=Role_name, content="该用户信息不存在")
    print(jjc_record)
    return {"role_name": Role_name, "msg": "success", "data": jjc_record}


@app.get("/person/")
async def person_history_api(Role_name: str):
    person_res = await get_person_history(Role_name)
    if person_res is None:
        raise UnicornException(name=Role_name, content="该用户信息不存在")
    print(person_res)
    return {"role_name": Role_name, "msg": "success", "data": person_res}


@app.get("/role/")
async def role_api(School: str, Shape: str):
    school_dict = JX3Data.school_number
    shape_dict = JX3Data.bodyType
    if School not in school_dict:
        raise UnicornException(name="门派")
    if Shape not in shape_dict:
        raise UnicornException(name="体型")
    roleInfo, role_sum = await roles(Shape, School)
    print(roleInfo)
    print(role_sum)
    return {"school": School, "shape": Shape, "roles_sum": role_sum, "msg": "success", "data": roleInfo}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
