from flask_login import UserMixin
from db import db
class User(db.Model,UserMixin): # represents a user of the website
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    is_staff = db.Column(db.Boolean,default=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    carts = db.relationship('Cart',backref='user')