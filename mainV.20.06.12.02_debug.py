from deap import base
from deap import creator
from deap import tools

import copy
import numpy as np
import random
import json

from datetime import datetime

class optmizer():

    def __init__(self,):
        self.genrations = 1
        self.population_size = 300
        self.CXPB = 0.4 
        self.MUTPB = 0.2
        self.g = 0
        random.seed(64)
        pass

    class Grid():
        def __init__ (self,):
            self.size=(24,24)
            self.max_steps = 15
            
            self.cells_old=[]
            self.cells_new=[]
            for row in range(0, self.size[0]):
                self.cells_old.append([])                
                for col in range(0,self.size[1]):
                    self.cells_old[row].append(0)
            #seed
            self.cells_old[10][10] = 1
            pass
        
    def evaluation(self, individual):
        Grid = self.Grid()
        Grid.cells_new = copy.deepcopy(Grid.cells_old)
        

        squaredError=[]

        
        if self.save:
            Steps = {}
            Steps[0] = copy.deepcopy(Grid.cells_old)

        for step in range(1, Grid.max_steps):
            for row in range(0, Grid.size[0]):
                for col in range(0, Grid.size[1]):
                    #Checking Neighbour Cells Existance
                    neighbour_exist = False
                    for j in range(-1,2):
                        for k in range(-1,2):
                            if (row+j >= 0) and (row+j < Grid.size[0]) and (col+k >= 0) and (col+k < Grid.size[1]):
                                if Grid.cells_old[(row+j)][(col+k)] == 1:
                                    #print("cell", Grid.cells_old[(row)][(col)])
                                    #print("neighbour", Grid.cells_old[(row+j)][(col+k)])
                                    #print("step:", step, "cell:", row, col,"living neighbour:", row+j, col+k)
                                    neighbour_exist = True
                                else:
                                    neighbour_exist = False
                            if neighbour_exist:
                                break
                        if neighbour_exist:
                            break
                    #Growth And Death
                    if neighbour_exist: #and Grow.check(Grid.chem_new[row][col]) == 1::
                        Grid.cells_new[row][col] = 1


                    #Scoring Prep
                    if step > (Grid.max_steps-5):
                        squaredError.append((self.target[row,col] - Grid.cells_old[row][col])**2)

            Grid.cells_old = copy.deepcopy(Grid.cells_new)
            
            if self.save:
                Steps[step] = Grid.cells_old
                        
        if self.save:
            with open('Steps.js', 'w') as fp:
                json.dump(Steps, fp)

            with open("Steps.js", "r+") as f:
                 old = f.read() # read everything in the file
                 f.seek(0) # rewind
                 f.write("Steps=" + old) # write the new line before
                 
        score = sum(squaredError)
        return (score),

    def mutUniformFloat(self, individual, lowerBound=0.0, upperBound=1.0, indpb=0.3):
       size = len(individual)
       for i in range(size):
           if random.random() < indpb:
               individual[i] = random.uniform(lowerBound, upperBound)
       return (individual)

    def main(self,):
        self.save = False
        
        self.target = np.genfromtxt("Target.csv",delimiter=',',dtype=int)
        with open('target.js', 'w') as fp:
            json.dump(self.target.tolist(), fp)
            
        with open("target.js", "r+") as f:
             old = f.read() # read everything in the file
             f.seek(0) # rewind
             f.write("target=" + old) # write the new line before

        self.target=np.reshape(self.target,(24,24))
                         
        creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("attr_var", random.uniform, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_var, 22)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evaluation)
        toolbox.register("mate", tools.cxUniform, indpb=0.5)
        toolbox.register("mutate", self.mutUniformFloat)
        toolbox.register("select", tools.selTournament, tournsize=3)
        pop = toolbox.population(n=self.population_size)        
        print("Start of evolution")        
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit        
        print("  Evaluated %i individuals" % len(pop))
        fits = [ind.fitness.values[0] for ind in pop]        
        while self.g <= self.genrations:
            self.g += 1
            print("-- Generation %i --" % self.g)            
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))     
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            for mutant in offspring:
                if random.random() < self.MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values  
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit         
            print("  Evaluated %i individuals" % len(invalid_ind))         
            pop[:] = offspring         
            fits = [ind.fitness.values[0] for ind in pop]                 
            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))   
        print("-- End of (successful) evolution --")
        self.best_ind = tools.selBest(pop, 1)[0]
        np.save("Best_Ind.npy",self.best_ind)
        print("Best individual is %s, %s" % (self.best_ind, \
                                             self.best_ind.fitness.values))
        self.save = True
        self.evaluation(self.best_ind)
        pass

if __name__ == "__main__":
    start = datetime.now()
    run = optmizer()
    run.main()
    print("Duration:", datetime.now()-start)
