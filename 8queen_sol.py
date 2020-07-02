# Solving 8 Queen problem using Genetic Algorithm

import random
import numpy as np

maxFitness = 28 # 28 is the number of possible collissions for a queen in a chessboard
mutation_probability = 0.03

#Fitness function
# derives the fitment of a chromosome as the ideal solution.
# Column colission is 0 as the 8 queens are distributed across the 8 columns
# Derives colission across rows and diagonals
# Overall colission count = row colission + column colission + diagonal colission
# Overall fitment = max fitment - total colissions
def fitness(chromosome):
    row_colissions = abs(len(chromosome) - len(np.unique(chromosome)))
    colissions = row_colissions
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if ( i != j):
                if(abs(i-j) == abs(chromosome[i] - chromosome[j])):
                    colissions += 1
    fitment = maxFitness - colissions
    return fitment

#Chromosome selection function
# selects a random chromosome from the population based on the associated probability for a correct solution
def select_parents(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w

#Recombination function
# combines 2 chromosomes to generate an offspring chromosome        
def recombine(chromosome1, chromosome2):
    n = len(chromosome1)
    c = random.randint(0, n - 1)
    return chromosome1[0:c] + chromosome2[c:n]

#Mutation function
# introduce mutation to the provided chromosome by replacing a random gene at a ramdom position
def mutate(chromosome):
    n = len(chromosome)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    chromosome[c] = m
    return chromosome

#Advance the Generation
# initiates chromosome selection, recombination, mutation and generate next generation of same size as the current generation
def gen_nxt(population, fitness):
    new_population = []
    probabilities = [(fitness(n) / maxFitness) for n in population]
    for i in range(len(population)):
        x = select_parents(population, probabilities)
        y = select_parents(population, probabilities)
        child = recombine(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        new_population.append(child)
        if fitness(child) == 28: break
    return new_population

#Main Function
if __name__ == "__main__": 
    population = [[random.randint(1,8) for i in range(8)] for j in range(128)] 
    generation = 1 

    while not 28 in [fitness(x) for x in population]:
        print("Generation = {}".format(generation))
        population = gen_nxt(population, fitness)
        print("                    Max fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
#print the final solution
    print("")
    print("Solution Generation = {}".format(generation-1))
    for x in population:
        if fitness(x) == 28:
            print("Solution ={},  Fitness = {}".format(str(x), fitness(x)))