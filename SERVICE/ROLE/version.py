from pathlib import Path
from datetime import datetime


class VersionService:
    @staticmethod
    def create() -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def base_path(status: str, name: str) -> Path:
        return Path(f"ADAPTER/STORAGE/{status.upper()}/{name}")

    @staticmethod
    def version_path(status: str, name: str, version: str) -> Path:
        return VersionService.base_path(status, name) / version

    @staticmethod
    def last(status: str, name: str) -> Path | None:
        path = VersionService.base_path(status, name)

        if not path.exists():
            return None

        versions = [v for v in path.iterdir() if v.is_dir()]

        if not versions:
            return None

        return sorted(versions, key=lambda v: v.name)[-1]