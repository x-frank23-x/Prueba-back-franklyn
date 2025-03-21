
from sqlalchemy import Column, Integer, String, Table
from config.db import meta

category = Table(
    'category', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100), nullable=False)
)
