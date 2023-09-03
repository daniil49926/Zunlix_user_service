from builtins import object

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.future import select

from src.apps.auth.utils import get_current_active_user
from src.apps.users.models import User
from src.apps.users.serializers import UserIn, UserInDB, UserOut
from src.core.db.database import get_db
from src.core.db.exception_models import Message403, Message404, Message500
from src.core.security.auth_security import get_password_hash

v1 = APIRouter()


@v1.get("/users/{uid}", response_model=UserOut, responses={404: {"model": Message404}})
async def get_user(uid: int, session=Depends(get_db)) -> User:
    async with session.begin():
        user = await session.execute(
            select(User).where(User.id == uid, User.is_active == 1)
        )
    user = user.scalars().one_or_none()
    return (
        user
        if user
        else JSONResponse(status_code=404, content={"message": "User not found"})
    )


@v1.post("/users", response_model=UserOut)
async def add_user(
    user: UserIn, session: object = Depends(get_db)
) -> User:
    hash_pass = get_password_hash(user.password)
    new_user = UserInDB(
        name=user.name,
        surname=user.surname,
        username=user.username,
        gender=user.gender,
        email=user.email,
        hashed_password=hash_pass,
    )

    # TODO Отправлять в отдельный сервис для подтверждение мыла

    user = User(**new_user.model_dump())
    async with session.begin():
        session.add(user)
        # TODO Обработать ошибки если бд бьет в отбойник

    return user


@v1.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

