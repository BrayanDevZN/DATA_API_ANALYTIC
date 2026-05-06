from pathlib import Path
import shutil


class LimitService:
    def __init__(self, path: str, limit: int):
        self.path = Path(path)
        self.limit = limit

    def get_versions(self):
        if not self.path.exists():
            return []

        return [v for v in self.path.iterdir() if v.is_dir()]

    def execute(self) -> None:
        if self.limit <= 0:
            return

        versions = self.get_versions()

        if len(versions) <= self.limit:
            return

        versions_sorted = sorted(versions, key=lambda v: v.name)

        excess = len(versions_sorted) - self.limit

        for version in versions_sorted[:excess]:
            shutil.rmtree(version)