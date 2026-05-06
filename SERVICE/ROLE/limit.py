import os
from pathlib import Path
from DOMAIN.VALID.valid_func import Valid_func


class LimitService: #essa classe serve pra definir o limite de arquivos por camada, ai quando chegar, apaga o mais antigo

    def __init__(self, path: str, limit: int):
        self.path = Path(path)
        self.limit = limit
        self.valid = Valid_func()

    def get_files(self):
        if not self.path.exists():
            return []
        return [f for f in self.path.iterdir() if f.is_file()]

    def execute(self) -> None:
        files = self.get_files()
        if files:

            if not self.valid.limit(lenght=files, limit=self.limit):
                return

            files_sorted = sorted(files, key=lambda f: f.stat().st_mtime)

            file_to_delete = files_sorted[0]

            file_to_delete.unlink()