import itertools
from read_data import *
from initialization import *

def calculate_fitness(data, individual):
    #extract adjacency matrix and features
    adj, feats = data.adj, data.feats

    #constants
    NUM_VEHICLE_COST = 1000
    HARD_CONSTRAINT_VIOLATION_COST = 100_000

    #initialize starting values
    num_vehicles = 1
    total_distance = 0
    hard_constraint_penalty = 1
    routes = []

    #initialize starting information
    starting_idx = 0
    hard_constraint_penalizations = 0

    new_vehicle = False
    vehicle_distance = 0
    vehicle_node = 0
    vehicle_capacity = 0
    vehicle_pickups = []
    route = [0]
    prev_idx = 0

    #while there are still nodes to visit
    while (starting_idx < len(individual)):

        #Create a new vehicle if no current vehicle
        if new_vehicle:
            num_vehicles += 1
            vehicle_distance = 0
            vehicle_node = 0
            vehicle_capacity = 0
            vehicle_pickups = []
            prev_idx = 0
            route = [0]
            new_vehicle = False

        #Get the next node idx
        next_idx = individual[starting_idx]

        #Lookahead to see if travel is possible.
        #               Distance to next node     Distance to depot  Service time
        possible_dist = adj[prev_idx, next_idx] + adj[next_idx, 0] + feats[next_idx][6]
        
        #if not possible end the vehicles route and start another vehicle or if the service window for the next node has already expired
        if ((possible_dist + vehicle_distance > data.route_time) or (vehicle_distance + adj[prev_idx, next_idx] > feats[next_idx][5])):
            #return to depot
            vehicle_distance += adj[prev_idx, 0]
            total_distance += vehicle_distance
            new_vehicle = True
            route.append(0)
            routes.append(route)
            continue

        #If travel is possible, travel
        node_info = feats[next_idx]

        vehicle_distance += adj[prev_idx, next_idx]
        route.append(next_idx)

        node_capacity = node_info[3]
        early_time_window = node_info[4]
        late_time_window = node_info[5]
        service_time = node_info[6]
        pickup_pair = node_info[7]
        delivery_pair = node_info[8]

        #Penalize Hard Constraints

        #penalize not having enough room on the truck
        if (data.capacity - vehicle_capacity < node_capacity):
            hard_constraint_penalizations += hard_constraint_penalty

        #penalize visiting a delivery node without the pickup
        if (pickup_pair != 0 and pickup_pair not in vehicle_pickups):
            hard_constraint_penalizations += hard_constraint_penalty

        #if the place is not ready for you yet, wait
        if (vehicle_distance < early_time_window):
            vehicle_distance = early_time_window

        #if they are ready for you and they want a delivery, perform the service
        if (vehicle_distance <= late_time_window and pickup_pair in vehicle_pickups):
            vehicle_distance += service_time
            vehicle_capacity += node_capacity

        #if they are ready for you and they want a pickup, perform the service
        if (vehicle_distance <= late_time_window and delivery_pair != 0 and vehicle_capacity <= vehicle_capacity + node_capacity):
            vehicle_capacity += node_capacity
            vehicle_pickups.append(next_idx)
            vehicle_distance += service_time

        starting_idx += 1

        #make sure to add all metrics if end of genome is reached, otherwise the last route is lost
        if (starting_idx == len(individual)):
            vehicle_distance += adj[prev_idx, 0]
            total_distance += vehicle_distance
            route.append(0)
            routes.append(route)
            continue

        prev_idx = next_idx

    #objective value is staggered so different metrics are seperated
    obj_val = total_distance + NUM_VEHICLE_COST * num_vehicles + HARD_CONSTRAINT_VIOLATION_COST * hard_constraint_penalizations

    return num_vehicles, total_distance, hard_constraint_penalizations, routes, obj_val

if __name__ == "__main__":
    # num_vehicles, total_distance, hard_constraint_penalizations, routes = calculate_fitness(read_data("bar-n100-1"), \
    #     [
    #     31,44,35,81,16,66,32,82,19,85,94,69,
    #     29,21,71,27,47,79,11,22,97,77,72,6,61,25,56,75,1,51,
    #     40,48,9,59,5,55,90,98,41,8,10,91,60,38,28,78,88,58,
    #     26,76,30,80,7,39,57,42,92,12,89,18,62,68,37,36,87,50,100,86,
    #     14,15,64,49,45,43,65,4,99,46,95,96,54,93,23,73,
    #     33,13,63,20,83,17,67,2,34,52,84,24,70,74,3,53,
    #     ])

    data = read_data("bar-n100-1")
    num_vehicles, total_distance, hard_constraint_penalizations, routes, fitness = calculate_fitness(data, initialize_individual(data.n_nodes))

    print(num_vehicles)
    print(total_distance)
    print(hard_constraint_penalizations)
    print(routes)
    print(fitness)