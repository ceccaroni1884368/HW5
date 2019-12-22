def myPrim(set_nodes, dist, reduced_dict):
    set_nodes = list(set_nodes)
    start, set_nodes = set_nodes[0], set_nodes[1:]
    visited = [start]
    final_edges = {}
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
                    selected_edge = {(node, edge[0])}
        visited.append(selected_edge[1])
        set_nodes.remove(selected_edge[1])
        tot_distance += min_length
        final_edges.add(selected_edge)
    return final_edges, tot_distance
