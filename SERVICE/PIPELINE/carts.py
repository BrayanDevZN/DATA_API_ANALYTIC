from DOMAIN.TRANSFORM.clean import Cleaned
from SERVICE.MANAGER.control import Control
from SERVICE.PIPELINE.users import Data_Users
from SERVICE.PIPELINE.products import Data_Product
import numpy as np
import pandas as pd

class Data_Carts:
    def __init__(self) -> None:
        self.con = Control(name="carts", limit=5, update=2)
        self.Cleaned = Cleaned()
        self.data = Control(name="carts", limit=5, update=2).read()
        
        
    def bronze(self, data:pd.DataFrame) ->pd.DataFrame:
        self.con.save(status="raw", df=data)
        return data
    
    def silver(self, data:pd.DataFrame) ->pd.DataFrame:
        users = Data_Users().search(status="cleaned")["data"][["id", "name", "age", "gender", 'country', 'state', 'city']]
        
        
        products = Data_Product().search(status="cleaned")["data"][["id", "title", "category"]]
       
        data = self.Cleaned.clean_dict(df=data).rename(columns={
            "id": "cart_id"
        })
        data = self.Cleaned.clean_dict(df=self.Cleaned.clean_list(df=data)).rename(columns={
            "id": "product_id"
        })
        data = data[['cart_id', 'userId','product_id', 'totalProducts', 'totalQuantity',
        'title', 'price', 'quantity', 'total', 'discountPercentage',
       'discountedTotal']]
        
        data = pd.merge(
            users,
            data,
            left_on="id",
            right_on="userId",
            how="left"
            
            
            
        )[[ 'name', 'age', 'gender', 'country', 'state', 'city', 'product_id',   'totalProducts', 'totalQuantity',  'price', 'quantity', 'total',
       'discountPercentage', 'discountedTotal']]
        
        data = pd.merge(
            products,
            data,
            left_on="id",
            right_on="product_id",
            how="left"
        )[[ 'name', 'age', 'gender', 'country', 'state', 'city', 'title', 'category', 'price', 'quantity', 'total',
       'discountPercentage', 'discountedTotal']]
        
        data = self.Cleaned.clean_null_columns(df=data)
        data = self.Cleaned.clean_null_line(df=data)
        data = self.Cleaned.normalize(df=data)
        
        self.con.save(status="cleaned", df=data)
        
        return data
    
    def gold(self, data:pd.DataFrame) -> pd.DataFrame:
        
        data["range_age"] = np.where(
            data["age"] <= 27,
            "jovem (18 a 27)",
            np.where(
                 (data["age"] > 27) & (data["age"] <= 45),
                 "adulto (28 a 45)",
                 "mais velho(45+)"
            )        
            
        )
        data = data.groupby([ 'country', 'state', 'city']).agg(
            max_range_age=("range_age", lambda x: x.mode().iloc[0]),
            max_category=("category", lambda x: x.mode().iloc[0]),
            max_product=("title",lambda x: x.mode().iloc[0]),
            max_gender=("gender", lambda x: x.mode().iloc[0]),
            mean_quantity=("quantity", "mean"),
            mean_total=("total", "mean"),
            mean_percentage=("discountPercentage", "mean"),
            mean_discountedTotal=("discountedTotal", "mean")
        ).round(2).reset_index().sort_values(by= "mean_discountedTotal", ascending=False)
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
    
    
                
