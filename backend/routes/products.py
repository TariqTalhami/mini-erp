from flask import Blueprint, request, jsonify
from db import get_db_connection

products_bp = Blueprint("products", __name__)

@products_bp.route("/api/products", methods=["GET"])
def get_products():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, product_type, unit FROM products")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Convert tuple rows to dictionaries
    products = []
    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "product_type": row[2],
            "unit": row[3]
        })

    return jsonify(products)

@products_bp.route("/api/products", methods=["POST"])
def add_product():

    data = request.json
    print("Incoming data:", data)

    name = data["name"]
    product_type = data["product_type"]
    unit = data["unit"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO products (name, product_type, unit)
        VALUES (%s, %s, %s)
        """,
        (name, product_type, unit)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Product added successfully"})

@products_bp.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Product deleted"})

@products_bp.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):

    data = request.json

    name = data["name"]
    product_type = data["product_type"]
    unit = data["unit"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE products
        SET name = %s,
            product_type = %s,
            unit = %s
        WHERE id = %s
        """,
        (name, product_type, unit, id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Product updated"})