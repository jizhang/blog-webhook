import time
import hmac
import hashlib
from typing import Annotated
from app.services.deploy import DeployService

from fastapi import APIRouter, Depends, File, Form, HTTPException, status

from app.settings import SettingsDep

router = APIRouter(prefix="/deploy", )

ProjectInput = Annotated[str, Form(pattern=r"^[a-z][0-9a-z-]+$")]
ShortShaInput = Annotated[str, Form(pattern=r"^[0-9a-f]{8}$")]
HashInput = Annotated[str, Form(pattern=r"^[0-9a-f]{64}$")]


@router.post("/signed")
def deploy_signed(
    project: ProjectInput,
    short_sha: ShortShaInput,
    file_hash: HashInput,
    timestamp: Annotated[int, Form(ge=0)],
    signature: HashInput,
    file: Annotated[bytes, File()],
    settings: SettingsDep,
    deploy_svc: Annotated[DeployService, Depends()]
):
    message = f"project={project}&short_sha={short_sha}&file_hash={file_hash}&timestamp={timestamp}"
    h = hmac.new(settings.HMAC_SECRET.encode(), message.encode(), hashlib.sha256)
    if signature != h.hexdigest() or \
            time.time() - timestamp >= 300 or \
            file_hash != hashlib.sha256(file).hexdigest():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    deploy_svc.deploy(project, short_sha, file)
    return {"current": short_sha}


@router.post("/secured")
def deploy_secured(
    project: ProjectInput,
    short_sha: ShortShaInput,
    file: Annotated[bytes, File()],
    deploy_svc: Annotated[DeployService, Depends()]
):
    deploy_svc.deploy(project, short_sha, file)
    return {"current": short_sha}
