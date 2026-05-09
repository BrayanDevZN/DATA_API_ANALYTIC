from pathlib import Path
from dotenv import load_dotenv
import os
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

class Settings_urls: #retorna as urls das requisições
    def products(self) -> str:
        return os.getenv("url_products")
    
    def carts(self) -> str:
        return os.getenv("url_carts")
    
    def users(self) -> str:
        return os.getenv("url_users")
    
class Settings_database: #retorna os dados do banco
    
    def host(self) -> str:
        return os.getenv("DB_HOST")                     
    def name(self) -> str:
        return os.getenv("DB_NAME")
                                                       
    def port(self) -> str:
        return os.getenv("DB_PORT")                                                      
                                                        
    def user(self) -> str:
        return os.getenv("DB_USER")
    
    def password(self) -> str:
        return os.getenv("DB_PASSWORD")  
                                                   
    
    