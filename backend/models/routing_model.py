from ..db import get_db_connection


def fetch_finished_products():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name
        FROM products
        WHERE product_type = 'finished'
    """)

    rows = cur.fetchall()
    conn.close()

    return rows

def fetch_materials():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name
        FROM products
        WHERE product_type = 'primary_material'
    """)

    rows = cur.fetchall()
    conn.close()

    return rows


def fetch_routing_by_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM routings
        WHERE product_id = %s
        ORDER BY version DESC
        LIMIT 1
    """, (product_id,))

    routing = cur.fetchone()

    if not routing:
        conn.close()
        return None

    routing_id = routing[0]

    cur.execute("""
        SELECT 
            rs.id,
            rs.step_number,
            rs.step_name,
            rs.work_center,
            rs.estimated_time_minutes,
            bi.material_id
        FROM routing_steps rs
        LEFT JOIN bom_items bi 
            ON bi.routing_step_id = rs.id
        WHERE rs.routing_id = %s
        ORDER BY rs.step_number
    """, (routing_id,))

    steps = cur.fetchall()

    conn.close()

    return routing_id, steps


def insert_routing(product_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO routings (product_id)
        VALUES (%s)
        RETURNING id
    """, (product_id,))

    routing_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return routing_id


def insert_routing_step(routing_id, step):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO routing_steps
        (routing_id, step_number, step_name, work_center, estimated_time_minutes)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (
        routing_id,
        step['step_number'],
        step['step_name'],
        step['work_center'],
        step['estimated_time']
    ))

    step_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return step_id


def delete_steps_by_routing(routing_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM routing_steps
        WHERE routing_id = %s
    """, (routing_id,))

    conn.commit()
    conn.close()


def delete_routing(routing_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM routings
        WHERE id = %s
    """, (routing_id,))

    conn.commit()
    conn.close()

def insert_bom(product_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bill_of_materials (product_id)
        VALUES (%s)
        RETURNING id
    """, (product_id,))

    bom_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return bom_id

def insert_bom_item(bom_id, routing_step_id, material_id, quantity):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bom_items
        (bom_id, routing_step_id, material_id, quantity_per_unit)
        VALUES (%s, %s, %s, %s)
    """, (bom_id, routing_step_id, material_id, quantity))

    conn.commit()
    conn.close()