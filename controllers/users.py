from flask import request,render_template,redirect,url_for,flash
from flask_login import login_user,login_required,current_user,logout_user
from db import db
from models.user import User
from models.cart import Cart
from utils import is_staff_member,calculate_order
from controllers.forms import SignupForm

def new_signup():
    if current_user.is_authenticated:
        return render_template('users/main_page_auth.html')
    
    signup_form = SignupForm()
    if request.method == "POST" and signup_form.validate_on_submit(): # validating the form is correctly filled
        if signup_form.password.data == signup_form.confirm_password.data : # password validation
            new_user = User(
                username = signup_form.username.data,
                password = signup_form.password.data,
                first_name = signup_form.first_name.data,
                last_name = signup_form.last_name.data,
                email = signup_form.email.data,
                is_staff = False # making sure the is_staff will be false
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Your account was created successfully , you can now login','success')
                return redirect(url_for('users.login')) # pass the user from signup to login after creating an account
            except Exception as e:
                print(e)
                flash("Account creation has failed , please try again","error")
                return render_template('users/signup.html',form=signup_form)
        else:
            flash("The passwords do not match , please try again","error")
            return render_template("users/signup.html",form=signup_form)
    return render_template('users/signup.html',form=signup_form)



def login():
    if current_user.is_authenticated:
        return render_template('users/main_page_auth.html')
    if request.method == "POST":
        # remember_me will return on or none , so if remember_me == on then remember the cookie
        remember = False
        if request.form.get("remember_me") == 'on':
            remember = True
        user = User.query.filter_by(username=request.form['username']).first() # get the first user with this username
        if user != None: # if a match was found with the user attempting to log in
            if request.form['password'] == user.password: # password validation
                login_user(user,remember=remember)
                flash('You have successfully logged in')
                return redirect(url_for('main_page'))
            else:
                flash("The username or password you logged with are incorrect.","error")
        else:
            flash("No user found with this username , please try again.",'error')
    return render_template('users/login.html')


@login_required
def show_user():
    if is_staff_member() == True: # block staff users from entering the normal customer site
        return redirect(url_for("main_page"))
    cart = Cart.query.filter_by(user_id=current_user.id).order_by(Cart.id.desc()).first()
    return render_template('users/user.html',cart=cart)


@login_required
def edit_user_details():
    if is_staff_member() == True:
        return redirect(url_for("main_page")) 
    
    if request.method == "POST": # no need to make a "new" user , can use current_user
        if request.form['current_password'] == current_user.password:
             # if passwords match in form , or both password and confirm_password == empty string , and change all details but password
            if request.form.get("submit_changes") == "on":
                current_user.username = request.form['username']
                current_user.first_name = request.form['first_name']
                current_user.last_name = request.form['last_name']
                current_user.email = request.form['email']
                
                # check if the password fields are not empty and match, and only update the password if they do
                if request.form['password'] != "" or request.form['confirm_password'] != "":
                    if request.form['password'] == request.form['confirm_password']:
                        if request.form['password'] != current_user.password:
                            current_user.password = request.form['password']
                            flash("Password has been updated", "success")
                        else:
                            flash("The new password must be different from the old password", "error")
                            return render_template("users/edit_user_details.html")
                    else:
                        flash("Passwords must match in order to update.", "error")
                        return render_template("users/edit_user_details.html")
            else:
                flash("Must tick the 'Are you sure you want these changes in details' checkbox", "error")
                return render_template("users/edit_user_details.html")
            try :
                db.session.commit()
                flash('Your account details have been successfully updated',"success")
                return redirect(url_for('users.show_user'))
            except Exception as e:
                flash(f"Error {e}","error")
                return render_template('users/user.html')
        else:
            flash("Password confirmation failed fill in your current password, please try again","error")
            return render_template("users/edit_user_details.html")
    return render_template("users/edit_user_details.html")


@login_required
def order_history():
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    all_user_carts = Cart.query.filter_by(user_id=current_user.id).all()
    # sending the func without activating it , so i can get the cart parameter in the template
    return render_template("users/order_history.html",all_user_carts=all_user_carts,calculate_order=calculate_order)


@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))