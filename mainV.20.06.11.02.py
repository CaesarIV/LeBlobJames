from deap import base
from deap import creator
from deap import tools

import numpy as np
import random
import json

from datetime import datetime

class optmizer():

    def __init__(self,):
        self.genrations = 20
        self.population_size = 300
        self.CXPB = 0.4 
        self.MUTPB = 0.2
        self.g = 0
        random.seed(64)
        pass

    class Grid():
        def __init__ (self,):
            self.size=(24,24)
            self.chem = {}
            self.chem["new"]={}
            self.chem["old"]={}
            self.cells = {}
            for row in range(0,self.size[0]):
                self.chem["new"][row]={}
                self.chem["old"][row]={}
                self.cells[row]={}
                for col in range(0,self.size[1]):
                    self.cells[row][col]=0
                    self.chem["new"][row][col]={}
                    self.chem["old"][row][col]={}
                    for i in range(0,3):
                        self.chem["new"][row][col][i]=0
                        self.chem["old"][row][col][i]=0

            #seeds
            self.cells[10][10]=1
            #seedsNum = 10
            #for i in range(1,seedsNum):
            #    j = random.randint(0,self.size[0]-1)
            #    k = random.randint(0,self.size[1]-1)
            #    self.cells[j][k]=1
            pass

    class logistic_function():

        def __init__(self, attributes):
            self.attributes = attributes
            self.logistic_model()
            pass

        def logistic_model(self,):
            maximum = 10
            minimum = -10     
            self.p_threshhold = self.attributes[0]
            self.B0 = (self.attributes[1] * (maximum-minimum))+minimum
            self.B1 = (self.attributes[2] * (maximum-minimum))+minimum
            self.B2 = (self.attributes[3] * (maximum-minimum))+minimum
            self.B3 = (self.attributes[4] * (maximum-minimum))+minimum
            self.B4 = (self.attributes[5] * (maximum-minimum))+minimum
            self.B5 = (self.attributes[6] * (maximum-minimum))+minimum
            self.B6 = (self.attributes[7] * (maximum-minimum))+minimum
            pass

        def check(self,x):
            k = (self.B0 + (self.B1*x[0]) + (self.B2*x[1])) + (self.B3*x[2]) \
                +(self.B4*x[0]*x[1]) + (self.B5*x[0]*x[2]) + (self.B6*x[1]*x[2])
            p = 1/(1+(np.exp(-k)))
            if p >= self.p_threshhold:
                return 1
            else:
                return 0
        
    def evaluation(self, individual):
        Grow = self.logistic_function(individual[0:8])
        Die = self.logistic_function(individual[8:16])
        se=[]
        Grid = self.Grid()
        if self.save == True:
            Steps = {}
            cells=[]
            for row in Grid.cells:
                cells.append([])
                for col in Grid.cells[row]:
                    cells[row].append(Grid.cells[row][col])
            Steps[0]=cells

        max_steps = 15  
        for step in range(1,max_steps):
            if self.save == True:
                cells=[]
            for row in range(0, Grid.size[0]):
                if self.save == True:
                    cells.append([])
                for col in range(0, Grid.size[1]):
                    #updating chemical grid via diffusion and production
                    if Grid.cells[row][col] == 1:
                        chemProd = True
                    else:
                        chemProd = False
                    x=[]
                    neighbour_exist = False
                    for i in range(0,3):
                        #chemicals diffusion
                        Grid.chem["new"][row][col][i] = 0.5* Grid.chem["old"][row][col][i]
                        for j in range(-1,2):
                            for k in range(-1,2):
                                if (row+j >= 0) and (row+j < Grid.size[0]) and (j != 0) \
                                   and (col+k >= 0) and (col+k < Grid.size[1]) and (j != 0):
                                    Grid.chem["new"][row][col][i] += (1.0/16.0)*Grid.chem["old"][row+j][col+k][i]
                                    if Grid.cells[row+j][col+k] == 1:
                                        neighbour_exist = True
                        #chemicals production
                        if chemProd:
                            if self.target[row,col] == 1:
                                Grid.chem["new"][row][col][i]+= individual[16+i]
                            else:
                                Grid.chem["new"][row][col][i]+= individual[19+i]

                        x.append(Grid.chem["new"][row][col][i])
                    #GrowthAndDeath
                    if Grow.check(x) == 1 and neighbour_exist:
                        Grid.cells[row][col] = 1
                    if Die.check(x) == 1:
                        Grid.cells[row][col] = 0
                    if self.save:
                        cells[row].append(Grid.cells[row][col])
            Grid.chem["old"] = Grid.chem["new"]
            if self.save:
                Steps[step] = cells
                
            if step > max_steps-5:
                for row in range(0,Grid.size[0]):
                    for col in range(0,Grid.size[1]):
                        se.append((self.target[row,col]-Grid.cells[row][col])**2)
        if self.save:
            with open('Steps.js', 'w') as fp:
                json.dump(Steps, fp)

            with open("Steps.js", "r+") as f:
                 old = f.read() # read everything in the file
                 f.seek(0) # rewind
                 f.write("Steps=" + old) # write the new line before

        score = sum(se)
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
