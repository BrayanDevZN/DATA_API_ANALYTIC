
from control_data.data_lake.manager import ManagerRaw
from control_data.data_processed.Manager import ManagerPRQ
from control_data.data_warehouse.manager import ManagerDW

class ManagerControl:
    def __init__(self, name:str, url:str, update=None, Limit=None, get_api=None, dataframe=None)->None:
        self.name = name
        self.url = url
        self.up = update
        self.limit = Limit
        self.df = dataframe
        self.get = get_api
    
    def read_raw(self) -> dict | None:
        data = ManagerRaw(self.name, self.url, update=self.up, limit=self.limit)
        return data.get_data(get_api=True if self.get is not None else False)
    
    def read_cleaned(self) ->dict | None:
        data = ManagerPRQ(name=self.name,df=self.df if self.df is not None else None, update=self.up, limit=self.limit).get_data()
        return data
    
    def read_processed(self) -> dict | None:
        data = ManagerDW(name=self.name, Update=True if self.up is not None else False, dataframe=self.df)
        return data.read_sql()
    def save_cleaned(self) ->None:
        data = ManagerPRQ(name=self.name,df=self.df if self.df is not None else None, update=self.up, limit=self.limit).save()
        
    
    def save_sql(self, update=None) ->None:
        if self.df is None:
            raise ValueError("error line 7: (...dataframe=None), expected a dataframe.")
        ManagerDW(name=self.name, Update=True if update is not None else False, dataframe=self.df).save_sql()
        print(f"{self.name} saved!")
    
    def data(self, value:str) -> dict | None:
        match value:
            case "processed":
                return self.read_processed()
            case "cleaned":
                return self.read_cleaned()
            case "raw":
                return self.read_raw()
            case _:
                raise ValueError(f"Invalid data type: {value}")
            
    def read_data(self) ->dict | None:
        if self.get is not None:
            return self.read_raw()
        
        all_data = ["processed","cleaned","raw"]
        for v in all_data:
            data = self.data(v)
            if data is not None:
                break
        return data
    
    
aa = ManagerControl(name="product", url="https://dummyjson.com/products?limit=0", Limit=4, update=2)
df = aa.read_data()

ab = ManagerControl(name="product", dataframe=df["data"], Limit=4, update=2, url="https://dummyjson.com/products?limit=0")
ab.save_cleaned()
print(ab.read_data())
    
        
        
    
        
        
        
        
        
        
    
    
            
        
    