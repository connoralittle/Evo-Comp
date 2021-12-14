import random
from read_data import *
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.cluster import KMeans

#create a single individual
def initialize_individual(n_nodes):
    #create a range
    genome = list(range(1, n_nodes))
    #and permute it
    random.shuffle(genome)
    return genome

#create an individual from a range
def initialize_preset_individual(genome):
    #permute the individual
    random.shuffle(genome)
    return genome

#create individual from clusters
def initialize_clusters_population(genome):
    #permute cluster order
    random.shuffle(genome)
    #then for each cluster permute the order within the cluster
    for m in range(len(genome)):
        random.shuffle(genome[m])
    return genome
    
#returns a randomly created population
def initialize_population(population_size, n_nodes):
    return [initialize_individual(n_nodes) for n in range(0, population_size)]

#smart initialization sorts the data and keeps pickup delivery nodes in pairs
#then it permutes the pairs
#i have chosen not to use this as it contains an assumption that might not be true
#and thats that there are no loops or simultaneous pickup deliverys
#if A has a pickup to be delivered to B and also is expecting a delivery from B it cannot be sorted
def smart_initialization(population_size, data):
    feats = data.feats
    pairs = [[(int(n[0]), int(n[8])) for n in feats[1:] if n[8] != 0] for x in range(population_size)]
    pop = [initialize_preset_individual(n) for n in pairs]
    return [[item for t in n for item in t] for n in pairs]

#clusters the data based on spatial location then creates a population of clusters permuted individuals
def kmeans_initialization(population_size, data, k_guess):
    feats = data.feats[1:]
    locations = np.transpose([[x[1] for x in feats], [x[2] for x in feats]])
    locations = StandardScaler().fit(locations).transform(locations)
    clusters = KMeans(n_clusters=k_guess).fit(locations)
    pops = [[[] for i in range(k_guess)] for x in range(population_size)]
    for m in range(data.n_nodes-1):
        for n in pops:
            n[clusters.labels_[m]].append(m + 1)
    pop = [initialize_clusters_population(pop) for pop in pops]
    return [[item for t in n for item in t] for n in pop]
    
if __name__ == "__main__":
    population = kmeans_initialization(10, read_data("bar-n1000-1"), 6)
    print(population)