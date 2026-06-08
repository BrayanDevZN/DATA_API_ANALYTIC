
from ADAPTER.CLIENT.data_request import Url_requests
from ADAPTER.REPOSITORY.control_json import Control_DataJson
from ADAPTER.REPOSITORY.control_parquet import Control_DataParquet
from ADAPTER.REPOSITORY.control_sql import Control_DataSql
from SERVICE.ROLE.limit import LimitService
from SERVICE.ROLE.update import UpdateService
from SERVICE.ROLE.version import VersionService
import os
import pandas as pd
from SERVICE.MANAGER.tasks import save

class Control: #CONTROLA OS ARQUIVOS, QUANDO VAI ATUALIZAR, O LIMITE E AS CAMADAS
    def __init__(self, name:str, update: int, limit: int) -> None:
        self.name = name
        self.up = update
        self.Limit = limit
    def update(self) -> bool:
        cleaned_version = VersionService.last("cleaned", self.name)

        if cleaned_version is not None:
            file = cleaned_version / f"{self.name}.parquet"

            if file.exists():
                return UpdateService(
                    name=str(file),
                    limit=self.up
                ).execute()

        raw_version = VersionService.last("raw", self.name)

        if raw_version is not None:
            file = raw_version / f"{self.name}.json"

            if file.exists():
                return UpdateService(
                    name=str(file),
                    limit=self.up
                ).execute()

        return True
            
    def read(self, get_status=None) ->pd.DataFrame:
        data = {
            "processed": Control_DataSql().read_sql,
            "cleaned": Control_DataParquet().read_parquet,
            "raw": Control_DataJson().read_json
        }
        if get_status is not None:
            if get_status in data.keys():
                return {"status":get_status, "data":data[get_status](name=self.name)}
            raise KeyError(f"not key {get_status}")
        up = self.update()

        if up:
            return {
            "status": "request",
            "data": Url_requests().request(name=self.name)
        }

        

        for c in data.keys():

            res = data[c](name=self.name)

            if res is not None:
                return {
                    "status": c,
                    "data": res
                }

        return {
            "status": "request",
            "data": Url_requests().request(name=self.name)
        }
            
    def limit(self, status: str) -> None:
        path = f"ADAPTER/STORAGE/{status.upper()}/{self.name}"
        LimitService(path=path, limit=self.Limit).execute()
            
    def save(self, df:pd.DataFrame, status:str) -> None:
        
        Data = save(name=self.name, df=df, status=status)
        if status != "processed":
            self.limit(status=status)
            
        return Data

        
        
       
        
            
            

                
            
        
        