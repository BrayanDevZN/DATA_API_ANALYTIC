from datetime import datetime, timedelta
class Valid_func: #serve pra validar as funcionalidades update e limit
    @staticmethod
    def update(days:int, last_date:datetime) -> bool:
        now = datetime.now()

        return now - last_date > timedelta(days=days)
    
    @staticmethod
    def limit(lenght:list,limit:int) -> bool:
        return limit >=len(lenght)
        
