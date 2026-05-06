import json
import os
from SERVICE.ROLE.version import VersionService
import pandas as pd
class Control_DataJson: #le e salva arquivos json
    @staticmethod
    def save_json(name: str, df: pd.DataFrame, version: str) -> None:
        df.to_json(
        f"ADAPTER/STORAGE/RAW/{name}/{version}/{name}.json",
        orient="records",
        indent=4,
        force_ascii=False
    )
    @staticmethod      
    def read_json(name:str) -> pd.DataFrame:
        version_path = VersionService.last(
            status="raw",
            name=name
        )

        if version_path is None:
            return None

        file = version_path / f"{name}.json"

        if not file.exists():
            return None

        return pd.read_json(file)