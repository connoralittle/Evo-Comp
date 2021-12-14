from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
from read_data import *
import numpy

#solution printer
#if a solution is found this is a pretty print
def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    #for each vehicle
    for vehicle_id in range(data['num_vehicles']):
        #traverse the route
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        #and while there are still nodes
        while not routing.IsEnd(index):
            #calculate the distance
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))


def main():
    #if you change the dataset to a different number of nodes you have to update read_data.py
    dataset = read_data("bar-n100-1")

    #add the service times to the travel times
    adj =dataset.adj + [n[6] for n in dataset.feats]
    np.fill_diagonal(adj, 0)
    
    #get pickup delivery pairs
    pds = []
    for n in dataset.feats:
        if n[7] != 0:
            pds.append([n[7], n[0]])

    #set the number of vehicles
    num_vehicles = 100

    #create data
    data = {}
    data['distance_matrix'] = adj

    data['demands'] = [n[3] for n in dataset.feats]
    data['vehicle_capacities'] = num_vehicles * [300]

    data['pickups_deliveries'] = pds

    data['time_windows'] = [[int(n[4]), int(n[5])] for n in dataset.feats]

    data['num_vehicles'] = num_vehicles
    data['depot'] = 0
    
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    #distance callback is needed to define distance between nodes
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    #transit callback is a generalization of distance callback
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    #this makes all vehicles have the same distances
    #change if you want a heterogeneous fleet
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    #dimensions allow variables over the problem
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        480,  # vehicle maximum travel distance
        True,  # start cumul to zero
        'Distance')
    distance_dimension = routing.GetDimensionOrDie('Distance')
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Define Transportation Requests.
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(
                delivery_index))
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))

    #initial route copied over from my algorithm
    data['initial_routes'] = [
        [47, 97, 24, 7, 57, 27, 74, 77, 18, 25, 68, 75, 23, 1, 73, 51], 
        [14, 15, 64, 65, 16, 66, 50, 41, 91, 28, 100, 8, 78, 58], 
        [31, 32, 82, 5, 55, 11, 81, 61], 
        [33, 40, 83, 26, 76, 45, 12, 62, 95, 90, 37, 87, 3, 53], 
        [35, 17, 67, 85, 43, 30, 80, 9, 59, 93, 46, 6, 56, 36, 96, 86], 
        [20, 2, 42, 52, 92, 70], 
        [13, 63, 10, 29, 38, 60, 39, 79, 22, 72, 89, 88], 
        [21, 48, 98, 34, 49, 71, 84, 99, 19, 44, 69, 94, 4, 54],
    ]
   
   # Add Time Windows constraint.
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        480,  # allow waiting time
        480,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))


    initial_solution = routing.ReadAssignmentFromRoutes(data['initial_routes'],
                                                        True)
    # print(initial_solution)
    # print_solution(data, manager, routing, initial_solution)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)
    search_parameters.time_limit.FromSeconds(3000)

    # Solve the problem.

    #use this if there is an initial solution
    # solution = routing.SolveFromAssignmentWithParameters(initial_solution, search_parameters)

    #use this if there is no initial solution
    solution = routing.SolveWithParameters(search_parameters)


    # Print solution on console.
    if solution:
        print("solution found")
        print_solution(data, manager, routing, solution)
    else:
        print("no solution found")

    

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\n--- Time to run --- \n{time.time() - start_time}")