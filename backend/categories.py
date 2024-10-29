"""Módulo para gerenciar as categorias"""

import calendar
import datetime
import sqlite3

import schemas
import utils
from fastapi import HTTPException


def create_category(user_id:int, category:schemas.Category):
    """Cria uma categoria para o usuário"""
    try:
        with sqlite3.connect(utils.DB_ROUTE) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    INSERT INTO categoria(id_user_categoria, nome_categoria, cor_categoria)
                    VALUES (?, ?, ?)               
                """,
                (user_id, category.name, category.color)
            )
            connection.commit()
    except sqlite3.IntegrityError as exc:
        if "UNIQUE" in str(exc):
            raise HTTPException(409, "Category already exists") from exc
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc

def get_categories_info(user_id):
    """
        Obtem dados sobre as categorias de um usuário
        Returns:
            lista com dicionários com dados
    """

    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT c.nome_categoria,
                c.cor_categoria,
                SUM(valor_despesa)
            FROM despesa d,
                categoria c
            WHERE id_user_despesa = c.id_user_categoria
            AND c.id_user_categoria = ?
            AND d.id_categoria_despesa = c.id_categoria
            GROUP BY c.nome_categoria;
            """,
            (user_id,)
            )

        result = [
                {
            "category_name" : category_name,
            "category_all_expenses" : category_expenses,
            "category_color" : category_color
            } for category_name, category_color, category_expenses in cursor.fetchall()
        ]
    return result

def get_today_expenses(user_id):
    """
    Gera um relatório de despesas do dia atual 
    """

    today = datetime.datetime.now().date()

    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        cursor.execute(
            f"""
                SELECT SUM(p.valor_pagamento)
                  FROM pagamento p
                 WHERE p.data_pagamento = '{today}'
                   AND p.id_user_pagamento = ?;
            """,
            (user_id,)
            )

        result = cursor.fetchone()
        if result is not None:
            return result
        return 0


def get_this_week_expenses(user_id):
    """
    Retorna as despesas da semana de um usuário
    """

    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        today = datetime.datetime.now().date()


        this_week_start = today-datetime.timedelta(
        days=today.weekday() + 1
        ) if today.weekday() > 6 else today

    this_week_end = today+datetime.timedelta(days=6)

    cursor.execute(
        f"""
            SELECT SUM(p.valor_pagamento) 
                FROM pagamento p
                WHERE p.id_user_pagamento = ?
                AND p.data_pagamento BETWEEN '{this_week_start}' AND '{this_week_end}';
        """,
        (user_id,)
    )

    result = cursor.fetchone()
    if result is not None:
        return result
    return 0


def get_this_month_expenses(user_id):
    """
        Pega o valor total de gasto de um usuário
    """

    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        today = datetime.datetime.now().date()

        first_month_day = today.replace(day=1)

        last_month_day = today.replace(
            day=calendar.monthrange(first_month_day.year, first_month_day.month)[1]
            )

        cursor.execute(
            f"""
                SELECT SUM(p.valor_pagamento) 
                    FROM pagamento p
                    WHERE p.id_user_pagamento = ?
                    AND p.data_pagamento BETWEEN '{first_month_day}' AND '{last_month_day}';
            """,
            (user_id,)
        )

        result = cursor.fetchone()
        if result is not None:
            return result
        return 0


def get_all_installments(user_id):
    """
        Busca todos os parcelamentos de um usuário
    """
    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
                SELECT COUNT(*)
                  FROM parcelamento
                 WHERE id_user_parcelamento = ?;
            """,
            (user_id,)
        )

        result = cursor.fetchone()
        if result is not None:
            return result
        return 0
