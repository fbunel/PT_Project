#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import glob
from mpl_toolkits.mplot3d import Axes3D

from scipy.interpolate import griddata
#grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
#grid_z0 = griddata(points, values, (grid_x, grid_y), method='cubic',fill_value=0)


def plot_hist_2d(E,c,T):

    grid_x, grid_y = np.mgrid[np.min(T):np.max(T):100j,np.min(E):np.max(E):200j]
    hist_2d = griddata(
        (np.broadcast_to(T[:,None], E.shape).ravel(),E.ravel()),
        c.ravel(),
        (grid_x, grid_y),
        method='linear',fill_value=0)
    plt.figure()
    plt.imshow(hist_2d, origin='lower',extent=[np.min(E),np.max(E),np.min(T),np.max(T)],interpolation='nearest',aspect='auto')
    plt.colorbar()
    plt.savefig("plot_hist_2D_{}.png".format(np.random.randint(0,100000)))

    return hist_2d


def replot_all_hist_2d():
    for i in ['0','1','2','3','mean']:
        hist_2d = np.load('hist_2d_'+i+'.npy')
        if i == 'mean':
           E,T = [np.load("mean_E.npy"),np.load("mean_T.npy")]
        else:   
           E,T = [np.load("{}/E.npy".format(i)),np.load("{}/T.npy".format(i))]

        print('hist_2d_'+i+'.npy')
        plt.figure()
        plt.imshow(hist_2d, origin='lower',extent=[np.min(E),np.max(E),np.min(T),np.max(T)],interpolation='nearest',aspect='auto')
        plt.colorbar()
        plt.title(i)
        plt.savefig("plot_hist_2D_{}_{}.png".format(i,np.random.randint(0,100000)))
    plt.show()


def load_data(regex=None):
    if regex is None:
        E = np.load('E.npy')
        c = np.load('c.npy')
        T = np.load('T.npy')
    else : 
        prefix = regex.split("/")[0]
        E = np.load(prefix+'/E.npy')
        c = np.load(prefix+'/c.npy')
        T = np.load(prefix+'/T.npy')
    return E, c, T
    

if True:
    replot_all_hist_2d()
    raise Exception


if False:
    print("test")
    E,c,T = load_data()
    hist_2d = plot_hist_2d(E,c,T)
    np.save("hist_2d_test.npy",hist_2d)

for i in ['0','1','2','3']: 
    E,c,T = load_data(i+'/*.histo')
    hist_2d = plot_hist_2d(E,c,T)
    np.save("hist_2d_{}.npy".format(i),hist_2d)


E = np.load('mean_E.npy')
c = np.load('mean_c.npy')
T = np.load('mean_T.npy')
hist_2d = plot_hist_2d(E,c,T)
np.save("hist_2d_mean.npy",hist_2d)

plt.show()
raise Exception






