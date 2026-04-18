from ..models.routing_model import (
    fetch_finished_products,
    fetch_materials,
    fetch_routing_by_product,
    insert_routing,
    insert_routing_step,
    delete_steps_by_routing,
    delete_routing,
    insert_bom,
    insert_bom_item
)


def get_products():
    print("Fetching finished products only...")
    rows = fetch_finished_products()

    return [{"id": r[0], "name": r[1]} for r in rows]

def get_materials():
    rows = fetch_materials()
    
    return [{"id": r[0], "name": r[1]} for r in rows]


def get_routing_by_product(product_id):
    result = fetch_routing_by_product(product_id)

    if not result:
        return {}

    routing_id, steps = result

    return {
        "routing_id": routing_id,
        "steps": [
            {
                "id": s[0],
                "step_number": s[1],
                "step_name": s[2],
                "work_center": s[3],
                "estimated_time": s[4],
                "material_id": s[5]
            }
            for s in steps
        ]
    }


def create_routing_with_steps(data):
    product_id = data['product_id']

    # delete old routing first
    existing = fetch_routing_by_product(product_id)
    if existing:
        routing_id, _ = existing
        delete_steps_by_routing(routing_id)
        delete_routing(routing_id)

    steps = data['steps']

    # 1. Create routing
    routing_id = insert_routing(product_id)

    # 2. Create BOM
    bom_id = insert_bom(product_id)

    # 3. Insert steps + materials
    for i, step in enumerate(steps):
        step['step_number'] = i + 1

        step_id = insert_routing_step(routing_id, step)

        # 🔥 Save material if exists
        if step.get('material_id'):
            insert_bom_item(
                bom_id=bom_id,
                routing_step_id=step_id,
                material_id=step['material_id'],
                quantity=1  # default for now
            )


def delete_routing_with_steps(routing_id):
    delete_steps_by_routing(routing_id)
    delete_routing(routing_id)