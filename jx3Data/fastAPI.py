from ctypes import Union
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
import main
import uvicorn
import asyncio
import ServerDatas

app = FastAPI()


def prices_api(subServer):
    server = ServerDatas.ServerData[subServer]
    price = main.price(server, subServer)
    return price


def roles_api(school):
    roles = main.role(school)
    return roles


@app.get("/price/")
async def price_api(Server: str):
    price = await prices_api(Server)
    print(Server)
    print(price)
    return {"大区": Server, "金": price}


@app.get("/role/")
async def role_api(School: str):
    role = await roles_api(School)
    print(role)
    return {"门派": School, "体型": role}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
