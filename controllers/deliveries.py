from flask import request,render_template,redirect,url_for,flash
from flask_login import login_required
from db import db
from models.cart import Cart
from utils import is_not_staff_member,calculate_order


@login_required
def manage_deliveries():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    carts = Cart.query.all()
    return render_template("deliveries/manage_deliveries.html",carts=carts,calculate_order=calculate_order)

@login_required
def change_delivery_status(id):
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    cart = Cart.query.get(id)
    if request.method == "POST":
        if cart:
            if not cart.delivery.is_delivered:
                cart.delivery.is_delivered = True
                db.session.commit()
                flash("The delivery status was changed successfully","success")
                return redirect(url_for('deliveries.manage_deliveries'))
            else:
                flash("The delivery has already been delivered","error")
                return redirect(url_for('deliveries.manage_deliveries'))
        else:
            flash('Invalid delivery ID',"error")
            return redirect(url_for('deliveries.manage_deliveries'))   
    return redirect(url_for('deliveries.manage_deliveries'))