
from SERVICE.ROLE.version import VersionService
import pandas as pd
import logging
logger = logging.getLogger(__name__)
class Control_DataJson: #le e salva arquivos json
    @staticmethod
    def save_json(name: str, df: pd.DataFrame, version: str) -> None:
        logger.info(f"Salvando dados de {name} na camada raw...")
        df.to_json(
        f"ADAPTER/STORAGE/RAW/{name}/{version}/{name}.json",
        orient="records",
        indent=4,
        force_ascii=False
    )
        logger.info("Dados salvos!!")
    
    @staticmethod      
    def read_json(name:str) -> pd.DataFrame:
        logger.info(f"Lendo arquivo {name} na camada raw...")
        version_path = VersionService.last(
            status="raw",
            name=name
        )
        file = version_path / f"{name}.json"

        if version_path is None or not file.exists():
            logger.warning(f"Arquivo {name} não existe na camada raw.")
            return None

        

        logger.info(f"Arquivo {name} lido com sucesso!!!")

        return pd.read_json(file)