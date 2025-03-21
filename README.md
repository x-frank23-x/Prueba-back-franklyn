# Prueba Técnica: Gestión de Inventario

## Descripción del Proyecto

Esta aplicación es una API RESTful desarrollada con **FastAPI** para gestionar un sistema de inventario. Permite administrar usuarios, categorías y productos, con autenticación mediante JWT, persistencia en PostgreSQL y despliegue utilizando Docker.

## Estructura del Proyecto

```
PRUEBA
├── app
│   ├── config       # Configuración general del proyecto
│   ├── functions    # Funciones reutilizables
│   ├── models       # Modelos de base de datos (SQLAlchemy)
│   ├── routes       # Rutas de la API
│   ├── schemas      # Esquemas Pydantic para validación de datos
│   ├── static       # Archivos estáticos (si aplica)
│   └── templates    # Plantillas HTML (si aplica)
├── .env             # Variables de entorno
├── .gitignore       # Archivos y carpetas ignorados por Git
├── docker-compose.yml # Configuración de Docker Compose
├── Dockerfile       # Configuración del contenedor Docker
├── main.py          # Punto de entrada de la aplicación
├── README.md        # Documentación del proyecto
├── requirements.txt # Dependencias del proyecto
└── venv             # Entorno virtual
```

## Requisitos Previos

- **Python 3.x** instalado
- **Docker** y **Docker Compose** instalados
- Cuenta en **Postman** (para probar los endpoints)

## Configuración del Entorno de Desarrollo

1. Clona el repositorio:
   ```bash
   git clone https://github.com/x-frank23-x/Prueba-back-franklyn.git
   cd PRUEBA
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Linux/Mac
   venv\Scripts\activate    # En Windows
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crea un archivo `.env`

   ```env
   POSTGRES_USER=frank
   POSTGRES_PASSWORD=mitsuri23
   POSTGRES_DB=frank
   DATABASE_URL=postgresql://frank:mitsuri23@db:5432/frank

   SECRET_KEY="0oodqolfBEXcrxspkFSbMPf2jYQyoc5T0ZJuEZqkM"
   APP_HOST=0.0.0.0
   APP_PORT=8000
   ```

## Ejecución de la Aplicación

### Localmente

1. Inicia PostgreSQL y crea la base de datos manualmente si es necesario.
2. Ejecuta la aplicación:
   ```bash
   uvicorn main:app --reload
   ```
3. Accede a la documentación interactiva de la API en:
   - `http://127.0.0.1:8000/docs` (Swagger UI)
   - `http://127.0.0.1:8000/redoc` (Redoc)

### Con Docker

1. Construye y levanta los servicios:
   ```bash
   docker-compose up --build
   ```
2. Accede a la API en:
   - `http://localhost:8000`

## Endpoints Principales

- **Usuarios**

  - POST `/users/`: Crear usuario
  - GET `/users/{id}`: Obtener usuario por ID
  - PUT `/users/{id}`: Actualizar usuario
  - DELETE `/users/{id}`: Eliminar usuario

- **Categorías**

  - POST `/categories/`: Crear categoría
  - GET `/categories/`: Obtener todas las categorías
  - GET `/categories/{id}`: Obtener categoría por ID
  - PUT `/categories/{id}`: Actualizar categoría
  - DELETE `/categories/{id}`: Eliminar categoría

- **Productos**
  - POST `/products/`: Crear producto
  - GET `/products/`: Obtener todos los productos
  - GET `/products/category/{id}`: Obtener productos por categoría
  - GET `/products/{id}`: Obtener producto por ID
  - PUT `/products/{id}`: Actualizar producto
  - DELETE `/products/{id}`: Eliminar producto

Nota: Actualmente, la base de datos no contiene productos ni categorías predefinidos.
Los usuarios deberán agregar manualmente estos datos utilizando los endpoints proporcionados.

## Pruebas con Postman

1. Importa la colección de Postman desde el repositorio (`Postman_Collection.json`).
2. Realiza solicitudes a los endpoints con ejemplos de datos incluidos.

## Consideraciones Finales

- Asegúrate de que Docker esté ejecutándose correctamente para usar `docker-compose`.
- Usa buenas prácticas de seguridad para gestionar las claves y contraseñas.

## Modos de comunicacion

- Correo : xfranklyngarzonx@gmail.com
- Numero telefonico : 3223351010
