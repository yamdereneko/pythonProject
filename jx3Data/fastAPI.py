from enum import Enum
from fastapi import FastAPI
import main
import uvicorn
import asyncio
import ServerDatas


class Item(str, Enum):
    subServer: str = "斗转星移"
    server = ServerDatas.ServerData[subServer]
    price = asyncio.run(main.price(server, subServer))


app = FastAPI()
items_db = ServerDatas.ServerDatas

@app.post("/price/{item}")
async def price_api(item: Item):
    if item == Item.subServer:
        return {"大区": item.subServer, "金": item.price}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
