from lattice import lattice
from random import randint
import numpy as np

class discreteLattice(lattice):

	def __init__(self, size, dim, angleSize):
		"""Constructeur de la classe qui herite de lattice :
		-construit un objet lattice a partir de size et dim
		-le nombre d'orientations autorisees pour un site"""

		lattice.__init__(self, size, dim)
		self.angleSize = angleSize

	def randomOrientation(self):
		"""Fonction qui renvoie une orientation aleatoire parmis celles autorisees."""
		if self.dim==2 :
			return (np.pi/angleSize*
				np.array([randint(0,angleSize-1)]))
		elif self.dim==3 :
			return (np.pi/angleSize*
				np.array([randint(0,angleSize-1),randint(0,angleSize-1)]))


	def changeOrientation(self, loc, angle):
		"""Fonction qui change l'orientation d'un site a une nouvelle valeur angle."""
		
		if dim==2 :
			self.latticeArray[loc[0],loc[1]] = angle
		elif dim==3 :
			self.latticeArray[loc[0],loc[1],loc[2]] = angle

		
	