'''
Created on 01/07/2015

@author: Mollinetti
'''
import random, Gene, Parameters, GA

if __name__ == "__main__":
    
    #lb = [2, 5, 8]
    #ub = [4, 7, 10]
    
    #p = Parameters.Params(3, 10, True, False, 0.8, 2, 0.05, 0.075, 0.015, lb, ub)

    #init parameters by reading the txt
    p = Parameters.Params('MWTCS')
    #init mersenne twister seed
    random.seed(None,2)
    
    ga = GA.GA(p)
    
    ga.run()
    
    #g = []
   
    
    #for i in range(0, p.popNum):
        #g.append(Gene.Gene(lb, ub, 3))
        #ga.population[i].traverse()
        #ga.evaluate(ga.population[i])
        #print(ga.population[i].fitness)


    #print("\n\n SELECTION \n \n \n")
    #ga.selection()
    #for i in range(0, len(ga.tnPool)):
        #ga.tnPool[i].traverse()
        #print(ga.tnPool[i].fitness)

    #print("\n\nCROSSOVER\n\n\n")
    #ga.crossover()
    #for i in range(0, len(ga.tnPool)):
        #ga.tnPool[i].traverse()
        #print(i, ':', ga.tnPool[i].fitness)

    #print("\n\nUPDATES\n\n\n")
    #ga.update()
    #for i in range(0, p.popNum):
        #ga.population[i].traverse()
        #print(ga.population[i].fitness)

    #print("\n\nMUTATION\n\n\n")
    #ga.mutation()

    #print("\n\nFINAL POPULATION\n\n\n")
    #for i in range(0, p.popNum):
        #g.append(Gene.Gene(lb, ub, 3))
        #ga.population[i].traverse()
        #print(ga.population[i].fitness)

    #print("\n\nBEST:\n\n", ga.findBest().fitness)

    