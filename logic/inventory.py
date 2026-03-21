from database.db import get_connection

'''
before running main program initialize the database once
python -m database.schema
or
python database/schema.py
'''


def get_inventory():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT part_name, quantity FROM inventory")
    rows = cursor.fetchall()

    conn.close()

    return {part_name: quantity for part_name, quantity in rows}


def get_part_quantity(part_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT quantity FROM inventory WHERE part_name = ?",
        (part_name,)
    )
    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise ValueError(f"Unknown part: {part_name}")

    return row[0]


def use_part(part_name, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT quantity FROM inventory WHERE part_name = ?",
        (part_name,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise ValueError(f"Unknown part: {part_name}")

    current_quantity = row[0]

    if current_quantity < quantity:
        conn.close()
        raise ValueError(
            f"Not enough stock for {part_name}. "
            f"Available: {current_quantity}, Requested: {quantity}"
        )

    new_quantity = current_quantity - quantity

    cursor.execute(
        "UPDATE inventory SET quantity = ? WHERE part_name = ?",
        (new_quantity, part_name)
    )

    conn.commit()
    conn.close()

    return new_quantity