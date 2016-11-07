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

        if dim==2 :
            # dans le cas 2d les angles possibles sont les multiples de pi/angleSize
            self.possibleAngle=np.pi/self.angleSize*np.arange(self.angleSize)

        elif dim==3 :
            # dans le cas 3d les angles sont ceux prédéfinis
            if angleSize==3 :
                self.possibleAngle=np.array([[0,0],[0,np.pi/2],[np.pi/2,np.pi/2]])
            else :
                print('Not implemented yet')

    def randomOrientation(self):
        """Fonction qui renvoie une orientation aléatoire parmis celles autorisées."""
        
        return (self.possibleAngle[np.random.randint(self.angleSize)])


    def changeOrientation(self, loc, angle):
        """Fonction qui change l'orientation d'un site a une nouvelle valeur angle."""
        
        if dim==2 :
            self.latticeArray[loc[0],loc[1]] = angle
        elif dim==3 :
            self.latticeArray[loc[0],loc[1],loc[2]] = angle

        
if __name__ == '__main__':

    print('test 2D')
    test = discreteLattice(size=2,dim=2,angleSize=3)
    print(test.randomOrientation())


    print('test 3D')
    test = discreteLattice(size=2,dim=3,angleSize=3)
    print(test.randomOrientation())


