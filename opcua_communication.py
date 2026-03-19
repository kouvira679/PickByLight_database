import time
from opcua import Client, ua

ENDPOINT = "opc.tcp://172.21.x.1:4840"
S7_URI = "http://www.siemens.com/simatic-s7-opcua"

# SID_VAR1 = '"OPCUA_data"."var1"'
# SID_VAR2 = '"OPCUA_data"."var2"'
# SID_VAR3 = '"OPCUA_data"."var3"'
SID_RFID_DONE = 'ns=3;s="abstractMachine"."awaitApp"'
SID_APP_DONE = 'ns=3;s="abstractMachine"."appDone"'
SID_APP_RUN = 'ns=3;s="abstractMachine"."appRun"'
SID_RFID_DATA = 'ns=3;s="identData"."readData"'

flag = True
sid_trig = ""

class SubHandler:
    def datachange_notification(self, node, val, data):
        global flag, sid_trig
        # print("[DATA CHANGE]", node.nodeid.to_string(), "->", val)
        # pass
        flag = True
        sid_trig = node.nodeid.to_string()


if __name__ == "__main__":
    client = Client(ENDPOINT)
    try:
        client.connect()
        print("Connected:", ENDPOINT)

        idx = client.get_namespace_index(S7_URI)

        # var1 = client.get_node(nid(idx, SID_VAR1))
        # var2 = client.get_node(nid(idx, SID_VAR2))
        # var3 = client.get_node(nid(idx, SID_VAR3))
        rfid_done = client.get_node(SID_RFID_DONE)
        app_done = client.get_node(SID_APP_DONE)
        app_run = client.get_node(SID_APP_RUN)
        rfid_data = client.get_node(SID_RFID_DATA)

        handler = SubHandler()
        sub = client.create_subscription(50, handler)
        # sub.subscribe_data_change(var1)
        # sub.subscribe_data_change(var2)
        # sub.subscribe_data_change(var3)
        sub.subscribe_data_change(rfid_done)
        sub.subscribe_data_change(app_done)
        sub.subscribe_data_change(app_run)

        time.sleep(5)
        loop = True
        while loop:
            if flag:
                # print(f"Flag :{flag}, STR:{sid_trig} | {sid_trig == SID_RFID_DONE}")
                if sid_trig == SID_RFID_DONE:
                    # write_mock_valid_rfid_info()
                    rfidData = rfid_data.get_value()

                    input_str = input("0/1?:")
                    app_code = int(input_str)
                    # rfid here
                    #
                    if app_code == 0:
                        app_done.set_value(
                            ua.DataValue(
                                ua.Variant(True, app_done.get_data_type_as_variant_type())
                            )
                        )
                    elif app_code == 1:
                        app_run.set_value(
                            ua.DataValue(
                                ua.Variant(True, app_run.get_data_type_as_variant_type())
                            )
                        )
                    elif app_code == -1:
                        app_done.set_value(
                            ua.DataValue(
                                ua.Variant(True, app_done.get_data_type_as_variant_type())
                            )
                        )
                        loop = False

                flag = False
                print()

    finally:
        client.disconnect()