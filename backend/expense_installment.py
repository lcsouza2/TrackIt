"""Módulo para gerenciar as despesas e parcelamentos"""
import datetime
import sqlite3
import utils

import schemas
from fastapi.exceptions import HTTPException

def create_expense(user_id:int, expense:schemas.Expense):
    """Cria uma despesa no banco de dados"""

    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id_categoria FROM categoria
                WHERE nome_categoria  = ?
                AND id_user_categoria = ?
            """,
            (expense.category, user_id))

        result = cursor.fetchone()

        if result is None:
            raise HTTPException(404, "Category not found")

        id_categoria = result[0]

        date = datetime.datetime.strptime(expense.date, "%Y-%m-%d").date()

        try:
            cursor.execute(
                """
                INSERT INTO despesa(
                    id_categoria_despesa,
                    id_user_despesa, 
                    data_despesa, 
                    valor_despesa, 
                    obs_despesa
                    )
                VALUES (?, ?, ?, ?, ?)
                """,
                (id_categoria, user_id, date, expense.value, expense.description) #type: ignore
                )
            connection.commit()

        except sqlite3.IntegrityError as exc:
            if "UNIQUE" in str(exc):
                raise HTTPException(409, "Expense already exists") from exc


# def get_expenses(user_id, filters:dict):
#     with sqlite3.connect(utils.DB_ROUTE) as connection:
        
#         if filters.get("categorias")
        