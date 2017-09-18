'''
Created on 01/07/2015

@author: Mollinetti
'''

import Parameters, math, copy, random, Gene, KCrossover, Interaction
from operator import attrgetter
from  more_itertools import unique_everseen


class GA ():
    
    
    
    def __init__(self, outname,  param = Parameters):
        
        self.population = []
        self.param = param

        #output file name
        self.outname = outname

        #list with every best element
        self.bests = []

        #list holding information on the amount of each behavior in the population
        self.behavior_ind = []

        for _ in range(0, self.param.popNum):
            self.population.append(Gene.Gene(self.param))

            
    def process_makespam(self, permutation, param = Parameters):

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
    def makespam(self, permutation, param = Parameters):
        """Computes the makespan of the provided solution
        For scheduling problems, the makespan refers to the difference between
        the earliest start time of any job and the latest completion time of
        any job. Minimizing the makespan amounts to minimizing the total time
        it takes to process all jobs from start to finish."""
        return self.process_makespam(permutation,param)[-1][-1] + param.joblist[permutation[-1]][-1]

    #function to calculate the total fitness of an individual
    def calculateTotalFitness(self, g = Gene, param = Parameters):
        g.totalFitness = (param.alpha * g.fitness ) - (param.beta * g.socialFitness)

    #return a list with the selected individuals
    def selection(self,permutation, param = Parameters):
        #create a list of chosen indices to the crossover
        chosen_pool = []
        #pool of indices with the indices of the population
        index_pool = random.sample(range(0,param.popNum), param.popNum)

        if param.SIGA_flag == "Yes":     
            while(len(index_pool) > (param.popNum - param.tn_num)):

                if permutation[index_pool[1]].totalFitness > permutation[index_pool[0]].totalFitness:
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
    

    #Crossover following ackley's definition
    def crossover(self,permutation, param = Parameters):
        #obtain the index list of individuals who are selected for crossover
        index_pool = self.selection(permutation,param)
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


            #type 3:initialize offsprings as new clean individuals
            offspring.append(Gene.Gene(param,type=1))
            offspring.append(Gene.Gene(param, type=1))

            #type 1: offsprings inherit behavior from both parents
                #offspring[1].probC = self.population[index_pool[i]].probC
                #offspring[1].probD = self.population[index_pool[i]].probD
                #offspring[2].probC = self.population[index_pool[i+1]].probC
                #offspring[2].probD = self.population[index_pool[i+1]].probD

            #type 2: offsprings inherit behavior from the best parent
            #if self.population[index_pool[i]].socialFitness > self.population[index_pool[i]].socialFitness:
                #offspring[1].probC = self.population[index_pool[i]].probC
                #offspring[1].probD = self.population[index_pool[i]].probD
                #offspring[2].probC = self.population[index_pool[i]].probC
                #offspring[2].probD = self.population[index_pool[i]].probD
            #else:
                #offspring[1].probC = self.population[index_pool[i+1]].probC
                #offspring[1].probD = self.population[index_pool[i+1]].probD
                #offspring[2].probC = self.population[index_pool[i+1]].probC
                #offspring[2].probD = self.population[index_pool[i+1]].probD

          

            #append h1+ shuffle(diff1) + t2 
            offspring[i].genotype = h1 + random.sample(diff1,len(diff1)) + t2
            #append h2+ shuffle(diff2) + t1
            offspring[i+1].genotype = h2 + random.sample(diff2,len(diff2)) + t1

            #print(offspring[i].genotype)
            #print(offspring[i+1].genotype)

            #do any reparation necessary
            offspring[i].genotype = list(unique_everseen(offspring[i].genotype))
            offspring[i+1].genotype = list(unique_everseen(offspring[i+1].genotype))

            #print(offspring[i].genotype)
            #print(offspring[i+1].genotype)
            #print("\n")
        #print("POPULATION")
        #for i in range(0, int(len(permutation))):
            #print(permutation[i].genotype)
        #loop over the pool in order to evaluate everything
        #print("OFFSPRING")
        for i in range(0, int(len(offspring))):
            offspring[i].fitness = self.makespam(offspring[i].genotype,param)
            #print(offspring[i].genotype, offspring[i].fitness )

        return offspring            
    

    def mutation(self,permutation, param = Parameters):
        #getting a random index
        shift = random.sample(range(0,param.jobs),1)
        #saving the value of the random index
        tmp = permutation[shift[0]]
        #getting how many units the index will shift (it will either shift the length of permutation
        #vector - 1 to the left or to the right)
        move = random.randint(-(param.jobs-2),(param.jobs-2))
        #remove the element from the list
        permutation.remove(tmp)
        #add the removed element in the list mod(len(list)) units to right or left
        permutation.insert((shift[0]+move)%(len(permutation)+1),tmp)
        #print("VALUE:",tmp, " MOVE:", move)
        return permutation
        
    def update(self,population, offspring, param = Parameters):
        #sort the population acording to the best fitness and append the tournament pool to the population 
        #firstly, sort the population
        if param.SIGA_flag == "Yes":
            sort_perm = sorted(population, key = attrgetter('totalFitness'))

        #sort_perm = sorted(population, key = attrgetter('fitness'))
        #if its a minimization problem pick the least values

        sort_perm[param.popNum - param.tn_num:] = list(offspring)
 
        return sort_perm


    #function to find the best element of the population
    def findBest(self, population, param = Parameters):
        if param.SIGA_flag == "Yes":
            best = min(population, key=attrgetter('totalFitness'))
        best = min(population, key=attrgetter('fitness'))
        return best


    #funtion that writes the results of the algorithm
    def writeResult(self, filename):
        f = open(filename,'w')
        for i in range(0, int(len(self.bests))):
            f.write("%12.10f"%(self.bests[i].fitness)+ "\t")
            f.write("\n")
        #end it by closing the file\
        f.close()   

    #funtion that writes the behavior of the population
    def writeBehavior(self, filename):
        f = open(filename,'w')
        for i in range(0, int(len(self.behavior_ind))):
            f.write('{} {} {} {}'.format(self.behavior_ind[i][0],self.behavior_ind[i][1],self.behavior_ind[i][2],self.behavior_ind[i][3]))
            f.write("\n")
        #end it by closing the file\
        f.close()   

    #function to run the GA
    def run(self, population, p = Parameters):
        #initial evaluation
        for i in range(0, p.popNum):
            population[i].fitness = self.makespam(population[i].genotype, p)

        if p.SIGA_flag == "Yes":
            gEngine = Interaction.Interaction(self.param)

            #change the game payment matrix (if necessary)
            gEngine.change(1)

        #main loop   
        for i in range(0, int(p.generations)):
            gEngine.socialInteraction(self.findBest(population,p).fitness,self.population)
            #selection + crossover

            offspring = self.crossover(population,p)

            #mutation
            #get index of individuals for mutation 
            muta_index = random.sample(range(0, p.popNum), int(p.mutation_rate * p.popNum))
            for k in range(0, len(muta_index)):
                population[k].genotype = self.mutation(population[k].genotype, p)
                population[k].fitness = self.makespam(population[k].genotype, p)


            population = self.update(population, offspring, p)


            #print(g[len(g)-1].fitness, g[len(g)-1].genotype[0], g[len(g)-1].genotype[1])
            self.bests.append(copy.copy(self.findBest(population,p)))

            #storing information of the behavior of every individual
            tmp_list = [0,0,0,0]
            for ik in range(0, self.param.popNum):
                if population[ik].strat_name == 'ALLC':
                    tmp_list[0] +=1
                elif population[ik].strat_name == 'ALLD':
                    tmp_list[1] +=1
                elif population[ik].strat_name == 'TFT':
                    tmp_list[2] +=1
                else:
                    tmp_list[3] +=1

            #print(tmp_list)
            self.behavior_ind.append(tmp_list)


        
        #write result File
        self.writeResult("Out/C|"+ str(self.param.machines) + "|" + str(self.param.jobs)+"/"+self.outname)
        self.writeBehavior("Out/C|"+ str(self.param.machines) + "|" + str(self.param.jobs)+"/Behavior"+self.outname)

        #return best 
        return min(self.bests, key = attrgetter('fitness'))



        

