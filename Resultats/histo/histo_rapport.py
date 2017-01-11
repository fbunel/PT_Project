#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import glob

font = {'family' : 'serif',
        'weight' : 'bold',
        'size'   : 25}

plt.rc('font', **font)
plt.rc('text', usetex=True)



def plot_hist(f,xlim=[1.75,2.25],ylim=[0,0.005]):
    print(f)
    with open(f) as lines:
        T = float(lines.readline())
    print(T)

    data = np.loadtxt(f, skiprows=1)
    print("data shape : ",data.shape)

    print("reshaping")
    n=1
    data = data.T
    data[1]=data[1]/data[1].sum()
    
    #plt.plot(data[:,0],data[:,1])
    
    plt.figure()
    xlim=[1.9,2.2]
    ylim=[0,0.08]
    bins=np.linspace(xlim[0],xlim[1],100)
    plt.hist(data[0],bins=bins,weights=data[1])
    
    plt.ylim(*ylim)
    plt.xlim(*xlim)
    #plt.title("T : {}".format(T))
    plt.xlabel("$E^\star$")
    plt.ylabel("$\%$")
    plt.tight_layout()
    #plt.clf()
    #plt.show()
    





f="../2/histo057.histo"
plot_hist("../2/histo057.histo")
plt.savefig("histo_1.1228.pdf")
plot_hist("../3/histo056.histo")
plt.savefig("histo_1.124.pdf")
plot_hist("../0/histo052.histo")
plt.savefig("histo_1.1208.pdf")
plot_hist("../3/histo064.histo")
plt.savefig("histo_1.1256.pdf")

#plt.show()
