from main import *
from deap import base
from deap import creator
from deap import tools
import numpy as np
import json


if __name__ == "__main__":
    run = optmizer()
    run.save = True

    #Change Target file from here
    run.target = np.genfromtxt("Target.csv",delimiter=',',dtype=int)
    with open('target.js', 'w') as fp:
        json.dump(run.target.tolist(), fp)
        
    with open("target.js", "r+") as f:
         old = f.read() # read everything in the file
         f.seek(0) # rewind
         f.write("target=" + old) # write the new line before

    individual = np.load("Best_ind.npy")
        
    run.evaluation(individual)
