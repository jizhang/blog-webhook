from typing import Annotated

from fastapi import Header, HTTPException, status


async def authorize(authorization: Annotated[str, Header()]):
    if authorization != "Bearer token":  # FIXME
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
