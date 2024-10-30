"""Módulo com funcionalidades de registro de dados e login de usuário"""
import datetime
import sqlite3
from http import HTTPStatus

import bcrypt
import fastapi
import schemas
import utils

def register_user(user: schemas.User, response: fastapi.Response):
    """
    Registra o usuário no banco de dados
    Args:
        Objeto da classe User
            Class Data:
                username : str
                email    : EmailStr
                password : str
    Returns:
        {
            Status      : Resultado da operação
            Message     : Descrição do erro caso ocorra
            Session_JWT : Token de sessão para validar o login            
        }
        
    """

    connection = sqlite3.connect(utils.DB_ROUTE) #Conecta no banco
    cursor = connection.cursor() #Cria o cursor

    #Criptografa a senha do usuário
    hashed_pwd = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
        )

    try:
        #Tenta inserir o usuário no banco de dados
        cursor.execute(
            "INSERT INTO usuario(email, username, senha_hash) VALUES (?, ?, ?)", 
            (user.email, user.username, hashed_pwd)
            )

        #Confirma a criação do usuário
        connection.commit()

        #Retorna o status da requisição e o token caso cadastre devidamente
        response.set_cookie(
            key="session_token",
            value=utils.create_token(user.email, utils.JWT_SESSION_KEY, utils.JWT_SESSION_DURATION),
            httponly=True,
            samesite="strict",
            expires=datetime.datetime.now(datetime.timezone.utc) + utils.JWT_SESSION_DURATION
        )

    except sqlite3.IntegrityError as exc: #Erro de chave primária ou Unique
        raise fastapi.HTTPException(409, "Email already used") from exc

    finally:
        connection.close() #Fecha a conexão com ou sem erros


def login(user: schemas.UserLogin, response: fastapi.Response, request: fastapi.Request):
    """
    Verifica a senha cria um cookie que só pode ser acessado por HTTP no navegador, 
    esse cookie armazena o valor do token de refresh
    Args:
        user: Objeto da classe UserLogin
            Class Data:
                email       : str
                password    : str
                stay_logged : bool
        
        response: Objeto da classe response do FastAPI (Gerado automaticamente quando há requisição)
        
    Returns:
        Status      : Resultado da operação
        Message     : Descrição do erro caso ocorra
        Session_JWT : Token de sessão do usuário
    """

    conn = sqlite3.connect(utils.DB_ROUTE)
    cur = conn.cursor()

    cur.execute("SELECT senha_hash FROM usuario WHERE email = ?", (user.email,))
    result = cur.fetchone()

    if result is None:
        raise fastapi.HTTPException(404, "Email not found")

    if bcrypt.checkpw(user.password.encode(), result[0]):
        response.delete_cookie("session_token")

        response.set_cookie(
            key="session_token",
            value=utils.create_token(user.email, utils.JWT_SESSION_KEY, utils.JWT_SESSION_DURATION),
            httponly=True,
            samesite="strict",
            expires=datetime.datetime.now(datetime.timezone.utc) + utils.JWT_SESSION_DURATION
        )

        response.delete_cookie("refresh_token")

        if user.stay_logged:
            token = request.cookies.get("refresh_token")

            if token is None:
                response.set_cookie(
                    key="refresh_token",
                    value=utils.create_token(
                        user.email,
                        utils.JWT_REFRESH_KEY,
                        utils.JWT_REFRESH_DURATION
                        ),
                    httponly=True,
                    samesite="strict",
                    expires=datetime.datetime.now(
                        datetime.timezone.utc
                        ) + utils.JWT_REFRESH_DURATION
                    )

        return HTTPStatus.OK

    raise fastapi.HTTPException(401, "Invalid password")
