from collections import defaultdict
import heapq
import gzip
import matplotlib.pyplot as plt
import mplleaflet


def dijkstra(distance, start, end):
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
        for new_node, w in distance.get(node, ()):
            old_weight = dist.get(new_node, float("inf"))
            new_weight = weight + w
            if new_weight < old_weight:
                dist[new_node] = new_weight # relax
                heapq.heappush(queue, (new_weight, new_node, path))
    return (float('inf'), [])

def Functionality3(node, list_nodes, distance):
    """ ARGUMENTS:
            node : starting node (int)
            list_nodes : sequence of nodes that need to be visited in order (list of int)
            distance : character indicating the chosen distance ('d','t', or 'n')
        RETURNS:
            tot_dist : magnitude of the shortest ordered route (int)
            tot_path : route corresponding to the shortest ordered route (list of int)
    """
    #DICT = dict_distances[distance]
    start = node
    tot_path = []
    tot_dist = 0
    for i in range(len(list_nodes)):
        weight, path = dijkstra(distance, start, list_nodes[i])
        if weight == float('inf'):
            return float('inf')
        tot_dist += weight
        tot_path.extend(path)
        start = list_nodes[i]
    return (tot_dist, tot_path)

def Visualization3(tot_path, list_nodes, nodesDF):
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
