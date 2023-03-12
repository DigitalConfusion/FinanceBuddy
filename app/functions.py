# Importē nepieciešamās bibliotēkas
from datetime import date, datetime
import json


# Aprēķina kopējos ienākumus pašreizējā mēnesī, to parāda dashboard lapā kā income
def income_current_month(g, db):
    current_date = date.today()
    unix_start_month = int(
        datetime(current_date.year, current_date.month, 1).timestamp())
    income_data = db.execute("SELECT amount FROM income WHERE user_id = ? AND date >= ?",
                             (g.user["user_id"], unix_start_month)).fetchall()
    income = 0
    for row in income_data:
        income += row["amount"]
    return round(income, 2)


# Aprēķina kopējos izdevumus pašreizējā mēnesī, to parāda dashboard lapā kā expense
def expense_current_month(g, db):
    current_date = date.today()
    unix_start_month = int(
        datetime(current_date.year, current_date.month, 1).timestamp())
    expense_data = db.execute("SELECT amount FROM expense WHERE user_id = ? AND date >= ?",
                              (g.user["user_id"], unix_start_month)).fetchall()
    expense = 0
    for row in expense_data:
        expense += row["amount"]
    return round(expense, 2)


# Funkcija, kas pievieno jaunu lietotāja izveidotu ienākumu kategoriju
def add_new_to_income_category(g, db, category):
    current_db = db.execute("SELECT income_category FROM user WHERE user_id = ?",
                            (g.user["user_id"],)).fetchone()["income_category"]
    current_db = json.loads(current_db)
    current_db.append(category)
    return json.dumps(current_db)


# Funkcija, kas pievieno jaunu lietotāja izveidotu izdevumu kategoriju
def add_new_to_expense_category(g, db, category):
    current_db = db.execute("SELECT expense_category FROM user WHERE user_id = ?",
                            (g.user["user_id"],)).fetchone()["expense_category"]
    current_db = json.loads(current_db)
    current_db.append(category)
    return json.dumps(current_db)
