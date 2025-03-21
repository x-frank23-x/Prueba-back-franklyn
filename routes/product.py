from fastapi import APIRouter, HTTPException, Form, Query
from schemas.product import Product
from models.products import products
from models.category import category
from config.db import conn
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select, join
from typing import Optional
from pydantic import BaseModel, Field
import logging

# Configuración de logger
logger = logging.getLogger("product_router")
logger.setLevel(logging.INFO)

product_router = APIRouter()


# Modelo de respuesta para los productos
class ProductResponse(BaseModel):
    id: int
    name: str = Field(..., description="Nombre del producto")
    price: float = Field(gt=0, description="Precio del producto")
    description: str = Field(..., description="Descripción del producto")
    category_name: str = Field(..., description="Nombre de la categoría")


def apply_filters(query, category_id=None, min_price=None, max_price=None):
    """
    Aplica filtros opcionales a la consulta.
    """
    if category_id:
        query = query.where(products.c.category_id == category_id)
    if min_price:
        query = query.where(products.c.price >= min_price)
    if max_price:
        query = query.where(products.c.price <= max_price)
    return query


@product_router.get("/product", response_model=list[ProductResponse])
def product_all(
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    """
    Obtiene todos los productos con filtros opcionales de categoría, precio mínimo y máximo.
    """
    try:
        query = select(
            products.c.id,
            products.c.name,
            products.c.price,
            products.c.description,
            category.c.name.label("category_name"),
        ).select_from(
            join(products, category, products.c.category_id == category.c.id)
        )

        query = apply_filters(query, category_id, min_price, max_price)
        query = query.offset(skip).limit(limit)

        product_all = conn.execute(query).fetchall()

        if not product_all:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"No se encontraron productos con los filtros aplicados.",
            )

        return [
            {
                "id": row.id,
                "name": row.name,
                "price": row.price,
                "description": row.description,
                "category_name": row.category_name,
            }
            for row in product_all
        ]
    except SQLAlchemyError as e:
        logger.error("Error en la base de datos al obtener productos: %s", str(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}",
        )


@product_router.get("/product/id/{id}", response_model=Product)
def product_id(id: int):
    """
    Obtiene un producto por su ID.
    """
    try:
        product = conn.execute(products.select().where(products.c.id == id)).first()
        if not product:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        return dict(product._mapping)
    except SQLAlchemyError as e:
        logger.error("Error en la base de datos al obtener producto por ID: %s", str(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}",
        )


@product_router.post("/product/create", response_model=Product, status_code=HTTP_201_CREATED)
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(..., gt=0),
    category_id: int = Form(...),
):
    """
    Crea un nuevo producto.
    """
    try:
        existing_category = conn.execute(
            category.select().where(category.c.id == category_id)
        ).first()
        if not existing_category:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Categoría no existe"
            )

        result = conn.execute(
            products.insert().values(
                name=name, description=description, price=price, category_id=category_id
            )
        )
        conn.commit()

        created_product = conn.execute(
            products.select().where(products.c.id == result.lastrowid)
        ).first()
        if not created_product:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo obtener el producto creado",
            )

        logger.info("Producto creado exitosamente con ID: %s", result.lastrowid)
        return dict(created_product._mapping)
    except SQLAlchemyError as e:
        logger.error("Error al crear el producto: %s", str(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto: {str(e)}",
        )


@product_router.put("/product/update/{id}", response_model=Product)
def update_product(
    id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category_id: Optional[int] = Form(None),
):
    """
    Actualiza un producto por su ID.
    """
    try:
        existing_product = conn.execute(
            products.select().where(products.c.id == id)
        ).first()
        if not existing_product:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        if category_id is not None:
            existing_category = conn.execute(
                category.select().where(category.c.id == category_id)
            ).first()
            if not existing_category:
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Categoría no existe",
                )

        update_values = {
            key: value
            for key, value in {
                "name": name,
                "description": description,
                "price": price,
                "category_id": category_id,
            }.items()
            if value is not None
        }

        conn.execute(products.update().where(products.c.id == id).values(**update_values))
        conn.commit()

        updated_product = conn.execute(
            products.select().where(products.c.id == id)
        ).first()
        logger.info("Producto actualizado con ID: %s", id)
        return dict(updated_product._mapping)
    except SQLAlchemyError as e:
        logger.error("Error al actualizar el producto: %s", str(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el producto: {str(e)}",
        )


@product_router.delete("/product/delete/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_product(id: int):
    """
    Elimina un producto por su ID.
    """
    try:
        product = conn.execute(products.select().where(products.c.id == id)).first()
        if not product:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        conn.execute(products.delete().where(products.c.id == id))
        conn.commit()

        logger.info("Producto eliminado con ID: %s", id)
        return {"message": "Producto eliminado correctamente"}
    except SQLAlchemyError as e:
        logger.error("Error al eliminar producto: %s", str(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar producto: {str(e)}",
        )
