import numpy as np
from discreteLattice2D import discreteLattice2D

class latticeMC2D:

    def __init__(self, size, angleSize, sample, energieRatio):
        """Constructeur de la classe qui initialise :
        - la lattice à l'aide de size et anglesize
        - sample le nombre de Monte-Carlo step que l'on veut faire 
        - energieRatio qui est kbT/epsilon"""

        self.size = size
        self.angleSize = angleSize
        self.discreteLattice2D = discreteLattice2D(self.size, self.angleSize)
        self.energieRatio = energieRatio
        self.sample = sample
        self.energies = np.zeros(sample)
        self.partitionFunction = 0

    def runMC(self):
        """Fonction qui lance une simulation Monte-Carlo"""

        #Initialise une configuration aléatoire pour la lattice
        self.discreteLattice2D.randomConfiguration()

        for i in range(self.sample) :

            #On prends un site et un angle au hasard
            randomLoc = self.discreteLattice2D.randomLoc()
            newAngle = self.discreteLattice2D.latticeArray[tuple(randomLoc)]
            while newAngle==self.discreteLattice2D.latticeArray[tuple(randomLoc)]:
                newAngle = self.discreteLattice2D.randomOrientation()

            #On calcule la variation d'énergie
            energieVariation = self.energieVariation(newAngle, randomLoc)
            #On calcule la probabilité que le pas soit accepté
            acceptanceProbability = self.boltzmannFactor(energieVariation)
            #On teste cette proba
            if np.random.rand(1)>acceptanceProbability :
                self.discreteLattice2D.latticeArray[tuple(randomLoc)] = newAngle
            
            #On ajoute la nouvelle configuration aux résultats
            #if i==0 :
            #    energies[0] = self.energie()
            #else :
            #    energies[i] = energie[i-1] + energieVariation

            #self.partitionFunction += self.boltzmannFactor(energies[i])


    def energie(self):
        """Fonction qui renvoie l'énergie de la configuration actuelle"""
        #HADRI REMPLI CA SALE BATARD DE NOOB#
        #QUAND T'AS FINI DECOMENTE LA PARTIE DE CODE COMMENTE DANS runMC OU JTE BAISE#

    def energieVariation(self, newAngle, loc):
        """Fonction qui renvoie la variation d'énergie associée
         au changement d'un spin"""

        nearestNeighboorAngle=self.discreteLattice2D.nearestNeighboorAngle(loc)
       
        oldEnergy = sum((3*np.cos(
                nearestNeighboorAngle-self.discreteLattice2D.latticeArray[tuple(loc)])
                **2-1)/2)
        
        newEnergy = sum(
            (3*np.cos(nearestNeighboorAngle-newAngle)**2-1)/2)
        
        print (oldEnergy,newEnergy)

        return(oldEnergy-newEnergy)

    def boltzmannFactor(self, energie):
        """Fonction qui calcule le poid de Boltzmann d'une energie"""

        return(np.exp(-energie/self.energieRatio))


if __name__ == '__main__':

    print('Test 2D')
    test2D = latticeMC2D(8,2,5,1)
    test2D.runMC()