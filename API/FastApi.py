import uvicorn
import wanbaolou
import jx3Data.jxDatas as JX3Data

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException

app = FastAPI()


def roles(shape, school):
    role = wanbaolou.main(shape, school)
    return role


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=404,
        content={"code": "404", "msg": f"{exc.name}参数不存在，请修改尝试.", "data": {}},
    )

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
