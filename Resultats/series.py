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

    TrDeltaEn = np.zeros(nFile)
    TrDeltaOr = np.zeros(nFile)
    TrDiffEn = np.zeros(nFile)
    TrDiffOr = np.zeros(nFile)

    for file in np.arange(nFile):

        (temperaturefile, energiefile, deltaEnergiefile, orderfile, deltaOrderfile) = donnees(filenames[file], skiprow)  
        order += orderfile
        energie += energiefile
        deltaEnergie += deltaEnergiefile
        deltaOrder += deltaOrderfile
       
        TrDeltaEn[file] = temperature[np.argmax(deltaEnergie)]
        TrDeltaOr[file] = temperature[np.argmax(deltaOrder)]
        TrDiffOr[file] = temperature[np.argmax(abs(np.diff(energie)))]
        TrDiffEn[file] = temperature[np.argmax(abs(np.diff(order)))]


    order /= nFile
    energie /= nFile
    deltaEnergie /= nFile
    deltaOrder /= nFile

    print("Moyenne sur les réalisations puis température de transition :")
    print("Delta Energie")
    print(temperature[np.argmax(deltaEnergie)])
    print("Delta Ordre")
    print(temperature[np.argmax(deltaOrder)])

    print("Derivée Energie")
    print(temperature[np.argmax(abs(np.diff(energie)))])
    print("Derivée Ordre")
    print(temperature[np.argmax(abs(np.diff(order)))])


    print("Température de transition puis moyenne sur les transitions")
    print("Delta Energie")
    print(np.mean(TrDeltaEn))
    print(TrDeltaEn)
    print("Delta Ordre")
    print(np.mean(TrDeltaOr))
    print(TrDeltaOr)
    print("Derivée Energie")
    print(np.mean(TrDiffEn))
    print(TrDiffEn)
    print("Derivée Ordre")
    print(np.mean(TrDiffOr))
    print(TrDiffOr)
    
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
    plt.savefig("{0}_.pdf".format(outputname), bbox_inches='tight')
    plt.cla()

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()

    ax1.plot(temperature, deltaOrder,
        linewidth = 2,
        color = 'g')
    ax2.plot(temperature, deltaEnergie, 
        linewidth = 2,
        color = 'b')

    ax1.tick_params(labelsize = 16)
    ax2.tick_params(labelsize = 16)

    ax1.set_ylabel(r"Param\`etre d'ordre", fontsize = 18, color = 'g')
    ax2.set_ylabel(r"Energie", fontsize = 18, color = 'b')
    
    #enregistrement de l'image
    plt.savefig("{0}_delta.pdf".format(outputname), bbox_inches='tight')
    plt.cla()

# figure('veryverylocal/**/**study.save',3, 'veryverylocal')
# figure('global/**study.save',3, 'global')
figure('local/**/**study.save',3, 'local')
# figure('verylocal/**/**study.save',3, 'verylocal')
# figure('electricField/005/**/**study.save',3, 'electric005')
# figure('electricField/01/**/**study.save',3, 'electric01')
# figure('electricField/02_fail/**/**study.save',3, 'electric02')
# figure('series/**/*study.save',3,'series')
