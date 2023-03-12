# Importē nepieciešamās bibliotēkas
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
import time
from datetime import date, datetime

# No python moduļu failiem importē nepieciešamo
from app.forms import *
from app.functions import *
from app.auth import login_required
from app.db import get_db

# Izveido blueprint ar ko tiks associēta attiecīgā lapa un tās funkcija
bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# Šī funkcija piešķir funkcionalitāti /dashboard lapai, jeb dod iespēju reģistrēties
@bp.route("/", methods=["GET", "POST"])
# Pārbauda vai lietotājs ir pieslēdzies, lai piekļūtai šai lapai
@login_required
def dashboard():
    # Izveido formas, kurās lietotājs varēs ievadīt un izvēlēties
    # attiecīgos datus, un padod tos html lapai
    balanceForm = BalanceForm(request.form)
    incomeForm = IncomeForm(request.form)
    expenseForm = ExpenseForm(request.form)

    # Pieslēdzas datubāzei
    db = get_db()

    # Ja lapa nosūta ievadītos datus atpakaļ uz serveri, tie tiek pārbaudīti
    if request.method == "POST" and balanceForm.validate_on_submit():
        balance = balanceForm.balance.data
        # Atjauno lietotāja pieejamo balaci pēc ievadītajiem datiem
        db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?",
                   (round(float(balance), 2), g.user["user_id"]))
        db.commit()
        return redirect(url_for("dashboard.dashboard"))

    # Ja lapa nosūta ievadītos datus atpakaļ uz serveri, tie tiek pārbaudīti
    if request.method == "POST" and incomeForm.validate_on_submit():
        income = float(incomeForm.income.data)
        category = incomeForm.income_category.data
        # Ja lieotājs ir izvēlējies ievadīt pielāgotu kategoriju, to saglabā datubāzē pie
        # pie individuālā lietotāja kategorijām, lai to varētu izmantot atkārtoti
        if category == "Custom Category":
            category = incomeForm.custom_category.data
            db.execute("UPDATE user SET income_category = ? WHERE user_id = ?",
                       (add_new_to_income_category(g, db, category), g.user["user_id"]))
        description = incomeForm.description.data
        # No datubāzes iegūst lietotāja šobrīdējos bilances un kopējo ienākumu datus
        current_data = db.execute(
            "SELECT total_balance, total_income FROM user WHERE user_id = ?", (g.user["user_id"],)).fetchone()
        # Atjauno lietotāja balanci par attiecīgo ienākumu daudzumu
        db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?", (round(
            float(current_data["total_balance"]) + income, 2), g.user["user_id"]))
        # Ievieto ienākumu ienākumu tabulā ar attiecīgajiem lietotāja datiem, laiku, un ienākumu datiem
        db.execute("INSERT INTO income (user_id, date, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                   (g.user["user_id"], int(time.time()), income, category, description))
        # Atjauno lietotāja kopējo ienākumu datus
        db.execute("UPDATE user SET total_income = ? WHERE user_id = ?",
                   (income_current_month(g, db), g.user["user_id"]))
        db.commit()
        return redirect(url_for("dashboard.dashboard"))

    # Ja lapa nosūta ievadītos datus atpakaļ uz serveri, tie tiek pārbaudīti
    if request.method == "POST" and expenseForm.validate_on_submit():
        expense = float(expenseForm.expense.data)
        # No datubāzes iegūst lietotāja šobrīdējos bilances un kopējos izdevumu datus
        current_data = db.execute(
            "SELECT total_balance, total_expense FROM user WHERE user_id = ?", (g.user["user_id"],)).fetchone()
        category = expenseForm.expense_category.data
        # Ja lieotājs ir izvēlējies ievadīt pielāgotu kategoriju, to saglabā datubāzē pie
        # pie individuālā lietotāja kategorijām, lai to varētu izmantot atkārtoti
        if category == "Custom Category":
            category = expenseForm.custom_category2.data
            db.execute("UPDATE user SET expense_category = ? WHERE user_id = ?",
                       (add_new_to_expense_category(g, db, category), g.user["user_id"]))
        description = incomeForm.description.data
        # Ja lietotājam nav pietiekoši daudz pieejamā bilance, tad parāda kļūdu, ka nav pietiekoši daudz līdzekļu
        if expense > current_data["total_balance"]:
            flash("You do not have enough available balance!")
        else:
            # Atjauno lietotāja balanci par attiecīgo izdevumu daudzumu
            db.execute("UPDATE user SET total_balance = ? WHERE user_id = ?", (round(
                float(current_data["total_balance"]) - expense, 2), g.user["user_id"]))
            # Ievieto izdevumu izdevumu tabulā ar attiecīgajiem lietotāja datiem, laiku, un izdevumu datiem
            db.execute("INSERT INTO expense (user_id, date, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                       (g.user["user_id"], int(time.time()), -expense, category, description))
            # Atjauno lietotāja kopējo izdevumu datus
            db.execute("UPDATE user SET total_expense = ? WHERE user_id = ?",
                       (expense_current_month(g, db), g.user["user_id"]))
            db.commit()
            return redirect(url_for("dashboard.dashboard"))

    return render_template("dashboard/dashboard.html", user_data=g.user, balanceForm=balanceForm, incomeForm=incomeForm, expenseForm=expenseForm)


# Šī funkcija piešķir tikai atgiriež /history lapu, jo funkcionalitāte tajā tiek
# nodrošināta izmantojot JavaScript un citas funkcijas
@bp.route("/history", methods=["GET"])
def history():
    return render_template("dashboard/history.html")


# Šī ir api funkcija, ko izmanto, dashboard lapa, lai iegūtu lietotāja finanšu datus
# lai izveidotu ienākumu un izdevumu vēsturi
@bp.route("/api/financedata/<datatype>/<count>", methods=["GET", "POST"])
def api_get_finance_data(datatype, count):
    # Pārveido mainīgos uz nepieciešamajiem tipiem
    datatype = str(datatype.lower())
    count = int(count)
    # Mainīgie, kur saglabā atriežamos datus
    data = {}
    db_data = []
    # Savienojas ar datubāzi
    db = get_db()

    # Iegūst gan ienākumu, gan izdevumu datus
    if datatype == "all":
        # No datubāzes iegūst nepieciešamo daudzumu ienākumu un izdevumu datus
        db_income_data = db.execute(
            "SELECT amount, category, description, date FROM income WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)
        db_expense_data = db.execute(
            "SELECT amount, category, description, date FROM expense WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)
        # Saliek gan ienākumu, gan izdevumu datus vienā sarakstā
        for row in db_income_data:
            db_data.append([row["amount"], row["category"],
                           row["description"], row["date"]])
        for row in db_expense_data:
            db_data.append([row["amount"], row["category"],
                           row["description"], row["date"]])
        # Sakārto kopējos datus sarakstā pēc laika, ar jaunākajiem datiem sākumā
        db_data.sort(reverse=True, key=lambda x: x[3])
    # Iegūst tikai ienākumu datus
    elif datatype == "income":
        db_data = db.execute(
            "SELECT amount, category, description FROM income WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)
    # Iegūst tikai izdevumu datus
    elif datatype == "expense":
        db_data = db.execute(
            "SELECT amount, category, description FROM expense WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)).fetchmany(count)
    # Nepieciešamo skaitu rindiņas saglabā dictonary
    for i, row in enumerate(db_data[:count]):
        data[str(i)] = [row[0], row[1], row[2], row[3]]
    # Atgriež datus JSON formātā
    return jsonify(data)


# Šī ir api funkcija, ko izmanto, dashboard lapa, lai atgriztu lietotāja finanšu datus
# lai izveidotu ienākumu un izdevumu vēsturi
@bp.route("/api/category/<type>", methods=["GET", "POST"])
def api_get_category(type):
    # Pārveido mainīgos uz nepieciešamajiem tipiem
    type = str(type.lower())
    # savienojas ar datubāzi
    db = get_db()
    category = None
    # No datubāzes izvēlas attiecīgi ienākumu vai izdevumu datus un tos atgriež
    if type == "income":
        category = db.execute("SELECT income_category FROM user WHERE user_id = ?",
                              (g.user["user_id"],)).fetchone()["income_category"]
    else:
        category = db.execute("SELECT expense_category FROM user WHERE user_id = ?",
                              (g.user["user_id"],)).fetchone()["expense_category"]
    return jsonify(category)


# Šī ir api funkcija, ko izmanto, dashboard lapa, lai atgriztu lietotāja finanšu datus
# lai izveidotu bilances un ienākumu/izdevumu grafikus attiecīgā laika posmā
@bp.route("/api/graphdata/<timeframe>/<timeframe_amount>", methods=["GET", "POST"])
def api_get_graph_data(timeframe, timeframe_amount):
    # Pārveido mainīgos uz nepieciešamajiem tipiem
    timeframe = str(timeframe.lower())
    timeframe_amount = int(timeframe_amount)
    # Mainīgie, kur saglabās datus apstrādes laikā
    data = {}
    income_data = []
    expense_data = []
    # Savienojas ar datubāzi
    db = get_db()

    # Laika posmi sekundēs
    unix_time_amount = {"week": 604800,
                        "month": 2629743,
                        "year": 31556926}

    # Iegūst nepieciešamo laika posmu datiem, ko vajag attēlot grafikā
    current_date = date.today()
    current_date_timestamp = int(
        datetime(current_date.year, current_date.month, current_date.day).timestamp())
    history_date_timestamp = current_date_timestamp - \
        (unix_time_amount[timeframe] * timeframe_amount)

    # Iegūst datus no datubāzes
    db_income_data = db.execute(
        "SELECT amount, category, date FROM income WHERE user_id = ? AND date > ? ORDER BY date DESC", (g.user["user_id"], history_date_timestamp)).fetchall()
    db_expense_data = db.execute(
        "SELECT amount, category, date FROM expense WHERE user_id = ? AND date > ? ORDER BY date DESC", (g.user["user_id"], history_date_timestamp)).fetchall()

    # Ievieto iegūtos datus sarakstos
    for row in db_income_data:
        income_data.append([row["amount"], row["date"], row["category"]])
    for row in db_expense_data:
        expense_data.append([row["amount"], row["date"], row["category"]])

    # Izveido dictionary ar ienākumu un izdevumu datiem, lai atgrieztu visus datus ar JSON
    data["income"] = income_data
    data["expense"] = expense_data

    return jsonify(data)
