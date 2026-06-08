from pathlib import Path
import shutil
import logging
logger = logging.getLogger(__name__)

class LimitService:
    def __init__(self, path: str, limit: int):
        self.path = Path(path)
        self.limit = limit
        self.name = path

    def get_versions(self):
        if not self.path.exists():
            logger.info(f"Ainda não ha versões de {self.name}")
            return []

        return [v for v in self.path.iterdir() if v.is_dir()]

    def execute(self) -> None:
        if self.limit <= 0:
            return

        versions = self.get_versions()

        if len(versions) <= self.limit:
            logger.info(f"{self.name} ainda não excedeu o limite de arquivos!!")
            return
        
        logger.info(f"Limite de arquivos excedido, limpando arquivos mais antigos...")

        versions_sorted = sorted(versions, key=lambda v: v.name)

        excess = len(versions_sorted) - self.limit

        for version in versions_sorted[:excess]:
            shutil.rmtree(version)
            
        logger.info(f"Limpo com sucesso!!")