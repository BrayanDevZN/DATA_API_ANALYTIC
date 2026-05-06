import pandas as pd
import os
from SERVICE.ROLE.version import VersionService
class Control_DataParquet: #le e salva arquivos parquet
    
    @staticmethod
    def save_parquet(
    name: str,
    df: pd.DataFrame,
    version: str
    ) -> None:

        df.to_parquet(
            f"ADAPTER/STORAGE/CLEANED/{name}/{version}/{name}.parquet",
            index=False
        )
            
    @staticmethod
    def read_parquet(name:str) -> pd.DataFrame|None:
        version_path = VersionService.last(
        status="cleaned",
        name=name
        )

        if version_path is None:
            return None

        file = version_path / f"{name}.parquet"

        if not file.exists():
            return None

        return pd.read_parquet(file)