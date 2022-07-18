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


@app.get("/price/")
async def price_api(Server: str):
    price = await prices_api(Server)
    return {"大区": Server, "金": price}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
