import pandas as pd
import os
class Control_DataParquet: #le e salva arquivos parquet
    
    @staticmethod
    def save_parquet(name:str, df:pd.DataFrame) -> None:
        
        df.to_parquet(f"ADAPTER/STORAGE/CLEANED/{name}/{name}.parquet", index=False)
        
    @staticmethod
    def read_parquet(name:str) -> pd.DataFrame|None:
        if os.path.exists(f"ADAPTER/STORAGE/CLEANED/{name}/{name}.parquet"):
            return pd.read_parquet(f"ADAPTER/STORAGE/CLEANED/{name}/{name}.parquet")
        
        return None
        