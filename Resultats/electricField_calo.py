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

    electricField = np.array([0, 0.0003, 0.0006, 0.0009, 0.0012, 0.0015, 0.0018, 0.002, 0.004, 0.006, 0.008, 0.010,0.012, 0.014,0.016,0.018,0.02,0.03,0.04,0.05,0.06,0.07])

    electricFieldName = np.array(['../local','linear/00003','linear/00006','linear/00009','linear/00012','linear/00015','linear/00018', '0002', '0004', '0006', '0008', '0010', '0012', '0014','0016','0018','0020','0030','0040','0050','0060','0070'])

    TempMeanDeltaEnergie = np.zeros(22)
    TempMeanEnergie = np.zeros(22)
    TempMeanDeltaOrder = np.zeros(22)
    TempMeanOrder = np.zeros(22)

    TempDeltaEnergie = np.zeros(22)
    TempEnergie = np.zeros(22)
    TempDeltaOrder = np.zeros(22)
    TempOrder = np.zeros(22)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')


    fig, ax1 = plt.subplots()

    clor=['blue', 'red', 'green', 'black', 'purple', 'gray', 'yellow', 'cyan']

    mark=['o', 's', '^', '>', '<', 'h', '*']        
#disque #carré #triangle #triangle #triangle  #hexagone #étoile     
    marksize=[7,4,6,6,6,5,6]

    print('yolo')

    arange = np.array([0,11,16,17,19,21])

    for elec in arange:
        
        filebasename = basename + '/' + electricFieldName[elec] +  '/**/**study.save'

        filenames = np.array(glb.glob(filebasename))
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



        ax1.plot(temperature, energie, linewidth = 2,label=r"$U^\star = {0:.2f}$".format(electricField[elec]))

        ax1.set_xlim([1.05, 1.25])
        # ax1.set_ylim([0, 0.081])

        ax1.tick_params(labelsize = 20)
        ax1.set_ylabel(r"$E^\star$", fontsize = 22)
        ax1.set_xlabel(r"$T^\star$", fontsize = 22)

    #Position de la legende   
    legend_loc={'best'        : 0,
                'upper right' : 1,
                'upper left'  : 2,
                'lower left'  : 3,
                'lower right' : 4,
                'right'       : 5,
                'center left' : 6,
                'center right': 7,
                'lower center': 8,
                'upper center': 9,
                'center'      : 10
                }
    
    plt.legend(loc=4, numpoints=1, fontsize=22, borderpad=0.15, columnspacing=1, handlelength=1, shadow=True)

    #enregistrement de l'image
    plt.savefig("{}.pdf".format(outputname), bbox_inches='tight')
    plt.cla()


    
figure('electricField',4, 'electricField_calo')
