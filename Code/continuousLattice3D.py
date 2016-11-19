import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

class continuousLattice3D:

    def __init__(self, size):
        """Constructeur de la classe qui nécessite :
        -la taille de la lattice"""

        self.size = size 
        
        #Lattice, la dernière dimension corrspond aux deux angles theta et phi
        self.latticeArray = np.zeros((size,size,size,2))
        #Liste des plus proches voisins
        self.neighboor = np.array([[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]])
        #Liste ordonné de manière random des sites de la lattice
        self.randomOrderSite = np.arange(size**3)

    def randomOrientation(self):
        """Fonction qui renvoie une orientation aléatoire de la sphère unité
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure
        http://mathworld.wolfram.com/SpherePointPicking.html
        """
        return np.array([np.arccos(np.random.rand(1)),2*np.pi*np.random.rand(1)]).reshape(2)

    def groundstateConfiguration(self):
        """Function qui initialise/reset la lattice dans l'état fondamental"""
        
        self.latticeArray=np.zeros((self.size,self.size,self.size,2))

    def randomConfiguration(self):
        """Function qui initialise/reset la lattice dans un état random
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure
        http://mathworld.wolfram.com/SpherePointPicking.html
        """
        
        self.latticeArray = np.array(
            [np.arccos(np.random.rand(self.size,self.size,self.size)),
            2*np.pi*np.random.rand(self.size,self.size,self.size)]).T
  
    def nearRandomOrientation(self, oldAngle, dmin, dmax):
        """Fonction qui renvoie une orientation aléatoire de la sphère unité mais à une distance entre dmin et dmax de l'angle fourni en argument."""
        

        alpha = 0 #Angle avec l'ancien angle
        while alpha/(np.pi/2)<=dmin or alpha/(np.pi/2)>=dmax :

            #On tire au hasard un deltaPhi et un deltacosTheta qui implique chacun au 
            #maximum une distance dmax de l'ancien angle
            deltaPhi = (np.random.rand(1)*2-1)*np.pi/2*dmax
            deltaCosTheta = (np.random.rand(1)*2-1)*(
                np.cos(np.pi/2*dmax+oldAngle[0])-np.cos(oldAngle[0]))
            
            #Si tout se passe bien
            if 1>=np.cos(oldAngle[0]) + deltaCosTheta>=0 :
                newAngle = np.array(
                [np.arccos(np.cos(oldAngle[0])+deltaCosTheta), oldAngle[1] + deltaPhi])
            #Si le cosinus est supérieur à 1
            elif np.cos(oldAngle[0]) + deltaCosTheta>1 :
                newAngle = np.array(
                [np.arccos(2-(np.cos(oldAngle[0])+deltaCosTheta)), (oldAngle[1] + deltaPhi + np.pi)%(2*np.pi)])
            #Si il est inférieur à 0 (pour rester dans la demi sphère supérieure)
            elif np.cos(oldAngle[0]) + deltaCosTheta<0 :
                newAngle = np.array(
                [np.arccos(-(np.cos(oldAngle[0])+deltaCosTheta)), (oldAngle[1] + deltaPhi + np.pi)%(2*np.pi)])

            alpha = np.arccos(self.cosAngle(oldAngle,newAngle))

        return newAngle.reshape(2)

    def cosAngle(self, oldAngle, newAngle):
        """Fonction qui retourne le cosinus de la différence de 2 directions"""

        return abs(
            np.sin(oldAngle[0])*np.sin(newAngle[0])*np.cos(newAngle[1]-oldAngle[1])
            + np.cos(oldAngle[0])*np.cos(newAngle[0]))

    def nearestNeighboorAngle(self, loc):
        """Fonction qui retourne les valeurs des angles des voisins d'un site donné """

        return self.latticeArray[tuple(self.nearestNeighboor(loc).T)]

    def nearestNeighboor(self, loc):
        """Fonction qui retourne les coordonnées des plus proches voisins d'un site 
        donné en prenant en prenant en compte les conditions aux limites périodiques"""

        return self.periodicLoc(self.neighboor+loc)

    def periodicLoc(self, loc):
        """Fonction qui retourne les coordonnées periodisées."""

        return loc%self.size

    def randomLoc(self):
        """Fonction qui renvoie un site aléatoire de la lattice"""
        return np.random.randint(self.size, size=3)

    def randomOrder(self):
        """Fonction qui rend la liste des sites de la lattice de manière random"""
        np.random.shuffle(self.randomOrderSite)

    def randomLocOrdered(self, i):
        """Fonction qui renvoie le site correspondant au numéro donné"""
        site = self.randomOrderSite[i]
        loc = np.zeros(3)
        loc[0] = site%self.size
        loc[1]= (site - loc[0])/self.size %self.size
        loc[2]= (site - self.size*loc[1]- loc[0])/self.size**2 %self.size
        return(loc.astype(int))

    def display(self):
        """Fonction qui permet d'afficher une image de la lattice"""

        angle=self.latticeArray[:,:,:,1]

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

    print('test display 3D')
    test3D = continuousLattice3D(size=30)
    test3D.randomOrder()
    for i in range(1,27000):
        print(i)
        print(test3D.randomOrderSite[i])
        print(test3D.randomLocOrdered(i))
        print("\n")



