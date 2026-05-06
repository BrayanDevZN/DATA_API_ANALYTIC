import pandas as pd
from INFRA.CONNECT.main_connect import Engine_database

class Control_DataSql: #converte sql pra dataframe e salva dataframe em sql
    def __init__(self)-> None:
        self.engine = Engine_database()
        
    def read_sql(self, name:str) -> dict:
            try:
                df = pd.read_sql(f"processed_{name}", self.engine)

                if df.empty:
                    return None

                return df

            except Exception:
                return None
    def save_sql(self, name:str, df:pd.DataFrame) -> None:
        df.to_sql(name=f"processed_{name}",
                  con=self.engine,
                  if_exists="replace",
                  index=False)
        