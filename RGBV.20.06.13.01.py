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
        random.seed(64)

        self.Grid_size=(220,220)
        self.max_steps = 20
        
        self.cells = []
        for row in range(0,self.Grid_size[0]):
            self.cells.append([])
            for col in range(0, self.Grid_size[1]):
                self.cells[row].append([])
                self.cells[row][col]=[0,0,0]
        self.cells[110][110]=[0,110,0]            
        self.oldcells = copy.deepcopy(self.cells)
        self.neighbours =[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        pass

        
    def creat(self,):

        save = True
        
        if save:
            Steps={}

        
        for step in range(0, self.max_steps):
            for row in range(0,self.Grid_size[0]):
                for col in range(0, self.Grid_size[1]):
                    if self.oldcells[row][col][0]!=0 or \
                       self.oldcells[row][col][1]!=0 or \
                       self.oldcells[row][col][2]!=0:
                        neighbours = copy.deepcopy(self.neighbours)
                        random.shuffle(neighbours)
                        for neighbour in neighbours:
                            if (row+neighbour[0])>=0 and (row+neighbour[0])<self.Grid_size[0] and \
                               (col+neighbour[1])>=0 and (col+neighbour[1])<self.Grid_size[1]:
                                if self.oldcells[row+neighbour[0]][col+neighbour[1]][0] == 0 and \
                                   self.oldcells[row+neighbour[0]][col+neighbour[1]][1] == 0 and \
                                   self.oldcells[row+neighbour[0]][col+neighbour[1]][2] == 0:
                                    self.cells[row+neighbour[0]][col+neighbour[1]] = copy.deepcopy(self.oldcells[row][col])
                                    for RGB_value in self.cells[row+neighbour[0]][col+neighbour[1]]:
                                        if random.uniform(0,1) <0.05:
                                            if random.uniform(0,1) <=0.5:
                                                RGB_value -= (225*0.05)
                                            else:
                                                RGB_value += (225*0.05)
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
