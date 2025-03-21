from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv() 

# Configurar los parámetros de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Construir la URL de conexión
dbUrl =DATABASE_URL

# Crear el motor de la base de datos
engine = create_engine(dbUrl, echo=True)

# Crear la metadata
meta = MetaData()

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

conn=None

try:
    conn = engine.connect()
    print(f"Conexión exitosa a la base de datos ")
except Exception as e:
    print(f"Error en la conexión: {e}")

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
