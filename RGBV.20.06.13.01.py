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
        pass

    def creation_function(self, n):
        return(255*np.sin(n))
        pass

        
    def creat(self,):
        Grid_size=(24,24)
        max_steps = 20
        save = True
        
        if save:
            Steps={}
        n = 1
        for step in range(0, max_steps):
            image = []
            for row in range(0,Grid_size[0]):
                image.append([])
                for col in range(0, Grid_size[1]):
                    image[row].append([])
                    for RGB in range(0, 3):
                        n = n * 1.0009
                        image[row][col].append(self.creation_function(n))
                        
            
            Steps[step] = image
            
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