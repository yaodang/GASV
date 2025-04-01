#!/usr/bin/env python3

import math
import numpy as np
import sys
from scipy import interpolate
np.set_printoptions(precision=15)


from COMMON import *
#from read_eopFile import *


def interpEOP(eopApri,MJDObs,Param,flag):
    """
    Get the EOP at observe epoch
    ---------------------
    input: 
        EOP          : from apairori eop file, [rad,rad,s]
        MJDObs       : session observe epoch
    output: 
        EOPObs       : the EOP of observe epoch, [rad,rad,s]
    ---------------------
    """
    UT1corr = rg_zont2(eopApri.MJD)
    UT1eop = eopApri.UT1-UT1corr
    
    XPObs = lagint4v(eopApri.MJD, eopApri.XP, MJDObs)
    YPObs = lagint4v(eopApri.MJD, eopApri.YP, MJDObs)
    DXObs = lagint4v(eopApri.MJD, eopApri.DX, MJDObs)
    DYObs = lagint4v(eopApri.MJD, eopApri.DY, MJDObs)
    
    UT1Obs = lagint4v(eopApri.MJD, UT1eop, MJDObs)
    
    UT1corr = rg_zont2(MJDObs)
    UT1Obs = UT1Obs + UT1corr
    
    # high frequency correction
    if Param.Map.heopm != 'None' and flag == 1:
        TAB = getTab(Param.Map.heopm)
        corx,cory,corut = eop_hf_eanes(MJDObs,TAB)
    else:
        corx = np.zeros(len(MJDObs))
        cory = np.zeros(len(MJDObs))
        corut = np.zeros(len(MJDObs))

        
    UT1Obs += corut
    XPObs += corx
    YPObs += cory   
    
    eopObs = EOP(MJDObs, XPObs, YPObs, UT1Obs, DXObs, DYObs)
    return eopObs

def rg_zont2(MJD):
    """
    Get the UT1 correction of 5days to 18.6y
    ---------------------
    input: 
        MJD          : EOP MJD
    output: 
        ut1corr      : ut1 correction, s
    ---------------------
    Reference: IERS Conventions 2010
    """
    T = calc_T(MJD)
    alpha = fund_arg(T,0)
    
    #IERS Conventions 2010, table8.1
    #                                              B        C
    TAB = np.array([  [ 1,  0,  2,  2,  2,    -0.0235E0,0.0000E0],\
                      [ 2,  0,  2,  0,  1,    -0.0404E0,0.0000E0],\
                      [ 2,  0,  2,  0,  2,    -0.0987E0,0.0000E0],\
                      [ 0,  0,  2,  2,  1,    -0.0508E0,0.0000E0],\
                      [ 0,  0,  2,  2,  2,    -0.1231E0,0.0000E0],\
                      [ 1,  0,  2,  0,  0,    -0.0385E0,0.0000E0],\
                      [ 1,  0,  2,  0,  1,    -0.4108E0,0.0000E0],\
                      [ 1,  0,  2,  0,  2,    -0.9926E0,0.0000E0],\
                      [ 3,  0,  0,  0,  0,    -0.0179E0,0.0000E0],\
                      [-1,  0,  2,  2,  1,    -0.0818E0,0.0000E0],\
                      [-1,  0,  2,  2,  2,    -0.1974E0,0.0000E0],\
                      [ 1,  0,  0,  2,  0,    -0.0761E0,0.0000E0],\
                      [ 2,  0,  2, -2,  2,     0.0216E0,0.0000E0],\
                      [ 0,  1,  2,  0,  2,     0.0254E0,0.0000E0],\
                      [ 0,  0,  2,  0,  0,    -0.2989E0,0.0000E0],\
                      [ 0,  0,  2,  0,  1,    -3.1873E0,0.2010E0],\
                      [ 0,  0,  2,  0,  2,    -7.8468E0,0.5320E0],\
                      [ 2,  0,  0,  0, -1,     0.0216E0,0.0000E0],\
                      [ 2,  0,  0,  0,  0,    -0.3384E0,0.0000E0],\
                      [ 2,  0,  0,  0,  1,     0.0179E0,0.0000E0],\
                      [ 0, -1,  2,  0,  2,    -0.0244E0,0.0000E0],\
                      [ 0,  0,  0,  2, -1,     0.0470E0,0.0000E0],\
                      [ 0,  0,  0,  2,  0,    -0.7341E0,0.0000E0],\
                      [ 0,  0,  0,  2,  1,    -0.0526E0,0.0000E0],\
                      [ 0, -1,  0,  2,  0,    -0.0508E0,0.0000E0],\
                      [ 1,  0,  2, -2,  1,     0.0498E0,0.0000E0],\
                      [ 1,  0,  2, -2,  2,     0.1006E0,0.0000E0],\
                      [ 1,  1,  0,  0,  0,     0.0395E0,0.0000E0],\
                      [-1,  0,  2,  0,  0,     0.0470E0,0.0000E0],\
                      [-1,  0,  2,  0,  1,     0.1767E0,0.0000E0],\
                      [-1,  0,  2,  0,  2,     0.4352E0,0.0000E0],\
                      [ 1,  0,  0,  0, -1,     0.5339E0,0.0000E0],\
                      [ 1,  0,  0,  0,  0,    -8.4046E0,0.2500E0],\
                      [ 1,  0,  0,  0,  1,     0.5443E0,0.0000E0],\
                      [ 0,  0,  0,  1,  0,     0.0470E0,0.0000E0],\
                      [ 1, -1,  0,  0,  0,    -0.0555E0,0.0000E0],\
                      [-1,  0,  0,  2, -1,     0.1175E0,0.0000E0],\
                      [-1,  0,  0,  2,  0,    -1.8236E0,0.0000E0],\
                      [-1,  0,  0,  2,  1,     0.1316E0,0.0000E0],\
                      [ 1,  0, -2,  2, -1,     0.0179E0,0.0000E0],\
                      [-1, -1,  0,  2,  0,    -0.0855E0,0.0000E0],\
                      [ 0,  2,  2, -2,  2,    -0.0573E0,0.0000E0],\
                      [ 0,  1,  2, -2,  1,     0.0329E0,0.0000E0],\
                      [ 0,  1,  2, -2,  2,    -1.8847E0,0.0000E0],\
                      [ 0,  0,  2, -2,  0,     0.2510E0,0.0000E0],\
                      [ 0,  0,  2, -2,  1,     1.1703E0,0.0000E0],\
                      [ 0,  0,  2, -2,  2,   -49.7174E0,0.4330E0],\
                      [ 0,  2,  0,  0,  0,    -0.1936E0,0.0000E0],\
                      [ 2,  0,  0, -2, -1,     0.0489E0,0.0000E0],\
                      [ 2,  0,  0, -2,  0,    -0.5471E0,0.0000E0],\
                      [ 2,  0,  0, -2,  1,     0.0367E0,0.0000E0],\
                      [ 0, -1,  2, -2,  1,    -0.0451E0,0.0000E0],\
                      [ 0,  1,  0,  0, -1,     0.0921E0,0.0000E0],\
                      [ 0, -1,  2, -2,  2,     0.8281E0,0.0000E0],\
                      [ 0,  1,  0,  0,  0,   -15.8887E0,0.1530E0],\
                      [ 0,  1,  0,  0,  1,    -0.1382E0,0.0000E0],\
                      [ 1,  0,  0, -1,  0,     0.0348E0,0.0000E0],\
                      [ 2,  0, -2,  0,  0,    -0.1372E0,0.0000E0],\
                      [-2,  0,  2,  0,  1,     0.4211E0,0.0000E0],\
                      [-1,  1,  0,  1,  0,    -0.0404E0,0.0000E0],\
                      [ 0,  0,  0,  0,  2,     7.8998E0,0.0000E0],\
                      [ 0,  0,  0,  0,  1, -1617.2681E0,0.0000E0] ])
    #IERS Conventions 2010, chapter8
    phi = TAB[:,0:5]@alpha.T
    ut1corr = TAB[:,5]@np.sin(phi) + TAB[:,6]@np.cos(phi)
    return ut1corr*1.0E-4

