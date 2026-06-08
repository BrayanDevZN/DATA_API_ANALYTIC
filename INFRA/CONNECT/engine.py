from sqlalchemy import create_engine
import logging
logger = logging.getLogger(__name__)
class Connect_engine: #essaa classe retorna a conexão com o banco
    def __init__(self, user:str, Pass:str, host:str, port: str, dbname:str) -> None:
        self.user = user
        self.Pass = Pass
        self.host = host 
        self.port = port
        self.db_name = dbname
        
    def url(self) -> str:
        logger.info("Montando a url para a conexão do banco...")
        return f"postgresql+psycopg2://{self.user}:{self.Pass}@{self.host}:{self.port}/{self.db_name}"
    
    def execute(self):
        logger.info("Fazendo conexão...")
        return create_engine(url=self.url())
        