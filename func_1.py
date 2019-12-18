import pdb
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
    vertices, edges = get_distance_graph() 

    orderedn = find_order(strnode, vstnode, vertices)

    best_path = bellman_ford(orderedn)

    return best_path  


def find_order(start, vstnode, coordinates):
    visit_list = list(visit)  
    ordered_path = [] 

    while visit_list:

        min_dist = real_dist(start, visit_list[0], coordinates)
        nearest_node = visit_list[0]

        for node in visit_list:  
            if min_dist > real_dist(start, node, coordinates):  
                min_dist = real_dist(start, node, coordinates)  
                nearest_node = node 

    
        tvisit_list.remove(nearest_node) 
        start = nearest_node 
        ordered_path.append(nearest_node) 

    return ordered_path  

def real_dist(node1, node2, coordinates): 
    return np.linalg.norm(np.array(coordinates[node1]) - np.array(coordinates[node2]))


def bellman_ford(list_visit):
    return list_visit
