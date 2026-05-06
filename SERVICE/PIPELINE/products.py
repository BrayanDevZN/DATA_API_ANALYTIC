from DOMAIN.TRANSFORM.clean import Cleaned
from SERVICE.MANAGER.control import Control
import pandas as pd

class Data_Product:
    def __init__(self) -> None:
        self.con = Control(name="products", limit=5, update=2)
        self.Cleaned = Cleaned()
        self.data = Control(name="products", limit=5, update=2).read()
        
    def bronze(self, data:pd.DataFrame) -> pd.DataFrame:
       
       self.con.save(df=data, status="raw")
       return data
    
    def silver(self, data:pd.DataFrame) -> pd.DataFrame:
        
        
        data = self.Cleaned.clean_dict(df=data, update=True)[['id', 'title', 'description', 'category', 'price', 'discountPercentage',
       'rating', 'stock',   'meta.createdAt', 'meta.updatedAt', 'availabilityStatus']]
        data = self.Cleaned.clean_null_columns(df=data)
        data = self.Cleaned.clean_null_line(df=data)
        data = self.Cleaned.normalize(df=data)
        data["meta.createdAt"] = pd.to_datetime(data["meta.createdAt"])
        data['meta.updatedAt'] = pd.to_datetime(data['meta.updatedAt'])
        self.con.save(df=data, status="cleaned")
        return data
    
    def gold(self, data:pd.DataFrame) -> pd.DataFrame:
        
        result = data.groupby("category").agg(
        total_products=("id", "count"),
        avg_price=("price", "mean"),
        avg_rating=("rating", "mean"),
        total_stock=("stock", "sum"),
        avg_discount=("discountPercentage", "mean")
    ).reset_index().round(2)
        
        self.con.save(df=result, status="processed")

        return result
    
    def search(self, status:str) -> pd.DataFrame:
        return self.con.read(get_status=status)
    
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
            
        
        
        
        
   
