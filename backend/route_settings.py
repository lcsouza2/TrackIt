"""Definição das rotas"""

from http import HTTPStatus

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi import Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import schemas
import register_login

main_app = FastAPI()
main_app.mount("/static", StaticFiles(directory="frontend/static"), "statics")
html_templates = Jinja2Templates("frontend")


@main_app.get("/", response_class=HTMLResponse)
async def return_main_page(request:Request):
    """Retorna a página inicial do site"""
    return html_templates.TemplateResponse(request=request, name="landing.html")


@main_app.get("/manager", response_class=HTMLResponse)
def return_manager_page(request:Request):
    return html_templates.TemplateResponse(request=request, name="manager.html")


@main_app.post("/register_user", status_code=HTTPStatus.CREATED)
async def register_user(user:schemas.User, response:Response):
    """Registra o usuário no banco de dados ao receber uma requisição"""
    return register_login.register_user(user, response)


@main_app.post("/login")
def verify_token(user:schemas.UserLogin, response:Response, request: Request):
    """Verifica o login"""
    return register_login.login(user, response, request)
