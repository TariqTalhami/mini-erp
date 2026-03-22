from ..models.inventory_model import (
    insert_movement,
    get_product_stock,
    get_movements
)

# Add stock (e.g. purchase, production)
def add_stock(product_id, quantity, reference_id=None):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    # Convert empty string to None
    if reference_id == "":
        reference_id = None

    insert_movement(product_id, quantity, "IN", reference_id)


# Remove stock (e.g. sale)
def remove_stock(product_id, quantity, reference_id=None):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    # Convert empty string to None
    if reference_id == "":
        reference_id = None

    current_stock = get_product_stock(product_id)

    if current_stock < quantity:
        raise ValueError("Not enough stock")

    insert_movement(product_id, -quantity, "OUT", reference_id)


# Get current stock
def get_stock(product_id):
    return get_product_stock(product_id)


# Get movement history
def get_inventory_history(product_id):
    rows = get_movements(product_id)

    movements = []
    for row in rows:
        movements.append({
            "id": row[0],
            "quantity": row[1],
            "movement_type": row[2],
            "reference_id": row[3],
            "created_at": row[4]
        })

    return movements