import os
import time
import hmac
import hashlib
import tarfile
from typing import Annotated
from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, status

from app.auth import authorize
from app.settings import SettingsDep

router = APIRouter(prefix="/deploy", dependencies=[Depends(authorize)])


@router.post("/submit")
async def deploy_submit(
    project: Annotated[str, Form(pattern=r"^[a-z][0-9a-z-]+$")],
    short_sha: Annotated[str, Form(pattern=r"^[0-9a-f]{8}$")],
    file_hash: Annotated[str, Form(pattern=r"^[0-9a-f]{64}$")],
    timestamp: Annotated[int, Form(ge=0)],
    signature: Annotated[str, Form(pattern=r"^[0-9a-f]{64}$")],
    file: Annotated[bytes, File()],
    settings: SettingsDep,
):
    message = f"project={project}&short_sha={short_sha}&file_hash={file_hash}&timestamp={timestamp}"
    h = hmac.new(settings.HMAC_SECRET.encode(), message.encode(), hashlib.sha256)
    if signature != h.hexdigest() or \
            time.time() - timestamp >= 300 or \
            file_hash != hashlib.sha256(file).hexdigest():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    project_path = Path(settings.DEPLOY_BASE) / project
    release_path = project_path / "releases" / short_sha
    release_path.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=BytesIO(file), mode="r:gz") as tar:
        tar.extractall(path=release_path)

    tmp_link = project_path / f"current.{short_sha}"
    if tmp_link.exists():
        tmp_link.unlink()
    tmp_link.symlink_to(release_path)

    current_link = project_path / "current"
    os.replace(tmp_link, current_link)

    return {
        "current": short_sha,
    }
