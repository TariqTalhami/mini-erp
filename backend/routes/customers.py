# Import Flask tools:
# Blueprint → allows grouping routes into modules (customers module)
# request → used to access incoming request data (JSON body)
# jsonify → converts Python data into JSON response
from flask import Blueprint, request, jsonify

# Import database connection function from parent directory
from ..db import get_db_connection


# Create a Blueprint for customers-related routes
# "customers" is the name of the blueprint
customers_bp = Blueprint("customers", __name__)


# =========================
# GET ALL CUSTOMERS (READ)
# =========================
@customers_bp.route("/api/customers", methods=["GET"])
def get_customers():

    # Open database connection
    conn = get_db_connection()
    cur = conn.cursor()

    # Execute SQL query to fetch selected columns from customers table
    cur.execute("SELECT id, name, address, phoneNumber FROM customers")

    # Fetch all results (returns list of tuples)
    rows = cur.fetchall()

    # Close database resources
    cur.close()
    conn.close()

    # Convert tuple rows into dictionaries (JSON-friendly format)
    customers = []
    for row in rows:
        customers.append({
            "id": row[0],
            "name": row[1],
            "address": row[2],
            "phoneNumber": row[3]
        })

    # Return data as JSON response
    return jsonify(customers)


# =========================
# ADD CUSTOMER (CREATE)
# =========================
@customers_bp.route("/api/customers", methods=["POST"])
def add_customer():

    # Read JSON data sent from frontend
    data = request.json

    # Debug: print incoming request data in server logs
    print("Incoming data:", data)

    # Extract fields from request body
    name = data["name"]
    address = data["address"]
    phoneNumber = data["phoneNumber"]

    # Open database connection
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert new customer into database
    # %s placeholders prevent SQL injection
    cur.execute(
        """
        INSERT INTO customers (name, address, phoneNumber)
        VALUES (%s, %s, %s)
        """,
        (name, address, phoneNumber)
    )

    # Save changes to database
    conn.commit()

    # Close connection
    cur.close()
    conn.close()

    # Return success message
    return jsonify({"message": "Customer added successfully"})


# =========================
# DELETE CUSTOMER (DELETE)
# =========================
@customers_bp.route("/api/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):

    # Open database connection
    conn = get_db_connection()
    cur = conn.cursor()

    # Delete customer by ID
    cur.execute("DELETE FROM customers WHERE id = %s", (id,))

    # Save changes
    conn.commit()

    # Close connection
    cur.close()
    conn.close()

    # Return confirmation message
    return jsonify({"message": "Customer deleted"})


# =========================
# UPDATE CUSTOMER (UPDATE)
# =========================
@customers_bp.route("/api/customers/<int:id>", methods=["PUT"])
def update_customer(id):

    # Get updated data from frontend
    data = request.json

    name = data["name"]
    address = data["address"]
    phoneNumber = data["phoneNumber"]

    # Open database connection
    conn = get_db_connection()
    cur = conn.cursor()

    # Update customer record using provided ID
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

    # Save changes
    conn.commit()

    # Close connection
    cur.close()
    conn.close()

    # Return confirmation message
    return jsonify({"message": "Customer updated"})