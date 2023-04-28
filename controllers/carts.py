from flask import request,render_template,redirect,url_for,flash
from flask_login import login_required,current_user
from db import db
from models.category import Category
from models.delivery import Delivery
from models.items import Items
from models.dish import Dish
from models.cart import Cart
from utils import is_staff_member,calculate_order

@login_required
def new_cart():
    if is_staff_member() == True:
        return redirect(url_for("main_page")) 
    categories = Category.query.all() # to display all_dishes properly
    dishes = Dish.query.all()
    if request.method == "POST":
        cart = Cart.query.filter_by(user_id=current_user.id,finished_order=False).first() # tries to filter the first cart of the user's
        if not cart: # if cart == None
            cart = Cart(
                user_id=current_user.id,
                delivery_id=None,
                finished_order = False
                # because i want the delivery to be made at the end , and because cart object does not exist yet
                )
            try:
                db.session.add(cart)  # adding the cart to the catabase
                db.session.commit()
                flash("Cart created successfully.","success")
            except Exception as e:
                flash("Error creating cart: {}".format(str(e)),"error")
                return render_template("dishes/all_dishes.html",categories=categories,dishes=dishes)
            
        dish_id = request.form["dish_id"] # get the id of the desired dish
        amount = request.form["amount"] # get the amount of items after the cart is made
        dish = Dish.query.get(dish_id) # get the dish object itself
        # making a new item with the type of dish , cart_id and amount of items
        items = Items(
            dish_id=dish_id,
            cart_id=cart.id,
            amount=amount
        )
        db.session.add(items) # adding item to database
        db.session.commit()
        if amount == "1":   # message display
            flash(f"{amount} {dish.dish_name} has been added to the cart","success")
            return redirect(url_for('dishes.all_dishes'))
        if amount > "1":
            flash(f"{amount} {dish.dish_name}s have been added to the cart","success")
            return redirect(url_for('dishes.all_dishes'))
    else:
        return render_template("dishes/all_dishes.html",categories=categories,dishes=dishes)
    
@login_required
def show_cart():
    if is_staff_member() == True:
        return redirect(url_for("main_page")) 
    cart = Cart.query.filter_by(user_id=current_user.id,finished_order=False).first() # get the active cart
    if not cart:
        flash("You have not made a new cart yet , please add items to your cart first","error")
        flash("Go to userview to view latest delivery if made","error")
        return redirect(url_for("dishes.all_dishes"))
    return render_template("carts/one_cart.html",cart=cart,calculate_order=calculate_order(cart))

@login_required
def update_item(id):
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    if request.method == "POST":
        item = Items.query.get(id)
        item.amount = int(request.form.get('amount'))
        db.session.commit()
        flash('Item quantity updated successfully', 'success')
        return redirect(url_for('carts.show_cart'))
    else:
        return redirect(url_for("carts.show_cart"))

@login_required
def delete_item(id):
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    item = Items.query.get(id)
    dish_name = item.dish.dish_name
    if item and item.cart.user_id == current_user.id: # if the item exists and if it belongs to this cart
        db.session.delete(item)
        db.session.commit()
        flash(f"The item  {dish_name} has been deleted successfully","success")
    else:
        flash("Error deleting item.","error")
    return redirect(url_for("carts.show_cart"))

@login_required
def confirm_delivery():
    if is_staff_member() == True:
        return redirect(url_for("main_page")) 
    cart = Cart.query.filter_by(user_id=current_user.id,finished_order=False).first()
    if request.method == "POST":
        # make new delivery instance
        delivery = Delivery(
            address =  request.form["delivery_address"],
            comments = request.form["comments"],
            phone_for_delivery = request.form["phone_number"]
        )
        try:
            db.session.add(delivery)
            db.session.commit()
            if cart:
                if cart.items:
                    cart.delivery_id = delivery.id
                    cart.finished_order = True # make sure the user cant change the order after placing it
                    db.session.commit() # adding the delivery_id to the already existing cart object
                    flash("Your order was created successfully , for changes please call the business.","success")
                    return render_template('deliveries/one_delivery.html',delivery=delivery,calculate_order=calculate_order(cart))
                else:
                    flash("There are no items in your cart to make a delivery , please add items","error")
                    return(render_template("carts/one_cart.html",delivery=delivery,cart=cart))
            else:
                flash("There is no current active cart","error") # prevents adding items to a non-existent cart
                return render_template("carts/one_cart.html",delivery=delivery,cart=cart)
        except Exception as e:
            flash(f"Error {e}","error") # problem with the add or commit
            return render_template("carts/one_cart.html",delivery=delivery,cart=cart) 
        
    return redirect(url_for('carts.show-cart'))
    
    