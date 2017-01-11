#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import glob






files = glob.glob('*/*.histo')

for f in files : 
    print(f)
    prefix = f.split("/")[0]
    n= int(f.split("/")[1].split(".")[0][5:])
    print(n)
    new_name = "{}/histo{:03}.histo".format(prefix,n)
    
    print(new_name)
    glob.os.rename(f,new_name)
