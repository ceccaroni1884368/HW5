from collections import defaultdict


def graph_reduct(G, nodes):
    G_red = defaultdict(list)
    for n1 in nodes:
        for n2, d in G[n1]:
            if n2 in nodes:
                G_red[n1].append((n2, d))
    return G_red

def is_connected(v_list, G):
    Q = []
    V = []
    Q.append(v_list[0])
    while Q:
        u = Q.pop()
        V.append(u)
        for n, d in G[u]:
            if n not in V:
                Q.append(n)
    if set(v_list) == set(V):
        return True
    else:
        return False


def myPrim(set_nodes, reduced_dict):
    set_nodes = list(set_nodes)
    start, set_nodes = set_nodes[0], set_nodes[1:]
    visited = [start]
    final_edges = set()
    tot_distance = 0
    while len(set_nodes)>0:
        tot_edges = []
        min_length = float('inf')
        selected_edge = {}
        for node in visited:
            tot_edges.extend(reduced_dict[node])
            for edge in tot_edges:
                if edge[0] not in visited and edge[1] < min_length:
                    min_length = edge[1]
                    selected_edge = (node, edge[0])
        visited.append(selected_edge[1])
        set_nodes.remove(selected_edge[1])
        tot_distance += min_length
        final_edges.add(selected_edge)
    return final_edges, tot_distance


def Functionality2(dist, nodes):
    G = graph_reduct(dist, nodes)

    if is_connected(nodes, G):
        #print(G)
        return myPrim(nodes, G)
    else:
        return "Error!"
