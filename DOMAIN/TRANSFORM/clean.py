from ADAPTER.CLIENT.data_request import Url_requests
import pandas as pd


class Cleaned:
    
    @staticmethod
    def clean_dict(df:pd.DataFrame, update=False) -> pd.DataFrame:  #EXPANDE COLUNAS QUE SÃO DICT, E DEIXA SO ELAS
        if update:
            columns_del = [c for c in list(df.columns) if  not isinstance(df[c].iloc[0], dict)]
            df = df.drop(columns=columns_del)
        
        columns_dict = [c for c in list(df.columns) if isinstance(df[c].iloc[0], dict)]
        
        for c in columns_dict:
                new_df = pd.json_normalize(df[c])
                for i in  list(new_df.columns):
                    if i in list(df.columns):
                        df = df.drop(columns=[i])
                        
                    df[i] = new_df[i]
                    
        df = df.drop(columns=columns_dict)
                    
                
            
                
        return df
    
    @staticmethod
    def clean_list(df:pd.DataFrame) -> pd.DataFrame: #PEGA O CONTEUDO DENTRO DAS COLUNAS QUE SÃO LIST
        columns_list = [c for c in list(df.columns) if isinstance(df[c].iloc[0], list)]
        for c in columns_list:
            if len(df[c].iloc[0]) ==1:
                df[c] = df[c].apply(lambda x: x[0])
            
            else:
                df = df.explode(c)
            
        return df
    
    @staticmethod
    def clean_null_columns(df:pd.DataFrame) -> pd.DataFrame: #REMOVE AS COLUNAS QUE NO QUAL OS DADOS SÃO MAIS DE 30% VAZIOS
        df = df.drop_duplicates()
        columns = [c for c in list(df.columns) if (df[c].isna().mean()*100) > 30]
        df = df.drop(columns=columns)
        return df
    
    @staticmethod
    def clean_null_line(df:pd.DataFrame, fill=None) -> None: #LIMPA AS LINHAS VAZIAS, CASO O PARAMETRO fill ESTEJE PREENCHIDO, ELE SUBSTITUI AS LINHAS VAZIAS POR ESSE VALOR
        if fill is not None:
            df = df.fillna(fill)
            
            return df
        
        df = df.dropna()
        
        return df
    
    @staticmethod
    def normalize(df:pd.DataFrame) -> pd.DataFrame:
        for c in list(df.columns):
            if isinstance(df[c].iloc[0], str):
                df[c] = df[c].str.lower().str.capitalize()
            
        return df
    
    
        
    

                
                
