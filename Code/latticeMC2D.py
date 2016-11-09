import numpy as np
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
        self.energies = np.zeros(sample)
        self.partitionFunction = 0

    def runMC(self):
        """Fonction qui lance une simulation Monte-Carlo"""

        #Initialise une configuration aléatoire pour la lattice
        self.discreteLattice2D.randomConfiguration()

        for i in range(self.sample) :

            print("Lattice :")
            print(self.discreteLattice2D.latticeArray)

            #On prends un site et un angle au hasard
            randomLoc = self.discreteLattice2D.randomLoc()

            print("New loc")
            print(randomLoc)

            print("Old Angle")
            newAngle = self.discreteLattice2D.latticeArray[tuple(randomLoc)]
            print(newAngle)
            while newAngle==self.discreteLattice2D.latticeArray[tuple(randomLoc)]:
                newAngle = self.discreteLattice2D.randomOrientation()
            print("New Angle")
            print(newAngle)

            #On calcule la variation d'énergie
            energieVariation = self.energieVariation(newAngle, randomLoc)
            
            #On calcule la probabilité que le pas soit accepté
            print("Acceptance probability")
            acceptanceProbability = self.boltzmannFactor(energieVariation)
            print(acceptanceProbability)
            #On teste cette proba
            if np.random.rand(1)<acceptanceProbability :
                self.discreteLattice2D.latticeArray[tuple(randomLoc)] = newAngle
                print("Step accepted")

            print("\n \n \n")
            
            #On ajoute la nouvelle configuration aux résultats
            if i==0 :
                self.energies[0] = self.energie()
            else :
                self.energies[i] = self.energies[i-1] + energieVariation

            self.partitionFunction += self.boltzmannFactor(self.energies[i])


    def energie(self):
        """Fonction qui renvoie l'énergie de la configuration actuelle"""
        arr = self.discreteLattice2D.latticeArray
        
        totEnergy = (
             (3*np.cos(arr - np.roll(arr, 1,axis=0))**2-1)/2
            +(3*np.cos(arr - np.roll(arr,-1,axis=0))**2-1)/2
            +(3*np.cos(arr - np.roll(arr, 1,axis=1))**2-1)/2
            +(3*np.cos(arr - np.roll(arr,-1,axis=1))**2-1)/2
            ).sum()

        return totEnergy
        #HADRI REMPLI CA SALE BATARD DE NOOB#
        #QUAND T'AS FINI DECOMENTE LA PARTIE DE CODE COMMENTE DANS runMC OU JTE BAISE#

    def energieVariation(self, newAngle, loc):
        """Fonction qui ren voie la variation d'énergie associée
         au changement d'un spin"""

        nearestNeighboorAngle=self.discreteLattice2D.nearestNeighboorAngle(loc)
       
        oldEnergy = ((3*np.cos(
                nearestNeighboorAngle-self.discreteLattice2D.latticeArray[tuple(loc)])
                **2-1)/2).sum()
        
        newEnergy = (
            (3*np.cos(nearestNeighboorAngle-newAngle)**2-1)/2).sum()
        print("Old Energy and New Energy")
        print (oldEnergy,newEnergy)

        return(oldEnergy-newEnergy)

    def boltzmannFactor(self, energie):
        """Fonction qui calcule le poid de Boltzmann d'une energie"""

        return(np.exp(-energie/self.energieRatio))


if __name__ == '__main__':

    print('Test 2D')
    test2D = latticeMC2D(3,2,5,5)
    test2D.runMC()
