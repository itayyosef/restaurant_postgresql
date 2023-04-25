from flask import Blueprint
from controllers.users import new_signup,login,show_user,edit_user_details,order_history,logout

users_bp = Blueprint('users',__name__)


users_bp.add_url_rule('/signup',view_func=new_signup,methods=['GET','POST'])
users_bp.add_url_rule('/login',view_func=login,methods=['GET','POST'])
users_bp.add_url_rule('/user',view_func=show_user)
users_bp.add_url_rule('/edit-user-details',view_func=edit_user_details,methods=['GET','POST'])
users_bp.add_url_rule('/order-history',view_func=order_history)
users_bp.add_url_rule('/logout',view_func=logout)
