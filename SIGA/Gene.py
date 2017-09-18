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

        if p.SIGA_flag == "Yes":
            self.socialFitness = float(0)
            self.totalFitness = float(0)
            self.strat_name   = None

            #generating strategy profile
            num = random.uniform(0,1)
            if num >= 0 and num < p.allDRate:
                self.probC = 0.0
                self.probD = 1.0
                self.strat_name = "ALLD"
            elif num >= p.allDRate and num < p.allDRate + p.allCRate:
                self.probC = 1.0
                self.probD = 0.0
                self.strat_name = "ALLC"
            elif num >= p.allDRate + p.allCRate and num < p.allDRate + p.allCRate + p.TFTRate: 
                self.probC = 0.5
                self.probD = 0.5
                self.strat_name = "TFT"
            else:
                self.probC = random.random()
                self.probD = 1 - self.probC
                self.strat_name = "RND"
            
        Gene.population +=1

    #model what kind of move will the player do
    def play(self):
        #flip a coin
        coin = random.random()
        #C
        if (coin >= 0 and coin < self.probC):
            return "C"
        #D
        elif (coin >= self.probC and coin < 1):
            return "D"
                
    def traverse(self):
        print(self.genotype)

    @classmethod
    def howmany(cls):
        print ("currently {:d} genes".format(cls.population))
        
        