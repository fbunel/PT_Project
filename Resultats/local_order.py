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

    temperature = data[:,0]
    energie = data[:,1]
    deltaEnergie =  data[:,2]
    order = data[:,3]
    deltaOrder =  data[:,4]

    return (temperature, energie, deltaEnergie, order, deltaOrder)


"""fonction d'affichage"""
def figure(basename, skiprow, outputname):

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    filenames = np.array(glb.glob(basename))
    nFile = filenames.size

    (temperature, _, _, _, _) = donnees(
            filenames[0], skiprow) 

    size = temperature.shape

    order = np.zeros(size)
    energie = np.zeros(size)
    deltaEnergie = np.zeros(size)
    deltaOrder = np.zeros(size)

    for file in np.arange(nFile):

        (temperaturefile, energiefile, deltaEnergiefile, orderfile, deltaOrderfile) = donnees(filenames[file], skiprow)  
        order += orderfile
        energie += energiefile
        deltaEnergie += deltaEnergiefile
        deltaOrder += deltaOrderfile
       
    order /= nFile
    energie /= nFile
    deltaEnergie /= nFile
    deltaOrder /= nFile
   
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()

    ax2.plot(temperature, deltaOrder,
        linewidth = 2,
        color = 'g')
    ax1.plot(temperature, order, 
        linewidth = 2,
        color = 'b')
    ax1.set_xlim([0.99, 1.25])
    

    ax2.tick_params(labelsize = 20)
    ax1.tick_params(labelsize = 20)

    ax2.set_ylabel(r"$\sigma_S$", fontsize = 22, color = 'g')
    ax1.set_ylabel(r"$S$", fontsize = 22, color = 'b')
    ax1.set_xlabel(r"$T^\star$", fontsize = 22)
    
    #enregistrement de l'image
    plt.savefig("{0}.pdf".format(outputname), bbox_inches='tight')
    plt.cla()

    fig, ax1 = plt.subplots()



figure('local/**/**study.save',3, 'local_order')


