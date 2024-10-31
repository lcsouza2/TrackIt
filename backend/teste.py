
import json
import sqlite3
import utils


def get_expenses(user_id, filters:dict):
    if not filters:
        expenses_query = "SELECT * FROM despesa WHERE id_user_despesa = ?"
        installment_query =  "SELECT * FROM parcelamento WHERE id_user_parcelamento = ?"



    with sqlite3.connect(utils.DB_ROUTE) as connection:

        results = {
            "expenses" : [],
            "installments" : []
        }

        cursor = connection.cursor()

        cursor.execute(expenses_query, (user_id,))

        results["expenses"] = cursor.fetchall()

        cursor.execute(installment_query, (user_id,))

        results["installments"] = cursor.fetchall()

        print(json.dumps(results, indent=4, ensure_ascii=False))

get_expenses(23, {})