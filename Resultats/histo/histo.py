#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import glob
from mpl_toolkits.mplot3d import Axes3D





files = glob.glob('*/*.histo')


def load(f):
    print(f)
    with open(f) as lines:
        T = float(lines.readline())
    print(T)

    data = np.loadtxt(f,skiprows=1)
    print("data shape : ",data.shape)

    print("reshaping")
    n=100
    data = data.T.reshape(2,-1,n)
    rebined = data.sum(axis=-1)
    rebined[0]=rebined[0]/n
    rebined[1]=rebined[1]/rebined[1].sum()

    print("new data shape : ",data.shape)
    return rebined[0],rebined[1],T

def load_3D(regex = '1/*.histo'):
    #rebin factor:
    n=400
    
    files = sorted(glob.glob(regex))
    arrays = []
    temps = []
    for f in files:
        print(f)
        with open(f) as lines:
            T = float(lines.readline())
        print(T)

        data = np.loadtxt(f,skiprows=1)
        print("data shape : ",data.shape)

        print("reshaping")

        data = data.T.reshape(2,-1,n)
        rebined = data.sum(axis=-1)
        rebined[0]=rebined[0]/n
        rebined[1]=rebined[1]/rebined[1].sum()
        arrays.append(rebined)
        temps.append(T)

    E, c = np.array(arrays).transpose((1,0,2))
    T = np.array(temps)
    
    print("E: ",E.shape," c: ",c.shape," T: ",T.shape)
    return E, c, T




def plot_hist(f,xlim=[1.75,2.25],ylim=[0,0.005]):
    print(f)
    with open(f) as lines:
        T = float(lines.readline())
    print(T)

    data = np.loadtxt(f,skiprows=1)
    print("data shape : ",data.shape)

    print("reshaping")
    n=20
    data = data.T.reshape(2,-1,n)
    rebined = data.sum(axis=-1)
    rebined[0]=rebined[0]/n
    rebined[1]=rebined[1]/rebined[1].sum()

    print("new data shape : ",data.shape)
    #print(rebined)

    #plt.plot(data[:,0],data[:,1])
    plt.plot(rebined[0,:],rebined[1,:])
    plt.ylim(*ylim)
    plt.xlim(*xlim)
    plt.title("T : {}".format(T))
    plt.savefig("figs/"+f+".png")
    plt.clf()
    #plt.show()
    
def plot_all_quad_hist(xlim=[1.75,2.25],ylim=[0,0.005]):
    for j in range(100):
        for i in range(4):
            f = "{:}/histo{:03}.histo".format(i,j)
            with open(f) as lines:
                T = float(lines.readline())
            print(T)

            data = np.loadtxt(f,skiprows=1)
            print("data shape : ",data.shape)

            print("reshaping")
            n=20
            data = data.T.reshape(2,-1,n)
            rebined = data.sum(axis=-1)
            rebined[0]=rebined[0]/n
            rebined[1]=rebined[1]/rebined[1].sum()

            print("new data shape : ",data.shape)
            #print(rebined)

            #plt.plot(data[:,0],data[:,1])
            plt.subplot(2,2,i+1)
            plt.plot(rebined[0,:],rebined[1,:])
            plt.ylim(*ylim)
            plt.xlim(*xlim)
            plt.title("sim : {} , T : {}".format(i,T))
        plt.savefig("figs/quad/{:03}.png".format(j))
        plt.clf()
    #plt.show()

def plot_all_mean_hist(xlim=[1.75,2.25],ylim=[0,0.005]):
    for j in range(100):
        for i in range(4):
            f = "{:}/histo{:03}.histo".format(i,j)
            with open(f) as lines:
                T = float(lines.readline())
            print(T)

            data = np.loadtxt(f,skiprows=1)
            print("data shape : ",data.shape)

            print("rebining")
            n=20
            data = data.T.reshape(2,-1,n)
            rebined = data.sum(axis=-1)
            rebined[0]=rebined[0]/n
            rebined[1]=rebined[1]/rebined[1].sum()
            if i == 0:
                mean = np.zeros(rebined.shape)
            mean+=rebined


        mean/=4
        plt.plot(mean[0,:],mean[1,:])
        plt.ylim(*ylim)
        plt.xlim(*xlim)
        plt.title("T : {}".format(T))
        plt.savefig("figs/mean/{:03}.png".format(j))
        plt.clf()

def plot_hist_3D(f,xlim=[1.75,2.25],ylim=[0,4E6]):
    E, n, T=load(f)
    #print(rebined)

    #ax.bar(x, y, zs=z, zdir='y', alpha=0.8)
    print("E",E[:10])
    print("n",n[:10])
    ax.plot(E, n, T, alpha=0.8)
 
def get_data(regex=None):
    if regex is None:
        try :
            E = np.load('E.npy')
            c = np.load('c.npy')
            T = np.load('T.npy')
            return E, c, T
        except :
            pass      
    E, c, T = load_3D(regex)
    np.save('E.npy',E)
    np.save('c.npy',c)
    np.save('T.npy',T)
    return E, c, T

def plot_3D(E, c, T):
    fig = plt.figure(figsize=(10,8)) 
    ax = fig.add_subplot(111, projection='3d')
    for i in range(E.shape[0]):
        ax.plot(E[i], c[i], T[i], zdir='y', alpha=0.8)
    x,y,z=ax.get_xbound(), ax.get_ybound(), ax.get_zbound()
    ax.set_xlim(x)
    ax.set_ylim(z)
    ax.set_zlim(y)
    ax.set_xlabel('E')
    ax.set_ylabel('T')
    ax.set_zlabel('histogramme')
    plt.savefig("plot_hist_3D_{}.png".format(np.random.randint(0,10000)))

plot_all_mean_hist()
raise Exception

plot_all_quad_hist()
raise Exception

for f in sorted(files):
    plot_hist(f)
raise Exception

# plot histogramme 3D pour chaque dossier
for i in ['0','1','2','3']: 
    E,c,T = get_data(i+'/*.histo')
    plot_3D(E,c,T)
plt.show()
raise Exception









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

    filenames = np.array(glob.glob(basename))
    nFile = filenames.size


    
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

