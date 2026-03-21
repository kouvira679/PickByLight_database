from opcua import Client


class OPCUAClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.client = Client(endpoint)
        self.connected = False

# connecting to the plc
    def connect(self):
        if not self.connected:
            self.client.connect()
            self.connected = True
            print(f"Connected to PLC: {self.endpoint}")

#disconnecting from the plc
    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.connected = False
            print("Disconnected from PLC")

#getting a node
    def get_node(self, node_id):
        if not self.connected:
            raise RuntimeError("OPC UA client is not connected")
        return self.client.get_node(node_id)