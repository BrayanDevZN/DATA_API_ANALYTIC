from INFRA.CORE.config import Settings_database
from INFRA.CONNECT.DATABASE.engine import Connect_engine

def Engine_database(): #essa função serve pra chamar Settings_database e Connect_database e juntar
    data = Settings_database()
    return Connect_engine(user=data.user(), dbname=data.name(), port=data.port(), host=data.host(), Pass=data.password()).execute()