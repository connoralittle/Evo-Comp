import random

#swap mutation takes 2 elements and swaps them
def swap_mutation(parent):
    start, end = random.sample(range(0, len(parent)), 2)
    parent[start], parent[end] = parent[end], parent[start]
    return parent

#inversion mutation takes a sublist and reverses it
def inversion_mutation(parent):
    start, end = random.sample(range(0, len(parent)), 2)
    if start > end:
        start, end = end, start
    parent[start:end+1]=parent[start:end+1][::-1]
    return parent

#insertion mutation picks an element and translates it to be adjacent to another
def insertion_mutation(parent):
    start, end = random.sample(range(0, len(parent)), 2)
    if start > end:
        start, end = end, start
    parent.insert(start+1, parent[end])
    del parent[end+1]
    return parent

#chance mutation was an idea I was playing with
#that allows multiple mutations to be used simultaneously
#by having a random one chosen each time mutation is called
#I did not end up using it
def chance_mutation(parent):
    rand = random.random()
    if rand < 0.5:
        return swap_mutation(parent)
    elif rand < 0.8:
        return sublist_translation_mutation(parent)
    else:
        return inversion_mutation(parent)

#displacement mutation
#I named it this before I realised what it was
#its a variation on insertion mutation except the instead of a single element being translated
#it is a whole sublist
def sublist_translation_mutation(parent):
    start, end = random.sample(range(0, len(parent)), 2)
    if start > end:
        start, end = end, start
    sublist = parent[start:end+1]
    if len(parent[start:end+1]) == len(parent):
        return parent
    del parent[start:end+1]
    new_start = random.sample(range(0, len(parent)), 1)[0]
    parent[new_start:new_start] = sublist
    return parent

#Gaussian displacement mutation
#Displacement mutation has a fixed sized sublist
#this allows a dynamic sized sublist based on a random draw from a Gaussian distribution
def proportional_sublist_translation_mutation(parent):
    start = random.sample(range(0, len(parent)), 1)[0]
    end = min(len(parent), max(0, start + int(random.gauss(0, 2))))
    if start > end:
        start, end = end, start
    sublist = parent[start:end+1]
    if len(parent[start:end+1]) == len(parent):
        return parent
    del parent[start:end+1]
    new_start = random.sample(range(0, len(parent)), 1)[0]
    parent[new_start:new_start] = sublist
    return parent

if __name__ == "__main__":
    print(proportional_sublist_translation_mutation([0,1,2,3,4,5,6]))
