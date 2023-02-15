import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort
import time

from app.forms import *
from app.auth import login_required
from app.db import get_db
from app.functions import *

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    db = get_db()
    balanceForm = BalanceForm(request.form)
    incomeForm = IncomeForm(request.form)
    expenseForm = ExpenseForm(request.form)
    if request.method == "POST" and balanceForm.validate_on_submit():
        balance = balanceForm.balance.data
        db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?", (round(float(balance), 2), g.user["user_id"]))
        db.commit()
        return redirect(url_for("dashboard.dashboard"))
    
    if request.method == "POST" and incomeForm.validate_on_submit():
        income = float(incomeForm.income.data)
        current_data = db.execute("SELECT total_balance, total_income FROM user WHERE user_id = ?", (g.user["user_id"],)).fetchone()
        db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?", (round(float(current_data["total_balance"]) + income, 2), g.user["user_id"]))
        db.execute("INSERT INTO income (user_id, date, amount, category, description) VALUES (?, ?, ?, ?, ?)", (g.user["user_id"], int(time.time()), income, "TEST", "TEST"))
        db.execute("UPDATE user SET total_income = ? WHERE user_id = ?", (income_current_month(g, db), g.user["user_id"]))
        db.commit()
        return redirect(url_for("dashboard.dashboard"))
    
    if request.method == "POST" and expenseForm.validate_on_submit():
        expense = float(expenseForm.expense.data)
        current_data = db.execute("SELECT total_balance, total_expense FROM user WHERE user_id = ?", (g.user["user_id"],)).fetchone()
        db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?", (round(float(current_data["total_balance"]) - expense, 2), g.user["user_id"]))
        db.execute("INSERT INTO expense (user_id, date, amount, category, description) VALUES (?, ?, ?, ?, ?)", (g.user["user_id"], int(time.time()), expense, "TEST", "TEST"))
        db.execute("UPDATE user SET total_expense = ? WHERE user_id = ?", (expense_current_month(g, db), g.user["user_id"]))
        db.commit()
        return redirect(url_for("dashboard.dashboard"))
    
    return render_template("dashboard/dashboard.html", user_data=g.user, balanceForm=balanceForm, incomeForm=incomeForm, expenseForm=expenseForm)


@bp.route("/statistics", methods=["GET"])
def stats():
    return render_template("dashboard/statistics.html")

