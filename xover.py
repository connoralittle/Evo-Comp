import random
import numpy as np
from initialization import *

#pmx crossover that returns 2 offspring
def pmx_xover(parent1, parent2):
    start, end = random.sample(range(0, len(parent1)), 2)
    if start > end:
        start, end = end, start

    return pmx_xover_sub(parent1, parent2, start, end), pmx_xover_sub(parent2, parent1, start, end)

#pmx crossover for a single offspring
def pmx_xover_sub(parent1, parent2, start, end):
    offspring = [0] * len(parent1)
    offspring[start:end+1] = parent1[start:end+1]

    for i in range(start, end+1):
        possible_elem = parent2[i]

        if possible_elem in offspring:
            continue
        
        while (True):
            j = offspring[i]
            possible_idx = parent2.index(j)
            
            if possible_idx not in range(start, end+1):
                offspring[possible_idx] = possible_elem
                break
            else:
                i = possible_idx

    for idx, i in enumerate(parent2):
        if i not in offspring:
            offspring[idx] = i

    return offspring

#order crossover that returns 2 offspring
def order_xover(parent1, parent2):

    start, end = random.sample(range(0, len(parent1)), 2)
    if start > end:
        start, end = end, start
    
    return order_xover_sub(parent1, parent2, start, end), pmx_xover_sub(parent2, parent1, start, end)

#order crossover that returns a single offspring
def order_xover_sub(parent1, parent2, start, end):
    offspring = [0] * len(parent1)
    offspring[start:end+1] = parent1[start:end+1]

    pointer = end + 1
    for elem in parent2[end:] + parent2:
        if elem not in offspring:
            if pointer == len(parent2):
                pointer = 0
            offspring[pointer] = elem
            pointer += 1


    return offspring


if __name__ == "__main__":
    population = kmeans_initialization(10, read_data("bar-n100-1"), 6)
    a = population[0]
    b = population[1]
    order_xover(a, b)
    off1 = order_xover_sub([1,2,3,4,5,6,7,8,9], [9,3,7,8,2,6,5,1,4], 3, 6)
    off2 = order_xover_sub([9,3,7,8,2,6,5,1,4], [1,2,3,4,5,6,7,8,9], 3, 6)
    print(off1)
    print(off2)
