import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt 
import pandas as pd
import ipywidgets
import gzip
G = nx.Graph()

#graphnodes
with gzip.open('data/download/USA-road-d.CAL.co', 'rt') as f1:
    for line in f1:
        if line[0] == 'v':
            n,lo,la = list(map(int, line.strip().split()[1:]))
            G.add_node(n,latitude = la/1000000,longitude = lo/1000000)
            #edges
            adj = defaultdict(set)
with gzip.open('data/download/USA-road-d.CAL.gr', 'rt') as f:
    for line in f:
        if line[0] == 'a':
            n1,n2, d =  list(map(int, line.strip().split()[1:]))
            G.add_edge(n1,n2,distance = d,weight = 1)
            adj[n1].add(n2)
            adj[n2].add(n1)
            #time
            with gzip.open('data/download/USA-road-t.CAL.gr', 'rt') as f2:
                for line in f2:
                    if line[0] == 'a':
                        n1,n2, t =  list(map(int, line.strip().split()[1:]))
                        G.add_edge(n1,n2,time = t)
            
            #Functionalite1
import heapq as hp
def neighbors(v,w,d,graph = G, adjacent = adj):
    visited = {v: 0} #take all weigths
    F = [] #keep all nodes here
    hp.heapify(F)
    current_node = v #starting node
    edges_min_d = set()
    edges_max_d = set()
    while True:
        adjacents = adjacent[current_node]
        weight_to_current_node = visited[current_node]
        for node in adjacents:
            weight = graph[current_node][node][w] + weight_to_current_node 
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
    
    return neighbors,edges_min_d,edges_max_d,notneighbors

p = neighbors(11,'time',100000)
print (p[0])
print (p[1])
print (p[2])

#visualization
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
    #function vizualization
v = (int(input('Enter the node number: ')))
p = (input('Enter the type of weight, either distance or time: '))
d = int(input('Enter the thrushhold for the type of weight: '))

nodelst = 0
nodelst = neighbors(v,p,d,graph = G, adjacent = adj)
omap = map(nodelst[0])
map_routes(nodelst[1],omap)
map_routespoly(nodelst[2],omap)
circlemarker(nodelst[3],omap)

omap.save('F1map.html')
