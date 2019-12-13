from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


"""
The Functionality4 is an heuristic solution for the problem.
Given a starting node H and a path P to visit, its operation is:
1) Order the path P as the crow flies
2) Approximate the minor path between two nodes with the algorithm A* (A_star)
"""


def Functionality4(node, set_nodes, dist, nodes):

    """
    :param node: the start node H
    :type node: int
    :param set_nodes: set of node to visit
    :type set_nodes: list
    :param dist: distance between nodes (d, t, network distance)
    :type dist: dict
    :param nodes: nodes of the graph
    :type nodes: dict
    :return: the shortest path that visits the set_nodes in a list

    This function visualize the Shortest Approximate Route and
    return the list contain the shortest path
    """

    def h(nodes, current, neighbor):

        """
        Euclidean distance between current and neighbor
        """
        x1 = nodes[current]['Latitude']
        y1 = nodes[current]['Longitude']
        x2 = nodes[neighbor]['Latitude']
        y2 = nodes[neighbor]['Longitude']
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def reconstruct_path(cameFrom, current):

        """
        This function take as input a dict with the connected nodes
        and orders them in a chaim
        """
        total_path = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            total_path.insert(0, current)
        return total_path

    def A_Star(nodes, graph, start, goal, h):
        # A* finds a path from start to goal.
        # h is the heuristic function. h(n) estimates the cost to reach goal
        # from node n.
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        openSet = {start}

        # For node n, cameFrom[n] is the node immediately preceding it on
        # the cheapest path from start to n currently known.
        cameFrom = {} # an empty map

        # For node n, gScore[n] is the cost of the cheapest path from start
        # to n currently known.
        Q = list(set(graph))
        gScore = {node: float('inf') for node in Q}
        gScore[start] = 0

        # For node n, fScore[n] := gScore[n] + h(n).
        fScore = {node: float('inf') for node in Q}
        fScore[start] = h(nodes, start, goal)

        while openSet:
            current = min(openSet, key=fScore.get) # the node in openSet having
                                                   # the lowest fScore[] value
            if current == goal:
                return reconstruct_path(cameFrom, current)

            openSet.remove(current)
            for neighbor in graph[current]:
                # d(current,neighbor) is the weight of the edge
                # from current to neighbor
                # tentative_gScore is the distance from start to the neighbor
                # through current
                tentative_gScore = gScore[current] + graph[current][neighbor]
                if tentative_gScore < gScore[neighbor]:
                    cameFrom.update({neighbor: current})
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + h(nodes, neighbor, goal)
                    if neighbor not in openSet:
                        openSet.add(neighbor)
        # Open set is empty but goal was never reached
        return 'Not possible'

    def sort_by_distance_as_the_crow_flies(node, set_nodes):

        """
        This function takes a list of nodes as input
        and sorts them by distance as the crow flies
        """
        node_to_sort = set_nodes[:-1]
        node_sorted = [node]
        while node_to_sort:
            d = float('inf')
            for x in node_to_sort[:]:
                d_temp = h(nodes, node_sorted[-1], x)
                if d_temp <= d:
                    d = d_temp
                    next_node = x
            node_sorted.append(next_node)
            node_to_sort.remove(next_node)
        node_sorted += [set_nodes[-1]]
        return node_sorted

    """
    + sorted set nodes
    + calculate the path between two neighboring nodes
    + print a path
    + visualize a graph
    + return a path
    """
    sorted_set_nodes = sort_by_distance_as_the_crow_flies(node, set_nodes)
    path = [set_nodes[0]]
    for i in range(len(sorted_set_nodes)-1):
        start = sorted_set_nodes[i]
        end = sorted_set_nodes[i+1]
        temp_path = A_Star(nodes, dist, start, end, h)
        if temp_path == 'Not possible':
            return 'Not possible'
        else:
            path += temp_path[1:]
    print(path)

    # Graph networkx
    g = {key: dist[key] for key in path}
    edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    G=nx.Graph(g)

    # Plot
    figure(num=None, figsize=(20, 15), dpi=80, facecolor='w', edgecolor='k')
    pos = {key:(nodes[key]['Latitude'],nodes[key]['Longitude']) for key in nodes}
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='royalblue')
    nx.draw_networkx_nodes(G, pos, node_size=150, node_color='red', nodelist=path)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='yellow', nodelist=sorted_set_nodes)

    #nx.draw_networkx_nodes(G, pos, node_size=2000, nodelist=[188])
    nx.draw_networkx_edges(G, pos, width=3, edge_color='royalblue', style='dashed')
    nx.draw_networkx_edges(G, pos, width=3, edge_color='red', style='dashed', edgelist=edges)
    nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')

    plt.show()

    return path
