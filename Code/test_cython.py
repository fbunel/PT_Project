from MonteCarlo import MonteCarlo

#test = MonteCarlo(30,600,10,1.1,'groundstate')
test = MonteCarlo(30,3,10,1.1,'groundstate')
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
