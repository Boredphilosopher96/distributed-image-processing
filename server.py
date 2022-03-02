import random

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport

from client_server_interface import ClientServer
from server_compute_interface import ServerCompute

from timeit import default_timer as timer
from os.path import join
from glob import glob
from utils import NODE_MAPPING


class ServerHandler:
    def __init__(self):
        self.compute_nodes = [node for node in NODE_MAPPING.keys() if node.startswith('node')]

    def ping(self):
        print("ping() server")

    def get_all_eligible_files(self, source_path: str):
        # referenced from https://stackoverflow.com/a/26403164
        files = []
        for ext in ('*.png', '*.jpg'):
            files.extend([file.split("/")[-1] for file in glob(join(f"{source_path}/input_dir/", ext))])

        return files

    def get_rpc_client(self, node_id):
        transport = TSocket.TSocket(self.compute_nodes[node_id], 9090)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        client = ServerCompute.Client(protocol)

        # Connect
        transport.open()

        return client

    def get_server_randomly(self):
        node_id = random.choice(self.compute_nodes)
        return self.get_rpc_client(node_id)

    def submit_request(self, source_path: str, is_random: bool):
        start_time = timer()

        if source_path.endswith("/"):
            source_path = source_path[:-1]

        eligible_files = self.get_all_eligible_files(source_path)

        if is_random:
            for file in eligible_files:
                was_rejected = True
                while was_rejected:
                    status = self.get_server_randomly().execute(source_path, file)
                    was_rejected = "Rejected" in status
        else:
            for file in eligible_files:
                self.get_server_randomly().delayed_execute(source_path, file)

        end_time = timer()

        elapsed_time = end_time - start_time
        print(f"Elapsed time for request: {elapsed_time}")
        return str(elapsed_time)


if __name__ == '__main__':
    handler = ServerHandler()
    processor = ClientServer.Processor(handler)

    server_ip = NODE_MAPPING['server']
    transport = TSocket.TServerSocket(host=server_ip, port=9090)

    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
