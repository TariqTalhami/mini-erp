from ..db import get_db_connection

def create_sales_order(customer_id, order_date, status):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sales_orders (customer_id, order_date, status)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (customer_id, order_date, status))

    order_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return order_id


def add_order_item(order_id, product_id, quantity):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sales_order_items (sales_order_id, product_id, quantity)
        VALUES (%s, %s, %s)
    """, (order_id, product_id, quantity))

    conn.commit()
    cur.close()
    conn.close()


def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT so.id, c.name, so.order_date, so.status
        FROM sales_orders so
        JOIN customers c ON so.customer_id = c.id
        ORDER BY so.id DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_order_items(order_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.name, soi.quantity
        FROM sales_order_items soi
        JOIN products p ON soi.product_id = p.id
        WHERE soi.sales_order_id = %s
    """, (order_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows