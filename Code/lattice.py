import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from random import randint

class lattice:

    def __init__(self, size, dim):
        """Constructeur de la cl asse qui initialise :
        -la taille de la lattice dans une dimension
        -le nombre de dimension 
        -la lattice"""

        self.size = size
        self.dim = dim
        
        if dim==2 :
            # dans le cas 2d on a deux dimensions d'espace et 1 angle
            self.latticeArray=np.zeros((size,size,1))
            self.neighboor=np.array([[0,1],[0,-1],[1,0],[-1,0]])
        elif dim==3 :
            # dans le cas 3d on a trois dimensions d'espace et 2 angles
            self.latticeArray=np.zeros((size,size,size,2))
            self.neighboor=np.array([[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]])

    def randomConfiguration(self):
        """Function qui initialise une configuration aléatoire"""

        # de manière generale avec numpy il faut à tout prix éviter 
        # les boucles for pour itérer sur un array
        #for loc in np.nditer(self.latticeArray, op_flags=['writeonly']):
        #    loc[...]=self.randomOrientation()

        # exemple de la "bonne manière" d'assigner des valeurs 
        # aléatoire entre 0 et Pi :
        self.latticeArray = np.random.rand(*self.latticeArray.shape)*np.pi


    def display(self):
        """Fonction qui permet d'afficher une image de la lattice"""
        if self.dim == 2:
            arr=self.latticeArray[:,:,0]

        if self.dim == 3:
            arr=self.latticeArray[:,:,:,0]

        x,y=np.indices(arr.shape)[[0,1]]
        # on prend -arr a cause de l'inversion finale de l'axe y
        params = zip(x.ravel(),y.ravel(),(-arr).ravel())

        # angle en degrées ici
        ells = [Ellipse(xy=(x,y), width=0.6, height=0.1, angle=a,facecolor='#6495ED') for x,y,a in params ]

        fig = plt.figure(0)
        ax = fig.add_subplot(111, aspect='equal')
        for e in ells:
                ax.add_artist(e)

        ax.set_xlim(-1,arr.shape[0])
        ax.set_ylim(-1,arr.shape[1])
        plt.show()

    def nearestNeighboor(self, loc):
        """Fonction qui retourne les coordonnées des plus proches voisins d'un site donné
        en prenant en prenant en compte les conditions aux limites périodiques"""

        return periodicLoc(self.neighboor+loc)

    def periodicLoc(self, loc):
        """Fonction qui retourne les coordonnées periodisées."""
        return loc%self.dim

    def randomLoc(self):
        """Fonction qui renvoie un site aléatoire de la lattice"""
        return randint(self.size,size=self.dim) 


if __name__ == '__main__':
    #tout ce qui est ici n'est exécuté que si ce script est exécuté 
    #directement (via "python3 lattice.py" par ex)  

    
    print('test display 2D')
    test2D = lattice(size=2,dim=2)
    test2D.latticeArray = np.random.rand(*test2D.latticeArray.shape)*360
    print(test2D.latticeArray[:,:,0])
    test2D.display()

    print('test display 3D')
    test3D = lattice(size=2,dim=3)
    test3D.latticeArray = np.random.rand(*test3D.latticeArray.shape)*360
    print(test3D.latticeArray[:,:,:,0])
    test3D.display()



