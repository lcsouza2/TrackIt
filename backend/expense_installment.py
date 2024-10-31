"""Módulo para gerenciar as despesas e parcelamentos"""
import datetime
import sqlite3

import schemas
import utils
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









































def get_expenses(user_id, filters:schemas.Filters):

    expenses_query = """
                    SELECT 
                        d.obs_despesa, 
                        d.valor_despesa, 
                        d.data_despesa, 
                        c.nome_categoria 
                    FROM 
                        despesa d
                    JOIN categoria c ON d.id_categoria_despesa = c.id_categoria
                    LEFT JOIN pagamento p ON d.id_despesa = p.id_despesa_pagamento
                        WHERE id_user_despesa = ? 
                    """


    installment_query =  """
                        SELECT 
                            p.obs_parcelamento,
                            p.valor_parcelas,
                            p.qtd_parcelas,
                            p.id_categoria_parcelamento,
                            p.porcent_juros,
                            p.data_inicio_parcelamento
                        
                        FROM parcelamento p 
                        JOIN categoria c ON p.id_categoria_parcelamento = c.id_categoria
                        LEFT JOIN pagamento pag ON p.id_parcelamento = pag.id_parcelamento_pagamento
                        WHERE id_user_parcelamento = ? 
                        """

    args_list = [user_id]

    if filters.expense_types:
        if "paid" in filters.expense_types:
            expenses_query += "AND p.id_despesa_pagamento IS NOT NULL"
            installment_query += "AND pag.id_parcelamento_pagamento IS NOT NULL"

        elif "not-paid" in filters.expense_types:
            expenses_query += "AND p.id_despesa_pagamento IS NULL"
            installment_query += "AND pag.id_parcelamento_pagamento IS NULL"

    if len(filters.expense_categories) > 1:
        expenses_query += "AND c.nome_categoria IN ?"
        installment_query += "AND c.nome_categoria IN ?"
        args_list.append(tuple(filters.expense_categories))

    elif len(filters.expense_categories) == 1:
        expenses_query += "AND c.nome_categoria = ?"
        installment_query += "AND c.nome_categoria = ?"
        args_list.append(filters.expense_categories[0])


    with sqlite3.connect(utils.DB_ROUTE) as connection:

        results = {
            "expenses" : [],
            "installments" : []
        }

        cursor = connection.cursor()

        cursor.execute(expenses_query, args_list)

        results["expenses"] = cursor.fetchall()

        cursor.execute(installment_query, args_list)

        results["installments"] = cursor.fetchall()
        
        return results
