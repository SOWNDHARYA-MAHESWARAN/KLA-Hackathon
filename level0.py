import json

f = open('Input data\level0.json')
data = json.load(f)

def nearest_neighbor(distance_matrix, start_node, start_distances, vehicle_info):
    num_nodes = len(distance_matrix)
    unvisited_nodes = set(distance_matrix.keys())
    current_node = start_node
    path = [current_node]
    total_cost = 0

    while len(path) < num_nodes:
        # Check if the current node is in the distance_matrix
        if current_node not in distance_matrix:
            break

        # Find the nearest unvisited neighbor
        unvisited_neighbors = [neighbor for neighbor in distance_matrix[current_node] if neighbor not in path]
        if not unvisited_neighbors:
            break  # No unvisited neighbors, end the loop

        # Use the index of the current_node and neighbor to access the distance
        current_index = int(current_node[1:])
        nearest_unvisited = min(unvisited_neighbors, key=lambda neighbor: distance_matrix[current_node][neighbor])

        # Extract the indices from the neighbor string
        neighbor_index = int(nearest_unvisited[1:])

        # Add the cost of the current move to the total_cost
        total_cost += distance_matrix[current_node][nearest_unvisited]

        # Move to the nearest neighbor
        path.append(nearest_unvisited)
        current_node = nearest_unvisited

    # Return to the starting node to complete the cycle
    path.append(start_node)

    # Add the cost of returning to the starting node
    start_index = int(start_node[1:])
    total_cost += start_distances[start_index]

    # Format the output
    result = {vehicle_info["v0"]["start_point"]: {"path": path, "total_cost": total_cost}}
    return result

# Example usage
start_neighborhood = 'r0'
vehicle_info = data['vehicles']

# Construct the distance matrix with neighborhood distances
distance_matrix = {n: {neighbor: data['neighbourhoods'][n]['distances'][i] for i, neighbor in enumerate(data['neighbourhoods'])} for n in data['neighbourhoods']}

# Add distances from the restaurant to neighborhoods in the distance matrix
restaurant_distances = data['restaurants']['r0']['neighbourhood_distance']
distance_matrix[start_neighborhood] = {neighbor: restaurant_distances[i] for i, neighbor in enumerate(data['neighbourhoods'])}

# Check if the starting node is in the distance_matrix
if start_neighborhood not in distance_matrix:
    print(f"Error: Starting node '{start_neighborhood}' not found in the distance matrix.")
else:
    optimal_result = nearest_neighbor(distance_matrix, start_neighborhood, restaurant_distances, vehicle_info)
    # Print the optimal result and total cost
    output={}
    temp = {}
    temp['path']=optimal_result['r0']['path']
    output['v0']= temp
    print(output)
    with open("level0_output.json", "w") as outfile: 
        json.dump(output, outfile)

f.close()
f = open('Input data\level0.json')
data = json.load(f)
