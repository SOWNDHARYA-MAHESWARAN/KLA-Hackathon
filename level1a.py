
import networkx as nx
import json

with open('Input data\level1a.json') as json_file:
    data = json.load(json_file)

G = nx.Graph()
result = []

for neighborhood in data["neighbourhoods"]:
    G.add_node(neighborhood)

restaurant = list(data["restaurants"])[0]
for item in restaurant:
    G.add_node(item)

for neighborhood, disdict in data["neighbourhoods"].items():
    distances = disdict["distances"]
    for i, distance in enumerate(distances):
        G.add_edge(neighborhood, f"n{i}", weight=distance)

restaurant_distances = data["restaurants"][restaurant]["neighbourhood_distance"]

for i, distance in enumerate(restaurant_distances):
    G.add_edge(restaurant, f"n{i}", weight=distance)

def nearest_neighbor_algorithm(graph, start_node):
    n=0
    path = [start_node]
    current_node = start_node
    visited = set([start_node])
    capacity = data["vehicles"]["v0"]["capacity"]

    while n < graph.number_of_nodes():
        if current_node==start_node:
            path=[start_node]
            capacity=data["vehicles"]["v0"]["capacity"]
        neighbors = list(graph.neighbors(current_node))
        unvisited_neighbors = [neighbor for neighbor in neighbors if neighbor not in visited]
        
        if not unvisited_neighbors:
            # If all neighbors are visited, go back to the start
            break
        else:
            nearest_neighbor = min(unvisited_neighbors, key=lambda neighbor: graph[current_node][neighbor]['weight'])
            if capacity>data['neighbourhoods'][nearest_neighbor]["order_quantity"]:
                capacity-=data["neighbourhoods"][nearest_neighbor]["order_quantity"]

                path.append(nearest_neighbor)
                visited.add(nearest_neighbor)
                current_node = nearest_neighbor
                n+=1
            else:
                path.append("r0")
                result.append(path)
                current_node=start_node

    return path

start_node = data["vehicles"]["v0"]["start_point"]
nearest_neighbor_path = nearest_neighbor_algorithm(G, start_node)
# print("Nearest neighbor path:", nearest_neighbor_path)

nearest_neighbor_path.append("r0")
result.append(nearest_neighbor_path)
f=open("level1a_output.json","w")

output = {"v0":{"path1":result[0],"path2":result[1],"path3":result[2]}}
print(output)

with open("level1a_output.json", "w") as outfile: 
    json.dump(output, outfile)