from datetime import date, datetime


def income_current_month(g, db):
    current_date = date.today()
    unix_start_month = int(datetime(current_date.year, current_date.month, 1).timestamp())
    print(unix_start_month, flush=True)
    income_data = db.execute("SELECT amount FROM income WHERE user_id = ? AND date >= ?", (g.user["user_id"], unix_start_month)).fetchall()
    income = 0
    for row in income_data:
        income += row["amount"]
    return round(income, 2)


def expense_current_month(g, db):
    current_date = date.today()
    unix_start_month = int(datetime(current_date.year, current_date.month, 1).timestamp())
    print(unix_start_month, flush=True)
    expense_data = db.execute("SELECT amount FROM expense WHERE user_id = ? AND date >= ?", (g.user["user_id"], unix_start_month)).fetchall()
    expense = 0
    for row in expense_data:
        expense += row["amount"]
    return round(expense, 2)