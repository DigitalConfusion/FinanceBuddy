# Importē bibliotēkas
import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import json

# No python moduļu failiem importē nepieciešamo
from app.forms import *
from app.db import get_db

# Izveido blueprint ar ko tiks associēta attiecīgā lapa un tās funkcija
bp = Blueprint("auth", __name__, url_prefix="/auth")

# Ienākumu un izdevumu kategorijas, kas ir pieejamas katram lietotājam, izveidojot kontu
income_categories = ["Work", "Other", "Personal Income", "Sold Item"]
expense_categories = ["Groceries", "Other", "Home", "Beauty", "Restaurant"]


# Šī funkcija piešķir funkcionalitāti /register lapai, jeb dod iespēju reģistrēties
@bp.route("/register", methods=["POST", "GET"])
def register():
    # Izveido formu pēc kuras lietotājs ievadīs datus, un padod to html lapai
    form = RegisterForm(request.form)
    # Ja lapa nosūta ievadītos datus atpakaļ uz serveri, tie tiek pārbaudīti
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Savienojas ar datubāzi
        db = get_db()
        # Mēģina datubāzē ievadīt ievadītos datus, lai izveidotu jaunu lietotāju
        try:
            db.execute("INSERT INTO user (username, password_hash, total_balance, total_income, total_expense, income_category, expense_category) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (username, generate_password_hash(password), 0, 0, 0, json.dumps(income_categories), json.dumps(expense_categories)),)
            db.commit()
        # Ja tāds lietotājs jau eksistē, parāda kļūdu
        except db.IntegrityError:
            error = f"User {username} is already registered!"
        # Ja izdodas ievadīt jauno lietotāju, aizved lietotāju uz login lapu
        else:
            return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html", form=form)

# Šī funkcija piešķir funkcionalitāti /login lapai, jeb dod iespēju pieslēgties


@bp.route("/", methods=["POST", "GET"])
@bp.route("/login", methods=["POST", "GET"])
def login():
    # Izveido formu pēc kuras lietotājs ievadīs datus, un padod to html lapai
    form = LoginForm(request.form)
    # Ja lapa nosūta ievadītos datus atpakaļ uz serveri, tie tiek pārbaudīti
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        error = None
        # Savienojas ar datubāzi
        db = get_db()
        # No datubāzes izvēlas attiecīgo lietotāju ar tādu lietotājvārdu
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        # Ja šāds lietotājs neeksitē parāda brīdinājumu
        if user is None:
            error = "This username does not exist!"
        # Ja ievadītā paroles kriptējums nesakrīt ar datubāzē saglabāto, parāda kļūdu,
        # ka parole nav pareiza
        elif not check_password_hash(user["password_hash"], password):
            error = "Incorrect password!"

        # Ja nav nekādu kļūdu, tad saglabā lietotāja id mājaslapas cookies,
        # lai atcerētos kāds lietotājs ir pieslēdzies
        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("dashboard.dashboard"))

        # Ja ir kļūda to parāda
        flash(error)

    return render_template("auth/login.html", form=form)

# Funkcija, kas saglabā pieslēgušā lietotāja datus speciālā Flask mainīgajā g
# Tas ļauj atjaunināt un vieglāk piekļūt lietotāja datiem


@bp.before_app_request
def load_logged_in_user():
    # No mājaslapas cookies nolasa lieotāja id
    user_id = session.get('user_id')

    # Ja lietotājs ir pieslēdzies, no datubāzes iegūst lietotāja datus un tos saglabā g mainīgajā
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchone()

# Ja lietotājs vēlas izlogoties no mājaslapas, tad notīra visus mājaslapas cookies, tādejādi
# arī pieslegušā lietotāja datus


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Funkcija, kas pārbauda vai lietotājs ir pieslēdzies,
# lai varētu piekļūt sensitīvajiem lietotāja datiem,
# jeb parādīt galvenās lapas ar viesiem lietotāja finanšu datiem


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Ja lietotājs ir pieslēdzies, tad viss kārtībā, ja nē atgriež lietotāju login lapā
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
