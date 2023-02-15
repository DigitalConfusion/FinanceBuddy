import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.forms import *
from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None
        
        if error is None:
            try:
                db.execute("INSERT INTO user (username, password_hash, total_balance, total_income, total_expense) VALUES (?, ?, ?, ?, ?)",
                           (username, generate_password_hash(password), 0, 0, 0),)
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered!"
            else:
                return redirect(url_for("auth.login"))
        flash(error)
        
    return render_template("auth/register.html", form=form)

@bp.route("/", methods=["POST", "GET"])
@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        
        if user is None:
            error = "This username does not exist!"
        elif not check_password_hash(user["password_hash"], password):
            error = "Incorrect password!"
            
        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("dashboard.dashboard"))

        flash(error)
        
    return render_template("auth/login.html", form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
