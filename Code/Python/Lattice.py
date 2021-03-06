import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

class Lattice:

    def __init__(self, size):
        """Constructeur de la classe qui nécessite :
        -la taille de la lattice"""

        self.size = size 
        
        #Lattice, la dernière dimension corrspond aux deux angles costheta et phi
        self.latticeArray = np.zeros((size,size,size,2))
        #Liste des plus proches voisins
        self.neighboor = np.array([[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]])
        #Liste ordonné de manière random des sites de la lattice
        self.randomOrderSite = np.arange(size**3)

        ##Paramètre pour le paramètre d'ordre##
        self.orderMatrix = np.zeros((3,3))
        
    def randomOrientation(self):
        """Fonction qui renvoie une orientation aléatoire de la sphère unité
        Les orientations tirées au hasard sont uniformément répartis sur la demi-sphère
        unité supérieure
        http://mathworld.wolfram.com/SpherePointPicking.html
        """
        return np.array([2*np.random.rand(1)-1, 2*np.pi*np.random.rand(1)]).reshape(2)


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
            [2*np.random.rand(self.size,self.size,self.size)-1,
            2*np.pi*np.random.rand(self.size,self.size,self.size)]).T
  
    def nearRandomOrientation(self, oldAngle, dmax):
        """Fonction qui renvoie une orientation aléatoire de la sphère unité mais à une
        distance entre dmin et dmax de l'angle fourni en argument."""
        
        #On tire au hasard un deltaPhi et un deltacosTheta qui implique chacun au 
        #maximum une distance dmax de l'ancien angle
        deltaPhi = (2*random.random()-1)*np.pi*dmax
        deltaCosTheta = (2*random.random()-1)*dmax
            
            
        #on economise le temps de creation de l'array
        try:
            self.newAngle
        except AttributeError:
            self.newAngle = np.empty(2)

        self.newAngle[0] = (oldAngle[0] + deltaCosTheta-1)%2-1
        self.newAngle[1] = (oldAngle[1] + deltaPhi)%(2*np.pi)

        return self.newAngle

    def cosAngle(self, oldAngle, newAngle):
        """Fonction qui retourne le cosinus de la différence de 2 directions"""

        oldTheta = np.arccos(oldAngle[0])
        newTheta = np.arccos(newAngle[0])
        return np.abs(
            np.sin(oldTheta)*np.sin(newTheta)*np.cos(newAngle[1]-oldAngle[1])
            + oldAngle[0]*newAngle[0])

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

        #on créé directement un tuple
        l2, r = divmod(site,self.size**2)
        l1, l0 = divmod(r,self.size)
        return (l0,l1,l2)

    def fillOrderMatrix(self):
        """Fonction qui calcule la matrice du paramètre d'ordre"""

        latticeArrayXYZ = self.sphericalToCartesian(self.latticeArray.T).T
        
        self.orderMatrix[:,:] = np.sum(latticeArrayXYZ[:,:,:,:,None]
                *latticeArrayXYZ[:,:,:,None,:],
                axis=(0,1,2))

        self.orderMatrix = self.orderMatrix - np.eye(3)*self.size**3/3
   
    def updateOrderMatrix(self, oldAngle, newAngle):
        """Fonction qui update la matrice du paramètre d'ordre"""
        try:
            self.oldXYZ
            self.newXYZ
        except AttributeError:
            self.oldXYZ = np.empty(3)
            self.newXYZ = np.empty(3)

        self.oldXYZ[:] = self.sphericalToCartesian(oldAngle)
        self.newXYZ[:] = self.sphericalToCartesian(newAngle)
        self.orderMatrix[:,:] += (self.newXYZ[:,None]*self.newXYZ[None,:] 
                - self.oldXYZ[:,None]*self.oldXYZ[None,:])

    def orderParameter(self):
        """Fonction qui diagonalise la matrice d'ordre et renvoie le paramètre d'ordre
        """

        eigenValues = np.linalg.eigvalsh(self.orderMatrix)
        orderParameter = np.max(eigenValues)*3/2/self.size**3
        
        return(orderParameter)

    def sphericalToCartesian(self, angle):
        """Fonction qui transforme les coordonnées sphériques en cartesiennes"""
        #La pluspart du temps on traite un angle unique 
        #dans ce cas on économise la creation d'un array
        if angle.shape == (2,):
            try:
                self.XYZ
            except AttributeError:
                self.XYZ = np.empty(3)
            sin_theta = np.sin(np.arccos(angle[0]))
            self.XYZ[0] = sin_theta*np.cos(angle[1])
            self.XYZ[1] = sin_theta*np.sin(angle[1])
            self.XYZ[2] = angle[0]
            
            return self.XYZ

        else:
            theta = np.arccos(angle[0])
            return(np.array([
                np.sin(theta)*np.cos(angle[1]),
                np.sin(theta)*np.sin(angle[1]),
                angle[0]
                ]))

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
    test3D = Lattice(size=30)
    test3D.randomOrder()
    for i in range(1,27000):
        print(i)
        print(test3D.randomOrderSite[i])
        print(test3D.randomLocOrdered(i))
        print("\n")



