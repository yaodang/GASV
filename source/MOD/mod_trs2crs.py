#!/usr/bin/env python3

import numpy as np
import time
from multiprocessing import Pool

from MOD import *

np.set_printoptions(precision=15)

def mod_trs2crsn(eop, scanList, parallelFlag):
    as2rad = np.pi/180/3600
    
    T = calc_T(eop.MJD)
    #s'
    ss = -47E-6*T*as2rad
    
    #earth rotation angle
    ut = eop.MJD + eop.UT1/86400
    tu = ut - 51544.5
    frac = ut - np.floor(ut) + 0.5
    fac = 0.00273781191135448
    
    era = 2 * np.pi * (frac + 0.7790572732640 + fac * tu)
    era = np.mod(era, 2*np.pi)
    
    #precession and nutation (IAU2006A)
    [X, Y, S] = mod_iau2006a(T)
    #[X, Y, S] = mod_iau2006a_iers(eop.MJD)
    
    X = X + eop.DX
    Y = Y + eop.DY
    
    poolT2C = Pool(processes=4)
    args_list = []
    
    if parallelFlag == 'YES':
        for i in range(4):
            args = (len(scanList[i]), eop.XP[scanList[i]], eop.YP[scanList[i]], ss[scanList[i]], \
                    era[scanList[i]], X[scanList[i]], Y[scanList[i]], S[scanList[i]])
            args_list.append(args)
            
        results = poolT2C.map(ITRF2ICRF, args_list)
        trs2crs = np.vstack((results[0].trs2crs, results[1].trs2crs,results[2].trs2crs,results[3].trs2crs))
        dr_dxp = np.vstack((results[0].dxp, results[1].dxp,results[2].dxp,results[3].dxp))
        dr_dyp = np.vstack((results[0].dyp, results[1].dyp,results[2].dyp,results[3].dyp))
        dr_dut1 = np.vstack((results[0].dut1, results[1].dut1,results[2].dut1,results[3].dut1))
        dr_ddX = np.vstack((results[0].ddX, results[1].ddX,results[2].ddX,results[3].ddX))
        dr_ddY = np.vstack((results[0].ddY, results[1].ddY,results[2].ddY,results[3].ddY))
        t2c = T2C(trs2crs, dr_dxp, dr_dyp, dr_dut1, dr_ddX, dr_ddY)
    else:
        # allScanNum = len(scanList[0]) + len(scanList[1]) + len(scanList[2]) + len(scanList[3])
        allScanNum = len(scanList)
        args = [allScanNum, eop.XP, eop.YP, ss, era, X, Y, S]
        t2c = ITRF2ICRF(args)
        
    return t2c
    
