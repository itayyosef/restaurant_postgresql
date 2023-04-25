from flask import Blueprint
from controllers.categories import manage_categories,delete_category,edit_category,create_category

categories_bp = Blueprint('categories',__name__)

categories_bp.add_url_rule('/manage-categories',view_func=manage_categories)
categories_bp.add_url_rule('/delete-category/<int:id>',view_func=delete_category,methods=["GET","POST"])
categories_bp.add_url_rule('/edit_category/<int:id>',view_func=edit_category,methods=["GET","POST"])
categories_bp.add_url_rule('/create-category',view_func=create_category,methods=["GET","POST"])
