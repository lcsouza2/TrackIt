"""Funções muito usadas"""

import datetime
import sqlite3

import jwt
from fastapi import HTTPException, Request, Response
from pydantic import EmailStr

DB_ROUTE = "backend/TrackIt.db"

JWT_SESSION_KEY = "IEyP'yQ/rQ"

JWT_REFRESH_KEY = "YR:Lu%,QHL"

JWT_REFRESH_DURATION = datetime.timedelta(days=7)

JWT_SESSION_DURATION = datetime.timedelta(hours=1)


def get_user_id_from_email(user_email: EmailStr) -> int:
    """
    Consulta o id do usuário
    Args:
        Email: Email que o usuário usou para se cadastrar
    Returns:
        ID: Numero inteiro que é o ID
    """

    connection = sqlite3.connect("backend/TrackIt.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id_user FROM usuario WHERE email = ?", (user_email,)
    )

    return cursor.fetchone()[0]


def create_token(
    user_id: EmailStr | int, secret: str, duration: datetime.timedelta
) -> str:
    """
    Cria um JWT
    Args:
        user_id  : Email do usuário
        secret   : Chave para codificação
        duration : Duração do token em timedelta
    Returns
        Str com o token
    """
    create_time = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        # ID do usuário que foi autorizado
        "sub": get_user_id_from_email(user_id)
        if not isinstance(user_id, int)
        else user_id,
        "iat": create_time,  # Data e hora da criação do token
        "exp": create_time + duration,  # Data e hora de validade do token
    }

    return jwt.encode(payload, secret)


def get_user_from_token(token, key) -> HTTPException | dict:
    """Retorna o ID do usuário com base no token de sessao"""
    try:
        user = jwt.decode(token, key, ["HS256"])
    except jwt.InvalidSignatureError:
        return HTTPException(401, "Invalid signature")
    except jwt.DecodeError:
        return HTTPException(500, "Error decoding token")
    return user.get("sub")


def autenticate(request: Request, response: Response):
    """
    Verifica se o usuário está logado
    Returns:
        id do usuário ou erro
    """
    # Pega os tokens de refresh e sessão com os cookies
    session_token = request.cookies.get("session_token")
    refresh_token = request.cookies.get("refresh_token")

    # Pega o ID do usuário autenticado usando os tokens nos cookies
    user_by_session = get_user_from_token(session_token, JWT_SESSION_KEY)
    user_by_refresh = get_user_from_token(refresh_token, JWT_REFRESH_KEY)

    # Verifica se o token de sessão existe e obtém o usuário
    if isinstance(user_by_session, int):
        return user_by_session

    # Se o token de sessão não existir verifica usando o de refresh
    if isinstance(user_by_refresh, int):
        response.set_cookie(
            key="session_token",
            value=create_token(
                user_by_refresh, JWT_SESSION_KEY, JWT_SESSION_DURATION
            ),
            httponly=True,
            samesite="strict",
            expires=datetime.datetime.now(datetime.timezone.utc)
            + JWT_SESSION_DURATION,
        )
        return user_by_refresh

    raise HTTPException(401, "User not logged")
