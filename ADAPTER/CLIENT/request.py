import requests
import pandas as pd
def request(url:str) -> pd.DataFrame| None: #essa função e pra fazer requisições 
    
    response = requests.get(url=url)
    if response.status_code != 200:
        return None
    
    return pd.DataFrame(response.json())
    