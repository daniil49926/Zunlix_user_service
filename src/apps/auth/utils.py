from builtins import object

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.future import select

from src.apps.auth.serializers import TokenData
from src.apps.users.models import User
from src.core.db.database import get_db
from src.core.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_oauth2_scheme():
    return oauth2_scheme


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: object = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.CRYPTO_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
        if not token_data:
            raise JWTError
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(token_data.username, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_user(username: str, session):
    async with session.begin():
        user = await session.execute(
            select(User).where(User.username == username and User.is_active == 1)
        )
    user = user.scalars().one_or_none()
    return user
