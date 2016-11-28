from Lattice import Lattice

import numpy as np
import matplotlib.pyplot as plt

class MonteCarlo:

    def __init__(self, size, sample, meanSample, energieRatio, start):
        """Constructeur de la classe qui nécessite :
        - la taille de la lattice
        - le nombre de cycle réalisé
        un cycle correspond à une série de size**3 changement (1 sur chaque site)
        - le nombre de sample sur lequel on calcule la moyenne (en nombre de cycle)
        - la température qui intervient par enegieratio = kbT/epsilon
        - l'information si on part d'une configuration random ou de l'état fondamental
        """

        ##Paramètre de l'étude##
        self.size = size                    
        self.sample = sample
        self.meanSample = meanSample
        self.energieRatio = energieRatio
        self.lattice = Lattice(self.size)

        ##Paramètre d'énergie et de plots##
        #Energies au step i
        self.energies = np.zeros(sample*self.size**3)
        #Energie de l'état fondamentale utilisé pour plot les énergies toujours 
        #par rapport à la même référence
        self.minEnergy = -3*size**3
        #Absicess en termes de nombre de cycle pour les graphes
        self.cycles = np.arange(sample*self.size**3)/self.size**3

        ##Paramètres pour gérer le ratio acceptance##
        #1 si le step i accepté, 0 sinon
        self.accepted = np.zeros(sample*self.size**3)
        self.acceptedSample = 10    #Variables pour des test sur les variations imposées à l'angle
        self.dmaxArray = np.zeros(sample*self.size**3)

        ##Paramètre pour le paramètre d'ordre##
        self.orderParameters = np.zeros(sample*self.size**3)

        #Initialise une configuration aléatoire pour la lattice et pour dmin/dmax
        if start == 'random' :
            self.lattice.randomConfiguration()
            self.dmax = 1
        elif start == 'groundstate' :
            self.lattice.groundstateConfiguration()
            self.dmax = 0.01

    def runMC(self):
        """Fonction qui lance une simulation Monte-Carlo"""

        for cycle in np.arange(self.sample) :

            self.lattice.randomOrder()
            print ("Cycle {}/{}".format(cycle, self.sample), end="\r")

            for s in np.arange(self.size**3) :
                
                i = cycle*self.size**3 + s
                #On prend le site aléatoire
                loc = self.lattice.randomLocOrdered(s)

                #On sauvegarde l'ancien angle
                oldAngle = np.copy(self.lattice.latticeArray[loc])
                #On réalise le move
                energieVariation, accepted = self.moveMC(loc)

                #On update la valeur d'energie
                self.updateEnergie(energieVariation, i)
                #On update la valeur de distance à l'angle précédent
                self.updateDmax(accepted, i)
                #On update la matrice du paramètre d'ordre
                self.updateOrderParameter(
                    accepted, oldAngle, self.lattice.latticeArray[loc], i)

    def equilibrate(self, equilibrateSample):
        """Fonction qui lance une simulation Monte-Carlo"""

        for cycle in np.arange(equilibrateSample) :

            self.lattice.randomOrder()
            print ("Cycle {}/{}".format(cycle, self.sample), end="\r")

            for s in np.arange(self.size**3) :
                
                #On prend le site aléatoire
                loc = self.lattice.randomLocOrdered(s)
                #On réalise le move
                energieVariation, accepted = self.moveMC(loc)

    def moveMC(self, loc):
        """Fonction qui tente un move du site numéro s de MonteCarlo"""

        #On choisit un nouvel angle presque au hasard
        newAngle = self.lattice.nearRandomOrientation(
            self.lattice.latticeArray[loc], self.dmax)

        #On calcule la variation d'énergie
        energieVariation = self.energieVariation(newAngle, loc)
            
        #On calcule la probabilité que le pas soit accepté
        acceptanceProbability = min(1,self.boltzmannFactor(energieVariation))

        #On teste cette proba
        if np.random.rand(1)<acceptanceProbability :
            self.lattice.latticeArray[loc] = newAngle
            return(energieVariation,1)
        else :
            return(0,0)

    def updateEnergie(self, energieVariation, i):
        """Fonction qui update les valeurs d'energies"""

        #On update les tableaux de résultats
        if i==0 :
            self.energies[0] = self.energie()
        else :
            self.energies[i] = self.energies[i-1] + energieVariation

    def updateDmax(self, accepted, i):
        """Fonction qui update les valeurs de dmax"""

        self.accepted[i] = accepted

        #On adapte l'amplitude de variation des angles 
        if(i>=self.acceptedSample) :
            stat = sum(
                self.accepted[i-self.acceptedSample:i])/self.acceptedSample
        else :  
            stat = sum(self.accepted[0:i])/(i+1)

        self.dmax = max(
            0.005, min(1, self.dmax + (stat - 1/2)/10000))
        self.dmaxArray[i] = self.dmax

    def updateOrderParameter(self, accepted, oldAngle, newAngle, i):
        """Fonction qui update les valeurs du paramètre d'ordre"""

        if i==0 :
            self.lattice.fillOrderMatrix()
            self.orderParameters[i] = self.lattice.orderParameter()

        else :
            if accepted==1:
                #On update la  matrice d'ordre
                self.lattice.updateOrderMatrix(oldAngle, newAngle)
                #Et on récupère le paramètre d'ordre
                self.orderParameters[i] = self.lattice.orderParameter()
        
            else :
                self.orderParameters[i] = self.orderParameters[i-1]

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
            1-3*(self.lattice.cosAngle(nNA.T,self.lattice.latticeArray[loc])**2).sum()
            )/2

        newEnergy = (
            1-3*(self.lattice.cosAngle(nNA.T,newAngle)**2
            ).sum())/2

        return(newEnergy-oldEnergy)

    def boltzmannFactor(self, energie):
        """Fonction qui calcule le poid de Boltzmann d'une energie"""

        return(np.exp(-energie/self.energieRatio))

    def meanEnergy(self):
        """Fonction qui renvoie l'énergie moyenne sur les meanSample derniers sample"""


        return(np.array([
            np.mean(self.energies[-self.meanSample*self.size**3:]-self.minEnergy)
                /self.size**3,
            np.std(
                self.energies[-self.meanSample*self.size**3:]-self.minEnergy)
                /self.size**3]))

    def meanOrderParameter(self):
        """Fonction qui renvoie l'énergie moyenne sur les meanSample derniers sample"""
        return(np.array([
            np.mean(self.orderParameters[-self.meanSample*self.size**3:]),
            np.std(self.orderParameters[-self.meanSample*self.size**3:])]))

    def displayEnergies(self):
        """Fonction qui affiche l'évolution de l'énergie"""

        plt.plot(self.cycles,(self.energies-self.minEnergy)/self.size**3)
        plt.title('Energie par site en unité de epsilon')
        plt.show()

    def displayOrderParameter(self):
        """Fonction qui affiche l'évolution de l'énergie"""

        plt.plot(self.cycles, self.orderParameters)
        plt.title("Paramètre d'ordre")
        plt.show()

if __name__ == '__main__':

    print('Test')
    test = MonteCarlo(30,100,10,0.01,'groundstate')
    print('Temperature : {}'.format(test.energieRatio))
    test.runMC()
    print('Energie moyenne')
    print(test.meanEnergy())
    print("Paramètre d'ordre moyen")
    print(test.meanOrderParameter())
    #test.displayEnergies()
    #test.displayOrderParameter()
    print("Ratio d'acceptance")
    print(sum(test.accepted)/(test.sample*test.size**3))
