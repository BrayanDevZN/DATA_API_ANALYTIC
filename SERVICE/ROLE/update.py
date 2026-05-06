from DOMAIN.VALID.valid_func import Valid_func
import os
from datetime import datetime

class UpdateService: 
    def __init__(self, limit:int, name:str)->None:
        self.valid = Valid_func()
        self.limit = limit
        self.name = name
        self.last_date = self.last()
        
    def last(self) -> datetime:
        timestamp = os.path.getmtime(self.name)
        data = datetime.fromtimestamp(timestamp)
        return data
    
    def execute(self) ->bool:
        return True if  self.valid.update(last_date=self.last_date, days=self.limit) else False

        