from control_data.control.ArqParquet import toParquet
from control_data.control.ArqJson import ArchiveJson
from control_data.control.date import VersionDate
from control_data.control.folder_control import ManagerFolder
from control_data.control.limits import setup
import pandas as pd
import os
class ManagerPRQ:
    def __init__(self, name: str, df=None , limit = None, update=None) -> None:
        self.name = name
        self.df = df
        self.parquet = toParquet()
        self.Json = ArchiveJson()
        self.setup = setup()
        self.date = VersionDate(f"control_data/data/processed/{self.name}/{self.name}")
        self.limit = limit
        self.up = update
        self.Set = setup()
    def save(self) ->None: #SALVA O ARQUIVO E SUAS VERSÕES
        processed_data = ManagerFolder(f"control_data/data/processed/{self.name}").create_folder()  if not os.path.exists("control_data/data/processed") else None
        if not "processed" in os.listdir("control_data/data"):
            ManagerFolder("processed").create_folder()
            ManagerFolder("control_data/data").move_archive("processed")
        if not self.name in os.listdir("control_data/data/processed"):
             ManagerFolder(self.name).create_folder()
             ManagerFolder("control_data/data/processed").move_archive(self.name)
            
            
        self.date.add()
        
        last_date = self.date.last_date()
        name_archive = f"{self.name}_{last_date}"
        toParquet().create_parquet(name_archive, self.df, self.name)
        
    def Limit(self) -> None:# DEFINE O LIMITE DE ARQUIVOS
        if self.limit is not None:  
            
            self.Set.limit(name_folder="processed", name=self.name, limit=self.Limit)
            
    def Update(self) ->None: #DEFINA A QUANTIDADE DE REQUISIÇÕES PRA ATUALIZAR
        if self.up is not None:
            
            return self.Set.Update(name_folder="processed", name=self.name, limit=self.up)
        
    def get_data(self) ->dict: #RETORNA O DATAFRAME
        if not os.path.exists(f"control_data/data/processed/{self.name}"):
            return None
        if self.df is not None:
            Up = self.Update()
            if Up or (not os.path.exists(f"control_data/data/processed/{self.name}")) :
                self.save()
            self.Limit()
       
        dates = self.Json.read_json(f"control_data/data/processed/{self.name}/{self.name}_date")["versions"]
        data = self.parquet.read(name_folder=self.name, name=f"{self.name}_{dates[-1]}")
       
        return {"name": f"control_data/data/processed/{self.name}/{self.name}_{dates[-1]}"  , "status": "cleaned", "data":data, "versions":dates}
        
        
           
        
