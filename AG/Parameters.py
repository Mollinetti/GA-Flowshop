'''
Created on 01/07/2015

@author: Mollinetti
'''

import util,random, os

class Params:
    
    def __init__(self, filename):
        with open(filename) as f:
            data = f.read().splitlines()
        self.jobs      = int(data[0])
        self.machines  =int(data[1])
        self.popNum   = int(data[2])  
        self.tn_size  = int(data[3])
        self.crossover_rate = float(data[4])
        self.mutation_rate = float(data[5])
        self.generations  = int(data[6])
        self.jobBound = int(data[7])
        #number of individuals to have crossover
        self.tn_num = int(self.popNum * self.crossover_rate)
        #check for odd values
        if self.tn_num%2 != 0:
            self.tn_num = self.tn_num+1

        #processing time list for each job in each machine
        #ex: 4 jobs, 2 machines
        #[ [3,2],[1,1],[2,2],[3.3] ]
        self.joblist = []
        for i in range(0, self.jobs):
            self.joblist.append([random.randrange(1,(self.jobBound)+1) for _ in range(self.machines)])

        #check for the outfile
        if not os.path.exists("Out/C|"+ str(self.machines) + "|" + str(self.jobs)):
            os.makedirs("Out/C|"+ str(self.machines) + "|" +str(self.jobs))

        #print experiment report
        f = open("Out/C|"+ str(self.machines) + "|" + str(self.jobs)+'/Report','w')
        #f.write("Jobs = "+ str(self.jobs)+ " ranging from [0,"+ str(self.jobBound)+ "]\n")
        f.write("{:26s}{:>7s}\n".format("Jobs", "{}".format(str(self.jobs)+ " ranging from [0,"+ str(self.jobBound)+ "]")))
        f.write("{:20s}{:>7s}\n".format("Machines", "{}".format(self.machines)))
        f.write("{:20s}{:>7s}\n".format("Population", "{}".format(self.popNum)))
        f.write("{:20s}{:>7s}\n".format("Generations", "{}".format(self.generations)))
        f.write("{:20s}{:>7s}\n".format("Crossover Rate", "{:.2f}".format(self.crossover_rate)))
        f.write("{:20s}{:>7s}\n".format("Mutation Rate ", "{:.2f}".format(self.mutation_rate)))
        f.write("\n")
        f.write("Joblist:\n")
        for t in range(0,len(self.joblist)):
            #f.write(str(self.joblist[i])+"\n")
            f.write("{:5s}\n".format(str(self.joblist[t])))
        f.close()

        


