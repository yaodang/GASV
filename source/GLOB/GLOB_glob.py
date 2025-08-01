# -*- coding: utf-8 -*-

import numpy as np

from GLOB.GLOB_init import *
from GLOB.GLOB_constraint import *
from GLOB.GLOB_out import *

def GLOB(Param):
    
    sitAll, souAll, NGlob, bGlob, vtpvSession, numPar = globalPrepareNew(Param)
    #sitAll, souAll, NGlob, bGlob = globalPrepare(Param)
    
    Bcon = makeConstMatrix(sitAll, souAll, Param)
    
    zerosNum = Bcon.shape[0]
    tempN1 = np.hstack((NGlob,Bcon.T))
    tempN2 = np.hstack((Bcon,np.zeros((zerosNum,zerosNum))))
    bGlobc = np.vstack((bGlob,np.zeros((zerosNum,1))))
    NGlobc = np.vstack((tempN1,tempN2))
    
    xout=np.linalg.inv(NGlobc)@bGlobc
    vtpv = vtpvSession - xout.T@bGlobc
    mi = np.sqrt(vtpv/(numPar - len(bGlobc) + Bcon.shape[0]))*np.linalg.inv(NGlobc)
    #v = bGlobc-NGlobc@xout
    #nall = np.hstack((NGlobc,bGlobc))
    # print('R(N)=%d (n=%d)\nR(N,b)=%d (n=%d)'%(np.linalg.matrix_rank(NGlobc),NGlobc.shape[0],\
                    # np.linalg.matrix_rank(nall),nall.shape[0]))
    
    helmert = np.linalg.inv(Bcon@Bcon.T)@Bcon@xout[:Bcon.shape[1],:]
    if Param.Global.station[0] == 'YES':
        writeTRFResult(sitAll,xout,Param)
    if Param.Global.source[0] == 'YES':
        writeCRFResult(sitAll,souAll,xout)

    np.savetxt('NGlob.txt',NGlobc,delimiter=',')
    np.savetxt('bGlob.txt', bGlobc,delimiter=',')
    np.savetxt('Bcon.txt',Bcon,delimiter=',')
    return NGlob, bGlob, sitAll, souAll

def makeConstMatrix(sitAll, souAll, Param):
    
    sitNum = len(sitAll['name'])
    souNum = len(souAll['name'])
    trfConstNum = sum(sitAll['nnrt'])
    crfConstNum = sum(souAll['nnr'])
    
    flag = np.zeros(2,dtype=int)
    Ball = []
    
    # station and velocity constrain
    if trfConstNum > 0:
        Bsv = NNRT2TRF(sitAll,Param)
        
        if Param.Flags.vel[0] == 'YES':
            Bsv = velTieConst(Bsv, sitAll, Param)
            
        if crfConstNum > 0:
            Bsv = np.hstack((Bsv, np.zeros((Bsv.shape[0], souNum*2))))
            
        Ball.append(Bsv)
        flag[0] = 1
    else:
        Ball.append([])
    
    # source constrain
    if crfConstNum > 0:
        Bsou = NNR2CRF(souAll)
        if trfConstNum > 0:
            '''
            if Param.Flags.vel[0] == 'YES':
                Bsou = np.hstack((np.zeros((Bsou.shape[0], sitNum*6)), Bsou))
            else:
                Bsou = np.hstack((np.zeros((Bsou.shape[0], sitNum*3)), Bsou))
            '''
            Bsou = np.hstack((np.zeros((Bsou.shape[0], sum(sitAll['estNum']) * 3)), Bsou))
        
        Ball.append(Bsou)
        flag[1] = 1
    else:
        Ball.append([])
                
    posit = np.where(flag==1)[0]
    if len(posit) >= 1:
        Bcon = Ball[posit[0]]
        
        for i in range(1,len(posit)):
            Bcon = np.vstack((Bcon, Ball[posit[i]]))
    
    return Bcon