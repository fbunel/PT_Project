import numpy as np
import matplotlib.pyplot as plt
from continuousLattice3D import continuousLattice3D

class latticeMC3Dcontinuous:

    def __init__(self, size, sample, meanSample, energieRatio, start):
        """Constructeu de la classe """

        self.size = size
        self.lattice = continuousLattice3D(self.size)
        self.sample = sample
        self.meanSample = meanSample
        self.energieRatio = energieRatio

        self.accepted = np.zeros(sample)
        self.energies = np.zeros(sample)
        self.energiesForMean = np.zeros(meanSample)
        self.boltzmannFactors = np.zeros(meanSample)
        self.partitionFunction = 0
        self.minEnergy = -3*size**3
        self.referenceEnergy = 0 

        self.dminArray = np.zeros(sample)
        self.dmaxArray = np.zeros(sample)

        #Initialise une configuration aléatoire pour la lattice
        if start == 'random' :
            self.lattice.randomConfiguration()
        elif start == 'groundstate' :
            self.lattice.groundstateConfiguration()


    def runMC(self):
        """Fonction qui lance une simulation Monte-Carlo"""

        dmin = 0
        dmax = 1
        nAccepted = 100

        for i in range(self.sample) :

            print(i)

            #On prends un site et un angle au hasard
            randomLoc = self.lattice.randomLoc()

            #On choisit un nouvel angle au hasard
            #newAngle = self.lattice.randomOrientation()
            newAngle = self.lattice.nearRandomOrientation(
                self.lattice.latticeArray[tuple(randomLoc)], dmin, dmax)

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

            #On adapte la vitesse de changement en fonction de l'angle
            
            if(i>=nAccepted) :
                stat = sum(self.accepted[i-nAccepted:i])/nAccepted
                dmax = max(0.01, min(1, dmax + (stat - 1/2)/1000))
                dmin = max(0, min(0.3, dmax-0.01, dmin + (stat - 1/2)/2000))
            else :
                stat = sum(self.accepted[0:i])/i
                dmax = max(0.01, min(1, dmax + (stat - 1/2)/1000))
                dmin = max(0, min(0.3, dmax-0.01, dmin + (stat - 1/2)/2000))
            
            self.dminArray[i] = dmin
            self.dmaxArray[i] = dmax

        plt.plot(self.dminArray)
        plt.plot(self.dmaxArray)
        plt.show()

    def postMC(self):

        #Les facteurs de Boltzmanns et la fonction de partition sont calculés avec un
        #spectre d'énergie décalé par l'énergie minimale observée
        self.energiesForMean = self.energies[-self.meanSample:]
        self.referenceEnergy = min(self.energiesForMean)
        self.boltzmannFactors = self.boltzmannFactor(
            self.energiesForMean - self.referenceEnergy)
        self.partitionFunction = sum(self.boltzmannFactors)

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
        """Fonction qui ren voie la variation d'énergie associée
         au changement d'un spin"""

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
        """Fonction qui renvoie l'énergie moyenne sur la simulation Monte Carlo"""
        return(np.dot(self.boltzmannFactors,self.energies/self.size**3)/self.partitionFunction)


    def displayEnergies(self):
        """display the energy per site"""

        plt.plot((self.energies-self.minEnergy)/self.size**3)
        plt.title('Energy per site')
        plt.show()

    def displayBoltzmannFactors(self):
        """display the energy per site"""

        plt.plot(self.boltzmannFactors)
        plt.show()


if __name__ == '__main__':

    print('Test 3D')
    test3D = latticeMC3Dcontinuous(10,200000,50000,0.01,'groundstate')
    test3D.runMC()
    test3D.postMC()
    #test3D.lattice.display()    
    test3D.displayEnergies()
    test3D.displayBoltzmannFactors()
    print(sum(test3D.accepted))
