from fastapi import APIRouter

from src.apps.auth.views import v1 as auth_v1
from src.apps.users.views import v1 as user_v1

router = APIRouter()

router.include_router(user_v1, tags=["user"])
router.include_router(auth_v1, tags=["auth"])
