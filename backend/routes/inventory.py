from flask import Blueprint, request, jsonify
from ..services.inventory_service import (
    add_stock,
    remove_stock,
    get_stock,
    get_inventory_history
)

inventory_bp = Blueprint("inventory", __name__)


# Get current stock
@inventory_bp.route("/api/inventory/<int:product_id>", methods=["GET"])
def get_inventory(product_id):
    stock = get_stock(product_id)
    return jsonify({"product_id": product_id, "stock": stock})


# Add stock
@inventory_bp.route("/api/inventory/add", methods=["POST"])
def add_inventory():
    data = request.json

    add_stock(
        product_id=data["product_id"],
        quantity=data["quantity"],
        reference_id=data.get("reference_id")
    )

    return jsonify({"message": "Stock added"})


# Remove stock
@inventory_bp.route("/api/inventory/remove", methods=["POST"])
def remove_inventory():
    data = request.json

    remove_stock(
        product_id=data["product_id"],
        quantity=data["quantity"],
        reference_id=data.get("reference_id")
    )

    return jsonify({"message": "Stock removed"})


# Get movement history
@inventory_bp.route("/api/inventory/history/<int:product_id>", methods=["GET"])
def inventory_history(product_id):
    history = get_inventory_history(product_id)
    return jsonify(history)