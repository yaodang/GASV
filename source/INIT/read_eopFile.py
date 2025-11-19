#!/usr/bin/env python3

"""
eop_choice(filename): main subroutine
"""

import os, math
import numpy as np
import sys

from COMMON.time_transfer import leap_second

sys.path.append("..//")
from COMMON import *


def read_eop(filename, MJDObs):
    """
    Choice which eop file to read
    ---------------------
    input: 
        filename: the EOP file name
        MJDObs  : the session observe epoch
    output: 
        MJD     : Modified Julian Date
        eop     : [MJD,XP,YP,UT1],[ , rad, rad, s]
    ---------------------
    """
    as2rad = math.pi/180/3600

    if not os.path.exists(filename):
        sys.stderr.write('Error: The EOP file not exist!')
        sys.exit()

    if 'c04' in filename.lower():
        [MJD,XP,YP,UT1,DX,DY] = read_C04(filename)
    elif 'usno' in filename.lower():
        [MJD,XP,YP,UT1,DX,DY] = read_USNO(filename)
    elif 'finals_all' in filename.lower():
        [MJD,XP,YP,UT1,DX,DY] = read_IERSFinals(filename)
    else:
        [MJD,XP,YP,UT1,DX,DY] = read_other(filename)
        # sys.stderr.write('Error: The EOP file not in C04 or USNO format!')
        # sys.exit()
        
    XP = XP * as2rad
    YP = YP * as2rad
    DX = DX * as2rad
    DY = DY * as2rad
    
    posit = find_MJD(MJD, MJDObs)
    UT1New = processLeap(posit, MJD, UT1[posit[0]:posit[1]])

    eop = EOP(MJD[posit[0]:posit[1]],XP[posit[0]:posit[1]],YP[posit[0]:posit[1]],\
              UT1New,DX[posit[0]:posit[1]],DY[posit[0]:posit[1]])
    
    return eop

        
def read_C04(filename):
    """
    Read the IERS C04 file
    ---------------------
    input: 
        filename: the C04 EOP file name
    output: 
        MJD     : Modified Julian Date
        XP, YP  : pole, as
        UT1     : UT1-UTC, s
    ---------------------
    """
    fid = open(filename,'r')
    lines = fid.readlines()
    fid.close()
    #Find the rows contain 1972 1 1
    skiprow = 0
    for line in lines:
        skiprow = skiprow + 1
        if '1972   1   1' in line:
            break
    if skiprow == len(lines):
        skiprow = 15
    
    text = ''.join(lines[:3])
    if 'EOP (IERS) 14 C04' in text:
        [MJD,XP,YP,UT1,DX,DY] = np.loadtxt(filename, dtype=float, skiprows=skiprow-1, usecols=[3,4,5,6,8,9],unpack=True)
    elif 'EOP (IERS) 20 C04' in text:
        [MJD,XP,YP,UT1,DX,DY] = np.loadtxt(filename, dtype=float, skiprows=skiprow-1, usecols=[4,5,6,7,8,9],unpack=True)
        
    return [MJD,XP,YP,UT1,DX,DY]

def read_USNO(filename):
    """
    Read the USNO EOP file
    ---------------------
    input: 
        filename: the USNO EOP file name
    output: 
        MJD     : Modified Julian Date
        XP, YP  : pole, as
        UT1     : UT1-UTC, s
    ---------------------
    """
    
    [MJD,XP,YP,UT1] = np.loadtxt(filename, dtype=float, skiprows=13, usecols=[0,1,2,3],unpack=True)
    MJD = MJD - 2400000.5
    XP = XP * 0.1
    YP = YP * 0.1
    UT1 = UT1 * 10**-6
    DX = np.zeros(len(XP))
    DY = np.zeros(len(XP))
    
    #leap second correct
    tmu = leap_second(MJD)
    UT1 = UT1 + tmu
    
    return [MJD,XP,YP,UT1,DX,DY]

def read_other(filename):
    """
    Read the other EOP file
    ---------------------
    input: 
        filename: the EOP file name
        the file format should be:
        MJD    XPO     YPO      UT1     DX     DY
        
    """
    [MJD,XP,YP,UT1,DX,DY] = np.loadtxt(filename, comments='#', dtype=float, skiprows=1, usecols=[0,1,2,3,4,5],unpack=True)
    MJD = MJD - 2400000.5
    XP = XP * 0.1
    YP = YP * 0.1
    UT1 = UT1 * 10**-6
    tmu = leap_second(MJD)
    UT1 = UT1 + tmu
    
    return [MJD,XP,YP,UT1,DX,DY]
    
def read_IERSFinals(filename):
    fid = open(filename,'r')
    lines = fid.readlines()
    fid.close()
    
    MJD = []
    XP = []
    YP = []
    UT1 = []
    DX = []
    DY = []
    for i in range(164):
        line = lines[i]
        MJD.append(float(line[7:15]))
        XP.append(float(line[17:27]))
        YP.append(float(line[36:46]))
        UT1.append(float(line[58:68]))
        DX.append(float(line[96:106])*1E-3)
        DY.append(float(line[115:125])*1E-3)
        
    return [np.array(MJD),np.array(XP),np.array(YP),np.array(UT1),np.array(DX),np.array(DY)]
        
    
def find_MJD(MJD, MJDObs):
    """
    Get eht position of the MJDObs -+5 days
    ---------------------
    input: 
        MJD       : from the apriori eop file
        MJDObs    : the session observe epoch
    output: 
        MJDPosit  : 
    ---------------------
    """
    maxMJD = math.ceil(max(MJDObs)) + 6
    minMJD = math.floor(min(MJDObs)) - 5
    
    temp1 = np.where(MJD <= minMJD)
    temp2 = np.where(MJD >= maxMJD)
    
    if not (any(temp1[0]) and any(temp2[0])):
        sys.stderr.write('Error: No EOP data available for observation epochs (-+ 5days)!')
        sys.exit()
    
    return np.array([temp1[0][-1],temp2[0][0]])

    
def processLeap(posit,MJD,UT1):
    leap = leap_second(MJD[posit[0]:posit[1]])
    jump = np.where(np.diff(leap)!=0)[0]
    UT1New = UT1 + 0
    if len(jump):
        leapSecond = leap[jump[0]+1] - leap[jump[0]]
        if jump[0] < 5:
            UT1New[:jump[0]] += leapSecond
        else:
            UT1New[jump[0]+1:] -= leapSecond

    return UT1New
