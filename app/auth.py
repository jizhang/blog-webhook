from typing import Annotated

from fastapi import Header, HTTPException, status

from app.settings import SettingsDep


async def authorize(authorization: Annotated[str, Header()], settings: SettingsDep):
    if authorization != f"Bearer {settings.AUTH_TOKEN}":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
