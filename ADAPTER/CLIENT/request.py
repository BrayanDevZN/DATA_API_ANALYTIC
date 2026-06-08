import requests
import pandas as pd
import logging
logger = logging.getLogger(__name__)
def request(url:str) -> pd.DataFrame| None: #essa função e pra fazer requisições 
    logger.info(f"Fazendo a requisição para {url}...")
    response = requests.get(url=url)
    if response.status_code != 200:
        logger.warning(f"A requisição de {url} falhou!!")
        return None
    
    return pd.DataFrame(response.json())
    