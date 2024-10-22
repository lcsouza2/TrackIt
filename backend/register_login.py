"""Módulo com funcionalidades de registro de dados e login de usuário"""
import datetime
import sqlite3
from pydantic import EmailStr
import bcrypt
import fastapi
import jwt
import schemas

DB_ROUTE = "backend/TrackIt.db"

JWT_SESSION_TOKEN = "IEyP'yQ/rQ"

JWT_REFRESH_TOKEN = "YR:Lu%,QHL"

def create_session_token(user_id:EmailStr):
    """Cria um token de sessão"""

    session_payload={
        "sub": user_id, #ID do usuário que foi autorizado
        "iat": datetime.datetime.now(datetime.timezone.utc), #Data e hora da criação do token

        #Data e hora de validade do token
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }

    return jwt.encode(session_payload, JWT_SESSION_TOKEN) #Retorna o token criado


def create_refresh_token(user_id:EmailStr):
    """Cria um token de refresh"""

    session_payload={
        "sub": user_id, #ID do usuário autorizado
        "iat": datetime.datetime.now(datetime.timezone.utc), #Data e hora de ciração do token
        #Data e hora de validade do token
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }

    return jwt.encode(session_payload, JWT_REFRESH_TOKEN) #Retorna o token criado


def register_user(user:schemas.User):
    """Registra o usuário no banco de dados"""

    connection = sqlite3.connect(DB_ROUTE) #Conecta no banco
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
        return {"Status" : "Success",
                "Session_JWT" : create_session_token(user.email)}

    except sqlite3.IntegrityError: #Erro de chave primária ou Unique

        #Retorna o Status do erro e uma mensagem descrevendo
        return {"Status" : "Error",
                "Message" : "Email já registrado!"}

    finally:
        connection.close() #Fecha a conexão com ou sem erros



def login(user:schemas.User, response:fastapi.Response):
    """
    Cria um cookie que só pode ser acessado por HTTP no navegador, 
    esse cookie armazena o valor do token de refresh
    """

    conn = sqlite3.connect(DB_ROUTE)
    cur = conn.cursor()


    cur.execute("SELECT senha_hash FROM usuario WHERE email = ?", (user.email,))
    result = cur.fetchone()

    if not result:
        return {"Status" : "Error",
                "Message" : "Email Não encontrado"}
    

    # if bcrypt.checkpw(user.password, result):

    #         if user.stay_loged:
    #         response.set_cookie(
    #             key="refresh_token",
    #             value=create_refresh_token(user.email),
    #             httponly=True,
    #         ) 

    #     return {"Status" : "Success"}

    

