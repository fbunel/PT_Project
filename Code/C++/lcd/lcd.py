"""
Demo of TeX rendering.

You can use TeX to render all of your matplotlib text if the rc
parameter text.usetex is set.  This works currently on the agg and ps
backends, and requires that you have tex and the other dependencies
described at http://matplotlib.org/users/usetex.html
properly installed on your system.  The first time you run a script
you will see a lot of output from tex and associated tools.  The next
time, the run may be silent, as a lot of the information is cached in
~/.tex.cache

"""
import numpy as np
import matplotlib.pyplot as plt
import glob as glb

"""fonction d'import des données"""
def importer(fichier, skiprow):             
        return np.loadtxt(fichier, skiprows=skiprow)

"""fonction d'extraction des données : ajouter le nombre de colonne nécessaire, les incertitudes ont des noms prédéfinis"""
def donnees(fichier, skiprow):
    
    data=importer(fichier, skiprow)
    il = data[:,0]
    jl = data[:,1]
    kl = data[:,2]
    cosTheta = data[:,3]
    Phi = data[:,4]

    return (il, jl, kl, cosTheta, Phi)


"""fonction d'affichage"""
def figure(basename, skiprow, outputname):

    (il, jl, kl, cosTheta, Phi) = donnees(basename, skiprow) 
    cosTheta = np.resize(cosTheta, (30,30,30)) 
    Phi = np.resize(Phi, (30,30,30))

    Phi = np.mod(Phi,np.pi)
    
    print('Phi')
    meanPhi = np.mean(Phi, axis=(0,1))
    print(meanPhi)

    print('cosTheta')
    meancosTheta = np.mean(cosTheta, axis=(0,1))
    print(meancosTheta)

    meancosTheta = np.arccos(meancosTheta)
    plt.plot(meancosTheta)
    plt.show()


figure('lcd_lattice.dat',0, 'lcd')



