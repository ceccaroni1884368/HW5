from collections import defaultdict
import heapq 
import gzip
#
def dict_node_distance():
    """
    :return: Default dictionary having the nodes as keys and the list of connecetd nodes as values
        EX:    
            G = {id_node_1 : [(id_node_2, weight), (id_node_3, weight), ...] }
    The weight used is the physical distance between each pair of nodes.
    """
    G= defaultdict(list)
    with gzip.open('USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                G[int(line.split()[1])].append((int(line.split()[2]),int(line.split()[3])))
    return G

def dict_node_travel_time():
    """
    :return: Default dictionary having the nodes as keys and the list of connecetd nodes as values
        EX:    
            G = {id_node_1 : [(id_node_2, weight), (id_node_3, weight), ...] }
    The weight used is the travel time distance between each pair of nodes.
    """
    G= defaultdict(list)
    with gzip.open('USA-road-t.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                G[int(line.split()[1])].append((int(line.split()[2]),int(line.split()[3])))
    return G


def dict_node_network_distance():
    """
    :return: Default dictionary having the nodes as keys and the list of connecetd nodes as values
        EX:    
            G = {id_node_1 : [(id_node_2, 1), (id_node_3, 1), ...] }
    The weight used is the network distance between each pair of nodes.
    """
    G= defaultdict(list)
    with gzip.open('USA-road-t.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                G[int(line.split()[1])].append((int(line.split()[2]),1))
    return G


def dijkstra(DICT, start, end):
    """
    :return: Shortest distance between the node "start" and node "end", 
             together with the path that connects them and that gives the shortest distance
    """
    queue, dist = [(0,start,())], {start: 0}
    while queue:
        (weight, node, path) = heapq.heappop(queue) 
        if weight > dist[node]: continue
        path += (node,)
        if node == end: 
            return (weight, list(path))
        for new_node, w in DICT.get(node, ()):
            old_weight = dist.get(new_node, float("inf"))
            new_weight = weight + w
            if new_weight < old_weight:
                dist[new_node] = new_weight # relax
                heapq.heappush(queue, (new_weight, new_node, path))
    return (float('inf'), [])

D = dict_node_distance()
T = dict_node_travel_time()
N = dict_node_network_distance()


dict_distances = {'d' : D, 't' : T, 'n' : N}  # d : physical distance, t : time distance, n : network distance


def Functionality3(node, list_nodes, distance):
    """ ARGUMENTS:
            node : starting node (int)
            list_nodes : sequence of nodes that need to be visited in order (list of int)
            distance : character indicating the chosen distance ('d','t', or 'n')
        RETURNS: 
            tot_dist : magnitude of the shortest ordered route (int)
            tot_path : route corresponding to the shortest ordered route (list of int)
    """
    DICT = dict_distances[distance]
    start = node
    tot_path = []
    tot_dist = 0
    for i in range(len(list_nodes)):
        weight, path = dijkstra(DICT, start, list_nodes[i])
        if weight == float('inf'):
            return float('inf')
        tot_dist += weight
        tot_path.extend(path)
        start = list_nodes[i]
    return (tot_dist, tot_path)
        
