from flask import Blueprint
from controllers.dishes import all_dishes,show_by_category,manage_dishes,create_dish,edit_dish,delete_dish

dishes_bp = Blueprint('dishes',__name__)

dishes_bp.add_url_rule('/dishes',view_func=all_dishes)
dishes_bp.add_url_rule('/dishes/category/<int:id>',view_func=show_by_category)
dishes_bp.add_url_rule('/manage-dishes',view_func=manage_dishes)
dishes_bp.add_url_rule('/create-dish',view_func=create_dish,methods=["GET","POST"])
dishes_bp.add_url_rule('/edit-dish/<int:id>',view_func=edit_dish,methods=["GET","POST"])
dishes_bp.add_url_rule('/delete-dish/<int:id>',view_func=delete_dish,methods=["GET","POST"])
