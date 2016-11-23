from Lattice import Lattice
from MonteCarlo import MonteCarlo

import numpy as np
import matplotlib.pyplot as plt

class Study:

    def __init__(self, size, sample, meanSample, eRstart, eRend, eRsample, start):
        """Constructeur de la classe qui nécessite :
        - la taille de la lattice
        - le nombre de cycle réalisé pour équilibrer le système à chaque température
        un cycle correspond à une série de size**3 changement (1 sur chaque site)
        - le nombre de sample sur lequel on calcule la moyenne (en nombre de cycle)
        - le energieRatio auquel on commence
        - le energieRatio auquel on finit
        - le nombre de energieRatio qu'on veut observer
        - l'information si on part d'une configuration random ou de l'état fondamental
        """

        ##Paramètre de l'étude##
        self.eRstart = eRstart
        self.eRend = eRend
        self.eRsample = eRsample
        self.energieRatios = np.linspace(eRstart, eRend, num=eRsample)
        self.monteCarlo = MonteCarlo(size, sample, meanSample, eRstart, start)

        #Paramètre de résultats
        self.orderParameter = np.zeros(eRsample)
        self.energy = np.zeros(eRsample)


    def run(self):
        """Lance une simulation sur toutes les températures dans energiesRatios"""

        for i, energieRatio in enumerate(self.energieRatios) :
            print("Température {}/{} : {}".format(i+1, self.eRsample, energieRatio))
            self.monteCarlo.energieRatio = energieRatio
            self.monteCarlo.runMC()
            self.orderParameter[i] = self.monteCarlo.meanOrderParameter()
            self.energy[i] = self.monteCarlo.meanEnergy()

    def display(self):
        """Fonction qui affiche l'évolution de l'énergie"""

        plt.plot(self.energieRatios, self.orderParameter)
        plt.title("Paramètre d'ordre")
        plt.show()

        plt.plot(self.energieRatios, self.energy)
        plt.title("Energie")
        plt.show()


if __name__ == '__main__':

    print('Test 3D')
    test = Study(30,500,200,0.01,2.2,100,'groundstate')
    test.run()
    test.display()