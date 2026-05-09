from DOMAIN.TRANSFORM.clean import Cleaned
from SERVICE.MANAGER.control import Control
import pandas as pd

class Data_Users:
    def __init__(self)-> None:
        self.con = Control(name="users", limit=5, update=2)
        self.Cleaned = Cleaned()
        self.data = Control(name="users", limit=5, update=2).read()
        
    def bronze(self, data:pd.DataFrame) -> pd.DataFrame:
        
        self.con.save(df=data, status="raw")
        return data
    
    def silver(self, data: pd.DataFrame) -> pd.DataFrame:
        
        data = self.Cleaned.clean_dict(df=data)
        data["name"] = data["firstName"] + " " + data['lastName']
        data = data[['id', 'name',  'age', 'gender', 'address.country', 'address.state', 'address.city', 'company.name', 'company.title']]
        data = self.Cleaned.clean_null_columns(df=data)
        data = self.Cleaned.clean_null_line(df=data)
        data = self.Cleaned.normalize(df=data)
        data = data.rename(
            columns={
               "address.country": "country",
               "address.state": "state",
               "address.city":"city",
               "company.name": "company",
               "company.title": "job"
                   
            }
        )
        
        self.con.save(status="cleaned", df=data)
        return data
    
    def gold(self, data:pd.DataFrame) -> pd.DataFrame:
        
        data = data.groupby(["state", "city"]).agg(
            quantity_clients = ("id", "count"),
            mean_age = ("age", "mean"),
            max_job = ("job", lambda x: x.mode().iloc[0]),
            max_gender= ("gender", lambda x: x.mode().iloc[0])
        ).reset_index().sort_values(by="quantity_clients", ascending=False)
        self.con.save(status="processed", df=data)
        return data
    
    def search(self, status:str) -> pd.DataFrame:
        data = self.con.read(get_status=status)
        if data is None:
            self.execute()
            
        return data
    
    def execute(self) -> pd.DataFrame:
        
        if self.data["status"] == "processed":
            return self.data["data"]
            
        match self.data["status"]:
            case "cleaned":
                result = self.gold(data=self.data["data"])
                
            case "raw":
                df = self.silver(data=self.data["data"])
                result = self.gold(data=df)
            case "request":
                df = self.bronze(data=self.data["data"])
                new_df = self.silver(data=df)
                result = self.gold(data=new_df)
            
            
            
        return result
    
    
