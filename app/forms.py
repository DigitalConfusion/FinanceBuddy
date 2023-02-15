from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField("Register")
    
class BalanceForm(FlaskForm):
    balance = DecimalField("Balance", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class IncomeForm(FlaskForm):
    income = DecimalField("Income", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class ExpenseForm(FlaskForm):
    expense = DecimalField("Expense", validators=[DataRequired()])
    submit = SubmitField("Submit")
