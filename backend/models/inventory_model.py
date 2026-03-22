from ..db import get_db_connection

# Insert a new inventory movement
def insert_movement(product_id, quantity, movement_type, reference_id=None):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO inventory_movements 
        (product_id, quantity, movement_type, reference_id)
        VALUES (%s, %s, %s, %s)
    """, (product_id, quantity, movement_type, reference_id))

    conn.commit()
    cur.close()
    conn.close()


# Get total stock for a product
def get_product_stock(product_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM inventory_movements
        WHERE product_id = %s
    """, (product_id,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result


# Get all movements for a product
def get_movements(product_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, quantity, movement_type, reference_id, created_at
        FROM inventory_movements
        WHERE product_id = %s
        ORDER BY created_at DESC
    """, (product_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# ================= GET ALL PRODUCTS WITH STOCK =================
def get_products_with_stock():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.id,
            p.name,
            p.product_type,
            COALESCE(SUM(im.quantity), 0) as stock
        FROM products p
        LEFT JOIN inventory_movements im 
            ON p.id = im.product_id
        GROUP BY p.id, p.name, p.product_type
        ORDER BY p.id
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows