import numpy as np


class Grid():

    def __init__(self):
        self.max_steps = 35
        self.X_size = 24
        self.Y_size = 24
        
        self.neighbours = [ (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1) ]
        self.locations = []
        for row in range(0, self.X_size): 
            for col in range(0, self.Y_size):
                self.locations.append((row,col))
        self.reset()
        pass
        


    def reset(self,):
        #old
        self.old_cells = np.zeros((self.X_size, self.Y_size))
        self.old_energy = np.zeros((self.X_size, self.Y_size))
        self.old_chemical_0 = np.zeros((self.X_size, self.Y_size))
        self.old_chemical_1 = np.zeros((self.X_size, self.Y_size))
        self.old_chemical_2 = np.zeros((self.X_size, self.Y_size))

        #seed
        self.old_cells[10][10] = 1
        self.old_energy[10][10] = 1

        #new
        self.new_cells = np.zeros((self.X_size, self.Y_size))
        self.new_energy = np.zeros((self.X_size, self.Y_size))
        self.new_chemical_0 = np.zeros((self.X_size, self.Y_size))
        self.new_chemical_1 = np.zeros((self.X_size, self.Y_size))
        self.new_chemical_2 = np.zeros((self.X_size, self.Y_size))
        pass
