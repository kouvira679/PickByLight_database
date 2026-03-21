from opcua import ua
from opcua.opcua_client import OPCUAClient

ENDPOINT = "opc.tcp://172.21.x.1:4840"

APP_DONE_NODE_ID = 'ns=3;s="abstractMachine"."appDone"'
APP_RUN_NODE_ID = 'ns=3;s="abstractMachine"."appRun"'
TASK_CODE_NODE_ID = 'ns=3;s="abstractMachine"."taskCode"'
QUANTITY_NODE_ID = 'ns=3;s="abstractMachine"."quantity"'
STEP_INDEX_NODE_ID = 'ns=3;s="abstractMachine"."stepIndex"'


def write_node_value(opc_client, node_id, value):
    node = opc_client.get_node(node_id)
    variant_type = node.get_data_type_as_variant_type()
    node.set_value(ua.DataValue(ua.Variant(value, variant_type)))


def send_task_to_plc(task_code, quantity, step_index):
    opc_client = OPCUAClient(ENDPOINT)

    try:
        opc_client.connect()

        # Python is running
        write_node_value(opc_client, APP_RUN_NODE_ID, True)

        # Send task data
        write_node_value(opc_client, TASK_CODE_NODE_ID, int(task_code))
        write_node_value(opc_client, QUANTITY_NODE_ID, int(quantity))
        write_node_value(opc_client, STEP_INDEX_NODE_ID, int(step_index))

        # Python finished sending data
        write_node_value(opc_client, APP_DONE_NODE_ID, True)

        print(
            f"Sent task_code={task_code}, quantity={quantity}, "
            f"step_index={step_index} to PLC"
        )

    finally:
        opc_client.disconnect()


if __name__ == "__main__":
    send_task_to_plc(task_code=411, quantity=1, step_index=3)