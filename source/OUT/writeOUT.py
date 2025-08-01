# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 20:15:47 2022

@author: yaodang
"""

import matplotlib.pyplot as plt
import numpy as np
import os,sys
import datetime

sys.path.append('../COMMON/')
sys.path.append('../MOD/')

from MOD.mod_eop import *
from INIT.init import *
from COMMON.time_transfer import *


def collectResult(param, scanInfo, eopApri, result):
    out = OUTRESULT()
    
    
    paramS = result.paramName.index('ut1')
    estP = np.where(result.paramNum[paramS:] > 0)
    out.estFlag[estP[0]] = 1
    
    for i in range(len(estP[0])):
        temp = sum(result.paramNum[0:paramS+i])
        if estP[0][i] == 0 or estP[0][i] == 1:
            out.estValue[estP[0][i]] = result.para[temp:temp+result.paramNum[estP[0][i]+paramS]]/15
            out.formalErr[estP[0][i]] = result.err[temp:temp+result.paramNum[estP[0][i]+paramS]]/15
        else:
            out.estValue[estP[0][i]] = result.para[temp:temp+result.paramNum[estP[0][i]+paramS]]
            out.formalErr[estP[0][i]] = result.err[temp:temp+result.paramNum[estP[0][i]+paramS]]
    
    if param.Flags.pm[0] == 'YES' or param.Flags.ut1[0] == 'YES' or param.Flags.nut[0] == 'YES':
        if param.Flags.type == 'SEGMENT':
            eopindex = []
            mjd0 = np.floor(scanInfo.scanMJD[0])
            eopmMJD = mjd0 + np.array(result.paramMJD[paramS])/1440
        
            # for i in range(len(eopmMJD)):
                # eopindex.append(eopApri.MJD.tolist().index(eopmMJD[i]))
        
            # meanEOP = EOP(eopmMJD, eopApri.XP[eopindex], eopApri.YP[eopindex], eopApri.UT1[eopindex], eopApri.DX[eopindex], eopApri.DX[eopindex])
        
        if param.Flags.type == 'POLY':
            eopmMJD = np.array([scanInfo.refMJD])
        
        meanEOP = interpEOP(eopApri, eopmMJD, param)
            
    temp = result.paramName.index('ut1')
    out.aprioriValue[temp-paramS] = meanEOP.UT1*1000  # ms
    out.mjd[temp-paramS] = eopmMJD
    
    temp = result.paramName.index('pmx')
    out.aprioriValue[temp-paramS] = meanEOP.XP*180*3600*1000/np.pi   # mas
    out.mjd[temp-paramS] = eopmMJD
    
    temp = result.paramName.index('pmy')
    out.aprioriValue[temp-paramS] = meanEOP.YP*180*3600*1000/np.pi   # mas
    out.mjd[temp-paramS] = eopmMJD
    
    temp = result.paramName.index('nutx')
    out.aprioriValue[temp-paramS] = meanEOP.DX*180*3600*1000/np.pi   # mas
    out.mjd[temp-paramS] = eopmMJD
    
    temp = result.paramName.index('nuty')
    out.aprioriValue[temp-paramS] = meanEOP.DY*180*3600*1000/np.pi   # mas
    out.mjd[temp-paramS] = eopmMJD    
            
    if param.Flags.pmr[0] == 'YES':
        xpr = getRate(eopApri.MJD, eopApri.XP, eopmMJD[0])
        xpr = xpr * 180/np.pi*3600*1E3  # rad/day to mas/day
        temp = result.paramName.index('pmxr')
        out.aprioriValue[temp-paramS] = np.array([xpr])
        out.mjd[temp-paramS] = eopmMJD
        
        ypr = getRate(eopApri.MJD, eopApri.YP, eopmMJD[0])
        ypr = ypr * 180/np.pi*3600*1E3  # rad/day to mas/day
        temp = result.paramName.index('pmyr')
        out.aprioriValue[temp-paramS] = np.array([ypr])
        out.mjd[temp-paramS] = eopmMJD
                
    if param.Flags.lod[0] == 'YES':
        lod = getRate(eopApri.MJD, eopApri.UT1, eopmMJD[0])
        lod = lod * 1E3                # s to ms
        temp = result.paramName.index('lod')
        out.aprioriValue[temp-paramS] = np.array([lod])
        out.mjd[temp-paramS] = eopmMJD
        
    
    return out
    
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
    
    year = 2000+int(scanInfo.sessionName[0:2])
    if not os.path.exists(param.Out.residualPath+'/'+str(year)):
        os.system('mkdir '+param.Out.residualPath+'/'+str(year))
    
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
    
    for i in range(len(staObs.mjd)):
        if len(staObs.mjd[i]):
            plt.plot(staObs.mjd[i],result.VReal[staObs.oc_nob[i]],color=colors[i],marker='o',linestyle='',label=scanInfo.stationAll[i])

    
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
    
def writeSNX(param, scanInfo, sourceInfo, stationInfo, eopApri, result, out):
    """
    Creat the SNX file
    ---------------------
    input:
        param         : 
        scanInfo      : scan struct
        sourceInfo    : 
        stationInfo   : 
    output: 
        save the SNX file
    ---------------------
    """
    if param.Out.snxPath == 'None':
        return
    print('    write the snx file......')
    time = datetime.datetime.now()
    runDay = date2doy(time.year, time.month, time.day)
    seconds = int(time.hour*3600 + time.minute*60 + time.second)
    
    fid = open(param.Out.snxPath+'/'+scanInfo.sessionName+'.snx','w')
    fid.writelines("%%=SNX 2.10 YAO %2d:%03d:%5d\n"%(time.year-2000, runDay, seconds))
    fid.writelines('*\n'+\
                   '* Created on:   %4d.%02d.%02d-%02d:%02d:%02d local time\n'\
                       %(time.year,time.month,time.day,time.hour,time.minute,int(time.second))+\
                   '* Created at:   Yao Dang\n'+\
                   '* Created by:     (   )\n'+\
                   '* Generated by: routine writeSNX\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+FILE/REFERENCE\n'+\
                   ' DESCRIPTION       YAO\n'+\
                   ' OUTPUT            Single session VLBI solution\n'+\
                   ' CONTACT             < >\n'+\
                   ' SOFTWARE          VLBI analysis system VDSP\n'+\
                   ' HARDWARE          Linux\n'+\
                   ' INPUT             VLBI experiment q22149, database $%s version 004\n'%(scanInfo.sessionName)+\
                   '-FILE/REFERENCE\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+FILE/COMMENT\n'+\
                   '-FILE/COMMENT\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+INPUT/ACKNOWLEDGEMENTS\n'+\
                   ' Yao  Yao Observatory, VLBI analysis group\n'+\
                   '-INPUT/ACKNOWLEDGEMENTS\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+SITE/ID\n'+\
                   '*Code PT Domes____ T Station description___ Approx_lon_ Approx_lat_ App_h__\n')
    
    
    ns_code = scanInfo.stationCode
    nsCode = []
    for sta in range(len(scanInfo.stationAll)):
        # if (not scanInfo.stationAll[sta] in scanInfo.refSta) and (not scanInfo.stationAll[sta] in scanInfo.rmSta):
        if not scanInfo.stationAll[sta] in scanInfo.noEstSta:
            fid.writelines(' %s  A %s R %-8s\n'%(ns_code[sta][3],ns_code[sta][2],ns_code[sta][1]))
            nsCode.append([ns_code[sta][3],ns_code[sta][2],ns_code[sta][1]])
        
    # SOURCE/ID    
    fid.writelines('-SITE/ID\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+SOURCE/ID\n'+\
                   '*Code IERS nam ICRF designator  IAU name   IVS name\n')
    
    for i in range(len(sourceInfo.sourceName)):
        fid.writelines(' %04d                                      %-8s\n'%(i+1,sourceInfo.sourceName[i]))

    
    # SOLUTION/EPOCHS    
    blank ='        ' 

    fid.writelines('-SOURCE/ID\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+SOLUTION/EPOCHS\n'+\
                   '*Code PT SBIN T Data_start__ Data_end____ Mean_epoch__\n')
    
    meanTime = []
    for i in range(len(nsCode)):
        name = nsCode[i][2]+blank[0:8-len(nsCode[i][2])]
        index = stationInfo.stationName.index(name)
        doys = date2doy(int(stationInfo.obsTimeRange[index][0][0]),int(stationInfo.obsTimeRange[index][0][1]),int(stationInfo.obsTimeRange[index][0][2]))
        doye = date2doy(int(stationInfo.obsTimeRange[index][1][0]),int(stationInfo.obsTimeRange[index][1][1]),int(stationInfo.obsTimeRange[index][1][2]))
        secs = stationInfo.obsTimeRange[index][0][3]*3600+stationInfo.obsTimeRange[index][0][4]*60+stationInfo.obsTimeRange[index][0][5]
        sece = stationInfo.obsTimeRange[index][1][3]*3600+stationInfo.obsTimeRange[index][1][4]*60+stationInfo.obsTimeRange[index][1][5]

        secm = int(secs + ((doye-doys)*86400+sece-secs)/2)
        if secm >= 86400:
            flag = 1
            doym = doye
            secm -= 86400
        else:
            flag = 0
            doym = doys
            
        meanTime.append([int(stationInfo.obsTimeRange[index][flag][0]),doym,secm,int(stationInfo.obsTimeRange[index][flag][1]),int(stationInfo.obsTimeRange[index][flag][2]),\
                         int(secm/3600),int((secm-int(secm/3600)*3600)/60), secm-int(secm/3600)*3600-int((secm-int(secm/3600)*3600)/60)*60])
        
        fid.writelines(' %s  A    1 R %2d:%03d:%05d %2d:%03d:%05d %2d:%03d:%05d\n'\
                       %(nsCode[i][0],stationInfo.obsTimeRange[index][0][0]-2000,doys,secs,stationInfo.obsTimeRange[index][1][0]-2000,\
                         doye,sece,stationInfo.obsTimeRange[index][flag][0]-2000,doye,secm))
        
    # NUTATION/DATA  PRECESSION/DATA
    fid.writelines('-SOLUTION/EPOCHS\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+NUTATION/DATA\n'+\
                   ' IAU2006/2000 Precession/Nutation apriori nutation modelwas used\n'+\
                   ' NONE     REF Total nutation angles are reported in estimation block\n'+\
                   '-NUTATION/DATA\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+PRECESSION/DATA\n'+\
                   ' CAPITAINE2003 apriori precession constant and obliquity rates were used \n'+\
                   '-PRECESSION/DATA\n'+\
                   '*\n'+\
                   '* -----------------------------------------------------------------------------\n'+\
                   '*\n'+\
                   '+SOLUTION/STATISTICS\n'+\
                   '* Units for WRMS: sec\n')
        
    # SOLUTION/STATISTICS
    ocStr = '%16.14E'%(np.dot(np.dot(result.o_creal.T,result.preal),result.o_creal))
    VTPVStr = '%16.14E'%(result.vTPv)
    chiStr = '%16.14E'%(result.chis)
    wrmsStr = '%16.14E'%(result.wrms*1E-12)
    
    fid.writelines(' NUMBER OF OBSERVATIONS          %11d\n'%(len(scanInfo.Obs2Scan))+\
                   ' NUMBER OF UNKNOWNS              %11d\n'%(len(scanInfo.Obs2Scan)-result.VReal.shape[0])+\
                   ' WEIGHTED SQUARE SUM OF O-C      %20s\n'%(ocStr.replace('E','D'))+\
                   ' SQUARE SUM OF RESIDUALS (VTPV)  %20s\n'%(VTPVStr.replace('E','D'))+\
                   ' VARIANCE FACTOR                 %20s\n'%(chiStr.replace('E','D'))+\
                   ' WRMS OF POSTFIT RESIDUALS       %20s\n'%(wrmsStr.replace('E','D'))+\
                   '-SOLUTION/STATISTICS\n'+\
                   '*\n* -----------------------------------------------------------------------------\n'+\
                   '*\n+SOLUTION/APRIORI\n'+\
                   '*Index Type__ CODE PT SBIN Ref_epoch___ Unit S Apriori_value________ Constraint_\n')
    
    # SOLUTION/APRIORI
    
    
    snum = 0
    xyzP = out.param.index('xyz') - len(out.param)
    estParamP = np.where(out.estFlag[:xyzP] == 1)
    for i in range(len(estParamP[0])):
        for j in range(len(out.mjd[estParamP[0][i]])):
            eopy,eopm,eopd = mjd2date(out.mjd[estParamP[0][i]][j])
            eopdoy = date2doy(eopy,eopm,eopd)
            eopSec = (out.mjd[estParamP[0][i]][j]-int(out.mjd[estParamP[0][i]][j]))*86400
            
            paramStr = '%17.14E'%(out.aprioriValue[estParamP[0][i]][j])        
            fid.writelines('%6d %-5s  ----  -    1 %2d:%03d:%05d %-4s 2 %21s 0.00000D+00\n'\
                           %(snum+1, out.snxName[estParamP[0][i]], eopy-2000,eopdoy,eopSec, out.unit[estParamP[0][i]], paramStr.replace('E','D')))
            snum += 1
            

    if param.Flags.xyz[0] == 'YES':
        xyzStr = ['STAX','STAY','STAZ']
        
        for i in range(len(nsCode)):
            name = nsCode[i][2]+blank[0:8-len(nsCode[i][2])]
            index = stationInfo.stationName.index(name)
            mMJD = modjuldat(np.array([meanTime[i][0]]),np.array([meanTime[i][3]]),np.array([meanTime[i][4]]),\
                             meanTime[i][5],meanTime[i][6],meanTime[i][7])
                
            for j in range(3):
                posit = '%17.14E'%(stationInfo.posit[index][j] + stationInfo.vel[index][j]*(mMJD-stationInfo.epoch[index]))
                fid.writelines('%6d %s   %4s  A    1 %2d:%03d:%05d m    2 %21s 0.00000D+00\n'\
                               %(i*3+j+1+snum,xyzStr[j],nsCode[i][0],meanTime[i][0]-2000,meanTime[i][1],meanTime[i][2],posit.replace('E', 'D')))
        snum += (i+1)*3
    
    sourceID = scanInfo.estSou
    if param.Flags.sou[0] == 'YES':
        radeStr = ['RS_RA','RS_DE']
        
        for i in range(len(sourceID)):
            name = scanInfo.sourceAll[sourceID[i]]
            index = sourceInfo.sourceName.index(name)
            for j in range(2):
                rade = '%17.14E'%(sourceInfo.rade[index][j])
                
                fid.writelines('%6d %s  %04d  A    1 22:222:22222 rad  2 %21s 0.00000D+00\n'%(snum+i*2+j+1,radeStr[j],sourceID[i]+1,\
                                                                                              rade.replace('E','D')))
        snum += (i+1)*2        
        
    fid.writelines('-SOLUTION/APRIORI\n'+\
                   '*\n* -----------------------------------------------------------------------------\n*\n'+\
                   '+SOLUTION/ESTIMATE\n'+\
                   '*Index TYPE__ CODE PT SBIN Ref_epoch___ Unit S Total_value__________ Formal_erro\n')
        
    # SOLUTION/ESTIMATE
    snum = 0
    for i in range(len(estParamP[0])):
        for j in range(len(out.mjd[estParamP[0][i]])):
            eopy,eopm,eopd = mjd2date(out.mjd[estParamP[0][i]][j])
            eopdoy = date2doy(eopy,eopm,eopd)
            eopSec = (out.mjd[estParamP[0][i]][j]-int(out.mjd[estParamP[0][i]][j]))*86400
            
            paramStr = '%17.14E'%(out.aprioriValue[estParamP[0][i]][j] + out.estValue[estParamP[0][i]][j])
            errStr = '%7.5E'%(out.formalErr[estParamP[0][i]][j])
            fid.writelines('%6d %-5s  ----  -    1 %2d:%03d:%05d %-4s 2 %21s %11s\n'\
                           %(snum+1, out.snxName[estParamP[0][i]], eopy-2000,eopdoy,eopSec, out.unit[estParamP[0][i]], \
                             paramStr.replace('E','D'), errStr.replace('E','D')))
            snum += 1
    
    startP = sum(result.paramNum[:xyzP])
    if param.Flags.xyz[0] == 'YES':
        xyzStr = ['STAX','STAY','STAZ']
        for i in range(len(nsCode)):
            name = nsCode[i][2]+blank[0:8-len(nsCode[i][2])]
            index = stationInfo.stationName.index(name)
            mMJD = modjuldat(np.array([meanTime[i][0]]),np.array([meanTime[i][3]]),np.array([meanTime[i][4]]),\
                             meanTime[i][5],meanTime[i][6],meanTime[i][7])
            
            for j in range(3):
                posit = '%17.14E'%(stationInfo.posit[index][j] + stationInfo.vel[index][j]*(mMJD-stationInfo.epoch[index])+\
                                   result.para[startP+i*3+j]/100)
                err = '%7.5E'%(result.err[startP+i*3+j]/100)
                #fid.writelines('%6d %s   %4s  A    1 %2d:%03d:%05d m    2 %21.14f 0.00000D+00\n'%(i*3+j+1,xyzStr[j],nsCode[i][0]))
                fid.writelines('%6d %s   %4s  A    1 %2d:%03d:%05d m    2 %21s %11s\n'\
                               %(i*3+j+1+snum,xyzStr[j],nsCode[i][0], meanTime[i][0]-2000,meanTime[i][1],meanTime[i][2],\
                                 posit.replace('E', 'D'),err.replace('E', 'D')))
        snum += (i+1)*3
    
    
    souP = out.param.index('sou') - len(out.param)
    startP = sum(result.paramNum[:souP])

    if param.Flags.sou[0] == 'YES':
        for i in range(len(sourceID)):
            name = scanInfo.sourceAll[sourceID[i]]
            index = sourceInfo.sourceName.index(name)
            for j in range(2):
                rade = '%17.14E'%(sourceInfo.rade[index][j]+result.para[startP+i*2+j]*np.pi/180/3600000)
                err = '%7.5E'%(result.err[startP+i*2+j]*np.pi/180/3600000)
                #fid.writelines('%6d %s  %04d  A    1 %2d:%03d:%05d rad  2 %21.14f 0.00000D+00\n'%(i*3+j+1,radeStr[j],nsCode[i][0]))
                fid.writelines('%6d %s  %04d  A    1 22:222:22222 rad  2 %21s %11s\n'%(snum+i*2+j+1,radeStr[j],sourceID[i]+1,
                                                                                        rade.replace('E', 'D'),err.replace('E', 'D')))
        snum += (i+1)*2
        
    fid.writelines('-SOLUTION/ESTIMATE\n'+\
                   '*\n* -----------------------------------------------------------------------------\n*\n'+\
                   '+SOLUTION/NORMAL_EQUATION_VECTOR\n'+\
                   '*Index TYPE__ CODE Pt Soln Ref_epoch___ Unit S RightHandSideVector_b\n')
        
    # SOLUTION/NORMAL_EQUATION_VECTOR
    snum = 0
    for i in range(len(estParamP[0])):
        for j in range(len(out.mjd[estParamP[0][i]])):
            eopy,eopm,eopd = mjd2date(out.mjd[estParamP[0][i]][j])
            eopdoy = date2doy(eopy,eopm,eopd)
            eopSec = (out.mjd[estParamP[0][i]][j]-int(out.mjd[estParamP[0][i]][j]))*86400
            
            bStr = '%17.14E'%(result.bsnx[i+j])
            fid.writelines('%6d %-5s  ----  -    1 %2d:%03d:%05d %-4s 2 %21s\n'\
                           %(snum+1, out.snxName[estParamP[0][i]], eopy-2000,eopdoy,eopSec, out.unit[estParamP[0][i]], bStr.replace('E','D')))
            snum += 1
        
    startP = sum(result.paramNum[2:xyzP])
    if param.Flags.xyz[0] == 'YES':
        xyzStr = ['STAX','STAY','STAZ']
        for i in range(len(nsCode)):
           for j in range(3):
               bstr = '%17.14E'%(result.bsnx[startP+3*i+j])
               fid.writelines('%6d %s   %4s  A    1 %2d:%03d:%05d m    2 %21s\n'\
                               %(i*3+j+1+snum,xyzStr[j],nsCode[i][0], meanTime[i][0]-2000,meanTime[i][1],meanTime[i][2],\
                                 bstr.replace('E', 'D')))
        snum += (i+1)*3
        
   
    fid.writelines('-SOLUTION/NORMAL_EQUATION_VECTOR\n'+\
                   '*\n* -----------------------------------------------------------------------------\n*\n'+\
                   '+SOLUTION/NORMAL_EQUATION_MATRIX L\n'+\
                   '*Row__ Col__ Norm_Equ_Matrix_Value Norm_Equ_Matrix_Value2 Norm_Equ_Matrix_Value3\n')
    
    blank = '                      '
    for i in range(result.Nsnx.shape[0]):
        k = (i+1)/3
        
        if k <= 1:
            nstr = ''
            for j in range(i+1):
                nstr += '%22s'%('%16.13E  '%(result.Nsnx[i,j]))
            fid.writelines('%6d%6d  %s\n'\
                           %(i+1,1, nstr[:-2].replace('E', 'D')))
        else:
            for m in range(int(k)):
                nstr = ''
                for n in range(3):
                    nstr += '%22s'%('%16.13E  '%(result.Nsnx[i,3*m+n]))
                fid.writelines('%6d%6d  %s\n'\
                               %(i+1,3*m+1, nstr[:-2].replace('E', 'D')))
            if int(k) - k != 0:
                nstr = ''
                for n in range(3*(m+1),i+1):
                    nstr += '%22s'%('%16.13E  '%(result.Nsnx[i,n]))
                fid.writelines('%6d%6d  %s\n'\
                               %(i+1,3*(m+1)+1, nstr[:-2].replace('E', 'D')))
                
    fid.writelines('-SOLUTION/NORMAL_EQUATION_MATRIX L\n'+\
                   '*\n* -----------------------------------------------------------------------------\n*\n'+\
                   '%ENDSNX')
    fid.close()
    
def writeSFF(param, scanInfo, eopApri, result):
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
    if param.Out.reportPath == 'None':
        return
    print('    Write the spool file......')
    
    time = datetime.datetime.now()
    fid = open(param.Out.reportPath+'/'+scanInfo.sessionName+'.SFF','w')
    fid.writelines('1Run\n'+\
                   ' Analysis center: \n'+\
                   ' Analyst:         yaodang ( yaodang@shao.ac.cn )\n'+\
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
    fid.writelines('\n\n Data Type     Number of   Weighted RMS    Normalized RMS   Chi Square\n'+\
                   '             Observations    Residual         Residual      (precis)\n'+\
                   '                 Used\n'+\
                   '   Delay    %5d%19.3f ps              0.00%13.4f\n'%(len(result.VReal),result.wrms,result.chis)+\
                   '   Rate         0                  0 fs/s            0.00       0.0000\n'+\
                   'Combined        0                                    0.00       0.0000\n'+\
                   '-----------------------------------------------------------------------\n')
        
    # EOP
    #meanMJD = (scanInfo.scanMJD[0]+scanInfo.scanMJD[-1])/2
    meanMJD = scanInfo.refMJD
    meanEOP = interpEOP(eopApri, [meanMJD], param)
    
    year,mon,day = mjd2date(meanMJD)
    hour = (meanMJD-int(meanMJD))*24
    minute = (hour-int(hour))*60
    
    fid.writelines('\n\n Parameter adjustments for %s\n'%scanInfo.sessionName+\
                   '                                        Parameter               Adjustment              a-sigma              m-sigma\n')
    
    eopParam = [['ut1','pmx','pmy'],['UT1-TAI ','X Wobble','Y Wobble'],\
                ['msec','masec','masec'],['microsec','microasec','microasec']]
    eopValue = [meanEOP.UT1[0],meanEOP.XP[0]*180*3600/np.pi,meanEOP.YP[0]*180*3600/np.pi] # [s,as,as]
    estValue = np.zeros((2,3))
    for i in range(len(eopParam[0])):
        ppa = result.paramName.index(eopParam[0][i])
        if result.paramNum[ppa] != 0:
            if i == 0:
                estValue[0][i] = result.para[sum(result.paramNum[0:ppa])]/15*1E3  # us
                estValue[1][i] = result.err[sum(result.paramNum[0:ppa])]/15*1E3   # us
            else:
                estValue[0][i] = result.para[sum(result.paramNum[0:ppa])]*1E3  # uas
                estValue[1][i] = result.err[sum(result.paramNum[0:ppa])]*1E3   # uas
    for i in range(len(eopParam[0])):
        ppa = result.paramName.index(eopParam[0][i])
        if result.paramNum[ppa] != 0:
            fid.writelines('       %7s  0,  %2d/%02d/%02d %02d:%02d %13.4f %-5s %10.2f %-9s %11.2f %-9s        0.00 %-9s\n'\
                           %(eopParam[1][i],year-2000,mon,day,hour,int(minute),eopValue[i]*1E3+estValue[0][i]*1E-3,eopParam[2][i],\
                             estValue[0][i],eopParam[3][i],estValue[1][i],eopParam[3][i],eopParam[3][i]))

    
    fid.writelines(' EOP without included hi-freq variations  (a-sigmas)\n'+\
                   '                      XWOB          YWOB          UT1-TAI          XSIG         YSIG         USIG\n'+\
                   '                       mas           mas            ms           microasec    microasec    microsec\n')
    
    if param.Flags.pm[0] == 'YES':
        fid.writelines('%2d/%02d/%02d %02d:%02d %14.4f %13.4f %14.4f %13.2f %13.2f %12.2f\n'\
                       %(year-2000,mon,day,hour,int(minute),eopValue[1]*1E3+estValue[0][1]*1E-3,eopValue[2]*1E3+estValue[0][2]*1E-3,\
                         eopValue[0]*1E3+estValue[0][0]*1E-3,estValue[1][1],estValue[1][2],estValue[1][0]))
    else:
        fid.writelines('%2d/%02d/%02d %02d:%02d %14.4f %13.4f %14.4f %13.2f %13.2f %12.2f\n'\
                       %(year-2000,mon,day,hour,int(minute),0,0,eopValue[0]*1E3+estValue[0][0]*1E-3,0,0,estValue[1][0]))
    fid.close()


def writeEOP(Param, scanInfo, result, eopApri, sessionNum, out):
    
    if os.path.isdir(Param.Out.eopPath):
        eopFile = Param.Out.eopPath+'/eop_out.txt'
    else:
        eopFile = Param.Out.eopPath
        
        
    fid = open(eopFile, Param.Out.eopMode)
    if sessionNum == 0 and Param.Out.eopMode == 'w':
        writeEOPFileHeader(fid)
        
    fileinfo = os.stat(eopFile)
    if sessionNum == 0 and Param.Out.eopMode == 'a' and fileinfo.st_size == 0:
        writeEOPFileHeader(fid)
    
    
    xyzP = out.param.index('xyz') - len(out.param)
    estParamP = np.where(out.estFlag[0:xyzP] == 1)
    eopLine = np.zeros(30).tolist()
    
    eopLine[0] = scanInfo.refMJD
    
    if Param.Flags.type == 'POLY':
        temp = out.param.index('pmx')
        if out.estFlag[temp] == 1:
            eopLine[1] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            eopLine[6] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('pmy')
        if out.estFlag[temp] == 1:
            eopLine[2] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            eopLine[7] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('ut1')
        if out.estFlag[temp] == 1:
            eopLine[3] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            eopLine[8] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('nutx')
        if out.estFlag[temp] == 1:
            eopLine[4] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            eopLine[9] = out.formalErr[temp]*1E-3
            
        temp = out.param.index('nuty')
        if out.estFlag[temp] == 1:
            eopLine[5] = (out.estValue[temp] + out.aprioriValue[temp])*1E-3
            eopLine[10] = out.formalErr[temp]*1E-3
            
    elif Param.Flags.type == 'CPWL':
        eopmMJD = np.array([scanInfo.refMJD])
        meanEOP = interpEOP(eopApri, eopmMJD, Param)
        
        temp = out.param.index('pmx')
        if out.estFlag[temp] == 1:
            eopLine[1] = out.estValue[temp][0]*1E-3 + meanEOP.XP[0]*180*3600/np.pi
            eopLine[6] = out.formalErr[temp][0]*1E-3
            
        temp = out.param.index('pmy')
        if out.estFlag[temp] == 1:
            eopLine[2] = out.estValue[temp][0]*1E-3 + meanEOP.YP[0]*180*3600/np.pi
            eopLine[7] = out.formalErr[temp][0]*1E-3
            
        temp = out.param.index('ut1')
        if out.estFlag[temp] == 1:
            eopLine[3] = out.estValue[temp][0]*1E-3 + meanEOP.UT1[0]
            eopLine[8] = out.formalErr[temp][0]*1E-3
            
        temp = out.param.index('nutx')
        if out.estFlag[temp] == 1:
            eopLine[4] = out.estValue[temp][0]*1E-3 + meanEOP.DX[0]*180*3600/np.pi
            eopLine[9] = out.formalErr[temp][0]*1E-3
            
        temp = out.param.index('nuty')
        if out.estFlag[temp] == 1:
            eopLine[5] = out.estValue[temp][0]*1E-3 + meanEOP.DY[0]*180*3600/np.pi
            eopLine[10] = out.formalErr[temp][0]*1E-3
    
    eopLine[11] = result.wrms
    eopLine[16] = len(scanInfo.Obs2Scan)
    eopLine[17] = scanInfo.expName
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
        if not scanInfo.stationAll[sta] in scanInfo.noEstSta:
            temp += ns_code[sta][0]
    
    eopLine[29] = temp
    
    lineFormat = '%12.6f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f %12.7f '+\
                   '%10.1f %10.1f %10.1f %10.1f %10.1f %5d %-s %5.2f %12.7f %12.7f %12.7f %12.7f %12.7f '+\
                   '%12.7f %12.7f %12.7f %12.7f %12.7f %s\n'
    fid.writelines(lineFormat%(eopLine[0],eopLine[1],eopLine[2],eopLine[3],eopLine[4],eopLine[5],eopLine[6],eopLine[7],eopLine[8],\
                     eopLine[9],eopLine[10],eopLine[11],eopLine[12],eopLine[13],eopLine[14],eopLine[15],eopLine[16],\
                     eopLine[17],eopLine[18],eopLine[19],eopLine[20],eopLine[21],eopLine[22],eopLine[23],eopLine[24],\
                     eopLine[25],eopLine[26],eopLine[27],eopLine[28],eopLine[29]))
    fid.close()
    
def writeEOPFileHeader(fid):
    fid.writelines('*			      IVS EOP FORMAT Version 2.2\n'+\
                   '*  1     Decimal MJD of the measurement as TAI time tag (with at least 5 decimal digits)\n'+\
                   '*\n'+\
                   '*  2     x of the pole (arcsec)\n'+\
                   '*  3     y of the pole (arcsec)\n'+\
                   '*  4     UT1-UTC (sec)\n'+\
                   '*  5     dpsi or dX (mas)\n'+\
                   '*  6     deps or dY (mas)\n'+\
                   '*\n'+\
                   '*  7     uncertainty in x (arcsec)\n'+\
                   '*  8     uncertainty in y (arcsec)\n'+\
                   '*  9     uncertainty in UT1-UTC (sec)\n'+\
                   '* 10     uncertainty in dpsi or dX (mas)\n'+\
                   '* 11     uncertainty in deps or dY (mas)\n'+\
                   '*\n'+\
                   '* 12     wrms residual delay of the session (ps)\n'+\
                   '*\n'+\
                   '* 13     correlation coefficient : x, y\n'+\
                   '* 14     correlation coefficient : x, UT1\n'+\
                   '* 15     correlation coefficient : y, UT1\n'+\
                   '* 16     correlation coefficient : dpsi,deps or dX/dY\n'+\
                   '*\n'+\
                   '* 17	 number of observables\n'+\
                   '* 18     6 character IVS session code\n'+\
                   '* 19 	 Session duration (hours)\n'+\
                   '*\n'+\
                   '* 20	 x rate of the pole (asc/day)\n'+\
                   '* 21	 y rate of the pole (asc/day)\n'+\
                   '* 22	 excess length of day (LOD) (sec), see comment below \n'+\
                   '* 23	 dpsi rate (mas/day)\n'+\
                   '* 24	 deps rate (mas/day)\n'+\
                   '*\n'+\
                   '* 25     uncertainty in x rate (asc/day)\n'+\
                   '* 26     uncertainty in y rate (asc/day)\n'+\
                   '* 27     uncertainty in LOD (sec)\n'+\
                   '* 28     uncertainty in dpsi rate (mas/day)\n'+\
                   '* 29     uncertainty in deps rate (mas/day)\n'+\
                   '*\n'+\
                   '* 30     sequence of two-character IVS station identifiers as maintained \n'+\
                   '*        in IVS master control file ns-codes.txt (no blanks between stations)\n'+\
                   '*        e.g. TsWzWfTcGcFt45Oh, TsWzNy or NyTs\n'+\
                   '*        N.B.: There may be several lines for an individual session\n'+\
                   '*              identifying different station configurations \n')

        

    