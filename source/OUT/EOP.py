#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:40:03 2023

@author: dangyao
"""

import os
import numpy as np
from MOD import *

def writeEOP(Param, scanInfo, result, sessionNum, out):
    if Param.Out.eopPath[0] != 'YES':
        return

    print('    write the eop file......')
    xyzP = out.param.index('xyz') - len(out.param)
    estParamP = np.where(out.estFlag[0:xyzP] == 1)
    
    if len(estParamP[0]) == 0:
        return

    if os.path.isdir(Param.Out.eopPath[1]):
        eopFile = Param.Out.eopPath[1]+'/eop_out.txt'
    else:
        eopFile = Param.Out.eopPath[1]

    lines = writeEOPFileHeader(1)

    expName = []
    epoch = np.array([])
    if os.path.exists(eopFile):
        fileinfo = os.stat(eopFile)
        if fileinfo.st_size != 0:
            fid = open(eopFile, 'r')
            lines = fid.readlines()
            fid.close()

            expName = np.loadtxt(eopFile, comments='*', usecols=[17], dtype=str, unpack=True)
            expName = expName.tolist()
            epoch = np.loadtxt(eopFile, comments='*', usecols=[0], dtype=float, ndmin=1, unpack=True)
    
    eopLine = np.zeros(30).tolist()
    eopLine[0] = scanInfo.refMJD
    
    if Param.Flags.type == 'POLY':
        temp = out.param.index('pmx')
        if out.estFlag[temp] == 1:
            eopLine[1] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            #if Param.Out.fileMode == 'simple':
            #    eopLine[1] = out.estValue[temp]*1E3
            eopLine[6] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('pmy')
        if out.estFlag[temp] == 1:
            eopLine[2] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            #if Param.Out.writeMode == 'simple':
            #    eopLine[2] = out.estValue[temp]*1E3
            eopLine[7] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('ut1')
        if out.estFlag[temp] == 1:
            eopLine[3] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            # eopLine[3] = (out.aprioriValue[temp])*1E-3
            #if Param.Out.writeMode == 'simple':
            #    eopLine[3] = out.estValue[temp]*1E3
            eopLine[8] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('nutx')
        if out.estFlag[temp] == 1:
            eopLine[4] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            eopLine[9] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('nuty')
        if out.estFlag[temp] == 1:
            eopLine[5] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            eopLine[10] = out.formalErr[temp]*1E-3
        
    eopLine[11] = result.wrms
    eopLine[16] = len(scanInfo.Obs2Scan)
    eopLine[17] = scanInfo.expName.lower()
    eopLine[18] = (scanInfo.scanMJD[-1]-scanInfo.scanMJD[0])*24
        
    temp = out.param.index('pmxr')
    if out.estFlag[temp] == 1:
        eopLine[19] = (out.estValue[temp][0] + out.aprioriValue[temp][0])*1E-3
        eopLine[24] = out.formalErr[temp][0]*1E-3

    temp = out.param.index('pmyr')
    if out.estFlag[temp] == 1:
        eopLine[20] = (out.estValue[temp][0] + out.aprioriValue[temp][0])*1E-3
        eopLine[25] = out.formalErr[temp][0]*1E-3    
        
    temp = out.param.index('lod')
    if out.estFlag[temp] == 1:
        eopLine[21] = (out.estValue[temp][0] + out.aprioriValue[temp][0])*1E-3
        eopLine[26] = out.formalErr[temp][0]*1E-3
    
    ns_code = scanInfo.stationCode
    temp = ''
    for sta in range(len(scanInfo.stationAll)):
        # if not scanInfo.stationAll[sta] in scanInfo.noEstSta:
            # temp += ns_code[sta][0]
        temp += ns_code[sta][0]
    
    eopLine[29] = temp
    
    if Param.Flags.type == 'SEGMENT':
        for i in range(len(out.mjd[0])):
            line = '%9s %12.6f %12.1f %12.1f\n'%(Param.Arcs.session[sessionNum], out.mjd[0][i], out.estValue[0][i]*1E3,\
                                                         out.formalErr[0][i]*1E3)
        
    else:
        lineFormat = '%12.6f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f '+\
                    '%10.1f %10.1f %10.1f %10.1f %10.1f %5d %-s %5.2f %12.7f %12.7f %12.7f %12.7f %12.7f '+\
                    '%12.7f %12.7f %12.7f %12.7f %12.7f %s\n'
        line = lineFormat%(eopLine[0],eopLine[1],eopLine[2],eopLine[3],eopLine[4],eopLine[5],eopLine[6],eopLine[7],eopLine[8],\
                        eopLine[9],eopLine[10],eopLine[11],eopLine[12],eopLine[13],eopLine[14],eopLine[15],eopLine[16],\
                        eopLine[17],eopLine[18],eopLine[19],eopLine[20],eopLine[21],eopLine[22],eopLine[23],eopLine[24],\
                        eopLine[25],eopLine[26],eopLine[27],eopLine[28],eopLine[29])
        if eopLine[17] in expName:
            index = expName.index(eopLine[17])
            lines[index+43] = line
        else:
            if epoch.size == 0:
                lines.append(line)
            else:
                insertPosit = np.where(epoch < eopLine[0])[0]
                if len(insertPosit) == epoch.size:
                    lines.append(line)
                elif len(insertPosit) == 0:
                    lines.insert(43,line)
                else:
                    lines.insert(insertPosit[-1]+44,line)
                
    fid = open(eopFile,'w')
    for line in lines:
        fid.writelines(line)        
    fid.close()
    
def writeEOPFileHeader(flag):
    if flag == 0:
        lines = [['*Session       MJD           Offset        Error       WRMS   ObsNum\n'],\
                 [      '*                     us           us         ps\n']]
    
    elif flag == 1:
        lines      = [['*			      IVS EOP 3.0 FORMAT\n'],\
                      ['*  1     epoch (with at least 5 decimal digits)\n'],\
                      ['*\n'],\
                      ['*  2     x of the pole (arcsec)\n'],\
                      ['*  3     y of the pole (arcsec)\n'],\
                      ['*  4     UT1-UTC (sec)\n'],\
                      ['*  5     dpsi or dX (mas)\n'],\
                      ['*  6     deps or dY (mas)\n'],\
                      ['*\n'],\
                      ['*  7     uncertainty in x (arcsec)\n'],\
                      ['*  8     uncertainty in y (arcsec)\n'],\
                      ['*  9     uncertainty in UT1-UTC (sec)\n'],\
                      ['* 10     uncertainty in dpsi or dX (mas)\n'],\
                      ['* 11     uncertainty in deps or dY (mas)\n'],\
                      ['*\n'],\
                      ['* 12     wrms residual delay of the session (ps)\n'],\
                      ['*\n'],\
                      ['* 13     correlation coefficient : x, y\n'],\
                      ['* 14     correlation coefficient : x, UT1\n'],\
                      ['* 15     correlation coefficient : y, UT1\n'],\
                      ['* 16     correlation coefficient : dpsi,deps or dX/dY\n'],\
                      ['*\n'],\
                      ['* 17	 number of observables\n'],\
                      ['* 18     6 character IVS session code\n'],\
                      ['* 19 	 Session duration (hours)\n'],\
                      ['*\n'],\
                      ['* 20	 x rate of the pole (asc/day)\n'],\
                      ['* 21	 y rate of the pole (asc/day)\n'],\
                      ['* 22	 excess length of day (LOD) (sec), see comment below \n'],\
                      ['* 23	 dpsi/dX rate (mas/day)\n'],\
                      ['* 24	 deps/dY rate (mas/day)\n'],\
                      ['*\n'],\
                      ['* 25     uncertainty in x rate (asc/day)\n'],\
                      ['* 26     uncertainty in y rate (asc/day)\n'],\
                      ['* 27     uncertainty in LOD (sec)\n'],\
                      ['* 28     uncertainty in dpsi/dX rate (mas/day)\n'],\
                      ['* 29     uncertainty in deps/dY rate (mas/day)\n'],\
                      ['*\n'],\
                      ['* 30     sequence of two-character IVS station identifiers as maintained \n'],\
                      ['*        in IVS master control file ns-codes.txt (no blanks between stations)\n'],\
                      ['*        e.g. TsWzWfTcGcFt45Oh, TsWzNy or NyTs\n'],\
                      ['*        N.B.: There may be several lines for an individual session\n'],\
                      ['*              identifying different station configurations \n']]
            
    return lines
