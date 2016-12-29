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
def importer(fichier):             
        return np.loadtxt(fichier,skiprows =1)

"""fonction d'extraction des données : ajouter le nombre de colonne nécessaire, les incertitudes ont des noms prédéfinis"""
def donnees(fichier):
    
    data=importer(fichier)
    energie = data[:,0]
    order = data[:,1]

    return (energie, order)


"""fonction d'affichage"""
def figure(filename):

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    (energie, order) = donnees(
            filename) 

    energie = energie/27000 +3
    cycle = np.arange(0,energie.size)/27000

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()

    ax1.plot(cycle, order,
        linewidth = 2,
        color = 'g')
    ax2.plot(cycle, energie, 
        linewidth = 2,
        color = 'b')

    ax1.tick_params(labelsize = 16)
    ax2.tick_params(labelsize = 16)

    ax1.set_ylabel(r"Param\`etre d'ordre", fontsize = 18, color = 'g')
    ax1.set_xlabel(r"Cycles", fontsize = 18)
    ax2.set_ylabel(r"Energie", fontsize = 18, color = 'b')
    
    #enregistrement de l'image
    plt.savefig("equilibrage.pdf", bbox_inches='tight')
    plt.cla()

figure('equilibrage.data')

