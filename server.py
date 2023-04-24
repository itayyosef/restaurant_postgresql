from flask import Flask,render_template,request,redirect,url_for,flash
from db import db
from datetime import datetime as dt
from datetime import timedelta
from flask_login import LoginManager,UserMixin,login_user,current_user,login_required,logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from signup_form import SignupForm

# app init stage
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SECRET_KEY'] = '2345iok45j34nitm345fg0-2[tv345g23452]fg34'

# db init stage
db.init_app(app)


#init login_manager 
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model,UserMixin): # represents a user of the website
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    is_staff = db.Column(db.Boolean,default=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    carts = db.relationship('Cart',backref='user')

class Cart(db.Model): # represents a user's cart, which can contain many Dish objects
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    delivery_id = db.Column(db.Integer,db.ForeignKey('delivery.id'),nullable=True)
    delivery = db.relationship('Delivery',backref='cart',uselist=False) # what determines the one to one relationship with delivery
    items = db.relationship('Items',backref='cart')
    finished_order = db.Column(db.Boolean,default=False)

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


class Category(db.Model): # represents a category that a dish can belong to
    id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(100),nullable=False,unique=True)
    image_url = db.Column(db.String(5000),nullable=False)
    dishes = db.relationship('Dish',backref='category')

class Delivery(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    is_delivered = db.Column(db.Boolean,default=False)
    address = db.Column(db.String(200),nullable=False)
    comments = db.Column(db.String(500))
    phone_for_delivery = db.Column(db.String(11),nullable=False)
    created = db.Column(db.DateTime,default=dt.now)

    
class Items(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    dish_id = db.Column(db.Integer,db.ForeignKey('dish.id'),nullable=False)
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'),nullable=False)
    amount = db.Column(db.Integer,nullable=False)

@login_manager.user_loader
def load_user(user_id): # userloader gets 1 parameter , user_id
    return User.query.get(int(user_id)) # because the id's are integers

@login_manager.unauthorized_handler # function that deals with unauthorized users.
def unauthorized():
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    if current_user.is_authenticated: # current user retrieves true or false from authenticated_user
        return render_template('main_page_auth.html')
    return render_template('main_page.html')

@app.route('/signup',methods=['GET','POST'])
def new_signup():
    if current_user.is_authenticated:
        return render_template('main_page_auth.html')
    
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
                return redirect(url_for('login')) # pass the user from signup to login after creating an account
            except Exception as e:
                print(e)
                flash("Account creation has failed , please try again","error")
                return render_template('signup.html',form=signup_form)
        else:
            flash("The passwords do not match , please try again","error")
            return render_template("signup.html",form=signup_form)
    return render_template('signup.html',form=signup_form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return render_template('main_page_auth.html')
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
    return render_template('login.html')

@app.route('/user')
@login_required
def show_user():
    if is_staff_member() == True: # block staff users from entering the normal customer site
        return redirect(url_for("main_page"))
    cart = Cart.query.filter_by(user_id=current_user.id).order_by(Cart.id.desc()).first()
    return render_template('user.html',cart=cart)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dishes')
@login_required
def all_dishes():
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    categories = Category.query.all()
    dishes = Dish.query.all()
    return render_template('all_dishes.html',categories=categories,dishes=dishes)

@app.route('/dishes/category/<int:id>')
@login_required
def show_by_category(id):
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    category = Category.query.get(id)
    categories = Category.query.all()
    dishes = Category.query.get(id).dishes
    return render_template("dishes_by_category.html",dishes=dishes,categories=categories,category=category)

@app.route('/cart',methods=['GET','POST'])
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
                return render_template("all_dishes.html",categories=categories,dishes=dishes)
            
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
            return redirect(url_for('all_dishes'))
        if amount > "1":
            flash(f"{amount} {dish.dish_name}s have been added to the cart","success")
            return redirect(url_for('all_dishes'))
    else:
        return render_template("all_dishes.html",categories=categories,dishes=dishes)

@app.route('/show-cart')
@login_required
def show_cart():
    if is_staff_member() == True:
        return redirect(url_for("main_page")) 
    cart = Cart.query.filter_by(user_id=current_user.id,finished_order=False).first() # get the active cart
    if not cart:
        flash("You have not made a new cart yet , please add items to your cart first","error")
        flash("To see the current delivery , go to user view.","error")
        return redirect(url_for("all_dishes"))
    return render_template("one_cart.html",cart=cart,calculate_order=calculate_order(cart))

@app.route('/update-item-status/<int:id>',methods=["POST"])
@login_required
def update_item(id):
    if request.method == "POST":
        item = Items.query.get(id)
        item.amount = int(request.form.get('amount'))
        db.session.commit()
        flash('Item quantity updated successfully', 'success')
        return redirect(url_for('show_cart'))
    else:
        return redirect("show_cart")

@app.route('/confirm-delivery',methods=["GET","POST"])
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
                cart.delivery_id = delivery.id
                cart.finished_order = True # make sure the user cant change the order after placing it
                db.session.commit() # adding the delivery_id to the already existing cart object
                flash("Your order was created successfully , for changes please call the business.","success")
                return render_template('one_delivery.html',delivery=delivery,calculate_order=calculate_order(cart))
            else:
                flash("There is no current active cart","error")
                return render_template("one_cart.html",delivery=delivery,cart=cart)
        except Exception as e:
            flash(f"Error {e}","error")
            return render_template("one_cart.html",delivery=delivery,cart=cart) 
        
    flash("There was a problem with creating your order.","error")
    return redirect(url_for('show-cart'))

@app.route('/delete-item/<int:id>')
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
    return redirect(url_for("show_cart"))

@app.route('/edit-user-details',methods=['GET','POST'])
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
                            return render_template("edit_user_details.html")
                    else:
                        flash("Passwords must match in order to update.", "error")
                        return render_template("edit_user_details.html")
            else:
                flash("Must tick the 'Are you sure you want these changes in details' checkbox", "error")
                return render_template("edit_user_details.html")
            try :
                db.session.commit()
                flash('Your account details have been successfully updated',"success")
                return redirect(url_for('show_user'))
            except Exception as e:
                flash(f"Error {e}","error")
                return render_template('user.html')
        else:
            flash("Password confirmation failed fill in your current password, please try again","error")
            return render_template("edit_user_details.html")
    return render_template("edit_user_details.html")

@app.route('/order-history')
@login_required
def order_history():
    if is_staff_member() == True:
        return redirect(url_for("main_page"))
    all_user_carts = Cart.query.filter_by(user_id=current_user.id).all()
    # sending the func without activating it , so i can get the cart parameter in the template
    return render_template("order_history.html",all_user_carts=all_user_carts,calculate_order=calculate_order)

@app.route('/manage-deliveries')
@login_required
def manage_deliveries():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    carts = Cart.query.all()
    return render_template("manage_deliveries.html",carts=carts,calculate_order=calculate_order)

@app.route('/change-delivery-status/<int:id>',methods=['GET','POST'])
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
                return redirect(url_for('manage_deliveries'))
            else:
                flash("The delivery has already been delivered","error")
                return redirect(url_for('manage_deliveries'))
        else:
            flash('Invalid delivery ID',"error")
            return redirect(url_for('manage_deliveries'))   
    return redirect(url_for('manage_deliveries'))

@app.route('/manage-categories')
@login_required
def manage_categories():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    categories = Category.query.all()
    return render_template("manage_categories.html",categories=categories)

@app.route('/delete-category/<int:id>',methods=["GET","POST"])
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
        return redirect(url_for("manage_categories"))
    return render_template("category_delete_confirm.html",category=category)

@app.route('/edit_category/<int:id>',methods=["GET","POST"])
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
            return redirect(url_for('manage_categories'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return render_template("edit_category.html",category=category)
    return render_template("edit_category.html",category=category)

@app.route('/create-category',methods=["GET","POST"])
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
            return redirect(url_for('manage_categories'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return redirect(url_for('manage_categories'))
    return render_template("create_category.html")

@app.route('/manage-dishes',methods=["GET","POST"])
@login_required
def manage_dishes():
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    dishes = Dish.query.all()
    return render_template("manage_dishes.html",dishes=dishes)

@app.route('/create-dish',methods=["GET","POST"])
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
            return redirect(url_for("create_dish"))
        try:
            db.session.add(new_dish)
            db.session.commit()
            flash("Dish was successfully created","success")
            return redirect(url_for('manage_dishes'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return redirect(url_for('create_dish'))
    return render_template("create_dish.html",categories=categories)
    
@app.route('/edit-dish/<int:id>',methods=["GET","POST"])
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
            return redirect(url_for('manage_dishes'))
        except Exception as e:
            flash(f"Error : {e}","error")
            return render_template("edit_dish.html",dish=dish,categories=categories)
    return render_template("edit_dish.html",dish=dish,categories=categories)

@app.route('/delete-dish/<int:id>',methods=["GET","POST"])
@login_required
def delete_dish(id):
    if is_not_staff_member() == True:
        return redirect(url_for("main_page"))
    dish = Dish.query.get(id)
    if request.method == "POST":
        db.session.delete(dish)
        db.session.commit()
        flash("Dish was successfully deleted","success")
        return redirect(url_for("manage_dishes"))
    return render_template("dish_delete_confirm.html",dish=dish)

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


if __name__ == "__main__":
    app.run(debug=True)




# @app.route('/return_book/<int:id>', methods=['GET','POST'])
# @login_required
# def return_book(id):
#     loan = Loan.query.get(id)
#     if loan:
#         if not loan.did_return:
#             loan.did_return = True
#             db.session.commit()
#             flash('Book successfully returned!', 'success')
#         else:
#             flash('Book has already been returned', 'error')
#     else:
#         flash('Invalid loan ID', 'error')
#     return redirect(url_for('show_user'))




#  <div>{{last_delivery.address}}</div>
# <div>{{last_delivery.comments}}</div>
# <div>{{last_delivery.created}}</div> 
# {% if last_delivery.is_delivered %}
#     <p>Your order has been delivered!</p>
#     {% else %}
#     <p>Your order is on it's way</p>
#     {% endif %}

    # current_user_carts = current_user.carts
    # previous_cart = current_user_carts[-1]
    # previous_delivery = previous_cart.delivery ,previous_delivery=previous_delivery