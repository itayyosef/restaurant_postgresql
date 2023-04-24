from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email


class SignupForm(FlaskForm):
    username = StringField('Username',validators=[
        DataRequired("Please enter a username."),
        Length(4,20,"Username length must be between 4 to 20 characters")])
    
    password = PasswordField("Password",validators=[
        DataRequired("Please enter a password")])
    
    confirm_password = PasswordField("Confirm Password",validators=[
        DataRequired("Please confirm your password"),
        EqualTo("password","Passwords Must Match")])
    
    first_name = StringField("First Name",validators=[
        DataRequired("Please enter a first name")])
    
    last_name = StringField("Last Name",validators=[
        DataRequired("Please enter a last name")])
    
    email = StringField('Email',validators=[
        DataRequired("Please enter an email"),
        Email("Please enter a valid Email format")])
    
    submit = SubmitField("Sign Up")