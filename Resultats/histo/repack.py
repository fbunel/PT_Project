#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import glob


def load_3D(regex = '1/*.histo',rebin=None):
    #rebin factor:
    if rebin is None:
        n=1
    
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

 
def repack_data(regex=None):    
    E, c, T = load_3D(regex)
    prefix = regex.split("/")[0]
    np.save(prefix+'/E.npy',E)
    np.save(prefix+'/c.npy',c)
    np.save(prefix+'/T.npy',T)
    return E, c, T
    
     
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

input("repack [0123]/*.histo ?")

for i in ['0','1','2','3']: 
    E,c,T = repack_data(i+'/*.histo')

print("repacking done")

