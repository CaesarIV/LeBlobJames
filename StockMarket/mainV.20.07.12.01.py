#V.20.07.12.01
from logistic_graphs import decision, chemical
from leblobGrid import Grid
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

        self.problemSpecific_init()
        
        pass

    def problemSpecific_init(self,):
        
        self.save = False
        self.target = np.genfromtxt("Target.csv",delimiter=',',dtype=int)
        with open('target.js', 'w') as fp:
            json.dump(self.target.tolist(), fp)
            
        with open("target.js", "r+") as f:
             old = f.read() # read everything in the file
             f.seek(0) # rewind
             f.write("target=" + old) # write the new line before
        self.target = np.reshape(self.target,(24,24))
        pass

        
    def evaluation(self, individual):
        #assign myGrid to local variable for performance boost
        myGrid = Grid()
        score = 0

        Grow = decision(individual[0:8])
        Die = decision(individual[8:16])

        chemicals = ( chemical(individual[16:19]), \
                      chemical(individual[19:22]), \
                      chemical(individual[22:25]) )

        if self.save:
            Steps = {}
            Steps[0] = myGrid.old_cells.tolist()

        locations = copy.deepcopy(myGrid.locations)
        moore_neighbourhood = copy.deepcopy(myGrid.neighbours)

        step = 0
        while step <= myGrid.max_steps and np.sum(myGrid.old_cells) > 0 and np.sum(myGrid.old_energy) > 0: 
            random.shuffle(locations)
            
            for cell in locations:

                neighbours_sum = 0
                reproduced = False
                random.shuffle(moore_neighbourhood)
                
                for moore_neighbour in moore_neighbourhood:
                                  
                    neighbour = tuple(map(sum, zip(cell, moore_neighbour)))
                    if (neighbour[0] >= 0) and (neighbour[1] >= 0) and \
                              (neighbour[0] < myGrid.X_size) and (neighbour[1] < myGrid.Y_size):

                        #Cellular reproduction
                        if myGrid.old_cells[cell[0]][cell[1]] == 1 and (not reproduced):
                            x =(myGrid.old_chemical_0[neighbour[0]][neighbour[1]], \
                            myGrid.old_chemical_1[neighbour[0]][neighbour[1]], \
                            myGrid.old_chemical_2[neighbour[0]][neighbour[1]])
                            myGrid.new_cells[cell[0]][cell[1]] = 1
                            if  Grow.check(x) == 1:
                                myGrid.new_cells[neighbour[0]][neighbour[1]] = 1
                                myGrid.new_energy[neighbour[0]][neighbour[1]] = 0.5 * myGrid.old_energy[cell[0]][cell[1]]
                                myGrid.new_energy[cell[0]][cell[1]] = 0.5 * myGrid.old_energy[cell[0]][cell[1]]
                                reproduced = True

                        #Chemicals
                        myGrid.new_chemical_0[cell[0]][cell[1]] += (1.0/16.0) * myGrid.old_chemical_0[neighbour[0]][neighbour[1]]
                        myGrid.new_chemical_1[cell[0]][cell[1]] += (1.0/16.0) * myGrid.old_chemical_1[neighbour[0]][neighbour[1]]
                        myGrid.new_chemical_2[cell[0]][cell[1]] += (1.0/16.0) * myGrid.old_chemical_2[neighbour[0]][neighbour[1]]

                        #Energy
                        if myGrid.old_cells[neighbour[0]][neighbour[1]] == 1:
                            myGrid.new_energy[cell[0]][cell[1]] += (1.0/16.0) * myGrid.old_energy[neighbour[0]][neighbour[1]]
                            neighbours_sum += 1

                #Chemicals
                myGrid.new_chemical_0[cell[0]][cell[1]] += 0.5 * myGrid.old_chemical_0[cell[0]][cell[1]]
                myGrid.new_chemical_1[cell[0]][cell[1]] += 0.5 * myGrid.old_chemical_1[cell[0]][cell[1]]
                myGrid.new_chemical_2[cell[0]][cell[1]] += 0.5 * myGrid.old_chemical_2[cell[0]][cell[1]]

                #Energy                                                                                                       
                myGrid.new_energy[cell[0]][cell[1]] += ((16.0-neighbours_sum)/16.0) * myGrid.old_energy[cell[0]][cell[1]]

                if myGrid.old_cells[cell[0]][cell[1]] == 1:
                    myGrid.new_chemical_0[cell[0]][cell[1]] += chemicals[0].production(myGrid.old_energy[cell[0]][cell[1]])
                    myGrid.new_chemical_1[cell[0]][cell[1]] += chemicals[1].production(myGrid.old_energy[cell[0]][cell[1]])
                    myGrid.new_chemical_2[cell[0]][cell[1]] += chemicals[2].production(myGrid.old_energy[cell[0]][cell[1]])
                                                                                                                                    
                    #Energy
                    if self.target[cell] == 1:
                        myGrid.new_energy[cell[0]][cell[1]] += 0.2
                    else:
                        myGrid.new_energy[cell[0]][cell[1]] -= 0.2

                    max_energy = 1
                    if myGrid.new_energy[cell[0]][cell[1]] > max_energy:
                        myGrid.new_energy[cell[0]][cell[1]] = max_energy
 
                    #Death
                    x =(myGrid.old_chemical_0[cell[0]][cell[1]], \
                        myGrid.old_chemical_1[cell[0]][cell[1]], \
                        myGrid.old_chemical_2[cell[0]][cell[1]])
                    if Die.check(x) == 1:
                        myGrid.old_cells[cell[0]][cell[1]] = 0
                        myGrid.old_energy[cell[0]][cell[1]] = 0

            myGrid.old_cells = copy.deepcopy(myGrid.new_cells)
            myGrid.old_energy = copy.deepcopy(myGrid.new_energy)
            myGrid.old_chemical_0 = copy.deepcopy(myGrid.new_chemical_0)
            myGrid.old_chemical_1 = copy.deepcopy(myGrid.new_chemical_1)
            myGrid.old_chemical_2 = copy.deepcopy(myGrid.new_chemical_2)
            myGrid.new_cells = np.zeros((myGrid.X_size, myGrid.Y_size))
            myGrid.new_energy = np.zeros((myGrid.X_size, myGrid.Y_size))
            myGrid.new_chemical_0 = np.zeros((myGrid.X_size, myGrid.Y_size))
            myGrid.new_chemical_1 = np.zeros((myGrid.X_size, myGrid.Y_size))
            myGrid.new_chemical_2 = np.zeros((myGrid.X_size, myGrid.Y_size))
            step += 1
            if self.save:
                Steps[step] = myGrid.old_cells.tolist()
                        
        if self.save:
            with open('Steps.js', 'w') as fp:
                json.dump(Steps, fp)

            with open("Steps.js", "r+") as f:
                 old = f.read() # read everything in the file
                 f.seek(0) # rewind
                 f.write("Steps=" + old) # write the new line before
         
        return (np.sum(myGrid.old_energy),)

    def mutUniformFloat(self, individual, lowerBound=0.0, upperBound=1.0, indpb=0.3):
       size = len(individual)
       for i in range(size):
           if random.random() < indpb:
               individual[i] = random.uniform(lowerBound, upperBound)
       return (individual)

    def main(self,):                 
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("attr_var", random.uniform, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_var, 25)
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
        while self.g < self.genrations:
            start = datetime.now()
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
            fitnesses = list(map(toolbox.evaluate, invalid_ind))
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit         
            print("  Evaluated %i individuals" % len(invalid_ind))         
            pop[:] = offspring         
            fits = [ind.fitness.values[0] for ind in pop]                 
            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("Duration:", datetime.now()-start)
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
