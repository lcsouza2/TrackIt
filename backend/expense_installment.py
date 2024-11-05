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
                        d.id_despesa,
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
                            p.id_parcelamento,
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
            expenses_query += "AND p.id_despesa_pagamento IS NOT NULL "
            installment_query += "AND pag.id_parcelamento_pagamento IS NOT NULL "

        elif "not-paid" in filters.expense_types:
            expenses_query += "AND p.id_despesa_pagamento IS NULL "
            installment_query += "AND pag.id_parcelamento_pagamento IS NULL "

    if len(filters.expense_categories) > 1:
        placeholders = ", ".join(["?"] * len(filters.expense_categories))
        expenses_query += f"AND c.nome_categoria IN ({placeholders}) "
        installment_query += f"AND c.nome_categoria IN ({placeholders}) "
        args_list.extend(filters.expense_categories)

    elif len(filters.expense_categories) == 1:
        expenses_query += "AND c.nome_categoria = ? "
        installment_query += "AND c.nome_categoria = ? "
        args_list.append(filters.expense_categories[0])

    if filters.expense_date["init"] and filters.expense_date["end"]:
        expenses_query += "AND d.data_despesa BETWEEN ? AND ? "
        installment_query += "AND p.data_inicio_parcelamento BETWEEN ? AND ? "

        args_list.append(filters.expense_date["init"])
        args_list.append(filters.expense_date["end"])

    elif filters.expense_date["init"] or filters.expense_date["end"]:
        expenses_query += "AND d.data_despesa = ? "
        installment_query += "AND p.data_inicio_parcelamento = ? "

        args_list.append(filters.expense_date["init"] if filters.expense_date["init"] else filters.expense_date["end"])

    if filters.expense_values["init"] and filters.expense_values["end"]:
        expenses_query += "AND d.valor_despesa BETWEEN ? AND ? "
        installment_query += "AND p.valor_parcelas BETWEEN ? AND ? "

        args_list.append(filters.expense_values["init"])
        args_list.append(filters.expense_values["end"])

    elif filters.expense_values["init"] or filters.expense_values["end"]:
        expenses_query += "AND d.valor_despesa = ?"
        installment_query += "AND p.valor_parcelas = ?"

        args_list.append(filters.expense_values["init"] if filters.expense_values["init"] else filters.expense_values["end"])


    with sqlite3.connect(utils.DB_ROUTE) as connection:

        results = {
            "expenses" : [],
            "installments" : []
        }

        cursor = connection.cursor()

        cursor.execute(expenses_query + " ORDER BY c.nome_categoria;", args_list)

        results["expenses"] = cursor.fetchall()

        cursor.execute(installment_query + " ORDER BY c.nome_categoria;", args_list)

        results["installments"] = cursor.fetchall()

        return results

def delete_expense(expense:schemas.DeleteSpent):
    """
    Exclui uma despesa determinada pelo usuário
    Args: 
        expense_id: id da despesa
    """

    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        if expense.type == "Expense":
            cursor.execute("DELETE FROM despesa WHERE id_despesa = ?", (expense.id,))
        else:
            cursor.execute("DELETE FROM parcelamento WHERE id_parcelamento = ?", (expense.id,))


def edit_expenses(expense:schemas.ExpenseEdit):
    """
    Edita uma despesa determinada pelo usuário
    Args: 
        expense: id da despesa
    """

    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE despesa
                  SET id_categoria_despesa = c.id_categoria,
                      data_despesa         = ?,
                      valor_despesa        = ?,
                      obs_despesa          = ?
                 FROM categoria c
                WHERE id_despesa = ?
                  AND c.nome_categoria = ?""",
                    (expense.date, expense.value, expense.description, expense.id, expense.category)
                    )

def register_installment(installment:schemas.Installment, user_id):
    
    with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()
        
        cursor.execute("""
                       SELECT id_categoria 
                       FROM categoria 
                       WHERE id_user_categoria = ?
                       AND nome_categoria      = ?""",
                       (user_id, installment.category))
        
        installment_category = cursor.fetchone()[0]
        
        cursor.execute(
            """
                INSERT INTO parcelamento VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                installment_category,
                user_id,
                installment.description,
                installment.quantity,
                installment.installment_value,
                installment.interests,
                installment.quantity * installment.installment_value,
                installment.init_date
                )
        )