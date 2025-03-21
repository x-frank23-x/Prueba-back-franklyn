from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    id: Optional[int]  
    name: str
    price:int
    description:str  
