import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import gzip
from math import sqrt


def node_coordinate():
    nodes = {}
    with gzip.open('data/download/USA-road-d.CAL.co.gz', 'rt') as f:
        for line in f:
            if 'v' == line.split()[0]:
                nodes[int(line.split()[1])] = {'Latitude': int(line.split()[2]),
                                               'Longitude': int(line.split()[3])}
    return nodes


def node_distance():
    d = {}
    with gzip.open('data/download/USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                if int(line.split()[1]) in d:
                    d[int(line.split()[1])].update({int(line.split()[2]): int(line.split()[3])})
                    #d[int(line.split()[1])] = {k: v for k, v in sorted(d[int(line.split()[1])].items(), key=lambda x: x[1])}
                else:
                    d[int(line.split()[1])] = {int(line.split()[2]): int(line.split()[3])}
                    #d[int(line.split()[1])] = {k: v for k, v in sorted(d[int(line.split()[1])].items(), key=lambda x: x[1])}
    return d


def node_travel_time():
    t = {}
    with gzip.open('data/download/USA-road-t.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                if int(line.split()[1]) in t:
                    t[int(line.split()[1])].update({int(line.split()[2]): int(line.split()[3])})
                    #t[int(line.split()[1])] = {k: v for k, v in sorted(t[int(line.split()[1])].items(), key=lambda x: x[1])}
                else:
                    t[int(line.split()[1])] = {int(line.split()[2]): int(line.split()[3])}
                    #t[int(line.split()[1])] = {k: v for k, v in sorted(t[int(line.split()[1])].items(), key=lambda x: x[1])}

    return t


def node_network_distance():
    """
    {Id Node 1: {Id Node 2: weight, Id Node 2: weight},....}
    """
    nd = {}
    with gzip.open('data/download/USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                if int(line.split()[1]) in nd:
                    nd[int(line.split()[1])].update({int(line.split()[2]): 1})
                else:
                    nd[int(line.split()[1])] = {int(line.split()[2]): 1}
    return nd


print("Loading data...", end=' ')
node = node_coordinate()
d = node_distance()
t = node_travel_time()
net_d = node_network_distance()
print("DONE!")


def h(current, neighbor):
    x1 = node[current]['Latitude']
    y1 = node[current]['Longitude']
    x2 = node[neighbor]['Latitude']
    y2 = node[neighbor]['Longitude']
    return sqrt(( x1 - x2)**2 + (y1 - y2)**2)


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path


# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n.
def A_Star(graph, start, goal, h):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    openSet = {start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start to n currently known.
    cameFrom = {} # an empty map

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    Q = list(set(graph))
    gScore = {node: float('inf') for node in Q}
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n).
    fScore = {node: float('inf') for node in Q}
    fScore[start] = h(start, goal)

    while openSet:
        current = min(openSet, key=fScore.get) # the node in openSet having the lowest fScore[] value
        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.remove(current)
        for neighbor in graph[current]:
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = gScore[current] + graph[current][neighbor] # d(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom.update({neighbor: current})
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor, goal)
                if neighbor not in openSet:
                    openSet.add(neighbor)

    # Open set is empty but goal was never reached
    return 'failure'


print(A_Star(t, 1, 1048577, h))
