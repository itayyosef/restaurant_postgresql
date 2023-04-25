from db import db
class Cart(db.Model): # represents a user's cart, which can contain many Dish objects
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    delivery_id = db.Column(db.Integer,db.ForeignKey('delivery.id'),nullable=True)
    delivery = db.relationship('Delivery',backref='cart',uselist=False) # what determines the one to one relationship with delivery
    items = db.relationship('Items',backref='cart')
    finished_order = db.Column(db.Boolean,default=False)
