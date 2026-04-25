from control_data.data_warehouse.connect import SupabaseConnect
from sqlalchemy import text
import pandas as pd
class toSql:
    def __init__(self, name:str, dataframe=None, update=False)->None:
        self.engine = SupabaseConnect().connect()
        self.name = name
        self.df = dataframe
        self.update = update
        
        
    def df_to_sql(self) -> None: #CONVERTE O DATAFRAME PRA SQL
        if self.df is None:
            return
        up = "replace" if self.update else "append"
        self.df.to_sql(
            name=self.name,
            con=self.engine,
            if_exists=up,
            index=False
        )
    
       
    def sql_to_df(self) -> pd.DataFrame: #CONVERTE UMA TABELA SQL PRA DATAFRAME
        try:
            df = pd.read_sql(
                f"SELECT * FROM {self.name}",
                self.engine
            )
            return df
        except Exception as e:
            return None
        
        
    def setup(self) ->None: #CRIA UMA COLUNA DE DATA
        with self.engine.begin() as cur:
            cur.execute(text(
                F"""
                alter table {self.name}
                add column if not exists created_at timestamp default current_timestamp"""          
            ))
            
   
        
        
    
        
    
        
    
        
    
        