from continuousLattice3D import continuousLattice3D
import numpy as np

import matplotlib.pyplot as plt

class latticeMC3Dcontinuous:

    def __init__(self, size, sample, meanSample, energieRatio, start):
        """Constructeur de la classe qui nécessite :
        - la taille de la lattice
        - le nombre de cycle réalisé
        un cycle correspond à une série de size**3 changement (1 sur chaque site)
        - le nombre de sample sur lequel on calcule la moyenne (en nombre de cycle)
        - la température qui intervient par enegieratio = kbT/epsilon
        - l'information si on part d'une configuration random ou de l'état fondamental
        """

        self.size = size                    
        self.sample = sample
        self.meanSample = meanSample
        self.energieRatio = energieRatio
        self.lattice = continuousLattice3D(self.size)


        #Energies au step i
        self.energies = np.zeros(sample*self.size**3)
        #Energie de l'état fondamentale utilisé pour plot les énergies toujours 
        #par rapport à la même référence
        self.minEnergy = -3*size**3
        #Absicess en termes de nombre de cycle pour les graphes
        self.cycles = np.arange(sample*self.size**3)/self.size**3

        #1 si le step i accepté, 0 sinon
        self.accepted = np.zeros(sample*self.size**3)
        self.acceptedSample = 10    #Variables pour des test sur les variations imposées à l'angle
        self.dmaxArray = np.zeros(sample*self.size**3)


        #Initialise une configuration aléatoire pour la lattice et pour dmin/dmax
        if start == 'random' :
            self.lattice.randomConfiguration()
            self.dmax = 1
        elif start == 'groundstate' :
            self.lattice.groundstateConfiguration()
            self.dmax = 0.01


    def runMC(self):
        """Fonction qui lance une simulation Monte-Carlo"""

        for cycle in range(self.sample) :

            self.lattice.randomOrder()
            print(cycle)

            for s in range(self.size**3) : 
                self.moveMC(cycle,s)

                i = cycle*self.size**3 + s

                #On adapte l'amplitude de variation des angles 
                if(i>=self.acceptedSample) :
                    stat = sum(
                        self.accepted[i-self.acceptedSample:i])/self.acceptedSample
                else :  
                    stat = sum(self.accepted[0:i])/(i+1)

                self.dmax = max(
                    0.005, min(1, self.dmax + (stat - 1/2)/10000))
                self.dmaxArray[i] = self.dmax

        #Plot de test qui deviendra inutile ensuite
        plt.plot(self.cycles,self.dmaxArray)
        plt.title('dmax')
        plt.show()

    def moveMC(self, cycle, s):

        i = cycle*self.size**3 + s
        #On prends un site et un angle au hasard
        randomLoc = self.lattice.randomLocOrdered(s)

        #On choisit un nouvel angle presque au hasard
        newAngle = self.lattice.nearRandomOrientation(
            self.lattice.latticeArray[tuple(randomLoc)], self.dmax)

        #On calcule la variation d'énergie
        energieVariation = self.energieVariation(newAngle, randomLoc)
            
        #On calcule la probabilité que le pas soit accepté
        acceptanceProbability = min(1,self.boltzmannFactor(energieVariation))

        #On teste cette proba
        if np.random.rand(1)<acceptanceProbability :
            self.lattice.latticeArray[tuple(randomLoc)] = newAngle
            self.accepted[i] = 1
        else :
            energieVariation = 0

        #On update les tableaux de résultats
        if i==0 :
            self.energies[0] = self.energie()
        else :
            self.energies[i] = self.energies[i-1] + energieVariation

    def energie(self):
        """Fonction qui renvoie l'énergie de la configuration actuelle"""
        
        arr = self.lattice.latticeArray.T

        totEnergy = (
             (1-3*self.lattice.cosAngle(arr,np.roll(arr, 1,axis=1))**2)/2
            +(1-3*self.lattice.cosAngle(arr,np.roll(arr,-1,axis=1))**2)/2
            +(1-3*self.lattice.cosAngle(arr,np.roll(arr, 1,axis=2))**2)/2
            +(1-3*self.lattice.cosAngle(arr,np.roll(arr,-1,axis=2))**2)/2
            +(1-3*self.lattice.cosAngle(arr,np.roll(arr, 1,axis=3))**2)/2
            +(1-3*self.lattice.cosAngle(arr,np.roll(arr,-1,axis=3))**2)/2
            ).sum()/2

        return totEnergy

    def energieVariation(self, newAngle, loc):
        """Fonction qui renvoie la variation d'énergie associée au changement du site
        loc de la lattice vers newAngle. La fonction ne calcule que les variations 
        locales pour gagner du temps"""

        #Valeurs des angles des voisins
        nNA=self.lattice.nearestNeighboorAngle(loc)

        oldEnergy = (
            1-3*self.lattice.cosAngle(nNA.T,self.lattice.latticeArray[tuple(loc)])**2
            ).sum()/2

        newEnergy = (
            1-3*self.lattice.cosAngle(nNA.T,newAngle)**2
            ).sum()/2

        return(newEnergy-oldEnergy)

    def boltzmannFactor(self, energie):
        """Fonction qui calcule le poid de Boltzmann d'une energie"""

        return(np.exp(-energie/self.energieRatio))

    def meanEnergy(self):
        """Fonction qui renvoie l'énergie moyenne sur les meanSample derniers sample"""
        return((np.mean(self.energies[-self.meanSample*self.size**3:])-self.minEnergy)/self.size**3)


    def displayEnergies(self):
        """Fonction qui affiche l'évolution de l'énergie"""

        plt.plot(self.cycles,(self.energies-self.minEnergy)/self.size**3)
        plt.title('Energie par site en unité de epsilon')
        plt.show()


if __name__ == '__main__':

    print('Test 3D')
    test3D = latticeMC3Dcontinuous(30,100,100,0.01,'groundstate')
    test3D.runMC()    
    test3D.displayEnergies()
    test3D.lattice.display()
    print(sum(test3D.accepted)/(test3D.sample*test3D.size**3))
