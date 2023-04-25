from db import db
class Items(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    dish_id = db.Column(db.Integer,db.ForeignKey('dish.id'),nullable=False)
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'),nullable=False)
    amount = db.Column(db.Integer,nullable=False)