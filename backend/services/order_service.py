from ..models.order_model import (
    create_sales_order,
    add_order_item,
    get_orders,
    get_order_items
)

def create_order(data):
    customer_id = data["customer_id"]
    order_date = data["order_date"]
    status = "pending"

    items = data["items"]

    # 1. Create order
    order_id = create_sales_order(customer_id, order_date, status)

    # 2. Add items
    for item in items:
        add_order_item(order_id, item["product_id"], item["quantity"])

    return order_id


def get_all_orders():
    rows = get_orders()

    orders = []
    for row in rows:
        orders.append({
            "id": row[0],
            "customer": row[1],
            "order_date": row[2],
            "status": row[3]
        })

    return orders


def get_order_details(order_id):
    rows = get_order_items(order_id)

    items = []
    for row in rows:
        items.append({
            "product": row[0],
            "quantity": row[1]
        })

    return items