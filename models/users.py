from sqlalchemy import Column, Integer, String, DateTime, Table, Text
from config.db import meta, engine
from models.category import category
from models.products import products

# Redefinir la tabla 'users'
users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100)),
    Column('email', String(150), unique=True),
    Column('password', String(255)),
) 
 
# Crear la tabla nuevamente 
meta.create_all(engine)

 