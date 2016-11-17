import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

class continuousLattice3D:

    def __init__(self, size):
        """Constructeur de la cl asse qui initialise :
        -la taille de la lattice dans une dimension
        -le nombre de dimension 
        -la lattice"""

        self.size = size
        self.latticeArray=np.zeros((size,size,size,2))
        self.neighboor=np.array([[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]])

    def randomOrientation(self):
        """Fonction qui renvoie une orientation aléatoire de la sphère unité
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure
        http://mathworld.wolfram.com/SpherePointPicking.html
        """
        return np.array([np.arccos(np.random.rand(1)),2*np.pi*np.random.rand(1)]).reshape(2)

    def groundstateConfiguration(self):
        """Function qui initialise une configuration dans l'état fondamental"""
        
        self.latticeArray=np.zeros((self.size,self.size,self.size,2))

    def randomConfiguration(self):
        """Function qui initialise une configuration aléatoire
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure
        http://mathworld.wolfram.com/SpherePointPicking.html
        """
        
        self.latticeArray = np.array(
            [np.arccos(np.random.rand(self.size,self.size,self.size)),
            2*np.pi*np.random.rand(self.size,self.size,self.size)]).T
  
    def nearRandomOrientation(self, oldAngle, dmin, dmax):
        """Fonction qui renvoie une orientation aléatoire de la sphère unité
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure
        http://mathworld.wolfram.com/SpherePointPicking.html
        """
        alpha = 0
        counter = 0
        while alpha<=dmin*np.pi/2 or alpha>=dmax*np.pi/2 :
            counter += 1
            newAngle = np.array(
                [np.arccos(np.random.rand(1)),2*np.pi*np.random.rand(1)])
            alpha = np.arccos(self.cosAngle(oldAngle,newAngle))

        print(counter)
        print(newAngle.reshape(2))
        return newAngle.reshape(2)

    def newNearRandomOrientation(self, oldAngle, dmin, dmax):
        """Fonction qui renvoie une orientation aléatoire de la sphère unité
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure
        http://mathworld.wolfram.com/SpherePointPicking.html
        """
        alpha = 0
        counter = 0
        while alpha<=dmin*np.pi/2 or alpha>=dmax*np.pi/2 :
            counter+=1
            
            #On tire au hasard un deltaPhi et un deltacosTheta à la distance 
            #que l'on veut
            deltaPhi = 2*np.pi*np.random.rand(1)*dmax
            deltaCosTheta = np.random.rand(1)*dmax
            
            #On gère le cas ou on sort de [0,1] pour un cosinus...
            #et on stocke le nouvel angle
            if 1>=np.cos(oldAngle[0]) + deltaCosTheta>=0 :
                newAngle = np.array(
                [np.arccos(np.cos(oldAngle[0])+deltaCosTheta), oldAngle[1] + deltaPhi])
            
            elif np.cos(oldAngle[0]) + deltaCosTheta>1 :
                newAngle = np.array(
                [np.arccos(2-(np.cos(oldAngle[0])+deltaCosTheta)), (oldAngle[1] + deltaPhi + np.pi)%(2*np.pi)])

            elif np.cos(oldAngle[0]) + deltaCosTheta<0 :
                newAngle = np.array(
                [np.arccos(-(np.cos(oldAngle[0])+deltaCosTheta)), (oldAngle[1] + deltaPhi + np.pi)%(2*np.pi)])

            alpha = np.arccos(self.cosAngle(oldAngle,newAngle))
        print(counter)
        print(newAngle.reshape(2))

        return newAngle.reshape(2)

    def cosAngle(self, oldAngle, newAngle):

        return abs(
            np.sin(oldAngle[1])*np.sin(newAngle[1])*np.cos(newAngle[0]-oldAngle[0])
            + np.cos(oldAngle[1])*np.cos(newAngle[1]))


    def nearestNeighboor(self, loc):
        """Fonction qui retourne les coordonnées des plus proches voisins d'un site donné
        en prenant en prenant en compte les conditions aux limites périodiques"""

        return self.periodicLoc(self.neighboor+loc)

    def nearestNeighboorAngle(self, loc):
        """Fonction qui retourne les valeurs des angles des voisins d'un site donné """

        return self.latticeArray[tuple(self.nearestNeighboor(loc).T)] 

    def periodicLoc(self, loc):
        """Fonction qui retourne les coordonnées periodisées."""

        return loc%self.size

    def randomLoc(self):
        """Fonction qui renvoie un site aléatoire de la lattice"""
        return np.random.randint(self.size, size=3)

    def display(self):
        """Fonction qui permet d'afficher une image de la lattice"""

        angle=self.latticeArray[:,:,:,0]

        x,y=np.indices(angle.shape)[[0,1]]
        # on prend -angle a cause de l'inversion finale de l'axe y
        params = zip(x.ravel(),y.ravel(),(-angle*180/np.pi).ravel())

        # angle en degrées ici
        ells = [Ellipse(xy=(x,y), width=0.6, height=0.1, angle=a,facecolor='#6495ED') for x,y,a in params ]

        fig = plt.figure(0)
        ax = fig.add_subplot(111, aspect='equal')
        for e in ells:
                ax.add_artist(e)

        ax.set_xlim(-1,angle.shape[0])
        ax.set_ylim(-1,angle.shape[1])
        plt.show()


if __name__ == '__main__':
    #tout ce qui est ici n'est exécuté que si ce script est exécuté 
    #directement (via "python3 lattice.py" par ex)  


    print('test display 3D')
    test3D = continuousLattice3D(size=5)
    test3D.randomConfiguration()
    for i in range(1,10000):
        print(i)
        test3D.newNearRandomOrientation(test3D.randomOrientation(),0,0.005)
        test3D.nearRandomOrientation(test3D.randomOrientation(),0,0.005)
        print("\n")



