import gzip
import func_1
import func_2
import func_3
import func_4


def node_coordinate():
    """
    {Id Node : {Latitude: int, longitude: int},....}
    """
    nodes = {}
    with gzip.open('data/download/USA-road-d.CAL.co.gz', 'rt') as f:
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
    with gzip.open('data/download/USA-road-d.CAL.gr.gz', 'rt') as f:
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


def node_travel_time():
    """
    {Id Node 1: {Id Node 2: weight, Id Node 2: weight},....}
    """
    t = {}
    with gzip.open('data/download/USA-road-t.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                node1 = int(line.split()[1])
                node2 = int(line.split()[2])
                w = int(line.split()[3])
                if node1 in t:
                    t[node1].update({node2: w})
                else:
                    t[node1] = {node2: w}

    return t


def node_network_distance():
    """
    {Id Node 1: {Id Node 2: weight, Id Node 2: weight},....}
    """
    nd = {}
    with gzip.open('data/download/USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                node1 = int(line.split()[1])
                node2 = int(line.split()[2])
                if node1 in nd:
                    nd[node1].update({node2: 1})
                else:
                    nd[node1] = {node2: 1}
    return nd


def main():
    # Loading data
    print("Loading data...", end=' ')
    nodes = node_coordinate()
    d = node_distance()
    t = node_travel_time()
    net_d = node_network_distance()
    print("DONE!")


    # Choice the function
    print("\nChoose the function")
    n = int(input("Insert number (1-4): "))
    while not all([n > 0, n < 5]):
        n = int(input("Insert number (1-4): "))

    # Choice the distance
    print("\nChoose the distance")
    dist = int(input("1) Distance\n" +
                     "2) Travel time\n" +
                     "3) Network distance\n" +
                     "Insert number (1-3): "))
    while not all([dist > 0, dist < 4]):
        dist = int(input("1) Distance\n" +
                         "2) Travel time\n" +
                         "3) Network distance\n" +
                         "Insert number (1-3): "))
    if dist == 1:
        dist = d
    elif dist == 2:
        dist = t
    elif dist == 3:
        dist = net_d

    # Set start node
    node = int(input("Start node: "))

    # Switch
    if n == 1:
        # func_1
        pass
    elif n == 2:
        # func_2
        pass
    elif n == 3:
        # func_3
        pass
    elif n == 4:
        print("Enter the nodes to be visited separated by white space:", end='')
        set_nodes = list(map(int,input(" ").split()))
        func_4.Functionality4(node, set_nodes, dist, nodes)


if __name__:
    main()
