from flask import Blueprint, request, jsonify
from ..db import get_db_connection

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/api/customers", methods=["GET"])
def get_customers():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, address, phoneNumber FROM customers")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Convert tuple rows to dictionaries
    customers = []
    for row in rows:
        customers.append({
            "id": row[0],
            "name": row[1],
            "address": row[2],
            "phoneNumber": row[3]
        })

    return jsonify(customers)

@customers_bp.route("/api/customers", methods=["POST"])
def add_customer():

    data = request.json
    print("Incoming data:", data)

    name = data["name"]
    address = data["address"]
    phoneNumber = data["phoneNumber"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO customers (name, address, phoneNumber)
        VALUES (%s, %s, %s)
        """,
        (name, address, phoneNumber)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Customer added successfully"})

@customers_bp.route("/api/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM customers WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Customer deleted"})

@customers_bp.route("/api/customers/<int:id>", methods=["PUT"])
def update_customer(id):

    data = request.json

    name = data["name"]
    address = data["address"]
    phoneNumber = data["phoneNumber"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE customers
        SET name = %s,
            address = %s,
            phoneNumber = %s
        WHERE id = %s
        """,
        (name, address, phoneNumber, id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Customer updated"})