import heapq as hp
import networkx as nx
from collections import defaultdict
import folium
from folium import plugins
import heapq as hp

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



def Visualization2(e, graph, nodesDF):
    n = set()
    for x,y in e:
        n.add(x)
        n.add(y)
    n = list(n)

    nodesDF.set_index = 'Id Nodes'
    G = nx.Graph()
    for v in (n + ne):
        G.add_node(v, latitude=nodesDF.iloc[v].Longitude,
                      longitude= nodesDF.iloc[v].Latitude)

    E = defaultdict(list)
    for p in (n):
        for v,d in graph[p]:
            if v in (n + ne):
                E[p].append((v, d))
    for n1 in (n):
        for n2, d in E[n1]:
            G.add_edge(n1, n2, weight = d)

    #map
    def map(nodelst): #start point
        pos = G.nodes[nodelst[0]]
        vismap = folium.Map(location=[pos['latitude'], pos['longitude']], zoom_start=10)
        folium.raster_layers.TileLayer('Open Street Map').add_to(vismap)
        folium.raster_layers.TileLayer('Stamen Terrain').add_to(vismap)
        folium.LayerControl().add_to(vismap)
        #minimap
        visminimap = plugins.MiniMap(toggle_display=True)
        #add to map
        vismap.add_child(visminimap)
        plugins.ScrollZoomToggler().add_to(vismap)
        folium.Marker(location=[(pos['latitude']),(pos['longitude'])],
                      icon=folium.Icon(color='red', icon='home'), popup = (nodelst[0])).add_to(vismap)
        for i in range (len(nodelst)-1):
            pos = (G.nodes[nodelst[i+1]])
            folium.Marker(location=[(pos['latitude']),(pos['longitude'])],popup = (nodelst[i+1])).add_to(vismap)

        return vismap
    #adding all nodes to map
    def map_routes(lst,map_name):
        for t in range (len(lst)):
            cordlst = 0
            cordlst = []
            a = (lst[t])
            for i in a:
                cordlst.append(list(G.nodes[i].values()))
            plugins.AntPath(cordlst).add_to(map_name)
        return map_name

    omap = map(n)
    map_routes(e,omap)
    #map_routespoly(e_max,omap)
    #circlemarker(ne,omap)

    omap.save('F1map.html')
