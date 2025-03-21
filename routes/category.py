from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Annotated, List
from schemas.category import Category
from models.category import category
from config.db import conn
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

category_router = APIRouter()


# Ruta: Obtener todas las categorías
@category_router.get("/category", response_model=List[Category], status_code=HTTP_200_OK)
def category_all():
    """
    Obtiene todas las categorías disponibles.
    """
    try:
        category_list = conn.execute(select([category])).fetchall()
        return [dict(row._mapping) for row in category_list]
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}",
        )


# Ruta: Obtener categoría por ID
@category_router.get("/category/{category_id}", response_model=Category, status_code=HTTP_200_OK)
def get_category_by_id(category_id: int):
    """
    Obtiene una categoría por su ID.
    """
    try:
        category_data = conn.execute(
            category.select().where(category.c.id == category_id)
        ).first()
        if not category_data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return dict(category_data._mapping)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la categoría: {str(e)}",
        )


# Ruta: Crear categoría
@category_router.post("/category/create", response_model=Category, status_code=HTTP_201_CREATED)
def category_create(name: Annotated[str, Form(...)]):
    """
    Crea una nueva categoría.
    """
    try:
        existing_category = conn.execute(
            category.select().where(category.c.name == name)
        ).first()
        if existing_category:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="La categoría ya existe"
            )

        result = conn.execute(category.insert().values(name=name))
        conn.commit()

        created_category = conn.execute(
            category.select().where(category.c.id == result.lastrowid)
        ).first()
        return dict(created_category._mapping)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la categoría: {str(e)}",
        )


# Ruta: Actualizar categoría
@category_router.put("/category/{category_id}", response_model=Category, status_code=HTTP_200_OK)
def update_category(category_id: int, name: Annotated[str, Form(...)]):
    """
    Actualiza una categoría existente por su ID.
    """
    try:
        existing_category = conn.execute(
            category.select().where(category.c.id == category_id)
        ).first()
        if not existing_category:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )

        conn.execute(
            category.update().where(category.c.id == category_id).values(name=name)
        )
        conn.commit()

        updated_category = conn.execute(
            category.select().where(category.c.id == category_id)
        ).first()
        return dict(updated_category._mapping)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la categoría: {str(e)}",
        )


# Ruta: Eliminar categoría
@category_router.delete("/category/{category_id}", status_code=HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    """
    Elimina una categoría por su ID.
    """
    try:
        existing_category = conn.execute(
            category.select().where(category.c.id == category_id)
        ).first()
        if not existing_category:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )

        conn.execute(category.delete().where(category.c.id == category_id))
        conn.commit()
        return JSONResponse(
            status_code=HTTP_204_NO_CONTENT, content={"message": "Categoría eliminada"}
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la categoría: {str(e)}",
        )
