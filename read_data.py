import os.path
import sys 
from dataclasses import dataclass
import re
import numpy as np
import itertools

def read_data(name):

    #Ensure the data exists
    if not os.path.isfile("n100/" + name + ".txt"):
        sys.exit('Invalid File Name')

    f = open("n100/" + name + ".txt", "r")
    
    #The first 10 lines are set. Some info is good, some is not.
    name = f.readline().split(":")[1].strip()
    place = f.readline().split(":")[1].strip()
    comment = f.readline().split(":")[1].strip()
    type_ = f.readline().split(":")[1].strip()
    size = int(f.readline().split(":")[1].strip())
    distribution = f.readline().split(":")[1].strip()
    depot = f.readline().split(":")[1].strip()
    route_time = int(f.readline().split(":")[1].strip())
    time_window = int(f.readline().split(":")[1].strip())
    capacity = int(f.readline().split(":")[1].strip())

    #Nodes
    nodes = []
    f.readline()
    feats = np.loadtxt(itertools.islice(f, 0, size))

    #Edges
    f.readline()
    adj = np.loadtxt(itertools.islice(f, 0, size))

    f.close()

    return graph(adj, feats, size, route_time, time_window, capacity)

@dataclass
class graph:
    adj: np.array
    feats: np.array
    n_nodes: int
    route_time: int
    time_window: int
    capacity: int


if __name__ == "__main__":
    graph = read_data("bar-n1000-1")
    print(graph.adj)


