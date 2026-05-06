import os
import shutil
class ManagerFolder:
    def __init__(self, name:str):
        self.name = name
              
        
    def create_folder(self) -> None: #CRIA A PASTA SE NÃO EXISTIR
        os.makedirs(self.name, exist_ok=True)
    
    def move_archive(self, archive:str) -> None: #MOVE O ARQUIVO PRA PASTA
        if not archive in os.listdir(self.name):
            shutil.move(archive, self.name)
        
    def rename(self, name:str, new_name:str) ->None: #MUDA O NOME DO ARQUIVO
        
        if os.path.exists(f"{self.name}/{name}") and (name != new_name):
            shutil.move(name, new_name)
        else:
            raise FileNotFoundError(f"archive {name} not found")
        
    def delete(self, values: str | list) ->None: #DELETA O ARQUIVO OU PASTA
        if isinstance(values, list):
            for i in values:
                if os.path.exists(f"{self.name}/{i}"):
                    os.remove(f"{self.name}/{i}")
                else:
                    print(f"DELETE/ {i} not exists")
        else:
            if os.path.exists(f"{self.name}/{values}"):
                    os.remove(f"{self.name}/{values}")
            else:
                    print(f"DELETE/ {values} not exists")
                    
        
            if (values == "all") and (os.path.exists(values)):
                
                shutil.rmtree("data_lake")
          
    
        
        
        
        
        
        