def ITRF2ICRF(args):
    scanNum, XP, YP, ss, era, X, Y, S = args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7]
    
    trs2crs = np.zeros([scanNum,3,3])
    dr_dxp = np.zeros([scanNum,3,3])
    dr_dyp = np.zeros([scanNum,3,3])
    dr_dut1 = np.zeros([scanNum,3,3])
    dr_ddX = np.zeros([scanNum,3,3])
    dr_ddY = np.zeros([scanNum,3,3])
    
    for i in range(scanNum):
        XY = X[i]**2+Y[i]**2
        
        W = np.dot(np.dot(rotm1([-ss[i]],3),rotm1([XP[i]],2)),rotm1([YP[i]],1))
        R = rotm1(-era[i],3)
        
        E = np.arctan2(Y[i], X[i])
        d = np.arctan2(np.sqrt(XY), np.sqrt(1-XY))
        Q = np.dot(np.dot(np.dot(rotm1(-E,3),rotm1(-d,2)),rotm1(E,3)),rotm1(S[i],3))
    
        trs2crs[i,:,:] = np.dot(np.dot(Q,R),W)
        
        #----------------------------------------------------------------------
        #xp/yp partial
        dW_dxp = np.dot(np.dot(rotm1([-ss[i]],3),drotm1([XP[i]],2)),rotm1([YP[i]],1))
        dW_dyp = np.dot(np.dot(rotm1([-ss[i]],3),rotm1([XP[i]],2)),drotm1([YP[i]],1))
        
        #----------------------------------------------------------------------
        #ut1 partial
        dR_dut1 = drotm1(-era[i],3) * (-1.00273781191135448)
        
        #----------------------------------------------------------------------
        #dX/dY partial
        dE_ddX = -Y[i]/XY
        dd_ddX = X[i]/(np.sqrt(1-XY)*np.sqrt(XY))
        ds_ddX = -Y[i]/2
        
        dE_ddY = X[i]/XY
        dd_ddY = Y[i]/(np.sqrt(1-XY)*np.sqrt(XY))

        ds_ddY = -X[i]/2
        
        dQ_ddX = np.dot(np.dot(np.dot(np.dot(drotm1(-E,3),-dE_ddX),rotm1(-d,2)),rotm1(E,3)),rotm1(S[i],3)) +\
                 np.dot(np.dot(np.dot(np.dot(rotm1(-E,3),drotm1(-d,2)),-dd_ddX),rotm1(E,3)),rotm1(S[i],3))  +\
                 np.dot(np.dot(np.dot(np.dot(rotm1(-E,3),rotm1(-d,2)),drotm1(E,3)),dE_ddX),rotm1(S[i],3))+\
                 np.dot(np.dot(np.dot(np.dot(rotm1(-E,3),rotm1(-d,2)),rotm1(E,3)),drotm1(S[i],3)),ds_ddX)
                 
        dQ_ddY = np.dot(np.dot(np.dot(np.dot(drotm1(-E,3),-dE_ddY),rotm1(-d,2)),rotm1(E,3)),rotm1(S[i],3)) +\
                 np.dot(np.dot(np.dot(np.dot(rotm1(-E,3),drotm1(-d,2)),-dd_ddY),rotm1(E,3)),rotm1(S[i],3))  +\
                 np.dot(np.dot(np.dot(np.dot(rotm1(-E,3),rotm1(-d,2)),drotm1(E,3)),dE_ddY),rotm1(S[i],3))+\
                 np.dot(np.dot(np.dot(np.dot(rotm1(-E,3),rotm1(-d,2)),rotm1(E,3)),drotm1(S[i],3)),ds_ddY)
                 
        dr_dxp[i,:,:] = np.dot(np.dot(Q, R), dW_dxp)
        dr_dyp[i,:,:] = np.dot(np.dot(Q, R), dW_dyp)
        dr_dut1[i,:,:] = np.dot(np.dot(Q,dR_dut1),W)
        dr_ddX[i,:,:] = np.dot(np.dot(dQ_ddX,R),W)
        dr_ddY[i,:,:] = np.dot(np.dot(dQ_ddY,R),W)
        
    t2c = T2C(trs2crs, dr_dxp, dr_dyp, dr_dut1, dr_ddX, dr_ddY)
    return t2c   
         
def rotm(angle, flag):
    
    num = len(angle)
    ca = np.cos(angle)
    sa = np.sin(angle)
    
    zeros = np.zeros([num,3,3])
    
    if flag == 1:
        zeros[:,0,0] = 1
        zeros[:,1,1] = ca
        zeros[:,1,2] = sa
        zeros[:,2,1] = -sa
        zeros[:,2,2] = ca
    elif flag == 2:
        zeros[:,0,0] = ca
        zeros[:,0,2] = -sa
        zeros[:,1,1] = 1
        zeros[:,2,0] = sa
        zeros[:,2,2] = ca
    elif flag == 3:
        zeros[:,0,0] = ca
        zeros[:,0,1] = sa
        zeros[:,1,0] = -sa
        zeros[:,1,1] = ca
        zeros[:,2,2] = 1

    return zeros

def rotm1(angle, flag):
    
    ca = np.cos(angle)
    sa = np.sin(angle)
    
    zeros = np.zeros([3,3])
    
    if flag == 1:
        zeros[0,0] = 1
        zeros[1,1] = ca
        zeros[1,2] = sa
        zeros[2,1] = -sa
        zeros[2,2] = ca
    elif flag == 2:
        zeros[0,0] = ca
        zeros[0,2] = -sa
        zeros[1,1] = 1
        zeros[2,0] = sa
        zeros[2,2] = ca
    elif flag == 3:
        zeros[0,0] = ca
        zeros[0,1] = sa
        zeros[1,0] = -sa
        zeros[1,1] = ca
        zeros[2,2] = 1

    return zeros

def drotm1(angle, flag):
    
    ca = np.cos(angle)
    sa = np.sin(angle)
    
    zeros = np.zeros([3,3])
    
    if flag == 1:
        zeros[1,1] = -sa
        zeros[1,2] = ca
        zeros[2,1] = -ca
        zeros[2,2] = -sa
    elif flag == 2:
        zeros[0,0] = -sa
        zeros[0,2] = -ca
        zeros[2,0] = ca
        zeros[2,2] = -sa
    elif flag == 3:
        zeros[0,0] = -sa
        zeros[0,1] = ca
        zeros[1,0] = -ca
        zeros[1,1] = -sa

    return zeros