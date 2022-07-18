from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from jx3Data import price

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


prices = price("电信五区", "斗转星移")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/price")
def price_api():
    return {"price": prices}
