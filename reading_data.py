import json
import itertools
import matplotlib.pyplot as plt
from read_data import *
import statistics
import numpy as np

if __name__ == "__main__":
    #initialization
    records = []
    records2 = []
    records3 = []
    records4 = []
    records5 = []
    records6 = []
    records7 = []
    records8 = []
    num_islands = 6
    num_runs = 5
    data = read_data("bar-n100-1")

    #this reads in a records file
    for i in range(num_runs):
        #open the file
        with open("results/standard array results" + str(i) + ".txt", 'r') as f:
            #the first 2 lines are useless
            f.readline()
            f.readline()

            #read the records for each island
            for j in range(num_islands):
                rec = f.readline()
                #tuples cannot be converted by json so turn them to lists
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records.append(json.loads(rec))

    for i in range(num_runs):
        with open("results/displacement mutation results" + str(i) + ".txt", 'r') as f:
            f.readline()
            f.readline()

            for j in range(num_islands):
                rec = f.readline()
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records2.append(json.loads(rec))

    for i in range(num_runs):
        with open("results/swap mutation results" + str(i) + ".txt", 'r') as f:
            f.readline()
            f.readline()

            for j in range(num_islands):
                rec = f.readline()
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records3.append(json.loads(rec))

    for i in range(num_runs):
        with open("results/normal init results" + str(i) + ".txt", 'r') as f:
            f.readline()
            f.readline()

            for j in range(num_islands):
                rec = f.readline()
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records4.append(json.loads(rec))

    for i in range(num_runs):
        with open("results/guass 2 results" + str(i) + ".txt", 'r') as f:
            f.readline()
            f.readline()

            for j in range(num_islands):
                rec = f.readline()
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records5.append(json.loads(rec))

    for i in range(num_runs):
        with open("results/1000 pop results" + str(i) + ".txt", 'r') as f:
            f.readline()
            f.readline()

            for j in range(num_islands):
                rec = f.readline()
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records6.append(json.loads(rec))

    for i in range(num_runs):
        with open("results/500 pop results" + str(i) + ".txt", 'r') as f:
            f.readline()
            f.readline()

            for j in range(num_islands):
                rec = f.readline()
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records7.append(json.loads(rec))

    for i in range(num_runs):
        with open("results/100 pop results" + str(i) + ".txt", 'r') as f:
            f.readline()
            f.readline()

            for j in range(num_islands):
                rec = f.readline()
                rec = rec.replace('(', '[')
                rec = rec.replace(')', ']')
                records8.append(json.loads(rec))

    #below I graph lots of comparison graphs

    #extract relevant objective values
    objective_values = list(map(lambda x: x[1], records))
    objective_values = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values)]

    #extract relevant distances
    distances = list(map(lambda x: x[2], records5))
    distances = list(map(lambda x: list(map(lambda y: y[1], x)), distances))
    distances = [sum(sub_list) / len(sub_list) for sub_list in zip(*distances)]

    #extract relevant vehicle numbers
    num_vehicles = list(map(lambda x: x[2], records5))
    num_vehicles = list(map(lambda x: list(map(lambda y: y[0], x)), num_vehicles))
    num_vehicles = [sum(sub_list) / len(sub_list) for sub_list in zip(*num_vehicles)]

    objective_values2 = list(map(lambda x: x[1], records2))
    objective_values2 = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values2)]

    objective_values3 = list(map(lambda x: x[1], records3))
    objective_values3 = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values3)]

    objective_values4 = list(map(lambda x: x[1], records4))
    objective_values4 = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values4)]

    objective_values5 = list(map(lambda x: x[1], records5))
    objective_values5 = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values5)]

    objective_values6 = list(map(lambda x: x[1], records6))
    objective_values6 = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values6)]

    objective_values7 = list(map(lambda x: x[1], records7))
    objective_values7 = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values7)]

    objective_values8 = list(map(lambda x: x[1], records8))
    objective_values8 = [sum(sub_list) / len(sub_list) for sub_list in zip(*objective_values8)]

    distances4 = list(map(lambda x: x[2], records4))
    distances4 = list(map(lambda x: list(map(lambda y: y[1], x)), distances4))
    distances4 = [sum(sub_list) / len(sub_list) for sub_list in zip(*distances4)]

    num_vehicles4 = list(map(lambda x: x[2], records4))
    num_vehicles4 = list(map(lambda x: list(map(lambda y: y[0], x)), num_vehicles4))
    num_vehicles4 = [sum(sub_list) / len(sub_list) for sub_list in zip(*num_vehicles4)]

    #mutation plots
    plt.plot(range(len(objective_values)), objective_values5, label='Guassian Displacement SD 2')
    plt.plot(range(len(objective_values)), objective_values, label='Guassian Displacement SD 5')
    plt.plot(range(len(objective_values)), objective_values2, label='Displacement')
    plt.plot(range(len(objective_values)), objective_values3, label='Swap')
    plt.legend(loc="upper right")
    plt.title("Objective Value with different mutations")
    plt.savefig("figs/" + "Objective Value with different mutations", dpi=1000)
    plt.clf()

    #initialization plots
    plt.plot(range(len(objective_values5)), objective_values5, label='Kmeans')
    plt.plot(range(len(objective_values4)), objective_values4, label='Normal')
    plt.legend(loc="upper right")
    plt.title("Objective Value with different initializations")
    plt.savefig("figs/" + "Objective Value with different initializations", dpi=1000)
    plt.clf()

    plt.plot(range(len(distances)), distances, label='Kmeans')
    plt.plot(range(len(distances4)), distances4, label='Normal')
    plt.legend(loc="upper right")
    plt.title("Distance Value with different initializations")
    plt.savefig("figs/" + "Distance Value with different initializations", dpi=1000)
    plt.clf()

    plt.plot(range(len(num_vehicles)), num_vehicles, label='Kmeans')
    plt.plot(range(len(num_vehicles4)), num_vehicles4, label='Normal')
    plt.legend(loc="upper right")
    plt.title("Number of Vehicles with different initializations")
    plt.savefig("figs/" + "Number of Vehicles with different initializations", dpi=1000)
    plt.clf()

    #plot objective values over time
    #the time numbers is to visualize how much faster each is, because the longer time will obviously have a lower objective value
    plt.plot(np.linspace(0, 1316.3073308467865, len(objective_values5)), objective_values5, label='dynamic')
    plt.plot(np.linspace(0, 2664.0891184806824, len(objective_values6)), objective_values6, label='1000')
    plt.plot(np.linspace(0, 1351.2936100959778, len(objective_values6)), objective_values7, label='500')
    plt.plot(np.linspace(0, 307.9759609699249, len(objective_values6)), objective_values8, label='100')
    plt.legend(loc="upper right")
    plt.title("Objective Values with different populations")
    plt.savefig("figs/" + "Objective Values with different populations", dpi=1000)
    plt.clf()

    ## Single Run Graphs
    ## Final evaluation

    #use these if you want to graph routes and individual solution data

    # node_y = list(map(lambda x: data.feats[x][1], range(0, data.n_nodes)))
    # node_x = list(map(lambda x: data.feats[x][2], range(0, data.n_nodes)))
    # plt.scatter(node_x[0],node_y[0],marker=',', color='r')
    # plt.scatter(node_x[1:], node_y[1:])
    # plt.savefig("figs/" + "nodes", dpi=1000)
    # plt.clf()

    # for n in range(num_islands):

    #     routes = records[n][2][-1][3]
    #     for m in routes:
    #         routes_x = list(map(lambda x: node_x[x], m))
    #         routes_y = list(map(lambda x: node_y[x], m))
    #         plt.plot(routes_x, routes_y)
    #     plt.scatter(node_x, node_y)
    #     plt.savefig("figs/" + str(n) + "_route", dpi=1000)
    #     plt.clf()

    #     routes_x = list(map(lambda x: node_x[x], routes[0]))
    #     routes_y = list(map(lambda x: node_y[x], routes[0]))
    #     plt.plot(routes_x, routes_y)
    #     plt.scatter(node_x, node_y)
    #     plt.savefig("figs/" + str(n) + "_route_single", dpi=1000)
    #     plt.clf()

    # #graphs
    
    # #population graphs

    # for n in range(num_islands):
    #     plt.plot(range(len(records[0][0])), records[n][0])
    # plt.title("Poplations over time")
    # plt.savefig("figs/Poplations over time", dpi=1000)
    # plt.clf()

    # #average fitness graphs
    # for n in range(num_islands):
    #     plt.plot(range(len(records[0][1])), records[n][1])
    # plt.title("Average fitness over time")
    # plt.savefig("figs/Average fitness over time", dpi=1000)
    # plt.clf()

    # min_distances = [[y[1] for y in x[2]] for x in records]
    # min_vehicles = [[y[0] for y in x[2]] for x in records]
    # min_fitness = [[y[4] for y in x[2]] for x in records]



    # #min distance graphs
    # for n in range(num_islands):
    #     plt.plot(range(len(records[0][2])), min_distances[n])
    # plt.title("Min distance over time")
    # plt.savefig("figs/Min distance over time", dpi=1000)
    # plt.clf()

    # #min vehicles graphs
    # for n in range(num_islands):
    #     plt.plot(range(len(records[0][2])), min_vehicles[n])
    # plt.title("Min vehicles over time")
    # plt.savefig("figs/Min vehicles over time", dpi=1000)
    # plt.clf()

    # #min fitness graphs
    # for n in range(num_islands):
    #     plt.plot(range(len(records[0][2])), min_fitness[n])
    # plt.title("Min fitness over time")
    # plt.savefig("figs/Min fitness over time", dpi=1000)
    # plt.clf()
