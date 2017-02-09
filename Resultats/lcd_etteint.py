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
    Phi = np.unwrap(Phi)
    

    print('Phi')
    meanPhi = np.mean(Phi, axis=(0,1))
    erorPhi = np.std(Phi,axis=(0,1))
    print(meanPhi)

    print('Theta')
    Theta = np.arccos(np.abs(cosTheta))
    meanTheta = np.mean(Theta, axis=(0,1))
    erorTheta = np.std(Theta, axis=(0,1))
    print(Theta)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    fig, ax1 = plt.subplots()

    clor=['blue', 'red', 'green', 'black', 'purple', 'gray', 'yellow', 'cyan']

    mark=['o', 's', '^', '>', '<', 'h', '*']        
#disque #carré #triangle #triangle #triangle  #hexagone #étoile     
    marksize=[7,4,6,6,6,5,6]

    ax1.errorbar(np.arange(30),meanPhi, yerr = 0,
        fmt = 'o',
        label = r"$\phi$")
    ax1.errorbar(np.arange(30),meanTheta, yerr = erorTheta,
        fmt = 'o',
        label = r"$\theta$")

    ax1.set_yticks([0., 0.25*np.pi,0.5*np.pi])
    ax1.set_yticklabels(["$0$", r"$\pi/4$", r"$\pi/2$",])

    # ax1.set_xlim([1.05, 1.25])
    ax1.set_ylim([0-0.13, np.pi/2+0.13])

    ax1.tick_params(labelsize = 20)
    ax1.set_xlabel(r"Site", fontsize = 22)

    plt.legend(loc=9, numpoints=1, fontsize=22, borderpad=0.15, columnspacing=1, handlelength=1, shadow=True)

    #enregistrement de l'image
    plt.savefig("{}.pdf".format(outputname), bbox_inches='tight')
    plt.cla()

# figure('lcd/lcd_allume.dat',0, 'lcd_allume')
figure('lcd/lcd_etteint.dat',0, 'lcd_etteind')



