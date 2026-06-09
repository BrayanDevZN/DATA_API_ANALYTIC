import pandas as pd

from SERVICE.ROLE.version import VersionService
import logging
logger = logging.getLogger(__name__)
class Control_DataParquet: #le e salva arquivos parquet
    
    @staticmethod
    def save_parquet(
    name: str,
    df: pd.DataFrame,
    version: str
    ) -> None:
        logger.info(f"Salvando dados de {name} na camada cleaned...")

        df.to_parquet(
            f"ADAPTER/STORAGE/CLEANED/{name}/{version}/{name}.parquet",
            index=False
        )
        logger.info("Dados salvos!!")
            
    @staticmethod
    def read_parquet(name: str) -> pd.DataFrame | None:
        logger.info(f"Lendo arquivo {name} na camada cleaned...")

        version_path = VersionService.last(
            status="cleaned",
            name=name
        )

        if version_path is None:
            logger.warning(f"Nenhuma versão encontrada para {name} na camada cleaned.")
            return None

        file = version_path / f"{name}.parquet"

        if not file.exists():
            logger.warning(f"Arquivo {name} não existe na camada cleaned.")
            return None

        logger.info(f"Arquivo {name} lido com sucesso!!!")

        return pd.read_parquet(file)