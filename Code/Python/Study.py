from Lattice import Lattice
from MonteCarlo import MonteCarlo

import numpy as np
import matplotlib.pyplot as plt

import pickle

class Study:

    def __init__(self, size, equiSample, meanSample, eRstart, eRend, eRsample, start, reLoad = False, filename='studySave.save'):
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
        self.monteCarlo = MonteCarlo(
            size, equiSample, meanSample, self.energieRatios[0], start)
        self.equiSample = equiSample

        #Paramètre de résultats
        self.orderParameter = np.zeros((eRsample, 2))
        self.energy = np.zeros((eRsample, 2))

        #Paramètre d'avancée
        self.i = 0

        #Pour le stockage et le chargement
        self.filename = filename
        if reLoad :
            self.loadClass()

    def run(self):
        """Lance une simulation sur toutes les températures dans energiesRatios"""
        
        if self.i==0 :
            print(
                "Equilibrage inital à la température : {}".format(
                    self.energieRatios[0]))
            
            self.monteCarlo.equilibrate()       

        while self.i < self.eRsample :
            energieRatio = self.energieRatios[self.i]
            print("Température {}/{} : {}".format(
                self.i+1, self.eRsample, energieRatio))
            self.monteCarlo.energieRatio = energieRatio

            self.monteCarlo.equilibrate()
            self.monteCarlo.calculate()

            self.orderParameter[self.i, :] = self.monteCarlo.meanOrderParameter()
            self.energy[self.i, :] = self.monteCarlo.meanEnergy()
            self.i+=1
            self.saveClass()
            print("\n")

    def display(self):
        """Fonction qui affiche l'évolution de l'énergie"""

        plt.plot(self.energieRatios, self.orderParameter[:,1])
        plt.title("Paramètre d'ordre")
        plt.show()

        plt.plot(self.energieRatios, self.energy[:,1])
        plt.title("Energie")
        plt.show()

    def saveClass(self):
        """Fonction qui sauvegarde toute la classe"""

        with open(self.filename,'wb') as f :
            pickle.dump(self.__dict__,f)


    def loadClass(self):
        """Fonction qui recharge toute la classe"""

        with open(self.filename,'rb') as f :
            tmp_dict = pickle.load(f)

        self.__dict__.update(tmp_dict) 
        self.i+=10

if __name__ == '__main__':

    print('Test 3D \n')

    test = Study(30,1000,300,1,1.3,60,'groundstate',True,'10-13.save')
    test.run()