def eop_hf_eanes(MJD,TAB):
    """
    Get the xp/yp/ut1 high freqency correction
    ---------------------
    input: 
        MJD          : Modified Julian Date
        TAB          : the high frequency eop table
    output: 
        xphf         : xp hf correction, as
        yphf         : yp hf correction, as
        ut1hf        : ut1 hf correction, s
    ---------------------
    Reference: IERS Conventions 2010
    """
    as2rad = np.pi/180/3600
    T = calc_T(MJD)   
    alpha = fund_arg(T,1)

    phi = TAB[:,0:6]@alpha.T
    phi = np.mod(phi,2*np.pi)
    xphf = TAB[:,7]@np.cos(phi) + TAB[:,6]@np.sin(phi)
    yphf = TAB[:,9]@np.cos(phi) + TAB[:,8]@np.sin(phi)
    ut1hf = TAB[:,11]@np.cos(phi) + TAB[:,10]@np.sin(phi)
    
    corx = xphf*1E-6*as2rad
    cory = yphf*1E-6*as2rad
    corut = ut1hf*1E-6
    
    # correction due to the Earth's triaxiality
    # px, py (recommended by the IERS conventions 2003, chap. 5.4.2) 
    trix,triy,triut = libration(T)
    corx += trix
    cory += triy
    corut += triut
    
    return corx,cory,corut

def fund_arg(T, flag):
    """
    Get fundamental argument of Lunisolar Nutation
    ---------------------
    input: 
        T            : Julian centuries of TDB/TT since J2000, time vector
        flag         : 0 or 1 or 2
    output: 
        alpha        : 
    ---------------------
    Reference: IERS Conventions 2010
    """
    # alpha = np.array([])
    as2rad = np.pi/180/3600
    
    T2 = T**2
    T3 = T**3
    T4 = T**4
    
    
    a1 = ( 485868.249036 + 1717915923.2178*T +    31.8792*T2 +    0.051635*T3 + (-0.00024470)*T4).reshape(len(T),1)
    a2 = (1287104.793048 +  129596581.0481*T +  (-0.5532)*T2 +    0.000136*T3 + (-0.00001149)*T4).reshape(len(T),1)
    a3 = ( 335779.526232 + 1739527262.8478*T + (-12.7512)*T2 + (-0.001037)*T3 +    0.00000417*T4).reshape(len(T),1)
    a4 = (1072260.703692 + 1602961601.2090*T +  (-6.3706)*T2 +    0.006593*T3 + (-0.00003169)*T4).reshape(len(T),1)
    a5 = ( 450160.398036 + (-6962890.5431)*T +     7.4722*T2 +    0.007702*T3 + (-0.00005939)*T4).reshape(len(T),1)
    
    a1 = np.mod(a1,1296000)*as2rad
    a2 = np.mod(a2,1296000)*as2rad
    a3 = np.mod(a3,1296000)*as2rad
    a4 = np.mod(a4,1296000)*as2rad
    a5 = np.mod(a5,1296000)*as2rad
    
    if flag == 1:
        a0 = ((67310.54841 + (876600*3600 + 8640184.812866)*T + 0.093104*T2 + (-6.2E-6)*T3)*15+648000).reshape(len(T),1)
        a0 = np.mod(a0,1296000)*as2rad
        alpha = np.hstack((a0,a1,a2,a3,a4,a5))
    elif flag == 0:
        alpha = np.hstack((a1,a2,a3,a4,a5))
    elif flag == 2:
        a6  = (4.402608842E0 + 2608.7903141574E0 * T).reshape(len(T),1)
        a7  = (3.176146697E0 + 1021.3285546211E0 * T).reshape(len(T),1)
        a8  = (1.753470314E0 +  628.3075849991E0 * T).reshape(len(T),1)
        a9  = (6.203480913E0 +  334.0612426700E0 * T).reshape(len(T),1)
        a10 = (0.599546497E0 +   52.9690962641E0 * T).reshape(len(T),1)
        a11 = (0.874016757E0 +   21.3299104960E0 * T).reshape(len(T),1)
        a12 = (5.481293872E0 +    7.4781598567E0 * T).reshape(len(T),1)
        a13 = (5.311886287E0 +    3.8133035638E0 * T).reshape(len(T),1)
        a14 = (0.024381750E0 * T +    0.00000538691E0 * T2).reshape(len(T),1)
        alpha = np.hstack((a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14))
        
        
    return np.mod(alpha,2*np.pi)

