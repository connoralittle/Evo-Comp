import statistics
from initialization import *
from read_data import *
from fitness import *
from parent_selection import *
import numpy as np
from mutation import *
from xover import *
import itertools
from offspring_selection import *
import statistics
import time

#pretty print summary
def summary(population, fitness):
    fit = [x[4] for x in fitness]
    best_idx = fit.index(min(fit))
    s = "|------------------------------------------------------------------------------------------------------------|\n" + \
        f"Best Fitness: {min(fit)}\n" + f"Average Fitness: {statistics.mean(fit)}\n" + f"Best individual: {best_idx}\n" + \
        f"Number of Vehicles in best route: {fitness[best_idx][0]}\n" + f"Distance in best route: {fitness[best_idx][1]}\n" + \
        f"Hard constraint violations in best route: {fitness[best_idx][2] / 100_000}\n" + f"Routes in best route: {fitness[best_idx][3]}\n" + \
        "|------------------------------------------------------------------------------------------------------------|\n\n"
    print(s)

#parallel safe run of a genetic algorithm
def genetic_algorithm(data, xover, mut, parent_sel, offspring_sel, gens, mu, mut_rate, xover_rate, mating_pool_size, idx = 0, population = None, records = None):
    #init population
    if population == None:
        population = initialize_population(mu, data.n_nodes)
        # population = smart_initialization(mu, data)
        # population = kmeans_initialization(mu, data, int(data.n_nodes / 12))

    #initializations
    ka_prev = 1
    ks_prev = 1

    #for each generation
    for n in range(0, gens):
        #calculate fitness
        evaluations = list(map(lambda x: calculate_fitness(data, x), population))
        fitness = [x[4] for x in evaluations]

        #calculate min fitness
        min_fitness = min(fitness)
        #append relevant data
        records[0].append(mu)
        records[1].append(statistics.mean(fitness))
        records[2].append(evaluations[fitness.index(min_fitness)])
        if min_fitness < 100000 and records[3] == -1:
            records[3] = time.time()

        #select parents
        new_parents = np.array(parent_sel(population, fitness, mating_pool_size))
        random.shuffle(new_parents)
        new_parents = np.reshape(new_parents, (-1,2,len(population[0])))

        #xover
        xover_offspring = map(lambda x: xover(list(x[0]), list(x[1])) if random.random() <= xover_rate else (list(x[0]), list(x[1])), new_parents)
        flattened_offspring = [item for sublist in xover_offspring for item in sublist]

        #mutation
        mutation_offspring = list(map(lambda x: mut(x) if random.random() <= mut_rate else x, flattened_offspring))
        offspring_fitness = [calculate_fitness(data, x)[4] for x in mutation_offspring]

        #offspring selection
        population, mu, ka_prev, ks_prev = offspring_sel(population, fitness, mutation_offspring, offspring_fitness, mu, ka_prev, ks_prev)

        #population update
        mu = int(mu)
        if mu % 2 == 1:
            mu += 1
        mating_pool_size = 2*mu

        #every so often print things
        if n % 10 == 0:
            print(f"Idx: {idx}")
            print(f"Generation: {n}")
            print(f"Population: {mu}")
            summary(population, evaluations)

    return population, records

#async ready wrapper
def async_genetic_algorithm(idx, data, xover, mut, parent_sel, offspring_sel, gens, mu, mut_rate, xover_rate, mating_pool_size, pops, records):
    return genetic_algorithm(data, xover, mut, parent_sel, offspring_sel, gens, mu, mut_rate, xover_rate, mating_pool_size, idx, pops[idx], records)