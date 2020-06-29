from deap import base
from deap import creator
from deap import tools
import copy
import numpy as np
import random
import json

class optmizer():

    def __init__(self,):
        self.genrations = 19
        self.population_size = 300
        self.CXPB = 0.4 
        self.MUTPB = 0.2
        self.g = 0
        random.seed(64)
        pass

    class Grid():
        def __init__ (self,):
            self.size=(24,24)
            self.max_steps = 35
            
            self.cells_old=[]
            self.chem_old=[]
            self.cells_new=[]
            self.chem_new=[]
            self.neighbours =[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
            for row in range(0, self.size[0]):
                self.cells_old.append([])
                self.chem_old.append([])                
                for col in range(0,self.size[1]):
                    self.cells_old[row].append(0)
                    self.chem_old[row].append([]) 
                    for chem in range(0,3):
                        self.chem_old[row][col].append(0)
            #seed
            self.cells_old[10][10] = 1
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
        score = 0
        Grow = self.logistic_function(individual[0:8])
        Die = self.logistic_function(individual[8:16])
        Grid = self.Grid()
        Grid.cells_new = copy.deepcopy(Grid.cells_old)
        Grid.chem_new = copy.deepcopy(Grid.chem_old)

        squaredError=[]

        
        Steps = {}
        Steps[0] = Grid.cells_old

         
        for step in range(1, Grid.max_steps):
            for row in range(0, Grid.size[0]):
                for col in range(0, Grid.size[1]):

                    #Chemicals
                    for chem in range(0,3):
                        #Chem evaporation
                        Grid.chem_new[row][col][chem] = 0.5* Grid.chem_old[row][col][chem]
                        #Chem diffusion
                        for j in range(-1,2):
                            for k in range(-1,2):
                                if (row+j >= 0) and (row+j < Grid.size[0]) and (col+k >= 0) and (col+k < Grid.size[1]):
                                    Grid.chem_new[row][col][chem]+=(1.0/16.0) * Grid.chem_old[row+j][col+k][chem]
                        #Chem production
                        if Grid.cells_old[row][col] == 1:
                            if self.target[row,col] == 1:
                                Grid.chem_new[row][col][chem]+=individual[16+chem]
                            else:
                                Grid.chem_new[row][col][chem]+=individual[19+chem]

                    #Growth And Death
                    #Growth is relative to other life .. life needs neighbours/relatives    
                    if Grid.cells_old[row][col] == 1:
                        neighbours = copy.deepcopy(Grid.neighbours)
                        random.shuffle(neighbours)
                        for neighbour in neighbours:
                            j = neighbour[0]
                            k = neighbour[1]
                            if (row+j >= 0) and (row+j < Grid.size[0]) and (col+k >= 0) and \
                               (col+k < Grid.size[1]) and Grid.cells_old[row+j][col+k] == 0 and Grid.cells_new[row+j][col+k] == 0:
                                if  Grow.check(Grid.chem_new[row+j][col+k]) == 1:
                                    Grid.cells_new[row+j][col+k] = 1
                                break
                    #Death is absolute
                    if Die.check(Grid.chem_new[row][col]) == 1:
                        Grid.cells_new[row][col] = 0
                            
                    #Scoring Prep
                    if step > (Grid.max_steps-5):
                        if Grid.cells_old[row][col] == 1:
                            if self.target[row,col] == 1:
                                score += 1
                            else:
                                score -= 1

            Grid.chem_old = copy.deepcopy(Grid.chem_new)
            Grid.cells_old = copy.deepcopy(Grid.cells_new)
            Steps[step] = Grid.cells_old
                        
        with open('Steps.js', 'w') as fp:
            json.dump(Steps, fp)

        with open("Steps.js", "r+") as f:
             old = f.read() # read everything in the file
             f.seek(0) # rewind
             f.write("Steps=" + old) # write the new line before
                 
        return (score),

    def main(self,):
        
        self.target = np.genfromtxt("Target2.csv",delimiter=',',dtype=int)
        with open('target.js', 'w') as fp:
            json.dump(self.target.tolist(), fp)
            
        with open("target.js", "r+") as f:
             old = f.read() # read everything in the file
             f.seek(0) # rewind
             f.write("target=" + old) # write the new line before

        self.target=np.reshape(self.target,(24,24))
       

        self.best_ind = np.load("Best_Ind.npy")

        print(self.best_ind)
    
        self.evaluation(self.best_ind)
        
        pass

if __name__ == "__main__":
    run = optmizer()
    run.main()
