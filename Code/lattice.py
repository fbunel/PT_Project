import numpy as np
import matplotlib.pyplot as plt
from random import randint

class lattice:

    def __init__(self, size, dim):
        """Constructeur de la classe qui initialise :
        -la taille de la lattice dans une dimension
        -le nombre de dimension 
        -la lattice"""

        self.size = size
        self.dim = dim
        
        if dim==2 :
            self.latticeArray=np.zeros((size,size),np.ndarray)
            self.neighboor=np.array([[0,1],[0,-1],[1,0],[-1,0]])
        elif dim==3 :
            self.latticeArray=np.zeros((size,size,size),np.ndarray)
            self.neighboor=np.array([[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]])

    def randomConfiguration(self):
        """Function qui initialise une configuration aléatoire"""

        for loc in np.nditer(self.latticeArray, op_flags=['writeonly']):
            loc[...]=randomOrientation()

    def display(self):
        """Fonction qui permet d'afficher une image de la lattice"""

    def nearestNeighboor(self, loc):
        """Fonction qui retourne les coordonnées des plus proches voisins d'un site donné
        en prenant en prenant en compte les conditions aux limites périodiques"""

        return periodicLoc(self.neighboor+loc)

    def periodicLoc(self, loc):
        """Fonction qui retourne les coordonnées periodisées."""
        return loc%self.dim

    def randomLoc(self):
        """Fonction qui renvoie un site aléatoire de la lattice"""
        return randint(self.size,size=2) 



