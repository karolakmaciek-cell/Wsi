import numpy as np
from random import randrange
from random import sample
from random import random
from random import randint

def calibration_error(bits_list):
    x=to_real_number(bits_list)
    return 5*len(x) + sum(xi**2 - 5*np.cos(2*np.pi*xi) for xi in x)

def to_real_number(bits_list):
    real_n_l=[]
    bits_list_divided=[bits_list[i*8:8+i*8] for i in range(10)]
    for one_data in bits_list_divided:
        str_bits="".join(map(str,one_data))
        value= -5+((int(str_bits,2))/255)*10
        real_n_l.append(value)
    return real_n_l

def tournament_selection(k,population):
    lengt_list=len(population)
    best_index=randrange(0,len(population))
    best_result=calibration_error(population[best_index])
    for _ in range(1,k):
        curr_index=randrange(0,lengt_list)
        curr_result=calibration_error(population[curr_index])
        if curr_result<best_result:
            best_index=curr_index
            best_result=curr_result
    return population[best_index]

def crossbreeding(first_partent,second_parent,chromosome_length,n_place2cut):
    place2cut=sorted(sample(range(1,chromosome_length),n_place2cut))
    offspring1, offspring2=[], []
    p_before=0
    for i,v in enumerate(place2cut+[len(first_partent)]):
        if i%2==0:
            offspring1.extend(first_partent[p_before:v])
            offspring2.extend(second_parent[p_before:v])
        else:
            offspring1.extend(second_parent[p_before:v])
            offspring2.extend(first_partent[p_before:v])
        p_before=v
    return offspring1, offspring2

def mutate(chromosom):
    proc=1/len(chromosom)
    chrom_after_mutation=[]
    for bit in chromosom:
        rand_number=random()
        if rand_number<proc:
            if bit==1:
                bit_negation=0
            else:
                bit_negation=1
            chrom_after_mutation.append(bit_negation)
        else:
            chrom_after_mutation.append(bit)
    return chrom_after_mutation

def find_best(ind_list):
    best_individual = ind_list[0]
    best_score = calibration_error(best_individual)
    for chrom_obj in ind_list:
        current_score = calibration_error(chrom_obj)
        if calibration_error(chrom_obj)<best_score:
            best_individual=chrom_obj
            best_score=current_score
    return best_individual

#fes to liczba ktora mowi nam o tym ile mamy ewoluacji
#k to liczba ktora mowi nam o tymi z ilu osobnikow jest selekcja turnijowa
#n to liczba miejsc w ktorych tniemy w krzyzowaniau
#pc to prawdopodobienstwo krzyzowania
def genetic_algorithm(population,Fes,k,n,pc):
    number_of_indyviduals=len(population)
    length_of_chrom=len(population[0])
    current_population=population
    next_population=[]
    first_parent=[]
    second_parent=[]
    t=0
    tmax=Fes/number_of_indyviduals
    best_individual = find_best(population)
    best_score=calibration_error(best_individual)

    while t<tmax:
        for _ in range(0,int(len(population)/2)):
            first_parent=tournament_selection(k,current_population)
            second_parent=tournament_selection(k,current_population)
            if random() < pc:
                offspring1, offspring2=crossbreeding(first_parent,second_parent,length_of_chrom,n)
            else:
                offspring1=first_parent[:]
                offspring2=second_parent[:]
            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)
            next_population.append(offspring1)
            next_population.append(offspring2)
        current_gen_best = find_best(next_population)
        current_gen_score = calibration_error(current_gen_best)

        if current_gen_score < best_score:
            best_individual = current_gen_best
            best_score = current_gen_score
        current_population=next_population
        next_population = []
        t+=1

    return best_individual, calibration_error(best_individual)


def generate_population(number_of_indv, number_of_genes):
    return [[randint(0,1) for _ in range(number_of_genes)] for _ in range(0,number_of_indv) ]

if __name__ == '__main__':

    population=generate_population(100,80)
    print(genetic_algorithm(population,9000,4,2,0.9))