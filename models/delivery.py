from db import db
from datetime import datetime as dt
class Delivery(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    is_delivered = db.Column(db.Boolean,default=False)
    address = db.Column(db.String(200),nullable=False)
    comments = db.Column(db.String(500))
    phone_for_delivery = db.Column(db.String(11),nullable=False)
    created = db.Column(db.DateTime,default=dt.now)