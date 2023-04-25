from db import db
class Dish(db.Model): #  represents a dish that can be purchased by users
    id = db.Column(db.Integer,primary_key=True)
    dish_name = db.Column(db.String(100),nullable=False,unique=True)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.String(1000),nullable=False)
    imageURL = db.Column(db.String(5000),nullable=False)
    is_gluten_free = db.Column(db.Boolean,default=False)
    is_vegeterian = db.Column(db.Boolean,default=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'), nullable=False)
    items = db.relationship('Items',backref="dish")