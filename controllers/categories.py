from flask import request,render_template,redirect,url_for,flash
from flask_login import login_required
from db import db
from models.category import Category
from utils import is_not_staff_member


@login_required
def manage_categories():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    categories = Category.query.all()
    return render_template("categories/manage_categories.html",categories=categories)


@login_required
def delete_category(id):
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    category = Category.query.get(id)
    if request.method == "POST":
        for dish in category.dishes:
            db.session.delete(dish)
        db.session.delete(category)
        db.session.commit()
        flash("Category was successfully deleted along with it's dishes","success")
        return redirect(url_for("categories.manage_categories"))
    return render_template("categories/category_delete_confirm.html",category=category)


@login_required
def edit_category(id):
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    category = Category.query.get(id)
    if request.method == "POST":
        category.category_name = request.form["category_name"]
        category.image_url = request.form["image_url"]
        try:
            db.session.commit()
            flash("Category was successfully updated","success")
            return redirect(url_for('categories.manage_categories'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return render_template("categories/edit_category.html",category=category)
    return render_template("categories/edit_category.html",category=category)


@login_required
def create_category():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    if request.method == "POST":
        new_category = Category(
            category_name = request.form["category_name"],
            image_url = request.form["image_url"]
        )
        try:
            db.session.add(new_category)
            db.session.commit()
            flash("Category was successfully created","success")
            return redirect(url_for('categories.manage_categories'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return redirect(url_for('categories.manage_categories'))
    return render_template("categories/create_category.html")