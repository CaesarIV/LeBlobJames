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
        

        self.Grid_size=(220,220)
        
        
        self.cells = []
        for row in range(0,self.Grid_size[0]):
            self.cells.append([])
            for col in range(0, self.Grid_size[1]):
                self.cells[row].append([])
                self.cells[row][col]=[0,0,0]
                  
        self.oldcells = copy.deepcopy(self.cells)
        self.neighbours =[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

        #random seed can be changed or commented
        random.seed(64)

        #Number of steps
        self.max_steps = 200

        #seeds
        self.cells[0][0]=[0,1,0]
        #self.cells[219][219]=[0,0,110]
        #self.cells[0][0]=[110,0,0]

        #mutation chance of each RGB value
        self.RGB_mut = 0.50

        #chance of decreasing the RGB value while mutating (else: increase) [tilt towards decrease]
        self.RGB_dec = 0.5

        #RGB change Percentage when mutating
        self.RGB_change = 0.05
        pass

        
    def creat(self,):

        save = True
        
        if save:
            Steps={}

        
        for step in range(0, self.max_steps):
            for row in range(0,self.Grid_size[0]):
                for col in range(0, self.Grid_size[1]):
                    if (self.oldcells[row][col][0]!=0 or \
                       self.oldcells[row][col][1]!=0 or \
                       self.oldcells[row][col][2]!=0):
                        neighbours = copy.deepcopy(self.neighbours)
                        random.shuffle(neighbours)
                        for neighbour in neighbours:
                            if (row+neighbour[0])>=0 and (row+neighbour[0])<self.Grid_size[0] and \
                               (col+neighbour[1])>=0 and (col+neighbour[1])<self.Grid_size[1]:
                                if self.oldcells[row+neighbour[0]][col+neighbour[1]][0] == 0 and \
                                   self.oldcells[row+neighbour[0]][col+neighbour[1]][1] == 0 and \
                                   self.oldcells[row+neighbour[0]][col+neighbour[1]][2] == 0:
                                    self.cells[row+neighbour[0]][col+neighbour[1]] = copy.deepcopy(self.oldcells[row][col])
                                    i=0
                                    for RGB_value in self.cells[row+neighbour[0]][col+neighbour[1]]:
                                        if random.uniform(0,1) <self.RGB_mut:
                                            if random.uniform(0,1) <=self.RGB_dec:
                                                RGB_value -= (255*self.RGB_change)
                                            else:
                                                RGB_value += (255*self.RGB_change)
                                        if RGB_value < 0:
                                            RGB_value = 0
                                        if RGB_value > 255:
                                            RGB_value = 255
                                        self.cells[row+neighbour[0]][col+neighbour[1]][i] = RGB_value 
                                        i+=1
                                    #print(self.cells[row+neighbour[0]][col+neighbour[1]])
                                    break
            self.oldcells = copy.deepcopy(self.cells)
            Steps[step] = copy.deepcopy(self.oldcells)
            
        if save:
            with open('rossSteps.js', 'w') as fp:
                json.dump(Steps, fp)

            with open("rossSteps.js", "r+") as f:
                 old = f.read() # read everything in the file
                 f.seek(0) # rewind
                 f.write("rossSteps=" + old) # write the new line before
                 
        pass


    def main(self,):
        self.creat()
        pass

if __name__ == "__main__":
    start = datetime.now()
    run = optmizer()
    run.main()
    print("Duration:", datetime.now()-start)
