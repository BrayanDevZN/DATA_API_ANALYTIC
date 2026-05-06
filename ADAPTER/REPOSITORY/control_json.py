import json
import os
import pandas as pd
class Control_DataJson: #le e salva arquivos json
    @staticmethod
    def save_json(name:str, df:pd.DataFrame) -> None:
        df.to_json(
        f"ADAPTER/STORAGE/RAW/{name}/{name}.json",
        orient="records",
        indent=4,
        force_ascii=False
    )
    @staticmethod      
    def read_json(name:str) -> pd.DataFrame:
        if os.path.exists(f"ADAPTER/STORAGE/RAW/{name}/{name}.json"):
            with open(f"ADAPTER/STORAGE/RAW/{name}/{name}.json", "r") as f:
                return pd.DataFrame(json.load(f))
        
        return None