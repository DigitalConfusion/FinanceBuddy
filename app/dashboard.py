import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.exceptions import abort
import time
import json
from datetime import date, datetime

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
        db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?",
                   (round(float(balance), 2), g.user["user_id"]))
        db.commit()
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST" and incomeForm.validate_on_submit():
        income = float(incomeForm.income.data)
        category = incomeForm.income_category.data
        if category == "Custom Category":
            category = incomeForm.custom_category.data
            db.execute("UPDATE user SET income_category = ? WHERE user_id = ?",
                       (add_new_to_income_category(g, db, category), g.user["user_id"]))
        description = incomeForm.description.data
        current_data = db.execute(
            "SELECT total_balance, total_income FROM user WHERE user_id = ?", (g.user["user_id"],)).fetchone()
        db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?", (round(
            float(current_data["total_balance"]) + income, 2), g.user["user_id"]))
        db.execute("INSERT INTO income (user_id, date, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                   (g.user["user_id"], int(time.time()), income, category, description))
        db.execute("UPDATE user SET total_income = ? WHERE user_id = ?",
                   (income_current_month(g, db), g.user["user_id"]))
        db.commit()
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST" and expenseForm.validate_on_submit():
        expense = float(expenseForm.expense.data)
        current_data = db.execute(
            "SELECT total_balance, total_expense FROM user WHERE user_id = ?", (g.user["user_id"],)).fetchone()
        category = expenseForm.expense_category.data
        if category == "Custom Category":
            category = expenseForm.custom_category2.data
            db.execute("UPDATE user SET expense_category = ? WHERE user_id = ?",
                       (add_new_to_expense_category(g, db, category), g.user["user_id"]))
        description = incomeForm.description.data
        if expense > current_data["total_balance"]:
            flash("You do not have enough available balance!")
        else:
            db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?", (round(
                float(current_data["total_balance"]) - expense, 2), g.user["user_id"]))
            db.execute("INSERT INTO expense (user_id, date, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                       (g.user["user_id"], int(time.time()), -expense, category, description))
            db.execute("UPDATE user SET total_expense = ? WHERE user_id = ?",
                       (expense_current_month(g, db), g.user["user_id"]))
            db.commit()
            return redirect(url_for("dashboard.dashboard"))

    return render_template("dashboard/dashboard.html", user_data=g.user, balanceForm=balanceForm, incomeForm=incomeForm, expenseForm=expenseForm)


@bp.route("/statistics", methods=["GET"])
def stats():
    return render_template("dashboard/statistics.html")


@bp.route("/api/financedata/<datatype>/<count>", methods=["GET", "POST"])
def api_get_finance_data(datatype, count):
    datatype = str(datatype.lower())
    count = int(count)
    db = get_db()
    data = {}
    db_data = []

    if datatype == "all":
        db_income_data = db.execute(
            "SELECT amount, category, description, date FROM income WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)
        db_expense_data = db.execute(
            "SELECT amount, category, description, date FROM expense WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)
        for row in db_income_data:
            db_data.append([row["amount"], row["category"],
                           row["description"], row["date"]])
        for row in db_expense_data:
            db_data.append([row["amount"], row["category"],
                           row["description"], row["date"]])
        db_data.sort(reverse=True, key=lambda x: x[3])
    elif datatype == "income":
        db_data = db.execute(
            "SELECT amount, category, description FROM income WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)
    elif datatype == "expense":
        db_data = db.execute(
            "SELECT amount, category, description FROM expense WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)

    for i, row in enumerate(db_data[:count]):
        data[str(i)] = [row[0], row[1], row[2], row[3]]
    return jsonify(data)


@bp.route("/api/category/<type>", methods=["GET", "POST"])
def api_get_category(type):
    type = str(type.lower())
    db = get_db()
    category = None
    if type == "income":
        category = db.execute("SELECT income_category FROM user WHERE user_id = ?",
                              (g.user["user_id"],)).fetchone()["income_category"]
    else:
        category = db.execute("SELECT expense_category FROM user WHERE user_id = ?",
                              (g.user["user_id"],)).fetchone()["expense_category"]
    return jsonify(category)


@bp.route("/api/graphdata/<timeframe>/<timeframe_amount>", methods=["GET", "POST"])
def api_get_graph_data(timeframe, timeframe_amount):
    timeframe = str(timeframe.lower())
    timeframe_amount = int(timeframe_amount)
    db = get_db()
    data = {}
    income_data = []
    expense_data = []

    unix_time_amount = {"week": 604800,
                        "month": 2629743,
                        "year": 31556926}

    current_date = date.today()
    current_date_timestamp = int(datetime(current_date.year, current_date.month, current_date.day).timestamp())
    history_date_timestamp = current_date_timestamp - (unix_time_amount[timeframe] * timeframe_amount)

    db_income_data = db.execute(
        "SELECT amount, category, date FROM income WHERE user_id = ? AND date > ? ORDER BY date DESC", (g.user["user_id"], history_date_timestamp)).fetchall()
    db_expense_data = db.execute(
        "SELECT amount, category, date FROM expense WHERE user_id = ? AND date > ? ORDER BY date DESC", (g.user["user_id"], history_date_timestamp)).fetchall()
    
    for row in db_income_data:
        income_data.append([row["amount"], row["date"], row["category"]])
    for row in db_expense_data:
        expense_data.append([row["amount"], row["date"], row["category"]])
        
    data["income"] = income_data
    data["expense"] = expense_data
    
    return jsonify(data)
