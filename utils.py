from flask_login import current_user
from flask import flash

def calculate_order(cart):
    total_dish_price = 0
    for item in cart.items:
        total_dish_price += item.dish.price * item.amount
    return total_dish_price

def is_staff_member(): # one function instead of writing the code 10+ times
    if current_user.is_authenticated and current_user.is_staff:
        flash("This account does not have access to that part of the website , sorry.","error")
        return True
    return False

def is_not_staff_member():
    if current_user.is_authenticated and not current_user.is_staff:
        flash("This account does not have access to that part of the website , sorry.","error")
        return True
    return False