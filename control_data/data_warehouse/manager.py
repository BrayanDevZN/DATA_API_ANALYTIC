from control_data.data_warehouse.df_toSql import toSql
from control_data.control.ArqJson import ArchiveJson
import pandas as pd
import os
class ManagerDW:
    def __init__(self, name:str,  Update: bool, dataframe=None):
        self.name = name 
        self.df = dataframe
        self.db = toSql(name=name, dataframe=dataframe, update=True if Update else False)
        self.up = Update
        
        
    def save_sql(self) -> None:
        self.db.df_to_sql()
        self.db.setup()
    
    def read_sql(self) ->dict:
        
        data = self.db.sql_to_df()
        if data is not None:
            arq = ArchiveJson()
            raw = arq.read_json(f"data/raw/{self.name}/{self.name}_date")["versions"]
            cleaned = arq.read_json(f"data/processed/{self.name}/{self.name}_date")["versions"]
            return {"name": self.name,"status": "processed", "data": self.db.sql_to_df(), "versions": {"raw": raw, "cleaned":cleaned}}
        
        return None
    
    
        
    
