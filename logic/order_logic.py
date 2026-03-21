from models.model_catalog import get_model, get_step_for_model
from logic.inventory import use_part


def process_order_step(model_id, step_index):
    """
    Given a model_id and step_index:
    1. Find the correct workplan step
    2. Subtract required inventory
    3. Return task info for PLC output
    4. Detect whether this is the final step
    """

    model = get_model(model_id)
    if model is None:
        raise ValueError(f"Unknown model_id: {model_id}")

    workplan = model["workplan"]
    step = get_step_for_model(model_id, step_index)

    part_name = step["part_name"]
    quantity = step["quantity"]
    task_code = step["task_code"]

    remaining_quantity = use_part(part_name, quantity)

    is_final_step = step_index == len(workplan) - 1

    if is_final_step:
        next_step_index = step_index
    else:
        next_step_index = step_index + 1

    return {
        "model_id": model_id,
        "step_index": step_index,
        "task_code": task_code,
        "part_name": part_name,
        "quantity": quantity,
        "remaining_inventory": remaining_quantity,
        "next_step_index": next_step_index,
        "is_final_step": is_final_step,
        "model_name": model["model_name"],
    }