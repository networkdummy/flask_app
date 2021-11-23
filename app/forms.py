from flask_wtf import FlaskForm
from wtforms import StringField, TextField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class QueryForm(FlaskForm):
    querybody = TextAreaField('QueryBody', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    #email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email')])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In') 

class SignupForm(FlaskForm):
    #email = StringField('Email', validators=[Length(min=6),Email(message='Enter a valid email.'), DataRequired()])
    email = StringField('Email', validators=[Length(min=6), DataRequired()])
    fname= StringField('First Name', validators=[DataRequired()])
    lname= StringField('Last Name', validators=[DataRequired()])
    classcode= StringField('Class Code', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')
