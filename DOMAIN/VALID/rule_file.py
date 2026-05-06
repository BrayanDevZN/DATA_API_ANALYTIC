from pydantic import BaseModel, field_validator
from typing import Literal
class Valid_arq(BaseModel): #valida a camada do arquivo
    filename: str
    layer: Literal["raw", "cleaned", "processed"]

    @field_validator("layer", mode="before")
    def detect_layer(cls, v, info):
        name = info.data["filename"].lower()

        if "raw" in name:
            return "raw"
        elif "cleaned" in name:
            return "cleaned"
        elif "processed" in name:
            return "processed"

        raise ValueError("camada não identificada")