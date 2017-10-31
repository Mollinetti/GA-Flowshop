'''
Created on 01/07/2015

@author: Mollinetti
'''

import Parameters, Gene, random
from  more_itertools import unique_everseen
from operator import attrgetter


def evaluate(permutation, param = Parameters):

    #perm = permutation
    #data = param.joblist
 
    #create the list of machine times
    machine_times = [[] for _ in range(param.machines)]

    #assign the first job of the permutation to the machine
    machine_times[0].append(0)
    for mach in range(1,param.machines):
        # Start the next task in the job when the previous finishes
        machine_times[mach].append(machine_times[mach-1][0] + param.joblist[permutation[0]][mach-1])

    # Assign the remaining jobs
    for i in range(1, len(permutation)):

        # The first machine never contains any idle time
        job = permutation[i]
        machine_times[0].append(machine_times[0][-1] + param.joblist[permutation[i-1]][0])

        # For the remaining machines, the start time is the max of when the
        #  previous task in the job completed, or when the current machine
        #  completes the task for the previous job.
        for mach in range(1, param.machines):
            machine_times[mach].append(max(machine_times[mach-1][i] + param.joblist[permutation[i]][mach-1],machine_times[mach][i-1] + param.joblist[permutation[i-1]][mach]))

    return machine_times

#calculate makespam
def makespam(permutation, param = Parameters):
    """Computes the makespan of the provided solution
    For scheduling problems, the makespan refers to the difference between
    the earliest start time of any job and the latest completion time of
    any job. Minimizing the makespan amounts to minimizing the total time
    it takes to process all ajobs from start to finish."""
    return evaluate(permutation,param)[-1][-1] + param.joblist[permutation[-1]][-1]

def selection(permutation, param = Parameters):

    #create a list of chosen indices to the crossover
    chosen_pool = []
    #pool of indices with the indices of the population
    index_pool = random.sample(range(0,param.popNum), param.popNum)


    while(len(index_pool) > (param.popNum - param.tn_num)):

        if permutation[index_pool[1]].fitness > permutation[index_pool[0]].fitness:
            #add item 0 to chosen pool and pop it
            chosen_pool.append(index_pool.pop(0))
            #move the first item to the last
            index_pool.append(index_pool.pop(0))
        else:
            #move the first item to the last
            index_pool.append(index_pool.pop(0))
            #add item 0 to chosen pool and pop it
            chosen_pool.append(index_pool.pop(0))
    return chosen_pool


#perform the crossover
def crossover(permutation, param = Parameters):
    #obtain the index list of individuals who are selected for crossover
    index_pool = selection(permutation,param)
    #offsprings list
    offspring = []
    #loop over the pool in order to perform the crossovers
    for i in range(0, int(len(index_pool)), 2):
        #sample two indices of the list to be the cut points (1, len-2)
        cut_point = random.sample(range(1,param.jobs-1),2)
        #sort the cut point
        cut_point = sorted(cut_point)

        #crossover then reparation, it's faster to repair than to treat before repairing
        h1 = permutation[index_pool[i]].genotype[:cut_point[0]]
        h2 = permutation[index_pool[i+1]].genotype[:cut_point[0]]
        t1 = permutation[index_pool[i]].genotype[cut_point[1]+1:]
        t2 = permutation[index_pool[i+1]].genotype[cut_point[1]+1:]


        #look up the elements that are missing in both junctions of subsets
        diff1 = set(list(range(0,param.jobs))) - set(h1+t2)
        diff2 = set(list(range(0,param.jobs))) - set(h2+t1)


        #initialize offsprings as new clean individuals
        offspring.append(Gene.Gene(p,type=1))
        offspring.append(Gene.Gene(p, type=1))

        #append h1+ shuffle(diff1) + t2 
        offspring[i].genotype = h1 + random.sample(diff1,len(diff1)) + t2
        #append h2+ shuffle(diff2) + t1
        offspring[i+1].genotype = h2 + random.sample(diff2,len(diff2)) + t1

        print(offspring[i].genotype)
        print(offspring[i+1].genotype)

        #do any reparation necessary
        offspring[i].genotype = list(unique_everseen(offspring[i].genotype))
        offspring[i+1].genotype = list(unique_everseen(offspring[i+1].genotype))

        print(offspring[i].genotype)
        print(offspring[i+1].genotype)
    print("POPULATION")
    for i in range(0, int(len(permutation))):
        print(permutation[i].genotype)
    #loop over the pool in order to evaluate everything
    print("OFFSPRING")
    for i in range(0, int(len(offspring))):
        offspring[i].fitness = makespam(offspring[i].genotype,param)
        print(offspring[i].genotype)

    return offspring


def update(population, offspring, p = Parameters):
    #sort the population acording to the best fitness and append the tournament pool to the population 
    #firstly, sort the population
    sort_perm = sorted(population, key = attrgetter('fitness'))
    
    #if its a minimization problem pick the least values
    sort_perm[p.popNum - p.tn_num:] = list(offspring)
    print(p.tn_num)
    print("UPDATED POPULATION")
    for i in range(0, len(sort_perm)):
        print(sort_perm[i].genotype)

    return sort_perm

    

def mutation(permutation, p = Parameters):
    #getting a random index
    shift = random.sample(range(0,p.jobs),1)
    #saving the value of the random index
    tmp = permutation[shift[0]]
    #getting how many units the index will shift (it will either shift the length of permutation
    #vector - 1 to the left or to the right)
    move = random.randint(-(p.jobs-2),(p.jobs-2))
    #remove the element from the list
    permutation.remove(tmp)
    #add the removed element in the list mod(len(list)) units to right or left
    permutation.insert((shift[0]+move)%(len(permutation)+1),tmp)
    #print("VALUE:",tmp, " MOVE:", move)
    return permutation


p = Parameters.Params("test")
#print(p.jobs,p.machines, p.popNum, p.tn_size, p.generations)
#print(p.joblist)

perm = [] 
for i in range(0,p.popNum): 
    perm.append(Gene.Gene(p))
#print(perm[0].genotype)
#print(mutation(perm[0].genotype,p))
for i in range(0,len(perm)):
    perm[i].fitness= makespam(perm[i].genotype,p) 

#selection(perm,p)
update(perm,crossover(perm, p),p)