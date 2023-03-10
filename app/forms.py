# Importē nepieciešamās bibliotēkas
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, DataRequired
from flask import g
import json

# No python moduļa faila iegūst datubāzes piekļūšanas funkciju
from app.db import get_db


# Datu ievades forma, ko izmanto priekš pieslēgšanās lapas
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=6, max=30)])
    submit = SubmitField("Log In")


# Datu ievades forma, ko izmanto priekš reģistrēšanās lapas
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=6, max=30)])
    submit = SubmitField("Register")


# Datu ievades forma, ko izmanto priekš bilances nomainīšanas loga datu ievades
class BalanceForm(FlaskForm):
    balance = DecimalField("Balance", validators=[
                           InputRequired(), NumberRange(min=0)])
    submit = SubmitField("Submit")


# Datu ievades palīgforma, kas tiek izmantota, lai pievienotu vēl vienu formas elementu, ja ir izvēlēta custom kategorija
class RequiredIf(DataRequired):
    def __init__(self, other_field_name, other_field_value, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.other_field_value = other_field_value
        self.message = message

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        if other_field.data == self.other_field_value:
            super(RequiredIf, self).__call__(form, field)


# Datu ievades forma, ko izmanto priekš ienākumu pievienošanas loga datu ievades
class IncomeForm(FlaskForm):
    income = DecimalField("Income", validators=[
                          InputRequired(), NumberRange(min=0.01)])
    income_category = SelectField('Category')
    custom_category = StringField("Custom_Category", validators=[
                                  RequiredIf('income_category', "Custom Category")])
    description = StringField("Description", validators=[])
    submit = SubmitField("Submit")

    # Kad forma tiek ielādēta mājaslapā, tad tiek papildināti izvēles lauki ar iespējamām kategorijām
    def __init__(self, *args, **kwargs):
        super().__init__()
        db = get_db()
        categories = db.execute("SELECT income_category FROM user WHERE user_id = ?",
                                (g.user["user_id"],)).fetchone()["income_category"]
        categories = json.loads(categories)
        categories.sort()
        categories.append("Custom Category")
        self.income_category.choices = categories


# Datu ievades forma, ko izmanto priekš izdevumu pievienošanas loga datu ievades
class ExpenseForm(FlaskForm):
    expense = DecimalField("Expense", validators=[
                           InputRequired(), NumberRange(min=0.01)])
    expense_category = SelectField('Category')
    custom_category2 = StringField("Custom_Category", validators=[
                                   RequiredIf('expense_category', "Custom Category")])
    description = StringField("Description", validators=[])
    submit = SubmitField("Submit")

    # Kad forma tiek ielādēta mājaslapā, tad tiek papildināti izvēles lauki ar iespējamām kategorijām
    def __init__(self, *args, **kwargs):
        super().__init__()
        db = get_db()
        categories = db.execute("SELECT expense_category FROM user WHERE user_id = ?",
                                (g.user["user_id"],)).fetchone()["expense_category"]
        categories = json.loads(categories)
        categories.sort()
        categories.append("Custom Category")
        self.expense_category.choices = categories
