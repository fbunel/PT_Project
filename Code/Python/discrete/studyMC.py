import numpy as np
import matplotlib.pyplot as plt
from latticeMC2D import latticeMC2D

class studyMC:

    def __init__(
        self, size, angleSize, equiSample, meanSample,statisticalSample, T0, Tf, Tsample):
        """Constructeu r de la classe qui initialise :
        - un objet matticeMC2D
        - les energies ratio qui nous intéresse.
        - la précision sur ces ratios"""

        self.size = size
        self.angleSize = angleSize
        self.equiSample = equiSample
        self.latticeMC2D = latticeMC2D(size, angleSize, equiSample, T0)
        self.T0 = T0
        self.Tf = Tf
        self.Tsample = Tsample
        self.statisticalSample = statisticalSample

        self.results = np.zeros(Tsample)
        self.errors = np.zeros(Tsample)
        self.temperature = np.logspace(T0, Tf, num=Tsample)




    def runStudy(self):
        """Fonction qui lance une étude complète sur une série de température indépendante (pas de cooling)"""

        for t,T in enumerate(self.temperature):
            print(T)

            result = np.zeros(self.statisticalSample)

            for i in range(self.statisticalSample):
                print(i)
                self.latticeMC2D = latticeMC2D(self.size, self.angleSize, self.equiSample, T)
                self.latticeMC2D.runMC()
                result[i] = self.latticeMC2D.meanEnergy()

            self.results[t] = np.mean(result)
            self.errors[t] = np.std(result)


if __name__ == '__main__':

    print('Test 2D')
    test2D = studyMC(20,10,100000,1,5,-5,1,50)
    test2D.runStudy()
    plt.plot(test2D.temperature, test2D.results)
    plt.show()
    