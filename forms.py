from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,   Form, validators, ValidationError
from wtforms.validators import InputRequired, Optional, Email
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators = [Optional(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
