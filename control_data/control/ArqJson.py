import json
class ArchiveJson:
    def create_json(self, name:str, data:dict) -> None:
        with open(f"{name}.json", "w", encoding="utf-8") as f: #CRIA ARQUIVOS JSON
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    def read_json(self, name:str) -> dict | None:
        try:
            with open(f"{name}.json", "r") as f:  #LE ARQUIVOS JSON
                return json.load(f)
            
        except FileNotFoundError:
            
            return None