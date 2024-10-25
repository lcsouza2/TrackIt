"""Funções muito usadas"""
import datetime
import sqlite3

from fastapi import HTTPException
import jwt
from pydantic import EmailStr


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

    cursor.execute("SELECT id_user FROM usuario WHERE email = ?", (user_email,))

    return cursor.fetchone()[0]



def create_token(user_id: EmailStr | int, secret: str, duration: datetime.timedelta) -> str:
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

    payload={
        #ID do usuário que foi autorizado
        "sub": get_user_id_from_email(user_id) if not isinstance(user_id, int) else user_id, 
        "iat": create_time, #Data e hora da criação do token
        "exp": create_time + duration #Data e hora de validade do token
    }

    return jwt.encode(payload, secret)


def get_user_from_token(token, key) -> HTTPException | dict:
    """Retorna o ID do usuário com base no token de sessao"""
    try:
        user = jwt.decode(token, key, ["HS256"])
    except jwt.InvalidSignatureError:
        return HTTPException(401, "Invalid signature")
    except jwt.DecodeError:
        return HTTPException(502, "Error decoding token")
    return user.get("sub")
