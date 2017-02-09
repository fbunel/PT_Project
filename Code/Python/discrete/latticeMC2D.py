import numpy as np
import matplotlib.pyplot as plt
from discreteLattice2D import discreteLattice2D

class latticeMC2D:

    def __init__(self, size, angleSize, sample, meanSample, energieRatio):
        """Constructeu r de la classe qui initialise :
        - la lattice à l'aide de size et anglesize
        - sample le nombre de Monte-Carlo step que l'on veut faire 
        - energieRatio qui est kbT/epsilon"""

        self.size = size
        self.angleSize = angleSize
        self.discreteLattice2D = discreteLattice2D(self.size, self.angleSize)
        self.sample = sample
        self.meanSample = meanSample
        self.energieRatio = energieRatio


        self.accepted = np.zeros(sample)
        self.energies = np.zeros(sample)
        self.energiesForMean = np.zeros(meanSample)
        self.boltzmannFactors = np.zeros(meanSample)
        self.partitionFunction = 0
        self.minEnergy = -2*size**2
        self.referenceEnergy = 0 

    def runMC(self):
        """Fonction qui lance une simulation Monte-Carlo"""

        #Initialise une configuration aléatoire pour la lattice
        #self.discreteLattice2D.randomConfiguration()

        for i in range(self.sample) :

            #On prends un site et un angle au hasard
            randomLoc = self.discreteLattice2D.randomLoc()

            newAngle = self.discreteLattice2D.latticeArray[tuple(randomLoc)]
            while newAngle==self.discreteLattice2D.latticeArray[tuple(randomLoc)]:
                newAngle = self.discreteLattice2D.randomOrientation()

            #On calcule la variation d'énergie
            energieVariation = self.energieVariation(newAngle, randomLoc)
            
            #On calcule la probabilité que le pas soit accepté
            acceptanceProbability = min(1,self.boltzmannFactor(energieVariation))

            #On teste cette proba
            if np.random.rand(1)<acceptanceProbability :
                self.discreteLattice2D.latticeArray[tuple(randomLoc)] = newAngle
                self.accepted[i] = 1
            else :
                energieVariation = 0

            #On update les tableaux de résultats
            if i==0 :
                #On déplace tout le spectre d'energie pour veiter les divergences
                self.energies[0] = self.energie()
            else :
                self.energies[i] = self.energies[i-1] + energieVariation

            print(self.energies-self.minEnergy)

    def postMC(self):

        #Les facteurs de Boltzmanns et la fonction de partition sont calculés avec un
        #spectre d'énergie décalé par l'énergie minimale observée
        self.energiesForMean = self.energies[-self.meanSample:]
        self.referenceEnergy = min(self.energiesForMean)
        self.boltzmannFactors = self.boltzmannFactor(
            self.energiesForMean - self.referenceEnergy)
        self.partitionFunction = sum(self.boltzmannFactors)

        """
        print("Fonction de partition")
        print(self.partitionFunction)
        print("Energies")
        print(self.energies)
        print("Poids de Boltzmann")
        print(self.boltzmannFactors)
        """

    def energie(self):
        """Fonction qui renvoie l'énergie de la configuration actuelle"""
        arr = self.discreteLattice2D.latticeArray
        
        totEnergy = (
             (1-3*np.cos(arr - np.roll(arr, 1,axis=0))**2)/2
            +(1-3*np.cos(arr - np.roll(arr,-1,axis=0))**2)/2
            +(1-3*np.cos(arr - np.roll(arr, 1,axis=1))**2)/2
            +(1-3*np.cos(arr - np.roll(arr,-1,axis=1))**2)/2
            ).sum()/2

        return totEnergy

    def energieVariation(self, newAngle, loc):
        """Fonction qui ren voie la variation d'énergie associée
         au changement d'un spin"""

        nNA=self.discreteLattice2D.nearestNeighboorAngle(loc)
       
        oldEnergy = ((1-3*np.cos(
                nNA-self.discreteLattice2D.latticeArray[tuple(loc)])
                **2)/2).sum()
        
        newEnergy = (
            (1-3*np.cos(nNA-newAngle)**2)/2).sum()

        return(newEnergy-oldEnergy)

    def boltzmannFactor(self, energie):
        """Fonction qui calcule le poid de Boltzmann d'une energie"""

        return(np.exp(-energie/self.energieRatio))

    def meanEnergy(self):
        """Fonction qui renvoie l'énergie moyenne sur la simulation Monte Carlo"""
        return(np.dot(self.boltzmannFactors,self.energies/self.size**2)/self.partitionFunction)


    def displayEnergies(self):
        """display the energy per site"""

        plt.plot((self.energies-self.minEnergy)/self.size**2)
        plt.show()

    def displayBoltzmannFactos(self):
        """display the energy per site"""

        plt.plot(self.boltzmannFactors)
        plt.show()


if __name__ == '__main__':

    print('Test 2D')
    test2D = latticeMC2D(10,10,1,1,0.001)
    test2D.runMC()
    test2D.postMC()
    test2D.discreteLattice2D.display()
    print(sum(test2D.accepted)) 
