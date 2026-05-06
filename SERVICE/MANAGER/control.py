from DOMAIN.VALID.rule_file import Valid_arq
from DOMAIN.TRANSFORM.clean import Cleaned
from ADAPTER.CLIENT.data_request import Url_requests
from ADAPTER.REPOSITORY.control_json import Control_DataJson
from ADAPTER.REPOSITORY.control_parquet import Control_DataParquet
from ADAPTER.REPOSITORY.control_sql import Control_DataSql
from SERVICE.ROLE.limit import LimitService
from SERVICE.ROLE.update import UpdateService
import os
import pandas as pd

class Control:
    def __init__(self, name:str, update: int, limit: int) -> None:
        self.name = name
        self.up = update
        self.Limit = limit
    def update(self) -> bool:
        if (os.path.exists(f"ADAPTER/STORAGE/CLEANED/{self.name}")) and (self.name in os.listdir(f"ADAPTER/STORAGE/CLEANED")):
            name = os.listdir(f"ADAPTER/STORAGE/CLEANED/{self.name}")[-1]
            return UpdateService(name=f"ADAPTER/STORAGE/CLEANED/{self.name}/{name}", limit=self.Limit).execute()
        
        elif (os.path.exists(f"ADAPTER/STORAGE/RAW/{self.name}")) and (self.name  in os.listdir(f"ADAPTER/STORAGE/RAW")):
            name = os.listdir(f"ADAPTER/STORAGE/RAW/{self.name}")[-1]
            return UpdateService(name=f"ADAPTER/STORAGE/RAW/{self.name}/{name}", limit=self.Limit).execute()
            
    def read(self) ->pd.DataFrame:
        up = self.update()
        
        if up:
            return {"status": "request", "data":Url_requests().request(name=self.name)}
        data = {
            "processed":Control_DataSql().read_sql,
            "cleaned":Control_DataParquet().read_parquet,
            "raw":Control_DataJson().read_json,
            "request": Url_requests().request
        }
        
        
        
        for c in data.keys():
            res = data[c](name=self.name)
            if res is not None:
                return {"status": c, "data":res}
            
    def limit(self, status: str) -> None:
        path = f"ADAPTER/STORAGE/{status.upper()}/{self.name}"
        LimitService(path=path, limit=self.Limit).execute()
            
    def save(self, df:pd.DataFrame, status:str) -> None:
        
        
        
        data_save = {
            "raw":Control_DataJson().save_json,
            "cleaned":Control_DataParquet().save_parquet,
            "processed": Control_DataSql().save_sql
        }
        
        
        if not status in data_save.keys():
                raise KeyError(f"not key {status}")
        
        if status != "processed": 
            
            save_arq = os.makedirs(name=f"ADAPTER/STORAGE/{status.upper()}/{self.name}", exist_ok=True)
            self.limit(status=status)
            
        data_save[status](name=self.name, df=df)
            
        
       
        
            
            
aa = Control(name="products", limit=2, update=2)
data = aa.read()
print(data)
aa.save(status="cleaned", df=data["data"])

        
                
                
                
            
        
        