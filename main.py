from fastapi import FastAPI, Request, Depends, HTTPException,Cookie
from routes.user import user_router 
from routes.category import category_router
from routes.product import product_router 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from functions.token import validate_token
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from jose import JWTError
# Crear la instancia principal de FastAPI
app = FastAPI()

# Configurar Jinja2 para manejar plantillas
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Ruta raíz con formulario de login
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@user_router.get("/users/dashboard", response_class=HTMLResponse)
async def users_dashboard(request: Request,access_token:Annotated[str | None,Cookie()]=None):
    if access_token is None:
        return RedirectResponse("/",status_code=302)
    try:
         data_user=validate_token(request) 
         
    except JWTError:
            return RedirectResponse("/",status_code=302)
    data = {"title": "Dashboard", "username": "UsuarioEjemplo"}
    return templates.TemplateResponse("dashboard.html", {"request": request, **data})

@user_router.get("/users/product_list", response_class=HTMLResponse)
async def users_dashboard(request: Request,access_token:Annotated[str | None,Cookie()]=None):
    if access_token is None:
        return RedirectResponse("/",status_code=302)
    try:
         data_user=validate_token(request) 
         
    except JWTError:
            return RedirectResponse("/",status_code=302)
    data = {"title": "product_list", "username": "UsuarioEjemplo"}
    return templates.TemplateResponse("createPro.html", {"request": request, **data})

@user_router.get("/users/uptade_product", response_class=HTMLResponse)
async def users_dashboard(request: Request,access_token:Annotated[str | None,Cookie()]=None):
    if access_token is None:
        return RedirectResponse("/",status_code=302)
    try:
         data_user=validate_token(request) 
         
    except JWTError:
            return RedirectResponse("/",status_code=302)
    data = {"title": "product_list", "username": "UsuarioEjemplo"}
    return templates.TemplateResponse("actualizar.html", {"request": request, **data})

# Incluir las rutas del módulo 'user'
app.include_router(user_router)
app.include_router(product_router)
app.include_router(category_router)
