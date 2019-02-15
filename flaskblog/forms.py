from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=1, max=15) ])
    email = StringField('Email', validators=[InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Signup')


#CUSTOM VALIDATION FOR REGISTER FORM
#Show error in case user tries to input available username/email
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username not available,choose another')

#Email validation:raise error if users tries to register existing email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email not available')


#LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
    save = BooleanField('remember me?')

#UPDATE USER ACCOUNT
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=1, max=15) ])
    email = StringField('Email', validators=[InputRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

#CUSTOM VALIDATION FOR UPDATING USER ACCOUNT
#only the owner of the account can update it
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username not available,choose another')
#email can only be updated by user currrrently loggd in
    def validate_email(self, email):
         if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email not available')

#NEW POSTS GO HERE
class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')