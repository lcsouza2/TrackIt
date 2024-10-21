"""Módulo com funcionalidades de registro de dados e login de usuário"""
#pylint: disable=import-error
import sqlite3
import bcrypt
import schemas

DB_ROUTE = "backend/TrackIt.db"


def register_user(user:schemas.User):
    """Registra o usuário no banco de dados"""

    connection = sqlite3.connect(DB_ROUTE)
    cursor = connection.cursor()

    hashed_pwd = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO usuario(email, username, senha_hash) VALUES (?, ?, ?)", 
            (user.email, user.username, hashed_pwd)
            )
        connection.commit()
        return user
    except sqlite3.IntegrityError:
        return {"Status" : "User Already Exists"}
    finally:
        connection.close()
