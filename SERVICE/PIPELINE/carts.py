from DOMAIN.TRANSFORM.clean import Cleaned
from SERVICE.MANAGER.control import Control
from SERVICE.PIPELINE.users import Data_Users
from SERVICE.PIPELINE.products import Data_Product

import pandas as pd

class Data_Carts:
    def __init__(self) -> None:
        self.con = Control(name="carts", limit=5, update=2)
        self.Cleaned = Cleaned()
        self.data = Control(name="carts", limit=5, update=2).read()
        
        
    def bronze(self, data:pd.DataFrame) ->pd.DataFrame:
        self.con.save(status="raw", df=data)
        return data
    
    def silver(self) ->pd.DataFrame:
        users = Data_Users().search(status="cleaned")[["id", "name", "age", "gender"]]
        
        
        products = Data_Product().search(status="cleaned")
        data = self.data["data"]
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
            
            
            
        )
        data = pd.merge(
        data,
        products,
        left_on="product_id",
        right_on="id",
        how="left"
    )
        
        
        
        return data
    
    
print(Data_Carts().silver().columns)