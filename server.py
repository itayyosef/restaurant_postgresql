from flask import Flask,render_template
from db import db
from flask_login import current_user
from auth import login_manager
from routes.carts import carts_bp
from routes.categories import categories_bp
from routes.users import users_bp
from routes.dishes import dishes_bp
from routes.deliveries import deliveries_bp

# app init stage
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SECRET_KEY'] = '2345iok45j34nitm345fg0-2[tv345g23452]fg34'

# db init stage
db.init_app(app)

#init login_manager 
login_manager.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    if current_user.is_authenticated: # current user retrieves true or false from authenticated_user
        return render_template('users/main_page_auth.html')
    return render_template('main_page.html')

app.register_blueprint(carts_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(users_bp)
app.register_blueprint(dishes_bp)
app.register_blueprint(deliveries_bp)

if __name__ == "__main__":
    app.run(debug=True)