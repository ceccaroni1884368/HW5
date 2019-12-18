import pdb
import gzip
import numpy as np


def node_coordinate():
    """
    {Id Node : {Latitude: int, longitude: int},....}
    """
    nodes = {}
    with gzip.open('USA-road-d.CAL.co.gz', 'rt') as f:
        for line in f:
            if 'v' == line.split()[0]:
                node = int(line.split()[1])
                latitude = int(line.split()[2])
                longitude = int(line.split()[3])
                nodes[node] = {'Latitude': latitude, 'Longitude': longitude}
    return nodes


def node_distance():
    """
    {Id Node 1: {Id Node 2: weight, Id Node 2: weight},....}
    """
    d = {}
    with gzip.open('USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                node1 = int(line.split()[1])
                node2 = int(line.split()[2])
                w = int(line.split()[3])
                if node1 in d:
                    d[node1].update({node2: w})
                else:
                    d[node1] = {node2: w}
    return d

def initialize(get_distance_graph, source):
    d = {}
    p = {}
    for node in get_distance_graph:
        d[node] = float('Inf')
        p[node] = None
    d[source] = 0
    return d, p

def relax(node, neighbour, get_distance_graph, d, p):

    if d[neighbour] > d[node] + get_distance_graph[node][neighbour]:

        d[neighbour]  = d[node] + get_distance_graph[node][neighbour]
        p[neighbour] = node

def bellman_ford(get_distance_graph, source):
    d, p = initialize(get_distance_graph, source)
    for i in range(len(get_distance_graph)-1):
        for u in get_distance_graph:
            for v in get_distance_graph[u]:
                relax(u, v, get_distance_graph, d, p)

    for u in get_distance_graph:
        for v in get_distance_graph[u]:
            assert d[v] <= d[u] + get_distance_graph[u][v]

    return d, p

def functionality(strnode, vstnode):
    vertices, edges = node_coordinate(), node_distance()

    orderedn = find_order(strnode, vstnode, vertices)

    best_path = bellman_ford(orderedn)

    return best_path


def find_order(start, vstnode, coordinates):
    visit_list = list(vstnode)
    ordered_path = []

    while visit_list:

        min_dist = real_dist(start, visit_list[0], coordinates)
        nearest_node = visit_list[0]

        for node in visit_list:
            if min_dist > real_dist(start, node, coordinates):
                min_dist = real_dist(start, node, coordinates)
                nearest_node = node


        visit_list.remove(nearest_node)
        start = nearest_node
        ordered_path.append(nearest_node)

    return ordered_path

def real_dist(node1, node2, coordinates):
    return np.linalg.norm(np.array(coordinates[node1]) - np.array(coordinates[node2]))


def bellman_ford(list_visit):
    return list_visit


#functionality(1, [5,4,7])
