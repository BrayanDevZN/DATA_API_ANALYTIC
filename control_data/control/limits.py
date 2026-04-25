from control_data.control.ArqJson import ArchiveJson
from control_data.control.folder_control import ManagerFolder
class setup:
    def __init__(self)->None:
        self.Json = ArchiveJson()
   
    def Update(self, name_folder:str, name:str, limit:int) -> bool:#DECIDE DE QUANTAS EM QUANTAS REQUISIÇÕES VAI ATUALIZAR
        
            data = self.Json.read_json(f"control_data/data/{name_folder}/{name}/update")
            if data is None:
                data = {"min": 0, "max":limit}
                
            data["min"] +=1
            if data["min"] >= data["max"]:
                data["min"] = 0
                self.Json.create_json(f"control_data/data/{name_folder}/{name}/update", data)
                return True
                
            self.Json.create_json(f"control_data/data/{name_folder}/{name}/update", data)
          
            
            return  False
        
    
    def limit(self, name_folder:str, name:str, limit:int) -> None:  #DEFINE O LIMITE
        data = self.Json.read_json(f"control_data/data/{name_folder}/{name}/{name}_date")
        dates = data["versions"]
        print("DATES:", dates)
        print("LEN:", len(dates), "LIMIT:", limit)

        folder = ManagerFolder(f"control_data/data/{name_folder}/{name}")

        while len(dates) > limit:
            old_date = dates[0]
            old_file_name = f"{name}_{old_date}.json"

            folder.delete(old_file_name)
            del dates[0]

        self.Json.create_json(
            f"control_data/data/{name_folder}/{name}/{name}_date",
            {"versions": dates}
        )