def libration(T):
    '''
    pole Reference: Conventions 5.5.1
    UT1 Reference: Conventions 5.5.3
    '''
    as2rad = np.pi/180/3600
    narg_ut = np.array([[2,-2, 0,-2, 0,-2],\
                        [2, 0, 0,-2,-2,-2],\
                        [2,-1, 0,-2, 0,-2],\
                        [2, 1, 0,-2,-2,-2],\
                        [2, 0, 0,-2, 0,-1],\
                        [2, 0, 0,-2, 0,-2],\
                        [2, 1, 0,-2, 0,-2],\
                        [2, 0,-1,-2, 2,-2],\
                        [2, 0, 0,-2, 2,-2],\
                        [2, 0, 0, 0, 0, 0],\
                        [2, 0, 0, 0, 0,-1]])
    narg_pole = np.array([[1,-1, 0,-2, 0,-1],\
                          [1,-1, 0,-2, 0,-2],\
                          [1, 1, 0,-2,-2,-2],\
                          [1, 0, 0,-2, 0,-1],\
                          [1, 0, 0,-2, 0,-2],\
                          [1,-1, 0, 0, 0, 0],\
                          [1, 0, 0,-2, 2,-2],\
                          [1, 0, 0, 0, 0, 0],\
                          [1, 0, 0, 0, 0,-1],\
                          [1, 1, 0, 0, 0, 0]])
                           
    coeff_ut = np.array([[ 0.05, -0.03],\
                         [ 0.06, -0.03],\
                         [ 0.35, -0.20],\
                         [ 0.07, -0.04],\
                         [-0.07,  0.04],\
                         [ 1.75, -1.01],\
                         [-0.05,  0.03],\
                         [ 0.05, -0.03],\
                         [ 0.76, -0.44],\
                         [ 0.21, -0.12],\
                         [ 0.06, -0.04]])
        
    coeff_pole = np.array([[  -.4,   .3,   -.3,  -.4],\
                           [-2.3,  1.3,  -1.3, -2.3],\
                           [-.4,   .3,   -.3,  -.4],\
                           [-2.1,  1.2,  -1.2, -2.1],\
                           [-11.4,  6.5,  -6.5,-11.4],\
                           [.8,  -.5,    .5,   .8],\
                           [-4.8,  2.7,  -2.7, -4.8],\
                           [14.3, -8.2,   8.2, 14.3],\
                           [1.9, -1.1,   1.1,  1.9],\
                           [.8,  -.4,    .4,   .8]])
        
    arg = fund_arg(T, 1)
    
    agt_ut = narg_ut@arg.T
    agt_pole = narg_pole@arg.T
    agt_ut = np.mod(agt_ut, 2*np.pi)
    agt_pole = np.mod(agt_pole, 2*np.pi)
    
    cor_x = (np.cos(agt_pole).T@coeff_pole[:,1] + np.sin(agt_pole).T@coeff_pole[:,0])*1E-6*as2rad
    cor_y = (np.cos(agt_pole).T@coeff_pole[:,3] + np.sin(agt_pole).T@coeff_pole[:,2])*1E-6*as2rad
    cor_ut = (np.cos(agt_ut).T@coeff_ut[:,1] + np.sin(agt_ut).T@coeff_ut[:,0])*1E-6
    
    return cor_x,cor_y,cor_ut
    
