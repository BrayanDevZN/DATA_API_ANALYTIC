from INFRA.CORE.config import Settings_urls
import pandas as pd
from ADAPTER.CLIENT.request import request

class Url_requests: #essa classe retorna as requisições das urls salvas no env
    def products(self) -> pd.DataFrame:
        return request(url=Settings_urls().products())
    
    def carts(self) -> pd.DataFrame:
        return request(url=Settings_urls().carts())
    
    def users(self) -> pd.DataFrame:
        return request(url=Settings_urls().users())
    
    def request(self, name:str) ->pd.DataFrame:
        data ={
            "users": self.users,
            "carts": self.carts,
            "products": self.products
                
        }
        if not name in data.keys():
            raise KeyError(f"not key {name}")
        
        return data[name.lower()]()
        