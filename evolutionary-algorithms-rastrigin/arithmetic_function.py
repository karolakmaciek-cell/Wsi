import numpy as np
from random import gauss
from random import random
from random import randint

def calibration_error(x):
    return 5*len(x) + sum(xi**2 - 5*np.cos(2*np.pi*xi) for xi in x)

def gaussian_mutation(individual, sigma):
    individual_after_mutation=[]
    for gene in individual:
        gene_after_mutation=gene+gauss(0,sigma)
        if gene_after_mutation>5:
            individual_after_mutation.append(5)
        elif gene_after_mutation<-5:
            individual_after_mutation.append(-5)
        else:
            individual_after_mutation.append(gene_after_mutation)
    return individual_after_mutation


def arithmetic_crossover(first_parent, second_parent):
    offspring1=[]
    offspring2=[]

    for i in range(len(first_parent)):
        alpha=random()
        v1=first_parent[i]
        v2=second_parent[i]
        offspring1.append(alpha*v1 + (1-alpha)*v2)
        offspring2.append((1-alpha)*v1 + alpha*v2)

    return offspring1, offspring2

def find_best(population):
    best=population[0]
    best_score=calibration_error(best)
    for indiv in population:
        curr_score=calibration_error(indiv)
        if curr_score<best_score:
            best=indiv
            best_score=curr_score
    return best

# population - początkowa populacja osobników (rozwiązań)
# fes - maksymalna liczba ewaluacji funkcji celu (warunek stopu)
# mu - liczba rodziców wybieranych w każdej iteracji
# sigma - odchylenie standardowe mutacji (siła mutacji gaussowskiej)
# lambda_ - liczba potomków generowanych w każdej iteracji
# pc - prawdopodobieństwo krzyżowania
def evolutionary_algorithm(population,fes,mu,sigma,lambda_,pc):
    t=0
    current_population=population
    next_population = []
    population_size=len(population)
    #ocena+znajdz najlepszego
    #lista inicjalizacyjna dla osobnika na razie nic nie zostalo wybrane
    best_individual = find_best(population)
    best_score=calibration_error(best_individual)
    tmax=fes//population_size
    while t<tmax:
        parents=[]
        for indiv in current_population:
            parents.append((calibration_error(indiv),indiv))
        parents.sort(key=lambda x:x[0])
        parents=parents[:mu]
        count_parents=len(parents)
        for _ in range(lambda_//2):
            first_parent=parents[randint(0,count_parents-1)][1]
            second_parent=parents[randint(0,count_parents-1)][1]
            if random()<pc:
                offspring1, offspring2=arithmetic_crossover(first_parent,second_parent)
            else:
                offspring1 = first_parent[:]
                offspring2 = second_parent[:]
            offspring1 = gaussian_mutation(offspring1,sigma)
            offspring2 = gaussian_mutation(offspring2,sigma)
            next_population.append(offspring1)
            next_population.append(offspring2)
        current_gen_best = find_best(next_population)
        current_gen_score = calibration_error(current_gen_best)

        if current_gen_score < best_score:
            best_individual = current_gen_best
            best_score = current_gen_score
        current_population=next_population
        sigma = max(0.05, sigma * 0.995)
        next_population = []
        t+=1
    return best_individual, calibration_error(best_individual)
