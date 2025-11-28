#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:38:40 2023

@author: dangyao
"""
import numpy as np

name = np.loadtxt('station.txt',usecols=[0],dtype=str,unpack=True)
data = np.loadtxt('station.txt',usecols=[1,2,3],dtype=float,unpack=False)

for i in range(data.shape[0]-1):
    for j in range(i+1, data.shape[0]):
        length = np.sqrt((data[i][0]-data[j][0])**2+(data[i][1]-data[j][1])**2+(data[i][2]-data[j][2])**2)
        if length <= 1000:
            print(name[i]+'-'+name[j])