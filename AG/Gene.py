'''
Created on 01/07/2015

@author: Mollinetti
'''
import random, Parameters

class Gene():
    
    population = 0
        
    def __init__(self, p = Parameters, type = 0):
        if type == 0:
            self.genotype = random.sample(range(0,p.jobs),p.jobs)
            self.fitness = float("inf")
        else:
            self.genotype = []
            self.fitness = float("inf")
        
        Gene.population +=1
                
    def traverse(self):
        print(self.genotype)

    @classmethod
    def howmany(cls):
        print ("currently {:d} genes".format(cls.population))
        
        