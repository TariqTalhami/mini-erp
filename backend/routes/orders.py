from flask import Blueprint, request, jsonify
from ..services.order_service import (
    create_order,
    get_all_orders,
    get_order_details
)

orders_bp = Blueprint("orders", __name__)

# Create order
@orders_bp.route("/api/orders", methods=["POST"])
def create_new_order():
    data = request.json
    order_id = create_order(data)
    return jsonify({"message": "Order created", "order_id": order_id})


# Get all orders
@orders_bp.route("/api/orders", methods=["GET"])
def list_orders():
    return jsonify(get_all_orders())


# Get order details
@orders_bp.route("/api/orders/<int:order_id>", methods=["GET"])
def order_details(order_id):
    return jsonify(get_order_details(order_id))