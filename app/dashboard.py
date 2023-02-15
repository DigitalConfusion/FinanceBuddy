import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.forms import *

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/", methods=["GET", "POST"])
def dashboard():
    balanceForm = BalanceForm(request.form)
    incomeForm = IncomeForm(request.form)
    expenseForm = ExpenseForm(request.form)
    if request.method == "POST" and balanceForm.validate_on_submit():
        balance = balanceForm.balance.data
        return redirect(url_for("dashboard.dashboard"))
    
    if request.method == "POST" and incomeForm.validate_on_submit():
        income = incomeForm.income.data
        return redirect(url_for("dashboard.dashboard"))
    
    if request.method == "POST" and expenseForm.validate_on_submit():
        expense = expenseForm.expense.data
        return redirect(url_for("dashboard.dashboard"))
    
    return render_template("dashboard/dashboard.html", balanceForm=balanceForm, incomeForm=incomeForm, expenseForm=expenseForm)


@bp.route("/statistics", methods=["GET"])
def stats():
    return render_template("dashboard/statistics.html")

