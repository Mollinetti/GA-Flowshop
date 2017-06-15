'''
Created on 01/07/2015

@author: Mollinetti
'''
import random, Gene, Parameters, GA, sys, os

if __name__ == "__main__":

    try:
        best = []
        argfile = str(sys.argv[1])
        #init parameters by reading the txt
        p = Parameters.Params(argfile)
        #init mersenne twister seed
        random.seed(None,2)
        #check for the outfile
        if not os.path.exists("Out/C|"+ str(p.machines) + "|" + str(p.jobs)):
            os.makedirs("Out/C|"+ str(p.machines) + "|" +str(p.jobs))

        for i in range(0,int(sys.argv[2])):
            ga = GA.GA(str(i),p)
            
            best.append(ga.run(ga.population,p))
        f = open("Out/C|"+ str(p.machines) + "|" + str(p.jobs)+'/BESTS','w')
        for i in range(0, int(len(best))):
            f.write("%12.10f"%(best[i])+ "\t")
            f.write("\n")
        f.close()
    except IndexError:
        print("\nRight usage: python3 SIGA.py [Parameter file] [number of executions]\n")