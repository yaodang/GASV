#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:41:13 2023

@author: dangyao
"""

fid = open('color.txt','r')
lines = fid.readlines()
fid.close()

fid = open('plotColor.txt','w')
for i in range(150):
    line = lines[i]
    index = line.index('#')
    fid.writelines("'%s',"%line[index:index+7])
    if (i+1)%10 == 0:
        fid.writelines('\\\n')
fid.close()