from enum import Enum
from fastapi import FastAPI
import main
import uvicorn
import asyncio
import ServerDatas


class Item(str, Enum):
    server = "电信五区"
    subServer = "斗转星移"
    price = asyncio.run(main.price(server, subServer))


app = FastAPI()


@app.post("/price/{item}")
async def price_api(item: Item):
    if item == Item.subServer:
        return {"大区": item.subServer, "金": item.price}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
