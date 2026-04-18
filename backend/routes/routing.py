from flask import Blueprint, render_template, request, jsonify
from ..services.routing_service import (
    get_products,
    get_materials,
    get_routing_by_product,
    create_routing_with_steps,
    delete_routing
)

routing_bp = Blueprint('routing', __name__)

@routing_bp.route('/routing')
def routing_page():
    return render_template('routing.html')

@routing_bp.route('/api/finishedProducts')
def products():
    return jsonify(get_products())

@routing_bp.route('/api/materials')
def materials():
    return jsonify(get_materials())


@routing_bp.route('/api/routing/<int:product_id>')
def get_routing(product_id):
    return jsonify(get_routing_by_product(product_id))


@routing_bp.route('/api/routing', methods=['POST'])
def create_routing():
    data = request.json
    create_routing_with_steps(data)
    return jsonify({"message": "Routing saved"})


@routing_bp.route('/api/routing/<int:routing_id>', methods=['DELETE'])
def delete(routing_id):
    delete_routing(routing_id)
    return jsonify({"message": "Deleted"})