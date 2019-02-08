from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=1, max=15) ])
    email = StringField('email', validators=[InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Signup')


#CUSTOM VALIDATION
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username not available,choose another')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email not available')


#LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField('email or username', validators=[InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
    save = BooleanField('remember me?')

#UPDATE ACCOUNT
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=1, max=15) ])
    email = StringField('email', validators=[InputRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

#CUSTOM VALIDATION
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username not available,choose another')

    def validate_email(self, email):
         if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email not available')

    