from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import  HTTPException, Depends, Security,Request
from fastapi.security import OAuth2PasswordBearer
from starlette.status import ( 
    HTTP_401_UNAUTHORIZED,
 )
from passlib.context import CryptContext
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

security = HTTPBearer()
# Configuraciones JWT y bcrypt
SECRET_KEY = os.getenv("SECRET_KEY",)  # Cambia por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Funciones auxiliares

# Crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificar contraseña
def verify_password(plain_password:str, hashed_password:str):
    return bcrypt_context.verify(plain_password, hashed_password)

# Generar hash de una contraseña
def get_password_hash(password):
    return bcrypt_context.hash(password)

# Decodificar y validar el token


def validate_token(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implementa la lógica para validar el token
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": 1, "username": "example"} 