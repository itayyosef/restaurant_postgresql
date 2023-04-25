
from flask import redirect,url_for,flash
from flask_login import LoginManager
from models.user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id): # userloader gets 1 parameter , user_id
    return User.query.get(int(user_id)) # because the id's are integers

@login_manager.unauthorized_handler # function that deals with unauthorized users.
def unauthorized():
    flash('Access denied , please log in first','error')
    return redirect(url_for('users.login'))