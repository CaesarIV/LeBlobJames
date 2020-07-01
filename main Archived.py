from deap import base
from deap import creator
from deap import tools

import numpy as np
import random
import json

class optmizer():

    def __init__(self,):
        self.genrations = 60
        self.population_size = 600
        self.CXPB = 0.45 
        self.MUTPB = 0.2
        self.g = 0
        random.seed(23)
        pass

    class Grid():
        def __init__ (self,):
            self.cells = np.zeros(shape=(24,24))
            self.cells[11,11] = 1
            self.oldChem_0= np.zeros(shape=(24,24))
            self.oldChem_1= np.zeros(shape=(24,24))
            self.oldChem_2= np.zeros(shape=(24,24))
            self.newChem_0= np.zeros(shape=(24,24))
            self.newChem_1= np.zeros(shape=(24,24))
            self.newChem_2= np.zeros(shape=(24,24))
            pass

    def grow_logistic_function(self, individual, x):
        maximum = 10
        minimum = -10
        p_threshhold = individual[0]
        B0 = (individual[1] * (maximum-minimum))+minimum
        B1 = (individual[2] * (maximum-minimum))+minimum 
        B2 = (individual[3] * (maximum-minimum))+minimum
        B3 = (individual[4] * (maximum-minimum))+minimum
        B4 = (individual[5] * (maximum-minimum))+minimum
        B5 = (individual[6] * (maximum-minimum))+minimum
        B6 = (individual[7] * (maximum-minimum))+minimum
        k = (B0 + (B1*x[0]) + (B2*x[1])) + (B3*x[2]) \
            +(B4*x[0]*x[1]) + (B5*x[0]*x[2]) + (B6*x[1]*x[2])
        p = 1/(1+(np.exp(-k)))
        if p >= p_threshhold:
            return 1
        else:
            return 0

    def die_logistic_function(self, individual, x):
        maximum = 10
        minimum = -10
        p_threshhold = individual[8]
        B0 = (individual[9] * (maximum-minimum))+minimum
        B1 = (individual[10] * (maximum-minimum))+minimum 
        B2 = (individual[11] * (maximum-minimum))+minimum
        B3 = (individual[12] * (maximum-minimum))+minimum
        B4 = (individual[13] * (maximum-minimum))+minimum
        B5 = (individual[14] * (maximum-minimum))+minimum
        B6 = (individual[15] * (maximum-minimum))+minimum
        k = (B0 + (B1*x[0]) + (B2*x[1])) + (B3*x[2]) \
            +(B4*x[0]*x[1]) + (B5*x[0]*x[2]) + (B6*x[1]*x[2])
        p = 1/(1+(np.exp(-k)))
        if p >= p_threshhold:
            return 1
        else:
            return 0
        
    def evaluation(self, individual):
        Grid = self.Grid()
        Steps = {}
        Steps[0]=Grid.cells.tolist()
        for step in range(1,5):

            
            for row in range(0,len(Grid.cells)):
                for col in range(0,len(Grid.cells[row])):
                    #updating/Diffusing chemical grid
                    Grid.newChem_0[row,col]= 0.5*(Grid.oldChem_0[row,col])
                    Grid.newChem_1[row,col]= 0.5*(Grid.oldChem_1[row,col])
                    Grid.newChem_2[row,col]= 0.5*(Grid.oldChem_2[row,col])
                    for i in range(-1,2):
                        for j in range(-1,2):
                            if (row+i >= 0) and (row+i < len(Grid.cells)) and (col+j >= 0) and (col+j < len(Grid.cells[row])):
                                Grid.newChem_0[row,col] += (1.0/16.0)*Grid.oldChem_0[row+i,col+j]
                                Grid.newChem_1[row,col] += (1.0/16.0)*Grid.oldChem_1[row+i,col+j]
                                Grid.newChem_2[row,col] += (1.0/16.0)*Grid.oldChem_2[row+i,col+j]
                            else:
                                Grid.newChem_0[row,col] += 0
                                Grid.newChem_1[row,col] += 0
                                Grid.newChem_2[row,col] += 0
                    #chemicals production
                    if Grid.cells[row,col] == 1:
                        Grid.newChem_0[row,col]+= individual[16]
                        Grid.newChem_1[row,col]+= individual[17]
                        Grid.newChem_2[row,col]+= individual[18] 

                    #GrowthAndDeath
                    x = (Grid.newChem_0[row,col],Grid.newChem_1[row,col],Grid.newChem_2[row,col])
                    if self.grow_logistic_function(individual, x) == 1:
                        Grid.cells[row,col] = 1
                    if self.die_logistic_function(individual, x) ==1:
                        Grid.cells[row,col] = 0

            Grid.oldChem_0 = Grid.newChem_0
            Grid.oldChem_1 = Grid.newChem_1
            Grid.oldChem_2 = Grid.newChem_2
            Steps[step] = Grid.cells.tolist()

        se = []
        for row in range(0,len(Grid.cells)):
            for col in range(0,len(Grid.cells[row])):
                se.append((self.target[row,col]-Grid.cells[row,col])**2)
        score = sum(se)
        if self.save == True:
            with open('Steps.js', 'w') as fp:
                json.dump(Steps, fp)

            with open("Steps.js", "r+") as f:
                 old = f.read() # read everything in the file
                 f.seek(0) # rewind
                 f.write("Steps=" + old) # write the new line before
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
        self.target=np.reshape(self.target,(24,24))
                         
        creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("attr_var", random.uniform, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_var, 19)
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

    run = optmizer()
    run.main()
