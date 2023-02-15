from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField
from wtforms.validators import InputRequired, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=30)])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=30)])
    submit = SubmitField("Register")
    
class BalanceForm(FlaskForm):
    balance = DecimalField("Balance", validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField("Submit")
    
class IncomeForm(FlaskForm):
    income = DecimalField("Income", validators=[InputRequired(), NumberRange(min=0.01)])
    submit = SubmitField("Submit")
    
class ExpenseForm(FlaskForm):
    expense = DecimalField("Expense", validators=[InputRequired(), NumberRange(min=0.01)])
    submit = SubmitField("Submit")
