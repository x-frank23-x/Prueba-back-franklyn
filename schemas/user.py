from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: Optional[int]  
    email: EmailStr    
    name: str
    password:str           
    token:str  

    
# Esquema para crear un usuario
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


# Esquema para actualizar un usuario
class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]
    password: Optional[str] 


# Esquema para responder información de un usuario
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True   
