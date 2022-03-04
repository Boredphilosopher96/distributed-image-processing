from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from client_server_interface import ClientServer
from utils import get_base_path, NODE_MAPPING

if __name__ == '__main__':
    # Make socket
    transport = TSocket.TSocket(NODE_MAPPING['server'], 5000)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client: ClientServer.Client = ClientServer.Client(protocol)

    # Connect!
    transport.open()

    client.ping()
    print('ping()')

    time_elapsed = client.submit_request(f"{get_base_path()}/data", True)
    print("Time elapsed: " + str(time_elapsed))
