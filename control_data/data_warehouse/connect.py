import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

class SupabaseConnect:
    def __init__(self) ->None:
        load_dotenv()
        self.__host = os.getenv("DB_HOST")
        self.__name = os.getenv("DB_NAME")
        self.__user = os.getenv("DB_USER")
        self.__pass = os.getenv("DB_PASSWORD")
        self.__port = os.getenv("DB_PORT")
        
    def base_url(self):
        return f"postgresql+psycopg://{self.__user}:{self.__pass}@{self.__host}:{self.__port}/{self.__name}"#CONNECTA COM O BANCO
    
    def connect(self):
        engine = create_engine(self.base_url())#RETORNA A CONEXÃO
        
   