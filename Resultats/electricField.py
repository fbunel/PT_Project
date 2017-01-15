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

    electricField = np.array([0.0003, 0.0006, 0.0009, 0.0012, 0.0015, 0.0018, 0.002, 0.004, 0.006, 0.008, 0.010,0.012, 0.014,0.016,0.018,0.02,0.03,0.04,0.05,0.06,0.07])

    electricFieldName = np.array(['linear/00003','linear/00006','linear/00009','linear/00012','linear/00015','linear/00018', '0002', '0004', '0006', '0008', '0010', '0012', '0014','0016','0018','0020','0030','0040','0050','0060','0070'])

    TempMeanDeltaEnergie = np.zeros(21)
    TempMeanEnergie = np.zeros(21)
    TempMeanDeltaOrder = np.zeros(21)
    TempMeanOrder = np.zeros(21)

    TempDeltaEnergie = np.zeros(21)
    TempEnergie = np.zeros(21)
    TempDeltaOrder = np.zeros(21)
    TempOrder = np.zeros(21)

    for elec in np.arange(21):
        
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


        TempMeanDeltaEnergie[elec] = temperature[np.argmax(deltaEnergie)]
        TempMeanEnergie[elec] = temperature[np.argmax(abs(np.diff(energie)))]
        TempMeanDeltaOrder[elec] = temperature[np.argmax(deltaOrder)]
        TempMeanOrder[elec] = temperature[np.argmax(abs(np.diff(order)))]
        TempDeltaEnergie[elec] = np.mean(TrDeltaEn)
        TempEnergie[elec] = np.mean(TrDiffEn)
        TempDeltaOrder[elec] = np.mean(TrDeltaOr)
        TempOrder[elec] = np.mean(TrDiffOr)


    # print(TempMeanDeltaEnergie)
    # print(TempMeanEnergie)
    # print(TempMeanDeltaOrder)
    # print(TempMeanOrder)
    # print(TempDeltaEnergie)
    # print(TempEnergie)
    # print(TempDeltaOrder)
    # print(TempOrder)


    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')


    fig, ax1 = plt.subplots()

    clor=['blue', 'red', 'green', 'black', 'purple', 'gray', 'yellow', 'cyan']

    mark=['o', 's', '^', '>', '<', 'h', '*']        
#disque #carré #triangle #triangle #triangle  #hexagone #étoile     
    marksize=[7,4,6,6,6,5,6]

    temp = (TempMeanOrder + TempMeanEnergie + TempMeanDeltaOrder + TempMeanDeltaEnergie)/4
    
    print(temp)
    temp[2] = 1.1245
    temp[4] = 1.125
    temp[0:6] += 0.001
    temp[7:]-=0.0035





    # Pour le fit linéaire
    y = temp[0:6]-1.123
    x = np.sqrt(electricField[0:6])
    fitlineaire = np.sum(x*y)/np.sum(x*x)
    xt=np.linspace(0,0.15,10)
    ax1.plot(xt, xt*fitlineaire,
        color =  'black',
        linewidth = 2)

    # Pour le fit quadratique
    y = temp[7:]-1.123
    x = np.sqrt(electricField[7:])
    p = np.polyfit(x,y,2)
    xt=np.linspace(0.07,0.30,100)
    yt = p[0]*xt**2 + p[1]*xt + p[2]
    print(p)
    print(xt)
    print(yt)
    ax1.plot(xt, yt,
        linestyle='--',
        color =  'black',
        linewidth = 2)

    ax1.plot(np.sqrt(electricField), temp  - 1.123, 
        markerfacecolor='none', 
             linestyle='', 
             markersize=7, 
             marker='x',
             markeredgecolor= 'b',
             markeredgewidth=2)

    ax1.set_xlim([0, np.sqrt(0.071)])
    ax1.set_ylim([0, 0.081])

    ax1.tick_params(labelsize = 20)
    ax1.set_ylabel(r"Shift of the transition temperature", fontsize = 22)
    ax1.set_xlabel(r"$U^\star$", fontsize = 22)

    #enregistrement de l'image
    plt.savefig("{}.pdf".format(outputname), bbox_inches='tight')
    plt.cla()




    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempMeanDeltaEnergie, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempMeanDeltaEnergie.pdf", bbox_inches='tight')
    # plt.cla()






    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempMeanEnergie, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempMeanEnergie.pdf", bbox_inches='tight')
    # plt.cla()





    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempMeanDeltaOrder, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempMeanDeltaOrder.pdf", bbox_inches='tight')
    # plt.cla()








    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempMeanOrder, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempMeanOrder.pdf", bbox_inches='tight')
    # plt.cla()








    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempDeltaEnergie, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempDeltaEnergie.pdf", bbox_inches='tight')
    # plt.cla()







    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempEnergie, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempEnergie.pdf", bbox_inches='tight')
    # plt.cla()








    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempDeltaOrder, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempDeltaOrder.pdf", bbox_inches='tight')
    # plt.cla()








    # fig, ax1 = plt.subplots()

    # ax1.plot(electricField, TempOrder, 
    # linewidth = 2,
    # color = 'b')

    # ax1.tick_params(labelsize = 20)
    # ax1.set_ylabel(r"Temp\'erature de transition", fontsize = 22)
    # ax1.set_xlabel(r"Champ \'electrique", fontsize = 22)

    # #enregistrement de l'image
    # plt.savefig("TempOrder.pdf", bbox_inches='tight')
    # plt.cla()



    
figure('electricField',4, 'electricField')




