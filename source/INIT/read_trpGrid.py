#!/usr/bin/env python3

import os
import numpy as np
import sys
sys.path.append("..//")
from COMMON import *
        
def readGPT3(Param, path):
    gridData = np.loadtxt(path,comments='%',dtype=float,unpack=False)
    gpt3_grid = GPTGRID()
    gpt3_grid.lat = gridData[:,0]
    gpt3_grid.lon = gridData[:,1]
    gpt3_grid.P = gridData[:,2:7]
    gpt3_grid.T = gridData[:,7:12]
    gpt3_grid.Q = gridData[:,12:17]/1000
    gpt3_grid.dT = gridData[:,17:22]/1000
    gpt3_grid.u = gridData[:,22]
    gpt3_grid.Hs = gridData[:,23]
    gpt3_grid.ah = gridData[:,24:29]/1000
    gpt3_grid.aw = gridData[:,29:34]/1000
    gpt3_grid.la = gridData[:,34:39]
    gpt3_grid.Tm = gridData[:,39:44]
    gpt3_grid.gn_h = gridData[:,44:49]/1000
    gpt3_grid.ge_h = gridData[:,49:54]/1000
    gpt3_grid.gn_w = gridData[:,54:59]/1000
    gpt3_grid.ge_w = gridData[:,59:64]/1000
    
    Param.Setup.trpGrid = gpt3_grid
    
def readVMF3(Param, vmf3Param):
    
    data = np.loadtxt(vmf3Param,unpack=False)
    pvmf3 = VMF3PARAM()
    
    pvmf3.abh = data[0,:].reshape((91,5))
    pvmf3.abw = data[1,:].reshape((91,5))
    pvmf3.ach = data[2,:].reshape((91,5))
    pvmf3.acw = data[3,:].reshape((91,5))
    pvmf3.bbh = data[4,:].reshape((91,5))
    pvmf3.bbw = data[5,:].reshape((91,5))
    pvmf3.bch = data[6,:].reshape((91,5))
    pvmf3.bcw = data[7,:].reshape((91,5))
    
    Param.Setup.vmf3p = pvmf3
    
def read_trpgrid(Param):
    if Param.Map.mapFun == 'GPT3':
        gpt3File = Param.Map.sourceFile[0:Param.Map.sourceFile.rfind('/')+1]+'gpt3_5.grd'
        vmf3Param = Param.Map.sourceFile[0:Param.Map.sourceFile.rfind('/')+1]+'VMF3_param.txt'
        
        if os.path.exists(gpt3File):
            readGPT3(Param, gpt3File)
        else:
            sys.stderr.write('The file %s not exists!'%(gpt3File))
            sys.exit()
            
        if os.path.exists(vmf3Param):
            readVMF3(Param, vmf3Param)
        else:
            sys.stderr.write('The file %s not exists!'%(vmf3Param))
            sys.exit()
            
    #elif Param.Setup.mapFun == 'VM3':
        

        
    
