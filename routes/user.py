from fastapi import APIRouter, HTTPException, Depends, Response, Form, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from config.db import conn
from models.users import users
from schemas.user import UserCreate, UserUpdate, UserResponse
from functions.token import (
    get_current_user,
    create_access_token,
    get_password_hash,
    verify_password,
    validate_token,
)

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración para JWT y bcrypt
SECRET_KEY = os.getenv("SECRET_KEY")  # Cambiar por una clave segura en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Instancia del enrutador
user_router = APIRouter()

# **Rutas para manejo de usuarios**

# Obtener todos los usuarios
@user_router.get("/users", response_model=list[UserResponse])
def get_all_users():
    """
    Obtiene una lista de todos los usuarios registrados en la base de datos.
    """
    try:
        users_list = conn.execute(users.select()).fetchall()
        if not users_list:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No se encontraron usuarios.")
        return users_list
    except SQLAlchemyError as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")


# Obtener un usuario por ID
@user_router.get("/users/id/{id}", response_model=UserResponse)
def get_user_by_id(id: int):
    """
    Obtiene un usuario por su ID.
    """
    try:
        with conn.begin():  # Manejo correcto de transacciones
            result = conn.execute(users.select().where(users.c.id == id))
            user = result.fetchone()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
        
        # Convierte el resultado en un diccionario
        return dict(user._mapping)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )


# Crear un nuevo usuario
@user_router.post("/users/create")
def create_user(name: str = Form(), email: str = Form(), password: str = Form()):
    """
    Crea un nuevo usuario en la base de datos.
    """
    try:
        hashed_password = get_password_hash(password)
        new_user = {"name": name, "email": email, "password": hashed_password}
        conn.execute(users.insert().values(new_user))
        conn.commit()
        return JSONResponse(
            status_code=201,
            content={"message": "Usuario creado exitosamente."}
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")


# Actualizar un usuario por ID
@user_router.put("/users/update/{id}", response_model=UserResponse)
def update_user_by_id(id: int, user_data: UserUpdate):
    """
    Actualiza la información de un usuario existente.
    """
    try:
        with conn.begin():  # Manejo correcto de transacciones
            result = conn.execute(users.update().where(users.c.id == id).values(user_data.dict()))
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
        
        return {"message": "Usuario actualizado exitosamente."}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )


# Eliminar un usuario por ID
@user_router.delete("/users/delete/{id}")
def delete_user_by_id(id: int):
    """
    Elimina un usuario de la base de datos por su ID.
    """
    try:
        result = conn.execute(users.delete().where(users.c.id == id))
        if result.rowcount == 0:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
        return Response(status_code=HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {str(e)}")


# Inicio de sesión
@user_router.post("/users/login")
def login(email: str = Form(...), password: str = Form(...)):
    """
    Inicia sesión con credenciales válidas y genera un token de acceso.
    """
    try:
        # Busca el usuario por su correo electrónico
        db_user = conn.execute(users.select().where(users.c.email == email)).first()
        
        if not db_user or not verify_password(password, db_user.password):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas."
            )
        
        # Crear un token de acceso
        token_data = {"id": db_user.id, "email": db_user.email}
        access_token = create_access_token(data=token_data)
        
        # Crear una respuesta de redirección con la cookie
        response = RedirectResponse(url="/users/dashboard", status_code=302)
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        return response
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )
