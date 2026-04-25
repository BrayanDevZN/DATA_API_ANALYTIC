from datetime import datetime
from control_data.control.ArqJson import ArchiveJson
class VersionDate:
    def __init__(self, name:str) ->None:  
          
        self.name = name if "_date" in name else name + "_date"
        self.Json = ArchiveJson()
        self.date = datetime
        self.archive = self.read()
        
        
    def read(self) -> dict:
        data = self.Json.read_json(self.name)   #LE O ARQUIVO JSON QUE CONTEM A DATA DAS VERSOES
        if data is None:
            data = {"versions": []}
            
        return data
    
    def add(self) -> None:      #ADICONA A TEMPO ATUAL NO ARQUIVO, E CASO HAJA O PARAMETRO "LIMIT", ELE SO VAI ADICIONAR ATE CHEGAR NESSA QUANTIDADE, AI DEPOIS, ELE VAI APAGAR O DADO MAIS ANTIGO PRA MANTER A QUANTIDADE LIMITE
        now = self.date.now().strftime("%Y-%m-%d_%H-%M-%S") 
        self.archive["versions"].append(now)
        self.Json.create_json(self.name, self.archive)
        
    def last_date(self) ->str | None: #RETORNA A ULTIMA DATA ADICIONADA    
        return self.archive["versions"][-1] if self.archive["versions"] else None
    
    
    def search(self, date:str) -> str | bool: #CASO QUEIRA SABER DE UMA DATA ESPECIFICA, ELE VERIFICA SE EXISTE AQUELA DATA
        if date in self.archive["versions"]:
            return date
        return False
    
    def reset(self) -> None:  #ELE REMOVE TODAS AS DATAS ADICIONADAS
        self.archive["versions"] = []
        self.Json.create_json(self.name, self.archive)
        
    
    

        
        
    
        
        
        
        
    
        
        