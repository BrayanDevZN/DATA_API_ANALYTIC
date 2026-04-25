import pandas as pd
import os
class toParquet:
        
    def create_parquet(self, name:str, df:pd.DataFrame, name_folder:str) -> None:#CRIA ARQUIVO PARQUET
        df.to_parquet(f"control_data/data/processed/{name_folder}/{name}.parquet", index=False)
        
    def read(self, name:str, name_folder:str) -> pd.DataFrame: #LE ARQUIVO PARQUET
        data = f"control_data/data/processed/{name_folder}/{name}"
        if os.path.exists(f"{data}.parquet"):
            return pd.read_parquet(f"{data}.parquet")
        return None
        