from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Form

from ..dependencies import authorize

router = APIRouter(prefix="/deploy", dependencies=[Depends(authorize)])


@router.post("/submit")
async def deploy_submit(
    project: Annotated[str, Form(min_length=2)],
    sha1_short: Annotated[str, Form(pattern=r"^[0-9a-f]{8}$")],
    file: UploadFile,
):
    return {
        "project": project,
        "sha1_short": sha1_short,
        "filesize": file.size,
    }
