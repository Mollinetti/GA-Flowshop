'''
Created on 01/07/2015

@author: Mollinetti
'''
import random

class Gene():
    
    population = 0
        
    def __init__(self, lowerbound, upperbound, size):
        self.genotype = []
        self.fitness = float("inf")
        self.violations = float("inf")
        self.restrictions = []
        
        
        for i in range(0,size):
            self.genotype.append(random.uniform(lowerbound[i], upperbound[i]))
 
        Gene.population +=1
                
    def traverse(self):
        print(self.genotype)
    
    @classmethod
    def howmany(cls):
        print ("currently {:d} genes".format(cls.population))
        
        
