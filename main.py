import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import gzip

import func_1
import func_2
import func_3
import func_4


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
    with gzip.open('data/download/USA-road-d.CAL.co.gz', 'rt') as f:
        for line in f:
            if 'v' == line.split()[0]:
                Id_Node.append(line.split()[1])
                Latitude.append(line.split()[2])
                Longitude.append(line.split()[3])
    dataframe = pd.DataFrame({'Id Node': Id_Node,
                              'Latitude': Latitude,
                              'Longitude': Longitude})
    return dataframe


def node_distance():
    """
    :return: Pandas dataframe with distances between each pair of nodes
    EX:
             Id Node 1 Id Node 2 Distance
     0               1   1048577      456
     1         1048577         1      456
     ...          ...         ...       ...
    """
    Id_Node1 = []
    Id_Node2 = []
    d = []
    with gzip.open('data/download/USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                Id_Node1.append(line.split()[1])
                Id_Node2.append(line.split()[2])
                d.append(line.split()[3])
    dataframe = pd.DataFrame({'Id Node 1': Id_Node1,
                              'Id Node 2': Id_Node2,
                              'Distance': d})
    return dataframe


def node_travel_time():
    """
    :return: Pandas dataframe with time distances between each pair of nodes
    EX:
               Id Node 1 Id Node 2 Distance
       0               1   1048577      456
       1         1048577         1      456
     ...          ...         ...       ...
    """
    Id_Node1 = []
    Id_Node2 = []
    t = []
    with gzip.open('data/download/USA-road-d.CAL.gr.gz', 'rt') as f:
        for line in f:
            if 'a' == line.split()[0]:
                Id_Node1.append(line.split()[1])
                Id_Node2.append(line.split()[2])
                t.append(line.split()[3])
    dataframe = pd.DataFrame({'Id Node 1': Id_Node1,
                              'Id Node 2': Id_Node2,
                              'Distance': t})
    return dataframe


def main():
    node = node_coordinate()
    distance = node_distance()
    travel_time = node_travel_time()

    G = nx.Graph()

    n = int(input("Insert number (1-4): "))
    while not all([n > 0, n < 5]):
        n = int(input("Insert number (1-4): "))

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
        # func_4
        pass


if __name__:
    main()
