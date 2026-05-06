from DOMAIN.VALID.rule_file import Valid_arq
from DOMAIN.TRANSFORM.clean import Cleaned
from ADAPTER.CLIENT.data_request import Url_requests
from ADAPTER.REPOSITORY.control_json import Control_DataJson
from ADAPTER.REPOSITORY.control_parquet import Control_DataParquet
from ADAPTER.REPOSITORY.control_sql import Control_DataSql
from SERVICE.ROLE.limit import LimitService
from SERVICE.ROLE.update import UpdateService
from SERVICE.ROLE.version import VersionService
import os
import pandas as pd

class Control:
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
            
    def read(self) ->pd.DataFrame:
        up = self.update()

        if up:
            return {
            "status": "request",
            "data": Url_requests().request(name=self.name)
        }

        data = {
            "processed": Control_DataSql().read_sql,
            "cleaned": Control_DataParquet().read_parquet,
            "raw": Control_DataJson().read_json
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
        
        
        data_save = {
            "raw": Control_DataJson().save_json,
            "cleaned": Control_DataParquet().save_parquet,
            "processed": Control_DataSql().save_sql
        }

        if status not in data_save.keys():
            raise KeyError(f"not key {status}")

        version = VersionService.create()

        if status != "processed":

            os.makedirs(
                name=f"ADAPTER/STORAGE/{status.upper()}/{self.name}/{version}",
                exist_ok=True
            )

            self.limit(status=status)

        data_save[status](
            name=self.name,
            df=df,
            version=version
        )

        return version
            
        
       
        
            
            

                
            
        
        