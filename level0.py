import json
import numpy as np

f = open('Input data\level0.json')
data = json.load(f)
# for i in data:
#     print(i,data[i])

def nearest_neighbor(distance_matrix, start_node, start_distances, vehicle_info):
    num_nodes = len(distance_matrix)
    unvisited_nodes = set(distance_matrix.keys())
    current_node = start_node
    path = [current_node]

    while len(path) < num_nodes:
        # Find the nearest unvisited neighbor
        nearest_neighbor = min(unvisited_nodes, key=lambda neighbor: start_distances[int(neighbor[1:])])
        
        # Move to the nearest neighbor
        path.append(nearest_neighbor)
        unvisited_nodes.remove(nearest_neighbor)
        current_node = nearest_neighbor

    # Return to the starting node to complete the cycle
    path.append(start_node)

    # Format the output
    result = {vehicle_info["v0"]["start_point"]: {"path": path}}
    return result

# Example usage
start_neighborhood = 'r0'
vehicle_info = data['vehicles']
# print(vehicle_info)

distance_matrix = {}
for n in data['neighbourhoods']:
    distance_matrix[n] = data['neighbourhoods'][n]['distances']
# print(distance_matrix)

restaurant = data['restaurants']['r0']['neighbourhood_distance']
# print(restaurant)

optimal_result = nearest_neighbor(distance_matrix, start_neighborhood, restaurant, vehicle_info)

# Print the optimal result
print(optimal_result)

f.close()