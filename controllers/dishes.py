from flask import render_template,redirect,url_for,request,flash
from flask_login import login_required
from models.dish import Dish
from models.category import Category
from utils import is_staff_member,is_not_staff_member
from db import db

@login_required
def all_dishes():
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    categories = Category.query.all()
    dishes = Dish.query.all()
    return render_template('dishes/all_dishes.html',categories=categories,dishes=dishes)


@login_required
def show_by_category(id):
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    category = Category.query.get(id)
    categories = Category.query.all()
    dishes = Category.query.get(id).dishes
    return render_template("dishes/dishes_by_category.html",dishes=dishes,categories=categories,category=category)


@login_required
def manage_dishes():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    dishes = Dish.query.all()
    return render_template("dishes/manage_dishes.html",dishes=dishes)


@login_required
def create_dish():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    categories = Category.query.all()
    if request.method == "POST":
        is_gluten_free = request.form.get('is_gluten_free') == 'on'
        is_vegeterian = request.form.get('is_vegetarian') == "on"
        new_dish = Dish(
            dish_name = request.form["dish_name"],
            price = request.form["price"],
            description = request.form["description"],
            imageURL = request.form["image_url"],
            is_gluten_free = is_gluten_free,
            is_vegeterian = is_vegeterian,
            category_id = request.form.get("category_dish")
        )
        if not new_dish.category_id :
            flash("Please select a category before continuing.", "error")
            return redirect(url_for("dishes.create_dish"))
        try:
            db.session.add(new_dish)
            db.session.commit()
            flash("Dish was successfully created","success")
            return redirect(url_for('dishes.manage_dishes'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return redirect(url_for('dishes.create_dish'))
    return render_template("dishes/create_dish.html",categories=categories)


@login_required
def edit_dish(id):
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    categories = Category.query.all()
    dish = Dish.query.get(id)
    if request.method == "POST":
        is_gluten_free = request.form.get('is_gluten_free') == 'on'
        is_vegeterian = request.form.get('is_vegetarian') == "on"
        dish.dish_name = request.form["dish_name"]
        dish.price = request.form["price"]
        dish.description = request.form["description"]
        dish.imageURL = request.form["image_URL"]
        dish.is_gluten_free = is_gluten_free
        dish.is_vegeterian = is_vegeterian
        dish.category_id = request.form["category_dish"]
        try:
            db.session.commit()
            flash("dish was successfully updated","success")
            return redirect(url_for('dishes.manage_dishes'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return render_template("dishes/edit_dish.html",dish=dish,categories=categories)
    return render_template("dishes/edit_dish.html",dish=dish,categories=categories)


@login_required
def delete_dish(id):
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    dish = Dish.query.get(id)
    if request.method == "POST":
        db.session.delete(dish)
        db.session.commit()
        flash("Dish was successfully deleted","success")
        return redirect(url_for("dishes.manage_dishes"))
    return render_template("dishes/dish_delete_confirm.html",dish=dish)