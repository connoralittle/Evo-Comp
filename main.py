from initialization import *
from read_data import *
from fitness import *
from utils import *
from parent_selection import *
import numpy as np
from mutation import *
from xover import *
import itertools
from offspring_selection import *
import random
from concurrent.futures import ProcessPoolExecutor, wait
import time
import matplotlib.pyplot as plt

def main(counter, mutation, title, selection = mu_plus_lambda_w_dynamic_pop, mu = 500):
    #pick the dataset. If changing the number of nodes you have to change the read_data file as well
    data = read_data("bar-n100-1")

    #time limit for program, set to hearts content
    TIME_LIMIT = 14400

    #time used to find out when hard constraints are dealt with
    start_time = time.time()

    #initialize parameters

    #testing: 15
    epochs = 50
    #six is the max number of cores I can run
    num_islands = 6
    populations = [None] * num_islands
    #populations, average_fitness, best_result, time_to_no_hcv, min_fitness
    records = [[[], [], [], -1] for x in range(num_islands)]

    migration_rate = 20

    #testing: 25 
    gens = 40
    mu = mu
    mut_rate = 0.5
    xover_rate = 1
    mating_pool_size = 2 * mu

    #start evolution
    for n in range(1, epochs+1):
        
        print("|----------------------------------|")
        print("|----------------------------------|")
        print("|----------------------------------|")
        print(f"EPOCH: {n}")
        print("|----------------------------------|")
        print("|----------------------------------|")
        print("|----------------------------------|")

        #run the 6 processes in parallel
        with ProcessPoolExecutor(max_workers=6) as executor:
            #collect the results after an epoch for each of the islands
            results = [executor.submit(async_genetic_algorithm, 
                    i, 
                    data,
                    order_xover,
                    mutation,
                    multi_pointer_selection,
                    selection,
                    gens,#gens
                    mu,#mu
                    mut_rate,#mut_rate
                    xover_rate,#xover_rate
                    mating_pool_size,#mating_pool_size
                    populations,
                    records[i]) for i in range(len(populations))]

            #wait for the results since they need to exchange genomes
            wait(results)
            #extract the relevant information
            populations = list(map(lambda x: x.result()[0], results))
            records = list(map(lambda x: x.result()[1], results))

        #temp is needed since everyone is trading and the last island should trade new members
        temp = random.sample(populations[-1], migration_rate)
        #for each population shuffle it and take migration_rate members from the island to the "left" in a ring topology
        for i in range(len(populations)):
            populations[i] = sorted(populations[i], reverse=True)
            for j in range(1, migration_rate + 1):
                populations[i].pop()
            if i == len(populations) - 1:
                populations[i] = populations[i] + temp
            else:
                populations[i] = populations[i] + random.sample(populations[i+1], migration_rate)

        #time cutoff. If it runs too long, no more epochs
        #set the number to be the number of seconds you allow your program to run for
        if time.time() - start_time > TIME_LIMIT :
            print("Ran out of time!")
            break

    #after all of the epochs print a summary of the results for each island
    for idx, n in enumerate(populations):
        evaluations = list(map(lambda x: calculate_fitness(data, x), n))
        print(f"Population {idx}")
        summary(n, evaluations)

    #try to record when there were 0 hard constraint violations, if not do nothing
    try:
        if records[3] != -1:
            print("Time to 0 hard constraint violations")
            print(min(filter(lambda y: y != -1, [x[3] for x in records])) - start_time)
    except:
        print()

    #write to file, title, run number, and the records for each island
    with open(str(title) + " results" + str(counter) + ".txt", 'w') as f:
        f.write(title)
        f.write('\n')
        f.write("Run" + str(counter))
        f.write('\n')
        f.write(str(records[0]))
        f.write('\n')
        f.write(str(records[1]))
        f.write('\n')
        f.write(str(records[2]))
        f.write('\n')
        f.write(str(records[3]))
        f.write('\n')
        f.write(str(records[4]))
        f.write('\n')
        f.write(str(records[5]))
        f.write('\n')

if __name__ == "__main__":
    #a file to keep track of how long each run takes
    f = open("time to run", 'w')

    #different trials I attempted
    # for i in range(0, 5):
    #     start_time = time.time()
    #     main(i, proportional_sublist_translation_mutation, "guass 2")
    #     print(f"\n--- Time to run --- \n{time.time() - start_time}")
    #     f.write(f"\n--- Time to run --- \n{time.time() - start_time}\n")

    # for i in range(0, 5):
    #     start_time = time.time()
    #     main(i, sublist_translation_mutation, "displacement mutation")
    #     print(f"\n--- Time to run --- \n{time.time() - start_time}")

    # for i in range(0, 5):
    #     start_time = time.time()
    #     main(i, swap_mutation, "swap mutation")
    #     print(f"\n--- Time to run --- \n{time.time() - start_time}")

    # for i in range(0, 5):
    #     start_time = time.time()
    #     main(i, proportional_sublist_translation_mutation, "normal init")
    #     print(f"\n--- Time to run --- \n{time.time() - start_time}")

    # for i in range(0, 5):
    #     start_time = time.time()
    #     main(i, proportional_sublist_translation_mutation, "1000 pop", mu_plus_lambda, 1000)
    #     print(f"\n--- Time to run --- \n{time.time() - start_time}")
    #     f.write(f"\n--- Time to run --- \n{time.time() - start_time}\n")

    # for i in range(0, 5):
    #     start_time = time.time()
    #     main(i, proportional_sublist_translation_mutation, "500 pop", mu_plus_lambda, 500)
    #     print(f"\n--- Time to run --- \n{time.time() - start_time}")
    #     f.write(f"\n--- Time to run --- \n{time.time() - start_time}\n")

    #an example run for a trial
    #runs 5 trials iteratively and saves the results to a file
    for i in range(0, 5):
        start_time = time.time()
        main(i, proportional_sublist_translation_mutation, "real run4", mu_plus_lambda, 100)
        print(f"\n--- Time to run --- \n{time.time() - start_time}")
        # f.write(f"\n--- Time to run --- \n{time.time() - start_time}\n")

    f.close()