from fastapi import APIRouter
from fastapi.responses import JSONResponse


v1 = APIRouter()


@v1.get(path="/test")
async def test():
    return JSONResponse(status_code=200, content={"test": "ok"})
