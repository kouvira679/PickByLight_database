from database.schema import initialize_database
from database.queries import log_order_step
from opcua.opcua_reader import wait_and_read_rfid
from logic.order_logic import process_order_step
from opcua.opcua_task_writer import send_task_to_plc


def main():
    initialize_database()
    print("Python application started. Waiting for PLC triggers...")

    while True:
        try:
            # Step 1: wait for PLC trigger, then read RFID data
            rfid_result = wait_and_read_rfid()

            order_id = rfid_result["order_id"]
            model_id = rfid_result["model_id"]
            step_index = rfid_result["step_index"]

            # Step 2: process that step in Python
            order_result = process_order_step(model_id, step_index)

            print("Processed order step:")
            print(order_result)

            # Step 3: log processed step to database
            log_order_step(
                order_id=order_id,
                model_id=model_id,
                step_index=step_index,
                task_code=order_result["task_code"],
                part_name=order_result["part_name"],
                quantity=order_result["quantity"]
            )

            # Step 4: choose what step index to send back
            if order_result["is_final_step"]:
                plc_step_index = 0
                print(f"Model '{order_result['model_name']}' completed. Resetting step index to 0.")
            else:
                plc_step_index = order_result["next_step_index"]

            # Step 5: send task info + step index back to PLC
            send_task_to_plc(
                task_code=order_result["task_code"],
                quantity=order_result["quantity"],
                step_index=plc_step_index
            )

            print("Finished one cycle successfully.\n")

        except ValueError as e:
            print(f"Value error: {e}")

        except IndexError as e:
            print(f"Step error: {e}")

        except RuntimeError as e:
            print(f"Runtime error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()