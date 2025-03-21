# products.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table,Text
from config.db import meta
from models.category import category

products = Table(
    'products', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100), nullable=False),
    Column('price', Integer),
    Column('description', Text), 
    Column('category_id', Integer, ForeignKey('category.id'))  
) 
