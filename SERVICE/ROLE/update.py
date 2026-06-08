from DOMAIN.VALID.valid_func import Valid_func
import os
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
class UpdateService:
    def __init__(self, limit: int, name: str) -> None:
        self.valid = Valid_func()
        self.limit = limit
        self.name = name
        self.last_date = self.last()

    def last(self) -> datetime:
        timestamp = os.path.getmtime(self.name)
        logger.info(f"Conferindo as ultimas datas de {self.name}...")
        
        return datetime.fromtimestamp(timestamp)

    def execute(self) -> bool:
        limit =  self.valid.update(
            last_date=self.last_date,
            days=self.limit
        )
        if limit:
            logger.info(f"Dia de atualização, {self.name} vai ser atualizado!!")
            
        logger.info(f"{self.name} ainda não vai ser atualizado!!")
        return limit