# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 16:33:50 2023

@author: yaoda
"""
import numpy as np

sitNum = 46
index = [3,6,11,12]

if len(index) >= 2:
    velZeros = np.zeros(((len(index)-1)*3,sitNum*3))
    
    for ib in range(len(index)-1):
        velZeros[ib*3:(ib+1)*3,index[0]*3:(index[0]+1)*3]=np.eye(3)
        velZeros[ib*3:(ib+1)*3,index[ib+1]*3:(index[ib+1]+1)*3]=-np.eye(3)
