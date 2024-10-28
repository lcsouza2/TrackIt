import datetime
import calendar
import sqlite3
import utils


today = datetime.datetime.now().date()

this_week_start = today-datetime.timedelta(
    days=today.weekday() + 1
    ) if today.weekday() > 6 else today

this_week_end = today+datetime.timedelta(days=6)

first_month_day = today.replace(day=1)

last_month_day = today.replace(
    day=calendar.monthrange(first_month_day.year, first_month_day.month)[1]
    )

with sqlite3.connect(utils.DB_ROUTE) as connection:
    cursor = connection.cursor()

    cursor.execute(
        """                  
            SELECT COUNT(*) FROM parcelamento
                WHERE id_user_parcelamento = ?;
        """,
        (1,)
    )

    print(cursor.fetchall())