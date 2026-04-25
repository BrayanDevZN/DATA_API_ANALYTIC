import requests
class Extract:
    def __init__(self, url:str) -> None:
        self.url = url
        
    def request_api(self) -> dict:
        
        data = requests.get(self.url)    #AQUI EU FAÇO A REQUISÇÃO E RETORNO EM JSON
        if data.status_code !=200:
            return None
        return data.json()    
    
        