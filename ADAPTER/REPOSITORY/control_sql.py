import pandas as pd
import logging
logger = logging.getLogger(__name__)
from INFRA.CONNECT.DATABASE.main_connect import Engine_database

class Control_DataSql: #converte sql pra dataframe e salva dataframe em sql
    def __init__(self)-> None:
        self.engine = Engine_database()
        
    def read_sql(self, name:str) -> dict:
            try:
                logger.info(f"Lendo dados de {name} na camada processed...")
                df = pd.read_sql(f"processed_{name}", self.engine)

                if df.empty:
                    logger.warning(f"Não existe {name} na camada processed!!")
                    return None
                
                logger.info(f"Arquivo {name} lido com sucesso!!!")

                return df

            except Exception:
                return None
    def save_sql(self, name:str, df:pd.DataFrame) -> None:
        logger.info(f"Salvando dados de {name} na camada processed...")
        df.to_sql(name=f"processed_{name}",
                  con=self.engine,
                  if_exists="replace",
                  index=False)
        
        logger.info("Dados salvos!!")
        