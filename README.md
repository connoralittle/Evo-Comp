# Evo-Comp
A genetic algorithmic approach to the pickup delivery problem

The figs folder is to store images and graphs.

n100, n1000, and n5000 are the datasets. They include their own readmes to explain their layout.
They come from https://data.mendeley.com/datasets/wr2ct4r22f/2.

Results contains text files of all data needed to know solutions after a given run.
Typically I run each trial 5 times and average the results.
Each line containts [populations over time, average fitness, evaluations, time to 0 hard constraint violations].
evaluations contain [num vehicles, total distance, hard_constraint_penalizations, routes, objective value].

There are 3 main files that need to be run
All of the files contain code that can be run but aside from the 3 listed below it was only for testing purposes.
For example the code in fitness.py under if __name__ == "__main__" can be ignored as its just various tests

main.py:
    This runs the genetic algorithm and saves the results to a file. The main function deals with all aspects of this.
    If you want to make changes to the evolutionary algorithm you can pass parameters or alter the main directly.
    The recommended format is to run each trial 5 times.
    To run alter the parameters in the main and run the file. Keep track of what you name your results to access them later

Ortool.py
    An implementation of the capacitated vehicle routing problem with time windows and pickup and delivery
    Uses Google's Ortools
    To run Or-tools implementation simply choose the dataset you want and run

reading_data.py
    This honestly should have been a ipynb
    This file reads in the data from results and analyzes it
    creates graphs and data

    to use this file pick the data file you want
    read the data into a records list
    and graph data extracted from the list
    just running it will graph most of the graphs that I used.
    I changed things as needed to make the graphs

fitness.py:
    implements fitness algorithm
intialization.py:
    implements intializations algorithms
mutation.py:
    implements mutation algorithms
offspring_mutation.py:
    implements offspring selection algorithms
parent_selection.py:
    implements parent selection algorithms
read_data.py:
    reads data into a class for ease of use
utils.py:
    wraps the genetic algorithm into a parallel safe version
xover.py:
    implements crossover algorithm