def getTab(module):
    if module == 'Desai':
        TAB = np.array( [[1,-2, 0,-2,-2,-2,  -0.11,   0.24,  -0.24,  -0.11,   0.07,  -0.01],\
                         [1, 0, 0,-2,-4,-2,  -0.07,   0.15,  -0.15,  -0.07,   0.04,  -0.01],\
                         [1,-3, 0,-2, 0,-1,  -0.03,   0.10,  -0.10,  -0.03,   0.03,  -0.01],\
                         [1,-3, 0,-2, 0,-2,  -0.16,   0.54,  -0.54,  -0.16,   0.14,  -0.03],\
                         [1,-1, 0,-2,-2,-1,  -0.07,   0.26,  -0.26,  -0.07,   0.07,  -0.02],\
                         [1,-1, 0,-2,-2,-2,  -0.37,   1.40,  -1.40,  -0.37,   0.35,  -0.08],\
                         [1,-1, 1,-2,-2,-2,  -0.03,   0.10,  -0.10,  -0.03,   0.03,  -0.01],\
                         [1, 1, 0,-2,-4,-2,  -0.06,   0.27,  -0.27,  -0.06,   0.06,  -0.02],\
                         [1,-2, 0,-2, 0,-1,  -0.04,   0.83,  -0.83,  -0.04,   0.18,  -0.06],\
                         [1,-2, 0,-2, 0,-2,  -0.19,   4.41,  -4.41,  -0.19,   0.94,  -0.32],\
                         [1, 0, 0,-2,-2,-1,  -0.01,   0.99,  -0.99,  -0.01,   0.20,  -0.07],\
                         [1, 0, 0,-2,-2,-2,  -0.03,   5.24,  -5.24,  -0.03,   1.08,  -0.40],\
                         [1, 0, 1,-2,-2,-2,   0.01,   0.35,  -0.35,   0.01,   0.07,  -0.03],\
                         [1, 2, 0,-2,-4,-2,   0.00,   0.16,  -0.16,   0.00,   0.03,  -0.01],\
                         [1,-3, 0,-2, 2,-2,  -0.02,  -0.09,   0.09,  -0.02,  -0.02,   0.01],\
                         [1,-1,-1,-2, 0,-2,  -0.05,  -0.25,   0.25,  -0.05,  -0.04,   0.02],\
                         [1, 1, 0,-4, 0,-2,  -0.03,  -0.11,   0.11,  -0.03,  -0.02,   0.01],\
                         [1,-1, 0,-2, 0, 0,  -0.04,  -0.17,   0.17,  -0.04,  -0.03,   0.01],\
                         [1,-1, 0,-2, 0,-1,   1.33,   5.46,  -5.46,   1.33,   0.92,  -0.49],\
                         [1,-1, 0,-2, 0,-2,   7.08,  28.95, -28.95,   7.08,   4.88,  -2.58],\
                         [1, 0, 0,-2,-1,-2,  -0.04,  -0.15,   0.15,  -0.04,  -0.03,   0.01],\
                         [1,-1, 1,-2, 0,-2,   0.07,   0.27,  -0.27,   0.07,   0.04,  -0.02],\
                         [1, 1, 0,-2,-2,-1,   0.29,   1.01,  -1.01,   0.29,   0.17,  -0.09],\
                         [1, 1, 0,-2,-2,-2,   1.53,   5.38,  -5.38,   1.53,   0.88,  -0.49],\
                         [1,-1, 0, 0,-2, 0,  -0.09,  -0.31,   0.31,  -0.09,  -0.05,   0.03],\
                         [1,-1, 0, 0,-2,-1,   0.03,   0.10,  -0.10,   0.03,   0.02,  -0.01],\
                         [1, 1, 1,-2,-2,-2,   0.07,   0.24,  -0.24,   0.07,   0.04,  -0.02],\
                         [1,-2, 0,-2, 2,-2,  -0.20,  -0.39,   0.39,  -0.20,  -0.05,   0.04],\
                         [1, 0,-1,-2, 0,-2,  -0.23,  -0.44,   0.44,  -0.23,  -0.06,   0.04],\
                         [1, 0, 0,-2, 0, 0,  -0.39,  -0.73,   0.73,  -0.39,  -0.09,   0.07],\
                         [1, 0, 0,-2, 0,-1,  12.84,  23.85, -23.85,  12.84,   3.06,  -2.37],\
                         [1, 0, 0,-2, 0,-2,  68.16, 126.32,-126.32,  68.16,  16.18, -12.55],\
                         [1,-2, 0, 0, 0, 0,  -0.44,  -0.81,   0.81,  -0.44,  -0.10,   0.08],\
                         [1,-2, 0, 0, 0,-1,  -0.07,  -0.13,   0.13,  -0.07,  -0.02,   0.01],\
                         [1, 0, 1,-2, 0,-2,   0.21,   0.38,  -0.38,   0.21,   0.05,  -0.04],\
                         [1, 0, 0, 0,-2, 0,  -0.93,  -1.60,   1.60,  -0.93,  -0.20,   0.16],\
                         [1, 0, 0, 0,-2,-1,   0.20,   0.35,  -0.35,   0.20,   0.04,  -0.03],\
                         [1, 0, 1, 0,-2, 0,  -0.06,  -0.10,   0.10,  -0.06,  -0.01,   0.01],\
                         [1,-1, 0,-2, 2,-1,  -0.13,  -0.18,   0.18,  -0.13,  -0.02,   0.02],\
                         [1,-1, 0,-2, 2,-2,  -0.59,  -0.79,   0.79,  -0.59,  -0.08,   0.08],\
                         [1, 1, 0,-2, 0,-1,  -0.42,  -0.55,   0.55,  -0.42,  -0.06,   0.05],\
                         [1, 1, 0,-2, 0,-2,  -2.26,  -2.96,   2.96,  -2.26,  -0.31,   0.29],\
                         [1,-1, 0, 0, 0, 1,   0.18,   0.24,  -0.24,   0.18,   0.02,  -0.02],\
                         [1,-1, 0, 0, 0, 0,  -6.28,  -8.22,   8.22,  -6.28,  -0.86,   0.79],\
                         [1,-1, 0, 0, 0,-1,  -1.26,  -1.65,   1.65,  -1.26,  -0.17,   0.16],\
                         [1, 1, 0, 0,-2, 0,  -1.20,  -1.54,   1.54,  -1.20,  -0.16,   0.15],\
                         [1, 1, 0, 0,-2,-1,  -0.26,  -0.34,   0.34,  -0.26,  -0.04,   0.03],\
                         [1, 0,-2,-2, 2,-2,   0.08,   0.10,  -0.10,   0.08,   0.01,  -0.01],\
                         [1, 0,-1,-2, 2,-2,   2.02,   2.55,  -2.55,   2.02,   0.29,  -0.21],\
                         [1, 0, 0,-2, 2,-1,  -0.38,  -0.49,   0.49,  -0.38,  -0.06,   0.04],\
                         [1, 0, 0,-2, 2,-2,  30.11,  42.73, -42.73,  30.11,   5.22,  -3.08],\
                         [1, 0, 1,-2, 2,-2,  -0.28,  -0.36,   0.36,  -0.28,  -0.04,   0.03],\
                         [1, 0,-1, 0, 0, 0,  -0.80,  -1.03,   1.03,  -0.80,  -0.12,   0.08],\
                         [1, 0, 0, 0, 0, 1,   2.03,   2.65,  -2.65,   2.03,   0.32,  -0.20],\
                         [1, 0, 0, 0, 0, 0,-102.68,-134.45, 134.45,-102.68, -16.29,   9.95],\
                         [1, 0, 0, 0, 0,-1, -13.97, -18.30,  18.30, -13.97,  -2.22,   1.35],\
                         [1, 0, 0, 0, 0,-2,   0.30,   0.39,  -0.39,   0.30,   0.05,  -0.03],\
                         [1, 0, 1, 0, 0, 0,  -0.49,  -0.65,   0.65,  -0.49,  -0.08,   0.05],\
                         [1, 0, 0, 2,-2, 2,  -1.25,  -1.70,   1.70,  -1.25,  -0.22,   0.12],\
                         [1, 0, 1, 2,-2, 2,  -0.07,  -0.10,   0.10,  -0.07,  -0.01,   0.01],\
                         [1,-1, 0, 0, 2, 0,  -0.65,  -1.30,   1.30,  -0.65,  -0.23,   0.05],\
                         [1,-1, 0, 0, 2,-1,  -0.13,  -0.26,   0.26,  -0.13,  -0.05,   0.01],\
                         [1, 1, 0, 0, 0, 1,   0.09,   0.20,  -0.20,   0.09,   0.04,  -0.01],\
                         [1, 1, 0, 0, 0, 0,  -3.01,  -6.81,   6.81,  -3.01,  -1.26,   0.24],\
                         [1, 1, 0, 0, 0,-1,  -0.60,  -1.35,   1.35,  -0.60,  -0.25,   0.05],\
                         [1,-1, 0, 2, 0, 2,   0.05,   0.10,  -0.10,   0.05,   0.02,   0.00],\
                         [1, 0,-1, 0, 2, 0,   0.00,  -0.08,   0.08,   0.00,  -0.02,   0.00],\
                         [1, 0, 0, 0, 2, 0,  -0.01,  -1.21,   1.21,  -0.01,  -0.31,   0.00],\
                         [1, 0, 0, 0, 2,-1,   0.00,  -0.24,   0.24,   0.00,  -0.06,   0.00],\
                         [1, 2, 0, 0, 0, 0,   0.03,  -0.61,   0.61,   0.03,  -0.16,   0.00],\
                         [1, 2, 0, 0, 0,-1,   0.01,  -0.12,   0.12,   0.01,  -0.03,   0.00],\
                         [1, 0, 0, 2, 0, 2,   0.27,  -4.09,   4.09,   0.27,  -1.10,  -0.01],\
                         [1, 0, 0, 2, 0, 1,   0.18,  -2.62,   2.62,   0.18,  -0.71,  -0.01],\
                         [1, 0, 0, 2, 0, 0,   0.04,  -0.55,   0.55,   0.04,  -0.15,   0.00],\
                         [1, 1, 0, 0, 2, 0,   0.10,  -0.23,   0.23,   0.10,  -0.07,   0.00],\
                         [1,-1, 0, 2, 2, 2,   0.08,  -0.17,   0.17,   0.08,  -0.06,   0.00],\
                         [1,-1, 0, 2, 2, 1,   0.05,  -0.11,   0.11,   0.05,  -0.04,   0.00],\
                         [1, 3, 0, 0, 0, 0,   0.03,  -0.06,   0.06,   0.03,  -0.02,   0.00],\
                         [1, 1, 0, 2, 0, 2,   0.45,  -0.93,   0.93,   0.45,  -0.31,  -0.02],\
                         [1, 1, 0, 2, 0, 1,   0.29,  -0.60,   0.60,   0.29,  -0.20,  -0.01],\
                         [1, 1, 0, 2, 0, 0,   0.06,  -0.13,   0.13,   0.06,  -0.04,   0.00],\
                         [1, 0, 0, 2, 2, 2,   0.12,  -0.18,   0.18,   0.12,  -0.06,   0.00],\
                         [1, 0, 0, 2, 2, 1,   0.08,  -0.11,   0.11,   0.08,  -0.04,   0.00],\
                         [1, 2, 0, 2, 0, 2,   0.11,  -0.15,   0.15,   0.11,  -0.05,   0.00],\
                         [1, 2, 0, 2, 0, 1,   0.07,  -0.10,   0.10,   0.07,  -0.03,   0.00],\
                         [1, 1, 0, 2, 2, 2,   0.04,  -0.05,   0.05,   0.04,  -0.02,   0.00],\
                         [2,-4, 0,-2, 0,-2,  -0.01,   0.04,   0.09,   0.01,  -0.01,   0.00],\
                         [2,-2, 0,-2,-2,-2,  -0.07,   0.15,   0.36,   0.06,  -0.04,   0.00],\
                         [2, 0, 0,-2,-4,-2,  -0.05,   0.08,   0.21,   0.04,  -0.03,   0.00],\
                         [2,-3, 0,-2, 0,-2,  -0.35,   0.13,   0.60,   0.22,  -0.09,  -0.01],\
                         [2,-1, 0,-2,-2,-2,  -0.98,   0.25,   1.46,   0.61,  -0.22,  -0.03],\
                         [2,-1, 1,-2,-2,-2,  -0.08,   0.02,   0.11,   0.05,  -0.02,   0.00],\
                         [2, 1, 0,-2,-4,-2,  -0.20,   0.03,   0.26,   0.12,  -0.04,  -0.01],\
                         [2,-2,-1,-2, 0,-2,   0.07,   0.01,  -0.04,  -0.04,   0.01,   0.00],\
                         [2,-2, 0,-2, 0,-1,   0.19,   0.02,  -0.12,  -0.11,   0.02,   0.01],\
                         [2,-2, 0,-2, 0,-2,  -5.17,  -0.50,   3.14,   2.97,  -0.64,  -0.18],\
                         [2, 0,-1,-2,-2,-2,   0.09,   0.01,  -0.05,  -0.05,   0.01,   0.00],\
                         [2,-2, 1,-2, 0,-2,  -0.08,  -0.01,   0.05,   0.05,  -0.01,   0.00],\
                         [2, 0, 0,-2,-2,-1,   0.25,   0.03,  -0.13,  -0.14,   0.03,   0.01],\
                         [2, 0, 0,-2,-2,-2,  -6.57,  -0.79,   3.49,   3.76,  -0.75,  -0.23],\
                         [2, 0, 1,-2,-2,-2,  -0.46,  -0.06,   0.22,   0.26,  -0.05,  -0.02],\
                         [2, 2, 0,-2,-4,-2,  -0.21,  -0.03,   0.10,   0.12,  -0.02,  -0.01],\
                         [2,-3, 0,-2, 2,-2,   0.17,   0.03,  -0.04,  -0.09,   0.01,   0.01],\
                         [2,-1,-1,-2, 0,-2,   0.44,   0.07,  -0.11,  -0.25,   0.03,   0.01],\
                         [2, 1, 0,-4, 0,-2,   0.20,   0.03,  -0.05,  -0.12,   0.01,   0.01],\
                         [2,-1, 0,-2, 0,-1,   1.98,   0.33,  -0.47,  -1.13,   0.14,   0.06],\
                         [2,-1, 0,-2, 0,-2, -53.18,  -8.81,  12.56,  30.30,  -3.84,  -1.64],\
                         [2, 1,-1,-2,-2,-2,   0.10,   0.02,  -0.02,  -0.06,   0.01,   0.00],\
                         [2, 0, 0,-2,-1,-2,   0.29,   0.05,  -0.07,  -0.17,   0.02,   0.01],\
                         [2,-1, 1,-2, 0,-2,  -0.51,  -0.08,   0.11,   0.29,  -0.04,  -0.02],\
                         [2, 1, 0,-2,-2,-1,   0.39,   0.06,  -0.08,  -0.22,   0.03,   0.01],\
                         [2, 1, 0,-2,-2,-2, -10.40,  -1.68,   2.20,   5.94,  -0.71,  -0.31],\
                         [2, 1, 1,-2,-2,-2,  -0.49,  -0.08,   0.10,   0.28,  -0.03,  -0.01],\
                         [2, 0, 0,-4, 2,-2,   0.14,   0.01,  -0.02,  -0.08,   0.01,   0.00],\
                         [2,-2, 0,-2, 2,-2,   0.97,   0.10,  -0.14,  -0.56,   0.05,   0.02],\
                         [2, 0,-1,-2, 0,-2,   1.12,   0.11,  -0.16,  -0.65,   0.06,   0.03],\
                         [2, 0, 0,-2, 0, 0,  -0.17,  -0.02,   0.02,   0.10,  -0.01,   0.00],\
                         [2, 0, 0,-2, 0,-1,  12.19,   1.08,  -1.74,  -7.14,   0.63,   0.30],\
                         [2, 0, 0,-2, 0,-2,-326.96, -28.72,  46.64, 191.61, -16.94,  -8.11],\
                         [2,-2, 0, 0, 0, 0,  -0.19,  -0.02,   0.03,   0.11,  -0.01,   0.00],\
                         [2, 0, 1,-2, 0,-2,  -1.00,  -0.08,   0.14,   0.59,  -0.05,  -0.02],\
                         [2, 2, 0,-2,-2,-2,   0.19,   0.01,  -0.03,  -0.11,   0.01,   0.00],\
                         [2, 0, 0, 0,-2, 0,  -0.39,  -0.03,   0.06,   0.23,  -0.02,  -0.01],\
                         [2, 0, 0, 0,-2,-1,   0.19,   0.01,  -0.03,  -0.11,   0.01,   0.00],\
                         [2,-1,-1,-2, 2,-2,   0.12,   0.00,  -0.02,  -0.07,   0.01,   0.00],\
                         [2,-1, 0,-2, 2,-1,  -0.11,   0.01,   0.02,   0.07,  -0.01,   0.00],\
                         [2,-1, 0,-2, 2,-2,   2.52,  -0.14,  -0.48,  -1.54,   0.12,   0.05],\
                         [2, 1, 0,-2, 0,-1,  -0.35,   0.03,   0.07,   0.22,  -0.02,  -0.01],\
                         [2, 1, 0,-2, 0,-2,   9.66,  -0.81,  -2.00,  -5.95,   0.46,   0.16],\
                         [2,-1, 0, 0, 0, 0,  -2.42,   0.21,   0.51,   1.49,  -0.12,  -0.04],\
                         [2,-1, 0, 0, 0,-1,  -1.07,   0.09,   0.22,   0.66,  -0.05,  -0.02],\
                         [2,-1, 0, 0, 0,-2,  -0.15,   0.01,   0.03,   0.09,  -0.01,   0.00],\
                         [2, 1, 0, 0,-2, 0,  -0.46,   0.05,   0.11,   0.29,  -0.02,  -0.01],\
                         [2, 1, 0, 0,-2,-1,  -0.22,   0.03,   0.05,   0.14,  -0.01,   0.00],\
                         [2, 0,-2,-2, 2,-2,  -0.36,   0.10,   0.12,   0.23,  -0.02,   0.00],\
                         [2, 0,-1,-2, 2,-2,  -8.89,   2.57,   3.20,   5.78,  -0.49,  -0.08],\
                         [2, 0, 0,-2, 2,-1,  -0.34,   0.11,   0.13,   0.22,  -0.02,   0.00],\
                         [2, 0, 0,-2, 2,-2,-134.55,  69.53,  70.34,  85.37,  -8.44,  -0.71],\
                         [2, 0, 1,-2, 2,-2,   1.25,  -0.42,  -0.50,  -0.82,   0.07,   0.01],\
                         [2, 0,-1, 0, 0, 0,  -0.32,   0.11,   0.13,   0.21,  -0.02,   0.00],\
                         [2, 0, 0, 0, 0, 1,   0.52,  -0.19,  -0.22,  -0.34,   0.03,   0.00],\
                         [2, 0, 0, 0, 0, 0, -40.28,  14.62,  17.05,  26.66,  -2.37,  -0.27],\
                         [2, 0, 0, 0, 0,-1, -12.00,   4.37,   5.09,   7.95,  -0.71,  -0.08],\
                         [2, 0, 0, 0, 0,-2,  -1.30,   0.48,   0.55,   0.86,  -0.08,  -0.01],\
                         [2, 0, 1, 0, 0, 0,  -0.31,   0.12,   0.14,   0.21,  -0.02,   0.00],\
                         [2, 0, 0, 2,-2, 2,  -0.27,   0.11,   0.13,   0.18,  -0.02,   0.00],\
                         [2,-1, 0, 0, 2, 0,  -0.37,   0.27,   0.28,   0.26,  -0.03,   0.00],\
                         [2,-1, 0, 0, 2,-1,  -0.16,   0.12,   0.12,   0.12,  -0.01,   0.00],\
                         [2, 1, 0, 0, 0, 0,  -1.86,   1.50,   1.58,   1.36,  -0.16,   0.01],\
                         [2, 1, 0, 0, 0,-1,  -0.81,   0.65,   0.69,   0.59,  -0.07,   0.01],\
                         [2, 1, 0, 0, 0,-2,  -0.09,   0.07,   0.08,   0.07,  -0.01,   0.00],\
                         [2, 0, 0, 0, 2, 0,  -0.23,   0.34,   0.36,   0.19,  -0.03,   0.01],\
                         [2, 0, 0, 0, 2,-1,  -0.10,   0.15,   0.15,   0.08,  -0.01,   0.00],\
                         [2, 2, 0, 0, 0, 0,  -0.11,   0.17,   0.19,   0.09,  -0.02,   0.00],\
                         [2, 0, 0, 2, 0, 2,  -0.34,   0.56,   0.59,   0.29,  -0.05,   0.01],\
                         [2, 0, 0, 2, 0, 1,  -0.29,   0.48,   0.51,   0.25,  -0.05,   0.01],\
                         [2, 0, 0, 2, 0, 0,  -0.10,   0.16,   0.17,   0.08,  -0.02,   0.00],\
                         [2, 1, 0, 2, 0, 2,  -0.04,   0.13,   0.14,   0.04,  -0.01,   0.00],\
                         [2, 1, 0, 2, 0, 1,  -0.03,   0.11,   0.12,   0.04,  -0.01,   0.00]])
    else:
        #                                      xp      xp      yp      yp      ut1    ut1
        #                                      sin     cos     sin     cos     sin     cos
        TAB = np.array( [[1,-1, 0,-2,-2,-2,  -0.05,   0.94,  -0.94,  -0.05,  0.396, -0.078],\
                         [1,-2, 0,-2, 0,-1,   0.06,   0.64,  -0.64,   0.06,  0.195, -0.059],\
                         [1,-2, 0,-2, 0,-2,   0.30,   3.42,  -3.42,   0.30,  1.034, -0.314],\
                         [1, 0, 0,-2,-2,-1,   0.08,   0.78,  -0.78,   0.08,  0.224, -0.073],\
                         [1, 0, 0,-2,-2,-2,   0.46,   4.15,  -4.15,   0.45,  1.187, -0.387],\
                         [1,-1, 0,-2, 0,-1,   1.19,   4.96,  -4.96,   1.19,  0.966, -0.474],\
                         [1,-1, 0,-2, 0,-2,   6.24,  26.31, -26.31,   6.23,  5.118, -2.499],\
                         [1, 1, 0,-2,-2,-1,   0.24,   0.94,  -0.94,   0.24,  0.172, -0.090],\
                         [1, 1, 0,-2,-2,-2,   1.28,   4.99,  -4.99,   1.28,  0.911, -0.475],\
                         [1, 0, 0,-2, 0, 0,  -0.28,  -0.77,   0.77,  -0.28, -0.093,  0.070],\
                         [1, 0, 0,-2, 0,-1,   9.22,  25.06, -25.06,   9.22,  3.025, -2.280],\
                         [1, 0, 0,-2, 0,-2,  48.82, 132.91,-132.90,  48.82, 16.020,-12.069],\
                         [1,-2, 0, 0, 0, 0,  -0.32,  -0.86,   0.86,  -0.32, -0.103,  0.078],\
                         [1, 0, 0, 0,-2, 0,  -0.66,  -1.72,   1.72,  -0.66, -0.194,  0.154],\
                         [1,-1, 0,-2, 2,-2,  -0.42,  -0.92,   0.92,  -0.42, -0.083,  0.074],\
                         [1, 1, 0,-2, 0,-1,  -0.30,  -0.64,   0.64,  -0.30, -0.057,  0.050],\
                         [1, 1, 0,-2, 0,-2,  -1.61,  -3.46,   3.46,  -1.61, -0.308,  0.271],\
                         [1,-1, 0, 0, 0, 0,  -4.48,  -9.61,   9.61,  -4.48, -0.856,  0.751],\
                         [1,-1, 0, 0, 0,-1,  -0.90,  -1.93,   1.93,  -0.90, -0.172,  0.151],\
                         [1, 1, 0, 0,-2, 0,  -0.86,  -1.81,   1.81,  -0.86, -0.161,  0.137],\
                         [1, 0,-1,-2, 2,-2,   1.54,   3.03,  -3.03,   1.54,  0.315, -0.189],\
                         [1, 0, 0,-2, 2,-1,  -0.29,  -0.58,   0.58,  -0.29, -0.062,  0.035],\
                         [1, 0, 0,-2, 2,-2,  26.13,  51.25, -51.25,  26.13,  5.512, -3.095],\
                         [1, 0, 1,-2, 2,-2,  -0.22,  -0.42,   0.42,  -0.22, -0.047,  0.025],\
                         [1, 0,-1, 0, 0, 0,  -0.61,  -1.20,   1.20,  -0.61, -0.134,  0.070],\
                         [1, 0, 0, 0, 0, 1,   1.54,   3.00,  -3.00,   1.54,  0.348, -0.171],\
                         [1, 0, 0, 0, 0, 0, -77.48,-151.74, 151.74, -77.48,-17.620,  8.548],\
                         [1, 0, 0, 0, 0,-1, -10.52, -20.56,  20.56, -10.52, -2.392,  1.159],\
                         [1, 0, 0, 0, 0,-2,   0.23,   0.44,  -0.44,   0.23,  0.052, -0.025],\
                         [1, 0, 1, 0, 0, 0,  -0.61,  -1.19,   1.19,  -0.61, -0.144,  0.065],\
                         [1, 0, 0, 2,-2, 2,  -1.09,  -2.11,   2.11,  -1.09, -0.267,  0.111],\
                         [1,-1, 0, 0, 2, 0,  -0.69,  -1.43,   1.43,  -0.69, -0.288,  0.043],\
                         [1, 1, 0, 0, 0, 0,  -3.46,  -7.28,   7.28,  -3.46, -1.610,  0.187],\
                         [1, 1, 0, 0, 0,-1,  -0.69,  -1.44,   1.44,  -0.69, -0.320,  0.037],\
                         [1, 0, 0, 0, 2, 0,  -0.37,  -1.06,   1.06,  -0.37, -0.407, -0.005],\
                         [1, 2, 0, 0, 0, 0,  -0.17,  -0.51,   0.51,  -0.17, -0.213, -0.005],\
                         [1, 0, 0, 2, 0, 2,  -1.10,  -3.42,   3.42,  -1.09, -1.436, -0.037],\
                         [1, 0, 0, 2, 0, 1,  -0.70,  -2.19,   2.19,  -0.70, -0.921, -0.023],\
                         [1, 0, 0, 2, 0, 0,  -0.15,  -0.46,   0.46,  -0.15, -0.193, -0.005],\
                         [1, 1, 0, 2, 0, 2,  -0.03,  -0.59,   0.59,  -0.03, -0.396, -0.024],\
                         [1, 1, 0, 2, 0, 1,  -0.02,  -0.38,   0.38,  -0.02, -0.253, -0.015],\
                         [2,-3, 0,-2, 0,-2,  -0.49,  -0.04,   0.63,   0.24, -0.089, -0.011],\
                         [2,-1, 0,-2,-2,-2,  -1.33,  -0.17,   1.53,   0.68, -0.224, -0.032],\
                         [2,-2, 0,-2, 0,-2,  -6.08,  -1.61,   3.13,   3.35, -0.637, -0.177],\
                         [2, 0, 0,-2,-2,-2,  -7.59,  -2.05,   3.44,   4.23, -0.745, -0.222],\
                         [2, 0, 1,-2,-2,-2,  -0.52,  -0.14,   0.22,   0.29, -0.049, -0.015],\
                         [2,-1,-1,-2, 0,-2,   0.47,   0.11,  -0.10,  -0.27,  0.033,  0.013],\
                         [2,-1, 0,-2, 0,-1,   2.12,   0.49,  -0.41,  -1.23,  0.141,  0.058],\
                         [2,-1, 0,-2, 0,-2, -56.87, -12.93,  11.15,  32.88, -3.795, -1.556],\
                         [2,-1, 1,-2, 0,-2,  -0.54,  -0.12,   0.10,   0.31, -0.035, -0.015],\
                         [2, 1, 0,-2,-2,-2, -11.01,  -2.40,   1.89,   6.41, -0.698, -0.298],\
                         [2, 1, 1,-2,-2,-2,  -0.51,  -0.11,   0.08,   0.30, -0.032, -0.014],\
                         [2,-2, 0,-2, 2,-2,   0.98,   0.11,  -0.11,  -0.58,  0.050,  0.022],\
                         [2, 0,-1,-2, 0,-2,   1.13,   0.11,  -0.13,  -0.67,  0.056,  0.025],\
                         [2, 0, 0,-2, 0,-1,  12.32,   1.00,  -1.41,  -7.31,  0.605,  0.266],\
                         [2, 0, 0,-2, 0,-2,-330.15, -26.96,  37.58, 195.92,-16.195, -7.140],\
                         [2, 0, 1,-2, 0,-2,  -1.01,  -0.07,   0.11,   0.60, -0.049, -0.021],\
                         [2,-1, 0,-2, 2,-2,   2.47,  -0.28,  -0.44,  -1.48,  0.111,  0.034],\
                         [2, 1, 0,-2, 0,-2,   9.40,  -1.44,  -1.88,  -5.65,  0.425,  0.117],\
                         [2,-1, 0, 0, 0, 0,  -2.35,   0.37,   0.47,   1.41, -0.106, -0.029],\
                         [2,-1, 0, 0, 0,-1,  -1.04,   0.17,   0.21,   0.62, -0.047, -0.013],\
                         [2, 0,-1,-2, 2,-2,  -8.51,   3.50,   3.29,   5.11, -0.437, -0.019],\
                         [2, 0, 0,-2, 2,-2,-144.13,  63.56,  59.23,  86.56, -7.547, -0.159],\
                         [2, 0, 1,-2, 2,-2,   1.19,  -0.56,  -0.52,  -0.72,  0.064,  0.000],\
                         [2, 0, 0, 0, 0, 1,   0.49,  -0.25,  -0.23,  -0.29,  0.027, -0.001],\
                         [2, 0, 0, 0, 0, 0, -38.48,  19.14,  17.72,  23.11, -2.104,  0.041],\
                         [2, 0, 0, 0, 0,-1, -11.44,   5.75,   5.32,   6.87, -0.627,  0.015],\
                         [2, 0, 0, 0, 0,-2,  -1.24,   0.63,   0.58,   0.75, -0.068,  0.002],\
                         [2, 1, 0, 0, 0, 0,  -1.77,   1.79,   1.71,   1.04, -0.146,  0.037],\
                         [2, 1, 0, 0, 0,-1,  -0.77,   0.78,   0.75,   0.45, -0.064,  0.017],\
                         [2, 0, 0, 2, 0, 2,  -0.33,   0.62,   0.65,   0.19, -0.049,  0.018]])
    return TAB

def getRate(MJD, eopData, rateMJD):
    '''
    Parameters
    ----------
    MJD : TYPE
        DESCRIPTION.
    eopData : TYPE
        DESCRIPTION.
    rateMJD : TYPE
        DESCRIPTION.

    Returns
    -------
    interp : TYPE
        DESCRIPTION.

    '''
    index = np.where(MJD==np.floor(rateMJD))
    
    poly1d = interpolate.lagrange(MJD[index[0][0]-1:index[0][0]+3], eopData[index[0][0]-1:index[0][0]+3])
    interp = np.polyder(poly1d, 1)(rateMJD)
    return interp        
