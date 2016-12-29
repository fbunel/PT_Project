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

"""fonction d'affichage"""
def figure(fichier, skiprow):
    


    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    theta=np.linspace(0,np.pi,1000)
    f = (3*np.cos(theta)**2 - 1)/2

    fig, ax1 = plt.subplots()

    ax1.plot(theta, f,
        linewidth = 2)

    plt.xlim(0, np.pi)

    ax1.tick_params(labelsize = 30)
    ax1.set_xticks([0., 0.5*np.pi,np.pi])
    ax1.set_yticks([])
    ax1.set_xticklabels(["$0$", r"$\pi/2$", r"$\pi$",])
    ax1.set_ylabel(r"$f(\theta)$", fontsize = 35)
    ax1.set_xlabel(r"$\theta$", fontsize = 35)
    
    #enregistrement de l'image
    plt.savefig("figure.pdf", bbox_inches='tight')
    plt.cla()

figure('local3_study.save',3)
