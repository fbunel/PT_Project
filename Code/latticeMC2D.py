import numpy as np
import matplotlib.pyplot as plt
from discreteLattice2D import discreteLattice2D

class latticeMC2D:

    def __init__(self, size, angleSize, sample, energieRatio):
        """Constructeu r de la classe qui initialise :
        - la lattice à l'aide de size et anglesize
        - sample le nombre de Monte-Carlo step que l'on veut faire 
        - energieRatio qui est kbT/epsilon"""

        self.size = size
        self.angleSize = angleSize
        self.discreteLattice2D = discreteLattice2D(self.size, self.angleSize)
        self.energieRatio = energieRatio
        self.sample = sample
        
        self.maxEnergy=-2*size**2
        self.energies = np.zeros(sample)
        self.partitionFunction = 0
        self.boltzmannFactors = np.zeros(sample)

    def runMC(self):
        """Fonction qui lance une simulation Monte-Carlo"""

        #Initialise une configuration aléatoire pour la lattice
        self.discreteLattice2D.randomConfiguration()

        for i in range(self.sample) :

            print("Lattice")
            print(self.discreteLattice2D.latticeArray)
            print("Energie :")
            print(self.energie())

            #On prends un site et un angle au hasard
            randomLoc = self.discreteLattice2D.randomLoc()

            print("Site choisi au hasard:")
            print(randomLoc)

            newAngle = self.discreteLattice2D.latticeArray[tuple(randomLoc)]
            while newAngle==self.discreteLattice2D.latticeArray[tuple(randomLoc)]:
                newAngle = self.discreteLattice2D.randomOrientation()

            print("Nouvel angle")
            print(newAngle)

            #On calcule la variation d'énergie
            energieVariation = self.energieVariation(newAngle, randomLoc)
            
            print("Variation d'energie")
            print(energieVariation)

            #On calcule la probabilité que le pas soit accepté
            acceptanceProbability = min(1,self.boltzmannFactor(energieVariation))

            print("Probabilité d'acceptance")
            print(acceptanceProbability)

            #On teste cette proba
            if np.random.rand(1)<acceptanceProbability :
                print("Pas accepté")
                self.discreteLattice2D.latticeArray[tuple(randomLoc)] = newAngle
                
            else :
                print("Pas refusé")
                energieVariation = 0

            #On update les tableaux de résultats
            if i==0 :
                #On déplace tout le spectre d'energie pour veiter les divergences
                self.energies[0] = self.energie() - self.maxEnergy
            else :
                self.energies[i] = self.energies[i-1] + energieVariation

            self.boltzmannFactors[i] = self.boltzmannFactor(self.energies[i])

            print("\n \n \n")

        self.partitionFunction = sum(self.boltzmannFactors)

        print("Fonction de partition")
        print(self.partitionFunction)
        print("Energies")
        print(self.energies)
        print("Poids de Boltzmann")
        print(self.boltzmannFactors)

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

    def displayEnergies(self):
        """display the energy"""

        plt.plot(self.energies)
        plt.show()

if __name__ == '__main__':

    print('Test 2D')
    test2D = latticeMC2D(10,10,10000,10)
    test2D.runMC()
    test2D.discreteLattice2D.display()
    test2D.displayEnergies()
    
