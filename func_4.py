from math import sqrt


def Functionality4(node, set_nodes, dist, nodes):

    def h(nodes, current, neighbor):
        x1 = nodes[current]['Latitude']
        y1 = nodes[current]['Longitude']
        x2 = nodes[neighbor]['Latitude']
        y2 = nodes[neighbor]['Longitude']
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def reconstruct_path(cameFrom, current):
        total_path = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            total_path.insert(0, current)
        return total_path


    # A* finds a path from start to goal.
    # h is the heuristic function. h(n) estimates the cost to reach goal from node n.
    def A_Star(nodes, graph, start, goal, h):
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
        fScore[start] = h(nodes, start, goal)

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
                    fScore[neighbor] = gScore[neighbor] + h(nodes, neighbor, goal)
                    if neighbor not in openSet:
                        openSet.add(neighbor)
        # Open set is empty but goal was never reached
        return 'Not possible'

    def sort_by_distance_as_the_crow_flies(node, set_nodes):
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

    # Start functionality 4
    sorted_set_nodes = sort_by_distance_as_the_crow_flies(node, set_nodes)
    path = [set_nodes[0]]
    for i in range(len(sorted_set_nodes)-2):
        start = sorted_set_nodes[i]
        end = sorted_set_nodes[i+1]
        temp_path = A_Star(nodes, dist, start, end, h)
        if temp_path == 'Not possible':
            return 'Not possible'
        else:
            path += temp_path[1:]
    print(path)
    return path
