#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:41:47 2023

@author: dangyao
"""

import datetime
import numpy as np
from MOD.mod_eop import *
from COMMON.time_transfer import *


def writeSFF(param, scanInfo, eopApri, result, out):
    """
    Creat the SFF file
    ---------------------
    input:
        param         : 
        scanInfo      : scan struct
        eopApri       : 
        result        : RESULT struct
    output: 
        save the SFF file
    ---------------------
    """
    if param.Out.reportPath[0] == 'NO':
        return
    print('    Write the spool file......')
    
    time = datetime.datetime.now()
    [year,mon,day,hour,minute,second] = mjd2ymdhms(scanInfo.scanMJD[0])
    reportPath = os.path.join(param.Out.reportPath[1], str(year))
    if not os.path.exists(reportPath):
        os.mkdir(reportPath)

    fid = open(os.path.join(reportPath,scanInfo.sessionName+'.SFF'),'w')
    #fid = open(param.Out.reportPath[1]+'/'+scanInfo.sessionName+'.SFF','w')
    fid.writelines('1Run\n'+\
                   ' Analysis center: \n'+\
                   ' Analyst:         yaodang ( yaodang@ntsc.ac.cn )\n'+\
                   ' Machine:         Linux\n'+\
                   ' Executables:     .\n'+\
                   ' Solve initials:  yd\n'+\
                   ' Spool format:    SgLib-0.7.3 (New Market)\n'+\
                   ' Local time:      %4d.%02d.%02d-%02d:%02d:%02d\n'%(time.year,time.month,time.day,time.hour,time.minute,time.second)+\
                   ' Data base $%s\n'%scanInfo.sessionName+\
                   '\n\n  Flyby Station Cals:    DB Station Cals:              | DB Non-station Cals: | Atmosphere Partial:\n'+\
                   ' --------------------------------------------------------------------------------------------------\n')
    dbCal = ['Pol Tide','WobXCont','WobYCont','EarthTid','Ocean   ','UT1Ortho','XpYpOrth','XpYpLib ','UT1Libra','OPTLCont']
    for i in range(len(scanInfo.stationAll)):
        if i == 0:
            fid.writelines('    %-8s:NMFDRFLY             GION                 | %8s             |%4sWTFLY              \n'%(scanInfo.stationAll[i],dbCal[i],param.Map.mapFun))    
        elif i >= 8:
            fid.writelines('    %-8s:NMFDRFLY             GION                 |                      |                       \n'%(scanInfo.stationAll[i]))
        else:
            fid.writelines('    %-8s:NMFDRFLY             GION                 | %8s             |                       \n'%(scanInfo.stationAll[i],dbCal[i]))
    if i < 7:
        for j in range(i+1,7):
            fid.writelines('                                                       | %8s             |                       \n'%(dbCal[j]))
    # Met
    fid.writelines(' --------------------------------------------------------------------------------------------------\n'+\
                   '\n\n  Met Statistics:\n'+\
                   '                    Temperature      Pressure        Humidity\n'+\
                   '   Station         average   rms   average   rms   average   rms\n')
    for i in range(len(scanInfo.stationAll)):
        if np.mean(scanInfo.H[i]) == -999:
            format_H = '%4d'
        else:
            format_H = '%4.1f'
            
        if np.mean(scanInfo.T[i]) == -999:
            format_T = '%6d'
        else:
            format_T = '%6.1f'
            
        if np.mean(scanInfo.P[i]) == -999:
            format_P = '%6d'
        else:
            format_P = '%6.1f'
            
        format_str = '   %-8s  MET   '+'%s          %s            %s        \n'%(format_T,format_P,format_H)
        
        if np.mean(scanInfo.H[i]) == -999:
            fid.writelines(format_str\
                           %(scanInfo.stationAll[i],np.mean(scanInfo.T[i]),np.mean(scanInfo.P[i]),np.mean(scanInfo.H[i])))

        else:
            fid.writelines(format_str\
                           %(scanInfo.stationAll[i],np.mean(scanInfo.T[i]),np.mean(scanInfo.P[i]),np.mean(scanInfo.H[i])*100))
    # result
    index = scanInfo.baseInfo[0].index('X')
    fid.writelines('\n\n Data Type     Number of   Weighted RMS    Normalized RMS   Chi Square\n'+\
                   '             Observations    Residual         Residual      (precis)\n'+\
                   '                 Used\n'+\
                   '   Delay    %5d%19.3f ps              0.00%13.4f\n'%(len(result.VReal[index]),result.wrms,result.chis)+\
                   '   Rate         0                  0 fs/s            0.00       0.0000\n'+\
                   'Combined        0                                    0.00       0.0000\n'+\
                   '-----------------------------------------------------------------------\n')
        
    # EOP
    #meanMJD = (scanInfo.scanMJD[0]+scanInfo.scanMJD[-1])/2
    meanMJD = scanInfo.refMJD
    meanEOP = interpEOP(eopApri, [meanMJD], param, 0)
    
    year,mon,day,hours,minutes,seconds = mjd2date(meanMJD)
    hour = (meanMJD-int(meanMJD))*24
    minute = (hour-int(hour))*60
    fid.writelines('\n\n Parameter adjustments for %s\n'%scanInfo.sessionName+\
                   '                                        Parameter               Adjustment              a-sigma              m-sigma\n')
    if param.Flags.xyz[0] == 'YES':
    # if param.Flags.xyz[0] == 'YES':
        xyzLines = xyzBlock(out)
        fid.writelines(xyzLines)
        
    if param.Flags.sou[0] == 'YES':
        souLines = souBlock(out)
        fid.writelines(souLines)
    
    eopParam = [['ut1','lod','pmx','pmy','pmxr','pmyr'],\
                ['UT1-TAI ','UT1-TAI ','X Wobble','Y Wobble','X Wobble','Y Wobble'],\
                ['msec','ms/d','masec','masec','mas/d','mas/d'],\
                ['microsec','micros/d','microasec','microasec','microas/d','microas/d'],\
                [0,1,0,0,1,1]]
            
    for i in range(len(eopParam[0])):
        if out.estFlag[i] == 1:
            fid.writelines('       %7s  %d,  %2d/%02d/%02d %02d:%02d %13.4f %-5s %10.2f %-9s %11.2f %-9s        0.00 %-9s\n'\
                            %(eopParam[1][i],eopParam[-1][i],year-2000,mon,day,hour,int(minute),out.aprioriValue[i][0]+out.estValue[i][0],\
                              eopParam[2][i],out.estValue[i][0]*1E3,eopParam[3][i],out.formalErr[i][0]*1E3,eopParam[3][i],eopParam[3][i]))

    eopPosit = [out.param.index('ut1'),out.param.index('pmyr')]
    if sum(out.estFlag[eopPosit[0]:eopPosit[1]+1]) != 0:
        fid.writelines(' EOP without included hi-freq variations (a-sigmas)\n'+\
                       '                      XWOB          YWOB          UT1-TAI          XSIG         YSIG         USIG\n'+\
                       '                       mas           mas            ms           microasec    microasec    microsec\n')
        
        if param.Flags.pm[0] == 'YES':
            fid.writelines('%2d/%02d/%02d %02d:%02d %14.4f %13.4f %14.4f %13.2f %13.2f %12.2f\n'\
                           %(year-2000,mon,day,hour,int(minute),out.aprioriValue[2][0]+out.estValue[2][0],out.aprioriValue[3][0]+out.estValue[3][0],\
                             out.aprioriValue[0][0]+out.estValue[0][0],out.formalErr[2][0]*1E3,out.formalErr[3][0]*1E3,out.formalErr[0][0]*1E3))
        else:
            fid.writelines('%2d/%02d/%02d %02d:%02d %14.4f %13.4f %14.4f %13.2f %13.2f %12.2f\n'\
                           %(year-2000,mon,day,hour,int(minute),0,0,out.aprioriValue[0][0]+out.estValue[0][0],0,0,out.formalErr[0][0]*1E3))
    fid.close()
    
    
def xyzBlock(out):
    
    xyzLines = ''
    
    xyzP = out.param.index('xyz') - len(out.param)
    flag = ['X Comp', 'Y Comp', 'Z Comp']
    
    for i in range(len(out.nscode)):
        xyzLines += 'Station positions are for epoch: %4d.%02d.%02d-%02d:%02d:%02d\n'%(out.mjd[xyzP][i][6],out.mjd[xyzP][i][9],\
                                                                                      out.mjd[xyzP][i][10],out.mjd[xyzP][i][11],\
                                                                                      out.mjd[xyzP][i][12],out.mjd[xyzP][i][13])
            
        for j in range(3):
            # xyzLines += '%15s -001 YAO   %s %19.2f mm %14.3f mm %18.3f mm\n'%(out.nscode[i][2], flag[j], out.aprioriValue[xyzP][i,j]*1000+out.estValue[xyzP][j,i]*10,\
            #                                                         out.estValue[xyzP][j,i]*10, out.formalErr[xyzP][j,i]*10)
            xyzLines += '%15s -001 %4s  %s %19.2f mm %14.3f mm %18.3f mm\n'%(out.nscode[i][2], out.nscode[i][3], flag[j], out.aprioriValue[xyzP][i,j]*1000+out.estValue[xyzP][i,j]*1000,\
                                                                    out.estValue[xyzP][i,j]*1000, out.formalErr[xyzP][i,j]*1000)
        xyzLines += '\n'
    return xyzLines

def souBlock(out):
    
    souLines = ''
    
    souP = out.param.index('sou') - len(out.param)
    flag = ['RT. ASC.', 'DEC.']
    rad2mas = 180/np.pi*3600*1000
    estValue = out.estValue[souP]*rad2mas
    formalErr = out.formalErr[souP]*rad2mas
    
    for i in range(len(out.souName)):
        souLines += '%16s %-11s %22s %11.4f      m-asc %10.4f      m-asec\n%16s  CORRECTION %21.7f\n\n'%(out.souName[i], flag[0], ' ', estValue[i,0], \
                                                                                                       formalErr[i,0], ' ', estValue[i,0]*np.cos(out.aprioriValue[souP][i,1]))
        souLines += '%16s %-11s %22s %11.4f      m-asc %10.4f      m-asec\n%16s  CORRECTION %21.7f\n\n'%(out.souName[i], flag[1], ' ', estValue[i,1], \
                                                                                                       formalErr[i,1], ' ', estValue[i,1])
        
    souLines += '\n'
    
    return souLines

    