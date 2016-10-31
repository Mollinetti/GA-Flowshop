'''
Created on 01/07/2015

@author: Mollinetti
'''
import math

def fitnessFunc(function, arg):
    result = function(arg)
    return result


def GoldsteinPrice(x):
    result =  ( 1 + math.pow( x[0] + x[1] + 1, 2 ) * ( 19 - 14 * x[0] + 3 * math.pow( x[0], 2 ) - 14 * x[1] + 6 * x[0] * x[1] + 3 * pow( x[1], 2 ) ) )* ( 30 + math.pow( 2 * x[0] - 3 * x[1], 2 ) *( 18 - 32 * x[0] + 12 * math.pow( x[0], 2 ) + 48 * x[1] - 36 * x[0] * x[1] + 27 * pow( x[1], 2 ) ) )
    violation = 0
    return result, violation



def calculateG1(x):
    return float(1 - ((pow(x[1], 3) * x[2]) / (7178 * pow(x[0], 4))))



def calculateG2(x):
    return float(((4 * x[1] * x[1] - x[0] * x[1]) / (12566 * pow(x[0], 3) * x[1] - pow(x[0], 4))) + (1 / (5108.0 * x[0] * x[0])) - 1)


def calculateG3(x):
    return float(1 - 140.45 * x[0] / (x[2] * x[1] * x[1]))


def calculateG4(x):
    return float((x[0] + x[1]) / 1.5 - 1)
  


def calculateFitness(x):
    return float((x[2] + 2.0) * x[1] * pow(x[0],2.0))




def MWTCS(x):

    violations = 0

    restrictions = list(range(4))

    restrictions[0] = calculateG1(x)

    if restrictions[0] > 0:
        violations+=1
    

    restrictions[1] = calculateG2(x)

    if restrictions[1] > 0:
        violations+=1
    

    restrictions[2] = calculateG3(x)

    if restrictions[2] > 0:
        violations+=1
    

    restrictions[3] = calculateG4(x)

    if restrictions[3] > 0:
        violations+=1
    

    fitness = calculateFitness(x)
    
    return fitness, violations, restrictions

