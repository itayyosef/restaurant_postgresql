from flask import Blueprint
from controllers.deliveries import manage_deliveries,change_delivery_status

deliveries_bp = Blueprint('deliveries',__name__)

deliveries_bp.add_url_rule('/manage-deliveries',view_func=manage_deliveries)
deliveries_bp.add_url_rule('/change-delivery-status/<int:id>',view_func=change_delivery_status,methods=['GET','POST'])
