from sqlalchemy import create_engine

class Connect_engine: #essaa classe retorna a conexão com o banco
    def __init__(self, user:str, Pass:str, host:str, port: str, dbname:str) -> None:
        self.user = user
        self.Pass = Pass
        self.host = host 
        self.port = port
        self.db_name = dbname
        
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.Pass}@{self.host}:{self.port}/{self.db_name}"
    
    def execute(self):
        return create_engine(url=self.url())
        