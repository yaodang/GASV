#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:43:40 2023

@author: dangyao
"""

import matplotlib.pyplot as plt
import os
import numpy as np
from COMMON.time_transfer import *

def plotResuidal(param, scanInfo, staObs, result):
    """
    Plot and save the resuidal of LSM
    ---------------------
    input:
        param         : 
        scanInfo      : scan struct
        result        : RESULT struct
    output: 
        save the resuidal plot
    ---------------------
    """
    if param.Out.residualPath == 'None':
        return
    print('    plot and save resuidal......')
    '''
    if len(scanInfo.sessionName) == 9:
        year = 2000 + int(scanInfo.sessionName[:2])
    else:
        if '-' in scanInfo.sessionName:
            index = scanInfo.sessionName.index('-')
            if index == 8:
                year = int(scanInfo.sessionName[0:4])
            elif index == 7:
                year = 2000 + int(scanInfo.sessionName[1:3])'''
    year = 2024
    pngPath = os.path.join(param.Out.residualPath,str(year))
    if not os.path.exists(pngPath):
        os.mkdir(pngPath)
    
    useDay = np.floor(scanInfo.scanMJD[-1]) - np.floor(scanInfo.scanMJD[0])
    if useDay == 0:
        xlabel = '%02d.%02d.%4d'%(scanInfo.scanTime[0][2],scanInfo.scanTime[0][1],\
                                scanInfo.scanTime[0][0])
    elif useDay == 1:
        mon1 = getMon(scanInfo.scanTime[0][1])
        mon2 = getMon(scanInfo.scanTime[-1][1])
        xlabel = '%02d.%3s.%4d-%02d.%3s.%4d'%(scanInfo.scanTime[0][2],mon1,scanInfo.scanTime[0][0],\
                                                scanInfo.scanTime[-1][2],mon2,scanInfo.scanTime[-1][0])
    #xnum = np.linspace(0, len(scanInfo.scanMJD)-1, len(scanInfo.scanMJD),dtype=int)
    
    fig = plt.figure(1)
    colors = ['black','red','blue','peru','gold','orange','green','cyan','fuchsia','darkviolet',\
              'burlywood','tan','darkgreen','teal','plums']
        
    colors = ['#e50000','#653700','#ff81c0','#0343df','#15b01a','#7e1e9c','#acc2d9','#56ae57','#b2996e','#a8ff04',\
              '#69d84f','#894585','#70b23f','#d4ffff','#65ab7c','#952e8f','#fcfc81','#a5a391','#388004','#4c9085',\
              '#5e9b8a','#efb435','#d99b82','#0a5f38','#0c06f7','#61de2a','#3778bf','#2242c7','#533cc6','#9bb53c',\
              '#05ffa6','#1f6357','#017374','#0cb577','#ff0789','#afa88b','#08787f','#dd85d7','#a6c875','#a7ffb5',\
              '#c2b709','#e78ea5','#966ebd','#ccad60','#ac86a8','#947e94','#983fb2','#ff63e9','#b2fba5','#63b365',\
              '#8ee53f','#b7e1a1','#ff6f52','#bdf8a3','#d3b683','#fffcc4','#430541','#ffb2d0','#997570','#ad900d',\
              '#c48efd','#507b9c','#7d7103','#fffd78','#da467d','#410200','#c9d179','#fffa86','#5684ae','#6b7c85',\
              '#6f6c0a','#7e4071','#009337','#d0e429','#fff917','#1d5dec','#054907','#b5ce08','#8fb67b','#c8ffb0',\
              '#fdde6c','#ffdf22','#a9be70','#6832e3','#fdb147','#c7ac7d','#fff39a','#850e04','#efc0fe','#40fd14',\
              '#b6c406','#9dff00','#3c4142','#f2ab15','#ac4f06','#c4fe82','#2cfa1f','#9a6200','#ca9bf7','#875f42',\
              '#3a2efe','#fd8d49','#8b3103','#cba560','#698339','#0cdc73','#b75203','#7f8f4e','#26538d','#63a950',\
              '#c87f89','#b1fc99','#ff9a8a','#f6688e','#76fda8','#53fe5c','#4efd54','#a0febf','#7bf2da','#bcf5a6',\
              '#ca6b02','#107ab0','#2138ab','#719f91','#fdb915','#fefcaf','#fcf679','#1d0200','#cb6843','#31668a',\
              '#247afd','#ffffb6','#90fda9','#86a17d','#fddc5c','#78d1b6','#13bbaf','#fb5ffc','#20f986','#ffe36e',\
              '#9d0759','#3a18b1','#c2ff89','#d767ad','#720058','#ffda03','#01c08d','#ac7434','#014600','#9900fa']
    
    index = scanInfo.baseInfo[0].index('X')
    for i in range(len(staObs.mjd)):
        if len(staObs.mjd[i]):
            plt.plot(staObs.mjd[i],result.VReal[index][staObs.oc_nob[i]]*100,color=colors[i],marker='o',linestyle='',label=scanInfo.stationAll[i])

    
    xnum = plt.xticks()
    ynum = plt.yticks()
    xticks = []
    for i in range(len(xnum[0])):
        y,m,d,h,mi,s = mjd2ymdhms(xnum[0][i])
        xticks.append('%02d:%02d'%(h,mi))
    # plt.text(xnum[0][0]+0.0007, ynum[0][-3], 'wrms: %6.1f ps'%result.wrms)
    # plt.text(xnum[0][0]+0.0007, ynum[0][-3]-(ynum[0][-1]-ynum[0][0])*0.1, 'chi : %6.3f'%result.chis)
    

    plt.ylabel('Resuidal / cm')
    plt.xlabel(xlabel)
    # axRang = plt.axis()
    # legendPx = axRang[1] + (axRang[1]-axRang[0])*0.1
    # legendPy = axRang[3] - (axRang[3]-axRang[2])*0.1
    plt.legend(loc='upper right')
    
    plt.xticks(xnum[0].tolist(),xticks)
    plt.savefig(param.Out.residualPath+'/'+str(year)+'/'+scanInfo.sessionName+'.pdf')
    plt.close()
    