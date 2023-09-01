from fastapi import FastAPI, APIRouter

from src.apps.routers import router
from src.core.db import database

event_router = APIRouter()


@event_router.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@event_router.on_event("shutdown")
async def shutdown():
    await database.async_session().close()
    await database.engine.dispose()


_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(title="User_service", version="0.1.1", description="User service")
        _app.include_router(router)
        _app.include_router(event_router)

    return _app
