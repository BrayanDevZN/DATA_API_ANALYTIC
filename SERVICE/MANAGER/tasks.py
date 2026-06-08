from INFRA.CONNECT.REDIS.main_connect import main_redis
import pandas as pd
from ADAPTER.REPOSITORY.control_json import Control_DataJson
from ADAPTER.REPOSITORY.control_parquet import Control_DataParquet
from ADAPTER.REPOSITORY.control_sql import Control_DataSql
import os
from SERVICE.ROLE.version import VersionService
app = main_redis()

@app.task(bind=True, max_retries=3)
def save(self, name:str, status:str, df:pd.DataFrame):
    try:
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
                    name=f"ADAPTER/STORAGE/{status.upper()}/{name}/{version}",
                    exist_ok=True
                )

                

        save = data_save[status](
                name=name,
                df=df,
                version=version
                
            ) if status !="processed" else data_save[status](
                name=name,
                df=df,
                
                
            )

        return version
            
    except Exception as e:
        raise self.retry(
            countdown=3,
            exc=e
            
        )