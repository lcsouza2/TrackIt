import datetime
import calendar
import sqlite3
import utils

import time
import categories


with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
                SELECT c.nome_categoria,
                       SUM(d.valor_despesa)
                  FROM despesa d,
                       categoria c
                 WHERE d.id_categoria_despesa = c.id_categoria
                   AND d.id_user_despesa      = 23
                   
                 GROUP BY c.nome_categoria
                 ORDER BY SUM(d.valor_despesa) DESC;
            """
            
        )

        result = cursor.fetchone()
        
        print(result)