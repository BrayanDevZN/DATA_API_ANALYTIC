from fastapi import FastAPI
from typing import Literal
from SERVICE.MANAGER.main import Main_Data
app = FastAPI()

@app.get("/carts")
def carts(Layer:Literal["raw", "cleaned", "processed"] = None):
    data = Main_Data().Carts(Layer)
    return data

@app.get("/products")
def product(Layer:Literal["raw", "cleaned", "processed"] = None):
    data = Main_Data().Product(Layer)
    return data

@app.get("/users")
def users(Layer:Literal["raw", "cleaned", "processed"] = None):
    data = Main_Data().Users(Layer)
    return data
