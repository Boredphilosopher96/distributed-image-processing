import os


# Get the base path of the project
def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))


# Read and create a mapping of node_id and machine ip
NODE_MAPPING = {}
with open('machine.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        node_id, ip = line.split()
        NODE_MAPPING[node_id] = ip


# Custom exception
class IncorrectExecutionException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
