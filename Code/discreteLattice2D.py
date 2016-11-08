import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

class discreteLattice2D:

    def __init__(self, size, angleSize):
        """Constructeur de la cl asse qui initialise :
        -la taille de la lattice dans une dimension
        -le nombre de dimension 
        -la lattice"""

        self.size = size
        self.angleSize = angleSize
        self.latticeArray=np.zeros((size,size))
        self.neighboor=np.array([[0,1],[0,-1],[1,0],[-1,0]])

    def randomOrientation(self):
        """Fonction qui renvoie une orientation aléatoire parmis celles autorisées."""

        return (np.pi/self.angleSize*np.random.randint(self.angleSize))

    def randomConfiguration(self):
        """Function qui initialise une configuration aléatoire"""

        self.latticeArray=np.pi/self.angleSize*np.random.randint(self.angleSize, size=(self.size,self.size))

    def nearestNeighboor(self, loc):
        """Fonction qui retourne les coordonnées des plus proches voisins d'un site donné
        en prenant en prenant en compte les conditions aux limites périodiques"""

        return self.periodicLoc(self.neighboor+loc)

    def nearestNeighboorAngle(self, loc):
        """Fonction qui retourne les valeurs des angles des voisins d'un site donné """

        return self.latticeArray[tuple(self.nearestNeighboor(loc).transpose())] 

    def periodicLoc(self, loc):
        """Fonction qui retourne les coordonnées periodisées."""

        return loc%self.size

    def randomLoc(self):
        """Fonction qui renvoie un site aléatoire de la lattice"""
        return np.random.randint(self.size, size=2) 

    def display(self):
        """Fonction qui permet d'afficher une image de la lattice"""
        angle=self.latticeArray[:,:]

        x,y=np.indices(angle.shape)[[0,1]]
        # on prend -arr a cause de l'inversion finale de l'axe y
        params = zip(x.ravel(),y.ravel(),(-angle*180/np.pi).ravel())

        # angle en degrées ici
        ells = [Ellipse(xy=(x,y), width=0.95, height=0.2, angle=a,facecolor='#6495ED') 
            for x,y,a in params ]

        fig = plt.figure(0)
        ax = fig.add_subplot(111, aspect='equal')
        for e in ells:
                ax.add_artist(e)

        ax.set_xlim(-1,angle.shape[0])
        ax.set_ylim(-1,angle.shape[1])
        plt.show()


if __name__ == '__main__':
   
    print('test display 2D')
    test2D = discreteLattice2D(size=3,angleSize=5)
    test2D.randomConfiguration()
    print(test2D.nearestNeighboor([0,0]))
    print(test2D.latticeArray)
    test2D.display()




