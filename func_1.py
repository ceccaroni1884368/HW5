import heapq as hp
import networkx as nx
from collections import defaultdict
import folium
from folium import plugins
import heapq as hp


def Functionality1(v,G,d):#,graph = G, adjacent = adj):
    visited = {v: 0} #take all weigths
    F = [] #keep all nodes here
    hp.heapify(F)
    current_node = v #starting node
    edges_min_d = set()
    edges_max_d = set()
    while True:

        #adjacents = adjacent[current_node]
        weight_to_current_node = visited[current_node]
        for node, w in G[current_node]:
            weight = w + weight_to_current_node
            if weight > d: #filter, take only less than d
                edges_max_d.add((current_node,node))
            else:
                edges_min_d.add((current_node,node)) #add visiting border
                if node not in visited:
                    visited[node] = weight
                    hp.heappush(F,(weight,node))
                else:
                    current_shortest_weight = visited[node]
                    if current_shortest_weight > weight:
                        visited[node] = weight
                        hp.heappush(F,(weight,node))
        try:
            current_node = hp.heappop(F)[1]
        except:
            break
    neighbors = list(visited.keys())
    edges_max_d = list(edges_max_d)
    edges_min_d = list(edges_min_d)

    maxres = edges_max_d
    maxlst = []
    for y in range (len(maxres)):
        maxlst.append(maxres[y][0])
        maxlst.append(maxres[y][1])

    notneighbors = list(set(maxlst) - set(neighbors))

    return neighbors, edges_min_d, edges_max_d, notneighbors


def Visualization1(n, e_min, e_max, ne, graph, nodesDF):
    nodesDF.set_index = 'Id Nodes'
    G = nx.Graph()
    for v in (n + ne):
        G.add_node(v, latitude=nodesDF.iloc[v].Longitude,
                      longitude= nodesDF.iloc[v].Latitude)

    E = defaultdict(list)
    for p in (n + ne):
        for v,d in graph[p]:
            if v in (n + ne):
                E[p].append((v, d))
    for n1 in (n + ne):
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

    def map_routespoly(lst,map_name):
        for t in range (len(lst)):
            cordlst = 0
            cordlst = []
            a = (lst[t])
            for i in a:
                cordlst.append(list(G.nodes[i].values()))
                folium.vector_layers.PolyLine(cordlst, color = 'red').add_to(map_name)
        return map_name

    def circlemarker(lst,map_name):
        for i in range (len(lst)):
            pos = (G.nodes[lst[i]])
            folium.CircleMarker(location=[(pos['latitude']),(pos['longitude'])],
                                radius=10, color='blue', fill_color='red',
                                popup = (lst[i])).add_to(map_name)
        return map_name

    omap = map(n)
    map_routes(e_min,omap)
    map_routespoly(e_max,omap)
    circlemarker(ne,omap)

    omap.save('F1map.html')
