from celery import Celery
import logging
import ssl
logger = logging.getLogger(__name__)
def app(backend:str, broker:str):
    logger.info("Fazendo conexão com Redis...")
    app = Celery(
        "tasks",
        backend=backend,
        broker=broker
    )
  
    logger.info("Conexão feita com sucesso!!")
    return app
    

    