from collections import defaultdict
import heapq 
import gzip
import matplotlib.pyplot as plt
import mplleaflet

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

def node_coordinate():
    """
    :return: Pandas dataframe with node coordinates
    EX:
              Id Node    Latitude Longitude
     0              1  -114315309  34133550
     1              2  -114223946  34176221
     ...          ...         ...       ...
    """
    Id_Node = []
    Latitude = []
    Longitude = []
    with gzip.open('USA-road-d.CAL.co.gz', 'rt') as f:
        for line in f:
            if 'v' == line.split()[0]:
                Id_Node.append(int(line.split()[1]))
                Latitude.append(int(line.split()[2])/1000000)
                Longitude.append(int(line.split()[3])/1000000)
    dataframe = pd.DataFrame({'Id Node': Id_Node,'Latitude': Latitude,'Longitude': Longitude})
    return dataframe

D = dict_node_distance()
T = dict_node_travel_time()
N = dict_node_network_distance()
dict_distances = {'d' : D, 't' : T, 'n' : N}  # d : physical distance, t : time distance, n : network distance
nodesDF = node_coordinate()

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
        
def Visualization3(tot_path, list_nodes):
    """ ARGUMENT:
            tot_path : list of nodes composing the shortest path (list of int)
            list_nodes : sequence of nodes that need to be visited in order (list of int)
        RETURN:
            visualize the shortest path on an interactive map (it opens a new tab in the browser)
    """
    shortest_path_coords = nodesDF[nodesDF['Id Node'].isin(tot_path)]
    visit = nodesDF[nodesDF['Id Node'].isin(list_nodes)]
    lats = shortest_path_coords.Longitude.values
    longs = shortest_path_coords.Latitude.values
    lats_visit = visit.Longitude.values
    longs_visit = visit.Latitude.values
    fig, ax = plt.subplots(figsize=(12,9))
    ax.plot(longs, lats, 'orange', linewidth=1.5, marker =11, markersize=8)
    ax.plot(longs[0], lats[0], 'gX', markersize=18)
    ax.plot(longs_visit, lats_visit, 'bo', markersize = 10)
    ax.plot(longs[-1], lats[-1], 'ro', markersize=18)
    mplleaflet.show(fig=fig)
#    mplleaflet.show(fig=fig, path='map.html')
    return fig

