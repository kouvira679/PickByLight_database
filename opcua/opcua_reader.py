import time
from opcua.opcua_client import OPCUAClient

# Replace this with your real PLC endpoint
ENDPOINT = "opc.tcp://172.21.x.1:4840"

# PLC node ids
RFID_NODE_ID = 'ns=3;s="identData"."readData"'
AWAIT_APP_NODE_ID = 'ns=3;s="abstractMachine"."awaitApp"'


def parse_rfid_data(raw_data):
    """
    Expected RFID schema:
    byte[0:4] = order_id
    byte[4]   = model_id
    byte[5]   = step_index
    """

    if raw_data is None:
        raise ValueError("RFID data is empty")

    if isinstance(raw_data, list):
        raw_data = bytes(raw_data)

    if len(raw_data) < 6:
        raise ValueError(f"RFID data too short: {raw_data}")

    order_id = int.from_bytes(raw_data[0:4], byteorder="little")
    model_id = raw_data[4]
    step_index = raw_data[5]

    return order_id, model_id, step_index


def wait_for_trigger(poll_interval=0.2):
    opc_client = OPCUAClient(ENDPOINT)

    try:
        opc_client.connect()

        await_app_node = opc_client.get_node(AWAIT_APP_NODE_ID)

        print("Waiting for PLC trigger (awaitApp=True)...")

        while True:
            await_app_value = await_app_node.get_value()

            if await_app_value is True:
                print("PLC trigger received.")
                return True

            time.sleep(poll_interval)

    finally:
        opc_client.disconnect()


def read_rfid():
    opc_client = OPCUAClient(ENDPOINT)

    try:
        opc_client.connect()

        rfid_node = opc_client.get_node(RFID_NODE_ID)
        raw_data = rfid_node.get_value()

        print(f"Raw RFID data: {raw_data}")

        order_id, model_id, step_index = parse_rfid_data(raw_data)

        print(f"Order ID: {order_id}")
        print(f"Model ID: {model_id}")
        print(f"Step Index: {step_index}")

        return {
            "order_id": order_id,
            "model_id": model_id,
            "step_index": step_index,
            "raw_data": raw_data,
        }

    finally:
        opc_client.disconnect()


def wait_and_read_rfid():
    wait_for_trigger()
    return read_rfid()


if __name__ == "__main__":
    result = wait_and_read_rfid()
    print(result)