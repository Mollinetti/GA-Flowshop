'''
Created on 01/07/2015

@author: Mollinetti
'''
import random, Gene, Parameters, GA, sys, os, time

if __name__ == "__main__":

        best = []
        argfile = str(sys.argv[1])
        #init parameters by reading the txt
        p = Parameters.Params(argfile)

        #check for the outfile
        if not os.path.exists("Out/C|"+ str(p.machines) + "|" + str(p.jobs)+"x"+ str(p.popNum)):
            os.makedirs("Out/C|"+ str(p.machines) + "|" +str(p.jobs)+"x"+ str(p.popNum))
            
        for i in range(0,int(sys.argv[2])):
            #init mersenne twister seed
            t = time.time()
            random.seed(t)
            ga = GA.GA(str(i),p)
            
            best.append(ga.run(ga.population,p))
        f = open("Out/C|"+ str(p.machines) + "|" + str(p.jobs)+"x"+ str(p.popNum)+'/BESTS','w')
        for i in range(0, int(len(best))):
            f.write("%12.10f"%(best[i])+ "\t")
            f.write("\n")
        f.write("Upper Bound: "+str(max(best))+"\n")
        f.write("Lower Bound: "+str(min(best))+"\n")
        f.close()
