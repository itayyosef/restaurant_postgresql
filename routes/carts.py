from flask import Blueprint
from controllers.carts import new_cart,show_cart,update_item,delete_item,confirm_delivery

carts_bp = Blueprint('carts',__name__)

carts_bp.add_url_rule('/cart',view_func=new_cart,methods=['GET','POST'])
carts_bp.add_url_rule('/show-cart',view_func=show_cart)
carts_bp.add_url_rule('/update-item-status/<int:id>',view_func=update_item,methods=["POST"])
carts_bp.add_url_rule('/delete-item/<int:id>',view_func=delete_item)
carts_bp.add_url_rule('/confirm-delivery',view_func=confirm_delivery,methods=["GET","POST"])

