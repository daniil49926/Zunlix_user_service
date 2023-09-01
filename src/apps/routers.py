from fastapi import APIRouter

from src.apps.users.views import v1 as user_v1

router = APIRouter()

router.include_router(user_v1, tags=["user"])
