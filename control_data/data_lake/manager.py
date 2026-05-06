import pandas as pd
import os
from control_data.data_lake.extract import Extract
from control_data.control.date import VersionDate
from control_data.control.folder_control import ManagerFolder
from control_data.control.ArqJson import ArchiveJson
from control_data.control.limits import setup

class ManagerRaw:
    def __init__(self, name:str, url:str, limit=None , update=None)->None:
        self.name = name
        self.url = url
        self.Limit = limit
        self.update = update
        self.Folder = ManagerFolder(name)
        self.Date = VersionDate(name)
        self.Json = ArchiveJson()
        self.Extract = Extract(url)
        
    def save(self) -> None: #SALVA OS ARQUIVOS EM JSON
        request = self.Extract.request_api()
        if request is None:
            return False
        if not os.path.exists("control_data/data/raw"):
            ManagerFolder("control_data/data").create_folder()
        if not "raw" in os.listdir("control_data/data"):
            ManagerFolder("control_data/data/raw").create_folder()
            
    
        if os.path.exists(f"control_data/data/raw/{self.name}/{self.name}_date.json"):
            
            date_folder = VersionDate(f"control_data/data/raw/{self.name}/{self.name}")
            date_folder.add()
            last_date = date_folder.last_date()
            
        else:
            self.Date.add()      
            last_date = self.Date.last_date()
        
        name_archive = f"{self.name}_{last_date}"
        
        if not self.name in os.listdir("control_data/data/raw"):
            self.Folder.create_folder()
                  
        folder = ManagerFolder("control_data/data/raw")
        
        self.Json.create_json(name_archive, request)
        
        folder.move_archive(self.name)
        
        new_folder = ManagerFolder(f"control_data/data/raw/{self.name}")
        
        new_folder.move_archive(f"{name_archive}.json")
        
        new_folder.move_archive(f"{self.name}_date.json")
        return True
       
    
    def limit(self) -> None:  #DEFINE O LIMITE DE ARQUIVOS
        if self.Limit is not None:  
            Set = setup()
            Set.limit(name_folder="raw", name=self.name, limit=self.Limit)
        
    def Update(self) -> bool:#DEFINA A QUANTIDADE DE REQUISIÇÕES PRA ATUALIZAR
        if self.update is not  None:
            set = setup()
            return set.Update(name_folder="raw", name=self.name, limit=self.update)
            
    
    def get_data(self, get_api: bool) ->dict: #RETORNA O DATAFRAME
    
        if not os.path.exists(f"control_data/data/raw/{self.name}"):
            save = self.save()
        self.limit()   
        Up = self.Update()
        if Up or get_api:
            
            self.save()
        self.limit()
       
        dates = sorted(self.Json.read_json(f"control_data/data/raw/{self.name}/{self.name}_date")["versions"])
        data = self.Json.read_json(f"control_data/data/raw/{self.name}/{self.name}_{dates[-1]}")
        
        return {"name":f"control_data/data/raw/{self.name}/{self.name}_{dates[0]}", "status": "raw", "data":pd.DataFrame(data), "versions": dates}
                    
                
        
            
        
         

        
        
        
        

        
        