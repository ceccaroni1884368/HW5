import gzip
import pandas as pd
from collections import defaultdict

from func_1 import Functionality1, Visualization1
import func_2
from func_3 import Functionality3, Visualization3
from func_4 import Functionality4, Visualization4


# ----- Import Functions -----
def dict_node_distance():
    """
    :return: Default dictionary having the nodes as keys and the list of connecetd nodes as values
        EX:
            G = {id_node_1 : [(id_node_2, weight), (id_node_3, weight), ...] }
    The weight used is the physical distance between each pair of nodes.
    """
    G = defaultdict(list)
    with gzip.open('USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                G[int(line.split()[1])].append((int(line.split()[2]),
                                                int(line.split()[3])))
    return G


def dict_node_travel_time():
    """
    :return: Default dictionary having the nodes as keys and the list of connecetd nodes as values
        EX:
            G = {id_node_1 : [(id_node_2, weight), (id_node_3, weight), ...] }
    The weight used is the travel time distance between each pair of nodes.
    """
    G = defaultdict(list)
    with gzip.open('USA-road-t.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                G[int(line.split()[1])].append((int(line.split()[2]),
                                                int(line.split()[3])))
    return G


def dict_node_network_distance():
    """
    :return: Default dictionary having the nodes as keys and the list of connecetd nodes as values
        EX:
            G = {id_node_1 : [(id_node_2, 1), (id_node_3, 1), ...] }
    The weight used is the network distance between each pair of nodes.
    """
    G = defaultdict(list)
    with gzip.open('USA-road-t.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                G[int(line.split()[1])].append((int(line.split()[2]), 1))
    return G


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
    dataframe = pd.DataFrame({'Id Node': Id_Node,
                              'Latitude': Latitude,
                              'Longitude': Longitude})
    return dataframe


# ----- Load data -----
print("Loading data...", end='', flush=True)
D = dict_node_distance()
T = dict_node_travel_time()
N = dict_node_network_distance()
dict_distances = {'d' : D, 't' : T, 'n' : N}  # d : physical distance, t : time distance, n : network distance
nodesDF = node_coordinate()
print("[DONE]")


# ----- Main -----
def main():
    while True:
        # Choice the function
        print("\nChoose the functionality:")
        n = int(input("1) Functionality1\n" +
                      "2) Functionality2\n" +
                      "3) Functionality3\n" +
                      "4) Functionality4\n" +
                      "5) Exit\n" +
                     "Insert (1-5): "))
        while not all([n > 0, n < 6]):
            n = int(input("1) Functionality1\n" +
                          "2) Functionality2\n" +
                          "3) Functionality3\n" +
                          "4) Functionality4\n" +
                          "5) Exit\n" +
                         "Insert (1-5): "))
        if n == 5:
            print("Bye bye!!", flush=True)
            break

        # Choice the distance
        while True:
            print("\nChoose the distance:")
            dist = input("d) Distance\n" +
                         "t) Travel time\n" +
                         "n) Network distance\n" +
                         "Insert (d, t, n): ")
            if dist in ['d', 't', 'n']:
                break

        # Set start node
        node = int(input("Start node: "))

        # Switch
        if n == 1:
            d = int(input('Enter the thrushhold for the type of weight: '))
            n, e_min, e_max, ne = Functionality1(node, dict_distances[dist], d)
            print(n, flush=True)
            Visualization1(n, e_min, e_max, ne, dict_distances[dist], nodesDF)
        elif n == 2:
            # func_2
            pass
        elif n == 3:
            print("Enter the nodes to be visited separated by white space:", end='')
            list_nodes = list(map(int, input(" ").split()))
            tot_dist, tot_path = Functionality3(node, list_nodes, dict_distances[dist])
            Visualization3(tot_path, list_nodes, nodesDF)

        elif n == 4:
            print("Enter the nodes to be visited separated by white space:",
                  end='')
            set_nodes = list(map(int, input(" ").split()))
            path, list_nodes = Functionality4(node,
                                              set_nodes,
                                              dict_distances[dist],
                                              nodesDF)
            #Visualization4(nodesDF, dict_distances[dist], path, list_nodes)
            Visualization3(path, list_nodes, nodesDF)
            # try Functionality4(2, [4,6,5,49], d, nodes)
            print(path)


if __name__:
    main()
