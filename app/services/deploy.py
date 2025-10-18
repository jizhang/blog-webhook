import os
import tarfile
from io import BytesIO
from pathlib import Path

from app.settings import SettingsDep


class DeployService:
    def __init__(self, settings: SettingsDep):
        self.settings = settings

    def deploy(self, project: str, short_sha: str, file: bytes):
        project_path = Path(self.settings.DEPLOY_BASE) / project
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
