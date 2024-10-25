import datetime
import sqlite3

import jwt
import register_login
import schemas
import utils
from fastapi import Request, Response
from fastapi.exceptions import HTTPException

DB_ROUTE = "backend/TrackIt.db"

JWT_SESSION_KEY = "IEyP'yQ/rQ"

JWT_REFRESH_KEY = "YR:Lu%,QHL"

JWT_REFRESH_DURATION = datetime.timedelta(days=7)

JWT_SESSION_DURATION = datetime.timedelta(hours=1)

def create_expense(expense:schemas.Expense, request:Request, response:Response):
    """Cria uma despesa no banco de dados"""
    connection = sqlite3.connect(DB_ROUTE)
    cursor = connection.cursor()

    refresh_token = request.cookies.get("refresh_token")
    session_token = request.cookies.get("session_token")

    user_id = None

    if not session_token and refresh_token:
            
        user_id = utils.get_user_from_token(session_token, JWT_REFRESH_KEY)

        response.set_cookie(
            key="session_token",
            value=utils.create_token(user_id.get("sub"), JWT_SESSION_KEY, JWT_SESSION_DURATION),#type:ignore
            httponly=True,
            samesite="strict",
            expires=datetime.datetime.now(datetime.timezone.utc) + JWT_SESSION_DURATION
        )

    elif not session_token and not refresh_token:
        raise HTTPException(401, "User not logged")
    else:
        user_id = utils.get_user_from_token(session_token, JWT_SESSION_KEY)
    
    try:
        cursor.execute("""SELECT id_categoria FROM categoria
                            WHERE nome_categoria   = ?
                            AND id_user_categoria  = ?""",
                            (expense.category, user_id))

        id_categoria = cursor.fetchone()[0]

        if id_categoria is None:
            try:
                cursor.execute("""INSERT INTO categoria(id_user_categoria, nome_categoria, cor_categoria)
                                VALUES(?, ?, ?)""",
                                (user_id, expense.category, expense.category_color))
            except Exception as exc:
                raise HTTPException(502, str(exc))
            finally:
                connection.commit()
                connection.close()
    except Exception as exc:
        raise HTTPException(502, str(exc))
    finally:
        cursor.execute("""SELECT id_categoria FROM categoria
                        WHERE nome_categoria    = ? 
                        AND id_user_categoria = ?""",
                        (expense.category, user_id))

        id_categoria = cursor.fetchone()[0]

        connection.commit()
        connection.close()


    date = datetime.datetime.strptime(expense.date, "%Y-%m-%d").date()

    cursor.execute("""INSERT INTO despesa(id_categoria_despesa,
                                            id_user_despesa, 
                                            data_despesa, 
                                            valor_despesa, 
                                            obs_despesa)
                        VALUES (?, ?, ?, ?, ?)""",
                    (id_categoria, user_id, date, expense.value, expense.description))

    connection.commit()
    connection.close()
