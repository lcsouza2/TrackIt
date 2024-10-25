"""Definição das rotas"""

from http import HTTPStatus
import utils
import expense_installment
import register_login
import schemas
from fastapi import FastAPI, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

JWT_SESSION_KEY = "IEyP'yQ/rQ"

JWT_REFRESH_KEY = "YR:Lu%,QHL"

main_app = FastAPI()
main_app.mount("/static", StaticFiles(directory="frontend/static"), "statics")
html_templates = Jinja2Templates("frontend")


@main_app.get("/", response_class=HTMLResponse)
async def return_main_page(request:Request):
    """Retorna a página inicial do site"""
    return html_templates.TemplateResponse(request=request, name="landing.html")


@main_app.get("/manager", response_class=HTMLResponse)
def return_manager_page(request:Request, response:Response):
    """Retorna a página do gerenciador de despesas"""
    session_token = request.cookies.get("session_token")
    refresh_token =  request.cookies.get("refresh_token")

    user_by_session = utils.get_user_from_token(session_token, JWT_SESSION_KEY)
    user_by_refresh = utils.get_user_from_token(refresh_token, JWT_REFRESH_KEY)

    if user_by_session:
        return html_templates.TemplateResponse(request=request, name="manager.html")

    if user_by_refresh:
        response.set_cookie(
            key="session_token",
            value=utils.create_token(user.email, JWT_SESSION_KEY, JWT_SESSION_DURATION),
            httponly=True,
            samesite="strict",
            expires=datetime.datetime.now(datetime.timezone.utc) + JWT_SESSION_DURATION
        )
        
        
    
            
    

@main_app.post("/register_user", status_code=HTTPStatus.CREATED)
async def register_user(user:schemas.User, response:Response):
    """Registra o usuário no banco de dados ao receber uma requisição"""
    return register_login.register_user(user, response)


@main_app.post("/login")
def verify_login(user:schemas.UserLogin, response:Response, request: Request):
    """Verifica o login"""
    return register_login.login(user, response, request)


@main_app.post("/manager/register_expense")
def create_expense(expense:schemas.Expense, response:Response, request:Request):
    """Cria uma despesa simples"""
    return expense_installment.create_expense(expense, request, response)
