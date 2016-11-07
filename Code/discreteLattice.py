from lattice import lattice
from random import randint
import numpy as np

class discreteLattice(lattice):

    def __init__(self, size, dim, angleSize):
        """Constructeur de la classe qui  hérite de lattice :
        -construit un objet lattice a partir de size et dim
        -le nombre d'orientations autorisées pour un site"""

        lattice.__init__(self, size, dim)
        self.angleSize = angleSize

    def randomOrientation(self):
        """Fonction qui renvoie une orientation aléatoire parmis celles autorisées."""
        #sans les if:
        #return (np.pi/self.angleSize*
        #    np.random.randint(self.angleSize,size=self.dim-1))
        
        if self.dim==2 :
            return (np.pi/self.angleSize*
                np.random.randint(self.angleSize))
        elif self.dim==3 :
            return (np.pi/self.angleSize*
                np.random.randint(self.angleSize,size=2))

    def changeOrientation(self, loc, angle):
        """Fonction qui change l'orientation d'un site a une nouvelle valeur angle."""
        # apparament ya juste besoin de faire :
        #self.latticeArray[tuple(loc)] = angle
        #du coup la fonction est dispensable
        
        if dim==2 :
            self.latticeArray[loc[0],loc[1]] = angle
        elif dim==3 :
            self.latticeArray[loc[0],loc[1],loc[2]] = angle

        
if __name__ == '__main__':

    print('test 2D')
    test = discreteLattice(size=2,dim=2,angleSize=4)
    print(test.randomOrientation())
    test.randomConfiguration()

    print('test 3D')
    test = discreteLattice(size=2,dim=3,angleSize=4)
    print(test.randomOrientation())
    test.randomConfiguration()

