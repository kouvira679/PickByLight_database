from opcua import Client, ua

def write_tage(client, tag_name, value):
    node = client.get_node(tag_name)
    node.set_value(ua.DataValue(ua.Variant(value, node.get_data_type_as_variant_type())))


class SubHandler:
    def datachange_notification(self, node, val, data):
        print("Data change event at ", node, ". New value = ", val, sep='')

if __name__ == "__main__":
    client = Client("opc.tcp://172.21.4.1:4840")


    try:
        client.connect()

        # get namespace idx using the uri
        uri = "http://www.siemens.com/simatic-s7-opcua"
        idx = client.get_namespace_index(uri)

        # use the namespace idx and string identifier to get the desired node
        # var_1 = client.get_node("ns={3};s=OPCUA_data.var1".format(idx))
        # var_2 = client.get_node("ns={3};s=OPCUA_data.var2".format(idx))
        # var_3 = client.get_node("ns={3};s=OPCUA_data.var3".format(idx))
        var1 = client.get_node('ns=3;s="OPCUA_data"."var1"')
        var2 = client.get_node('ns=3;s="OPCUA_data"."var2"')
        var3 = client.get_node('ns=3;s="OPCUA_data"."var3"')

        #doing a read test
        print("Initial Values:")
        print("var =", var1.get_value())
        print("var =", var2.get_value())
        print("var =", var3.get_value())

        #doing a write test
        # var1.set_value(True)
        # var2.set_value(100)
        # var3.set_value([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8])

        write_tage(client, 'ns=3;s="OPCUA_data"."var1"', True)
        write_tage(client, 'ns=3;s="OPCUA_data"."var2"', 100)
        write_tage(client, 'ns=3;s="OPCUA_data"."var3"', [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8])

        print("new values written to plc ")


        # create the subhandler and subscription
        handler = SubHandler()
        sub = client.create_subscription(500, handler)

        # subscribe to changes in the node
        sub.subscribe_data_change(var1)
        sub.subscribe_data_change(var2)
        sub.subscribe_data_change(var3)

        print("monitoring var1 for changes... ")

        while True:
            pass

    finally:
        client.disconnect()