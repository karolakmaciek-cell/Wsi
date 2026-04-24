from binary_function import genetic_algorithm
from arithmetic_function import evolutionary_algorithm
from random import randint
from random import random

def generate_population_ga(number_of_indv, number_of_genes):
    return [[randint(0,1) for _ in range(number_of_genes)] for _ in range(0,number_of_indv) ]

def generate_population_ea(number_of_indv, number_of_genes):
    return [[random()*10-5 for _ in range(number_of_genes)] for _ in range(0,number_of_indv) ]

if __name__ == '__main__':

    population_ea=generate_population_ea(100,10)
    print(evolutionary_algorithm(population_ea,9000,20,0.5,100,0.9))

    population_ga=generate_population_ga(100,80)
    print(genetic_algorithm(population_ga,9000,4,2,0.9))