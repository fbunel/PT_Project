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

"""fonction d'import des données"""
def importer(fichier, skiprow):             
        return np.loadtxt(fichier, skiprows=skiprow)

"""fonction d'extraction des données : ajouter le nombre de colonne nécessaire, les incertitudes ont des noms prédéfinis"""
def donnees(fichier, skiprow):
    
    data=importer(fichier, skiprow)

    temperature = data[:,0]
    energie = data[:,1]
    deltaEnergie =  data[:,2]
    order = data[:,3]
    deltaOrder =  data[:,4]

    return (temperature, energie, deltaEnergie, order, deltaOrder)


"""fonction d'affichage"""
def figure(fichier, skiprow):
    
    #données    
    (temperature, energie, deltaEnergie, order, deltaOrder) = donnees(
        fichier, skiprow)  

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')


    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()

    ax1.plot(temperature, order,
        linewidth = 2,
        color = 'g')
    ax2.plot(temperature, energie, 
        linewidth = 2,
        color = 'b')

    ax1.tick_params(labelsize = 16)
    ax2.tick_params(labelsize = 16)

    ax1.set_ylabel(r"Param\`etre d'ordre", fontsize = 18, color = 'g')
    ax2.set_ylabel(r"Energie", fontsize = 18, color = 'b')
    
    #enregistrement de l'image
    plt.savefig("{}_figure.pdf".format(fichier), bbox_inches='tight')
    plt.cla()

figure('global_study.save',3)
figure('local_study.save',3)