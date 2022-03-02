import os


def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))


NODE_MAPPING = {}
with open('machine.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        node_id, ip = line.split()
        NODE_MAPPING[node_id] = ip
