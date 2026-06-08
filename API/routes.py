from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Literal
from SERVICE.MANAGER.main import Main_Data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://datapilotplataform.com",
        "datapilotplataform.com"
        
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/carts")
def carts(Layer: Literal["raw", "cleaned", "processed"] = None):
    data = Main_Data().Carts(Layer)
    return data

@app.get("/products")
def product(Layer: Literal["raw", "cleaned", "processed"] = None):
    data = Main_Data().Product(Layer)
    return data

@app.get("/users")
def users(Layer: Literal["raw", "cleaned", "processed"] = None):
    data = Main_Data().Users(Layer)
    return data