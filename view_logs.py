from database.queries import get_order_logs


def main():
    logs = get_order_logs(limit=20)

    if not logs:
        print("No logs found.")
        return

    print("\n=== ORDER LOGS ===\n")

    for log in logs:
        log_id, order_id, model_id, step_index, task_code, part_name, quantity, created_at = log

        print(f"Log ID: {log_id}")
        print(f"Order ID: {order_id}")
        print(f"Model ID: {model_id}")
        print(f"Step Index: {step_index}")
        print(f"Task Code: {task_code}")
        print(f"Part: {part_name}")
        print(f"Quantity: {quantity}")
        print(f"Time: {created_at}")
        print("-" * 30)


if __name__ == "__main__":
    main()