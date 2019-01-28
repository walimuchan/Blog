from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('Username', validators=[InputRequired(),Length(min=1, max=15) ])
    email = StringField('email', validators=[InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Signup')
    

class LoginForm(FlaskForm):
    email = StringField('email or username', validators=[InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
    save = BooleanField('remember me?')


    