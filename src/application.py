from fastapi import FastAPI

from src.apps.routers import router


_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(title="User_service", version="0.1.1", description="User service")
        _app.include_router(router)

    return _app
