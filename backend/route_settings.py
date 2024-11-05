"""Definição das rotas da aplicação"""

from http import HTTPStatus

import categories
import expense_installment
import register_login
import schemas
import utils
from fastapi import FastAPI, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#Aplicação
main_app = FastAPI()

#Monta o caminho para fornecer CSS e JS
main_app.mount("/static", StaticFiles(directory="frontend/static"), "static")

#Caminho dos arquivos HTML
html_templates = Jinja2Templates("frontend")


@main_app.get("/", response_class=HTMLResponse)
async def return_main_page(request:Request):
    """
    Fornece a página inicial do site
    Returns:
        Template HTML com a página para cadastro e login
    """
    return html_templates.TemplateResponse(request=request, name="landing.html")

#Retornar a página principal do gerenciador
@main_app.get("/manager", response_class=HTMLResponse)
async def return_manager_page(request:Request, response:Response):
    """
    Autentica o usuário usando os tokens armazenados nos cookies
    Fornece a página do gerenciador de despesas
    Returns:
        Template HTML com a página do gerenciado de despesas
    """
    utils.autenticate(request, response)
    return html_templates.TemplateResponse(request=request, name="manager.html")


@main_app.get("/manager/expenses", response_class=HTMLResponse)
async def return_expenses(request:Request, response:Response):
    """
    Autentica o usuário e retorna a página de despesas
    """
    utils.autenticate(request, response)
    return html_templates.TemplateResponse(request=request, name="expenses.html")


@main_app.get("/manager/user_categories")
def get_categories(request:Request, response:Response):
    """
    Retorna as categorias de cada usuário
    """
    user = utils.autenticate(request, response)
    return categories.get_categories_info(user)

#Rota para pegar informações legais
@main_app.get("/manager/user_manager_data")
def get_util_data(request:Request, response:Response):
    """
    Retorna dados uteis para a página principal
    """
    user_id = utils.autenticate(request, response)

    results = (
        categories.get_today_expenses(user_id),
        categories.get_this_week_expenses(user_id),
        categories.get_this_month_expenses(user_id),
        categories.get_biggest_category(user_id),
        categories.get_all_installments(user_id)
    )

    return {
        "today" : results[0],
        "this_week" : results[1],
        "this_month" : results[2],
        "biggest_category" : results[3],
        "installments" : results[4]

    }

#Rota para popular as tabelas
@main_app.post("/manager/expenses/get_expenses")
async def get_expenses(filters:schemas.Filters, request:Request, response:Response):
    """Retorna as despesas com base nos filtros lá no front"""
    user = utils.autenticate(request, response)
    return expense_installment.get_expenses(user, filters)


#Rota para cadastrar o usuário
@main_app.post("/register_user", status_code=HTTPStatus.CREATED)
async def register_user(user:schemas.User, response:Response):
    """Registra o usuário no banco de dados ao receber uma requisição"""
    register_login.register_user(user, response)


@main_app.post("/login")
def verify_login(user:schemas.UserLogin, response:Response, request:Request):
    """Verifica o login do usuário"""
    register_login.login(user, response, request)


@main_app.post("/manager/register_expense", status_code=HTTPStatus.CREATED)
def create_expense(expense:schemas.Expense, request:Request, response:Response):
    """Cria uma despesa simples"""
    user_id = utils.autenticate(request, response)

    expense_installment.create_expense(user_id, expense)


@main_app.post("/manager/create_category", status_code=HTTPStatus.CREATED)
def create_category(category:schemas.Category, response:Response, request:Request):
    """Cria uma categoria no banco"""

    user = utils.autenticate(request, response)
    categories.create_category(user, category)


@main_app.delete("/manager/expenses/delete_expense")
async def delete_expense(expense:schemas.DeleteSpent, request:Request, response:Response):
    """Remove um gasto do banco de dados"""
    utils.autenticate(request, response)
    expense_installment.delete_expense(expense)

@main_app.put("/manager/expenses/edit_expense")
async def edit_expense(expense:schemas.ExpenseEdit, request:Request, response:Response):
    """Edita uma despesa"""
    utils.autenticate(request, response)
    expense_installment.edit_expenses(expense)
    
@main_app.post("/manager/register_installment", status_code=HTTPStatus.CREATED)
async def register_installment(installment:schemas.Installment, response:Response, request:Request):
    """Cria um parcelamento no banco"""
    user_id = utils.autenticate(request, response)
    expense_installment.register_installment(installment, user_id)