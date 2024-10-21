from http import HTTPStatus

from fastapi import FastAPI
from fastapi.requests import Request
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


@main_app.post("/register_user", status_code=HTTPStatus.CREATED)
def register_user(user:schemas.User):
    """Registra o usuário no banco de dados ao receber uma requisição"""
    status = register_login.register_user(user)
    return status
