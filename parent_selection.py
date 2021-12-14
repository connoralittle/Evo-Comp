import random
import numpy as np

#linear rank is unecessary since there is always differences between the genomes
def linear_rank(fitness, s, u):
    #tuple: fitness, original index
    fitness_sorted = sorted(zip(fitness, range(len(fitness))), reverse=True)
    ranks = list(map(lambda i: ((2-s)/u) + (  (2*i*(s-1))  /  (u*(u-1))  ) , \
        range(0,u)))
    #tuple: cumulative probability, original index
    return sorted( zip(np.cumsum(ranks), [x[1] for x in fitness_sorted]))

def fitness_proportional(fitness):
    fitness_sorted = sorted(zip(fitness, range(len(fitness))), reverse=True)
    f_sum = sum(fitness)
    return sorted( zip(np.cumsum(list(map(lambda x: x/f_sum, fitness))), [x[1] for x in fitness_sorted]))

def multi_pointer_selection(population, fitness, mating_pool_size):
    new_parents = []
    probabilities = fitness_proportional(fitness)
    # probabilities = linear_rank(fitness, 2, len(fitness))
    pointer = random.uniform(0, 1/mating_pool_size)

    for idx, elem in enumerate(probabilities):
        if pointer < elem[0]:
            new_parents.append(population[elem[1]])
            pointer += 1/mating_pool_size
            probabilities.insert(idx+1, elem)
    return new_parents