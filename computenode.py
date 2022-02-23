import sys
import time

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport
import cv2 as cv
import numpy as np
from server_compute_interface import ServerCompute
from random import choices

max_lowThreshold = 100
window_name = 'Edge Map'
ratio = 3
kernel_size = 3


class ComputeNodeHandler:
    def __init__(self, load_proability):
        self.load_probability = float(load_proability)

    def process_image(self, base_path, file_name):
        print("Processing image: " + file_name)
        input_path = f"{base_path}/input_dir/{file_name}"
        output_path = f"{base_path}/output_dir/{file_name}"
        src = cv.imread(cv.samples.findFile(input_path))
        if src is None:
            print('Could not open or find the image: ', input_path)
            exit(0)

        src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        img_blur = cv.blur(src_gray, (3, 3))
        edge = cv.Canny(img_blur, 10, 30, apertureSize=5)
        vis = src.copy()
        vis = np.uint8(vis / 2.)
        vis[edge != 0] = (0, 255, 0)
        cv.imwrite(output_path, vis)
        print("Image processed: " + file_name)
        return "Success"

    def is_delayed_or_rejected(self):
        return choices([1, 0], [self.load_probability, 1.0 - self.load_probability])[0]

    def execute(self, base_path, file_name):
        if self.is_delayed_or_rejected():
            print("Rejecting image: " + file_name)
            return "Rejected"
        return self.process_image(base_path, file_name)

    def delayed_execute(self, base_path, file_name):
        if self.is_delayed_or_rejected():
            print("Delaying image processing: " + file_name)
            time.sleep(3)
        return self.process_image(base_path, file_name)


if __name__ == '__main__':
    handler = ComputeNodeHandler(sys.argv[1])
    processor = ServerCompute.Processor(handler)
    transport = TSocket.TServerSocket(host='10.0.50.0', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    server = TServer.TThreadPoolServer(
        processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
