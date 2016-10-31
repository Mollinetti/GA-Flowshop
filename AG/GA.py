'''
Created on 01/07/2015

@author: Mollinetti
'''

import Parameters, math, copy, random, Gene, KCrossover, Fitness
from operator import attrgetter

class GA ():
    
    
    
    def __init__(self,  param = Parameters):
        
        self.population = []
        self.tnPool = []
        self.param = param

        #list with every best element
        self.bests = []

        #list with all the children 
        self.children = []

        #number of restriction
        self.restrictions = param.restrictions

        #define the pool size
        self.pool_size = (math.floor(self.param.popNum * self.param.cRate))
        #ensuring an even value
        if self.pool_size % 2 != 0:
            self.pool_size = self.pool_size - 1

        for _ in range(0, self.param.popNum):
            self.population.append(Gene.Gene(self.param.lowBound, self.param.uppBound, self.param.dim))

        #as a placeholder, set the superindividual as the first element of the population
        self.super = self.population[0]

            
    def evaluate(self,  g = Gene):
    	#generic function for fitness assessment
        #bounding all parameters
        for i in range(0, self.param.dim):
            if g.genotype[i] < self.param.lowBound[i]:
                g.genotype[i] = self.param.lowBound[i]

            elif g.genotype[i] > self.param.uppBound[i]:
                g.genotype[i] = self.param.uppBound[i]

        result = getattr(Fitness, self.param.funcName)(g.genotype)
        g.fitness = copy.copy(result[0])
        if self.param.hasConst == True:
            g.violations = copy.copy(int(result[1]))
            g.restrictions = copy.copy(result[2])
        
        
        
    def selection(self):
        #firstly, append the superindividual to the list
        self.tnPool.append(self.findBest())
        #building a variable size tournament selection    
        for _ in range(0, int(self.pool_size) - 1):
            tn_index = []
            pool = []
            tn_index = random.sample(range(len(self.population)),self.param.tn_size)
            for i in range(0, len(tn_index)):
                pool.append(self.population[tn_index[i]])
            
            #if the problems has constraints sort by violation and fitness 
            if self.param.hasConst == True:      
                #sort the tournament pool
                pool = sorted(pool, key = attrgetter('violations','fitness'))
            
                #minimization prob, select the least value
                if(self.param.isMin == True):
                    self.tnPool.append(pool[0])
                #maximization problem, select the bigger value
                else:
                    self.tnPool.append(pool[len(pool)- 1])
            #if the problems has no constraints sort by fitness 
            else:
                #sort the tournament pool
                pool = sorted(pool, key = attrgetter('fitness'))               
                #minimization prob, select the least value
                if(self.param.isMin == True):
                    self.tnPool.append(pool[0])
                #maximization problem, select the biggest value
                else:
                    self.tnPool.append(pool[len(pool)- 1])
        #self.tnPool = sorted(self.tnPool, key = attrgetter('fitness'))


    def crossover(self):
        #perform the crossover
        self.children.extend(KCrossover.KCrossover(self.tnPool, self.param))
        #loop over the pool in order to evaluate everything
        for i in range(0, int(len(self.children))):
            self.evaluate(self.children[i])
            #print(i, ':', self.children[i].fitness, self.children[i].genotype)
        #clearing the tournament pool
        self.tnPool[:] = []


        #finding the superindividual
        if self.param.isMin == True:
            if self.param.hasConst == True:
                self.super = min(self.children, key=attrgetter('violations','fitness'))  
            else:
                self.super = min(self.children, key=attrgetter('fitness'))
                
        else:
            if self.param.hasConst == True:
                self.super = max(self.children, key=attrgetter('violations','fitness'))
                
            else:
                best = max(self.children, key=attrgetter('fitness'))


                
        
    def mutation(self):
        #if a gene get a percentage lower than the rate, multiply one of the allels by U(0,1)
        #spare the first individual
        for i in range(1,len(self.population)):
            if random.uniform(0,1) < self.param.mRate:
                self.population[i].genotype[random.randint(0,self.param.dim - 1)] *=  random.uniform(0,1)
                self.evaluate(self.population[i])
                #print("individual", i, "has mutated")
                #print(self.population[i].genotype, "Fitness:", self.population[i].fitness)
                
            
        
    def update(self):
    	#sort the population acording to the best fitness and append the tournament pool to the population 
    	#firstly, sort the population
    	#if the problem has constraints sort by violation and fitness 
        if self.param.hasConst == True:      
            self.population = sorted(self.population, key = attrgetter('violations','fitness'))
            #if the problem has no constraints sort by fitness 
        else:
            self.population = sorted(self.population, key = lambda Gene: Gene.fitness)
        #replace the population with the tn_pool
        #if its a minimization problem pick do not start from the least values
        if self.param.isMin == True:
        	self.population[(len(self.population) - int(len(self.children))):] = list(self.children)
        #otherwise if it is a maximization problem, start from the least values
        else:
            self.population[: int(len(self.children)) - 1] = list(self.children)
        #sort once again
        if self.param.hasConst == True:      
            self.population = sorted(self.population, key = attrgetter('violations','fitness'))
            #if the problem has no constraints sort by fitness 
        else:
            self.population = sorted(self.population, key = lambda Gene: Gene.fitness)

        #clear the children list
        self.children[:] = []


    #function to find the best element of the population
    def findBest(self):
        if self.param.isMin == True:

            if self.param.hasConst == True:
                best = min(self.population, key=attrgetter('violations','fitness'))
                return best
            else:
                best = min(self.population, key=attrgetter('fitness'))
                return best
        else:
            if self.param.hasConst == True:
                best = max(self.population, key=attrgetter('violations','fitness'))
                return best
            else:
                best = max(self.population, key=attrgetter('fitness'))
                return best

    #funtion that writes the results of the algorithm
    def writeResult(self, filename):
        f = open(filename,'w')
        f.write(str("Fitness").rjust(5))

        if self.param.hasConst == True:
            f.write(str("Violations").rjust(5))

        for i in range(0,int(self.param.dim)):
            f.write("Variable" + str(i) +"\t")

        if self.param.hasConst == True:
            for i in range(0,int(self.param.restrictions)):
                f.write("Restriction"+ str(i) + "\t")

        f.write("\n")

        if self.param.hasConst == True:
            for i in range(0, int(len(self.bests))):
                f.write(str(self.bests[i].fitness)[:12])
                f.write(str(self.bests[i].violations).rjust(3)+ "  ")
                for j in range(0, int(self.param.dim)):
                    f.write(str(self.bests[i].genotype[j])[:12] + "  ")
                f.write(str(self.bests[i].violations)+ "\t")
                for j in range(0, int(self.param.restrictions)):
                    f.write(str(self.bests[i].restrictions[j]) + "\t") 
                f.write("\n")

        else:        
            for i in range(0, int(len(self.bests))):
                f.write(str(self.bests[i].fitness)+ "\t")
                for j in range(0, int(self.param.dim)):
                    f.write(str(self.bests[i].genotype[j])+ "\t")
                f.write("\n")    

        #end it by closing the file\
        f.close()

    #function to run the GA
    def run(self):
        #g = []
        #initial evaluation
        for i in range(0, self.param.popNum):
                #g.append(Gene.Gene(lb, ub, 3))
                #ga.population[i].traverse()
                self.evaluate(self.population[i])
                #print(ga.population[i].fitness)
        #main loop

        for i in range(0, int(self.param.generations)):
            
           # print("\n\n SELECTION \n \n \n")
            self.selection()
            #for i in range(0, len(ga.tnPool)):
                #ga.tnPool[i].traverse()
                #print(ga.tnPool[i].fitness)

           # print("\n\nCROSSOVER\n\n\n")
            self.crossover()
            #for i in range(0, len(ga.tnPool)):
                #ga.tnPool[i].traverse()
                #print(i, ':', ga.tnPool[i].fitness)

            #print("\n\nUPDATES\n\n\n")
            self.update()


            #print("\n\n")
            #for i in range(0, self.param.popNum):
                #ga.population[i].traverse()
                 #print(self.population[i].fitness)

            #print("\n\nMUTATION\n\n\n")
            self.mutation()


            #sort the population once again
            #if the problem has constraints sort by violation and fitness 
            if self.param.hasConst == True:      
                self.population = sorted(self.population, key = attrgetter('violations','fitness'))
                #if the problem has no constraints sort by fitness 
            else:
                self.population = sorted(self.population, key = lambda gene: gene.fitness)

            #print("\n\nFINAL POPULATION\n\n\n")
            #for i in range(0, self.param.popNum):
                #g.append(Gene.Gene(lb, ub, 3))
              #  ga.population[i].traverse()
                #print(self.population[i].violations, self.population[i].fitness )

            #print("\n\nBEST:\n\n", self.findBest().fitness)
            #g.append(self.findBest())

        #print(g[len(g)-1].fitness, g[len(g)-1].genotype[0], g[len(g)-1].genotype[1])
            self.bests.append(copy.copy(self.findBest()))

        
        #write result File
        self.writeResult("Results")




        

