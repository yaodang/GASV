#!/usr/bin/env python3

import time
import sys
import numpy as np
from multiprocessing import Pool
from MOD import *

np.set_printoptions(precision=15)


class DELAYSCAN():
    def __init__(self):
        self.scanList = []
        self.com = []
        self.oc_obs = []
        self.pObs = []
        self.pEOP = []
        self.pxyz = []
        self.pxyzt = []
        self.psou = []

def mod(Param, eopApri, scanInfo, sourceInfo, stationInfo, ephem):
    print('\n-------------------------  MOD  ------------------------')
    GPT3Data = Param.Setup 
    numSta = len(scanInfo.stationAll)
    scanMJD = scanInfo.scanMJD
    scanTime = scanInfo.scanTime
    scanBl = scanInfo.scanBl
    scan2Source = scanInfo.scan2Source
    scanCabCal = scanInfo.scanCabCal
    bandNum = len(scanInfo.baseInfo[0])
    scanGD = scanInfo.scanGD
    scanGDSig = scanInfo.scanGDSig
    Press = scanInfo.P
    Temp = scanInfo.T
    refMJD = scanInfo.refMJD
    rq = np.array(sourceInfo.rq)
    pRaDec = sourceInfo.pRaDec
    createFlag = Param.Setup.calctheroe.upper()
    
    Scan2Station = np.delete(scanInfo.Scan2Station, scanInfo.rmScanNum, axis=0)
    StatScan = getStatScan(numSta, Scan2Station)

    #'''
    if numSta >= 4 and len(scanMJD) >= 500:
        parallelFlag = 'YES'
        
        scanList = []
        scanStepNum = int(len(scanMJD)/4)+1
        for i in range(4):
            if i == 3:
                scanList.append(np.linspace(scanStepNum*i, len(scanMJD)-1, len(scanMJD)-scanStepNum*i, dtype=int))
            else:
                scanList.append(np.linspace(scanStepNum*i, scanStepNum*(i+1)-1,scanStepNum,dtype=int))
    else:
        parallelFlag = 'NO'
        scanList = np.linspace(0, len(scanMJD)-1, len(scanMJD), dtype=int)
    #'''
        
    #parallelFlag = 'NO'
    #scanList = np.linspace(0, len(scanMJD)-1, len(scanMJD), dtype=int)
    
    
    print('    EOP interpolation......')
    eopObs = interpEOP(eopApri, scanInfo.scanMJD, Param.Map.heopm, 1)
    
    print('    The TRF to CRF matrix build......')
    t2c = mod_trs2crsn(eopObs,scanList,parallelFlag)

        
    print('    Compute Station correlation information......')
    resultStation = parallelStation(numSta, t2c.trs2crs, rq, scan2Source, ephem, scanMJD, scanTime, \
                                    StatScan, eopObs, stationInfo, createFlag, Press, Temp, GPT3Data, Param.Map.mapFun, Param.Map.tidalCorrect)
    print('    Compute theoretical delay and parameter partial......')        
    resultDelay = parallelDelay(scanList, scanMJD, refMJD, scan2Source, scanBl, scanCabCal, scanGD, scanGDSig, \
                                rq, pRaDec, t2c, ephem, StatScan, resultStation, bandNum, createFlag, parallelFlag)
        
    integrateResultSta(resultStation, StatScan, scanInfo, Scan2Station)
    com = integrateResultDelay(resultDelay, scanInfo, createFlag, parallelFlag)
        
    return eopObs,com
    
def parallelStation(numSta, trs2crs, rq, scan2Source, ephem, scanMJD, scanTime, \
                    StatScan, eopObs, stationInfo, createFlag, Press, Temp, GPT3Data, mapFlag, tidalFlag):
    
    poolSta = Pool(processes=numSta)
    args_list = []
    #'''
    for i in range(numSta):
        scanP = StatScan[i][0]
        if createFlag == 'CREATE':
            scanPress = []
            scanTemp = []
        else:
            #scanPress = Press[i]
            #scanTemp = Temp[i]
            scanPress = Press[i][StatScan[i][2]]
            scanTemp = Temp[i][StatScan[i][2]]
        
        args = (trs2crs[scanP], rq[scan2Source[scanP]], ephem.moon.xgeo[:,scanP], ephem.sun.xgeo[:,scanP], \
                                                ephem.earth.vbar[:,scanP], scanMJD[scanP], scanTime[scanP], \
                                                i, eopObs.XP[scanP], eopObs.YP[scanP], stationInfo, createFlag, \
                                                scanPress, scanTemp, GPT3Data, mapFlag, tidalFlag)
        args_list.append(args)
    #'''
    #    staPositCorr(args)
    results = poolSta.map(staPositCorr,args_list)
    
    return results
                            
    
def parallelDelay(scanList, scanMJD, refMJD, scan2Source, scanBl, scanCabCal, scanGD, scanGDSig, \
                  rq, pRaDec, t2c, ephem, StatScan, results_station, bandNum, createFlag, parallelFlag):
    
    if parallelFlag == 'YES':
        poolDelay = Pool(processes=4)
        args_list = []
        
        for i in range(4):
            args = (scanList[i], scanMJD, refMJD, scan2Source,scanBl, scanCabCal, scanGD, scanGDSig, \
                    rq, pRaDec, t2c, ephem, StatScan, results_station, bandNum, createFlag)
            args_list.append(args)
            
        results_delay = poolDelay.map(processScan,args_list)
    else:
        args = (scanList, scanMJD, refMJD, scan2Source,scanBl, scanCabCal, scanGD, scanGDSig, \
                rq, pRaDec, t2c, ephem, StatScan, results_station, bandNum, createFlag)
        results_delay = processScan(args)
    
    return results_delay   

def processScan(args):
    
    scanList, scanMJD, refMJD, scan2Source, scanBl, scanCabCal, scanGD, scanGDSig, \
        rq, pRaDec, t2c, ephem, StatScan, results, bandNum, createFlag = \
        args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args[9],\
            args[10],args[11],args[12],args[13],args[14],args[15]
    
    
    delayScan = DELAYSCAN()
    delayScan.scanList = scanList
    
    oc_obs = []
    pObs = []
    for i in range(bandNum):
        oc_obs.append([])
        pObs.append([])

    #fid = open('/home/GeoAS/Work/grav.delay', 'w')
    for iscan in scanList:
        
        # the observe source vector
        idSource = scan2Source[iscan]
        rqr = rq[idSource]
        rqu = rqr/np.linalg.norm(rqr) # unit vector
        
        vearth = ephem.earth.vbar[:,iscan]
        
        # theoretical delay compute for each baseline of each scan
        pxyz = []
                
        for ib in range(len(scanBl[iscan])):
            idSta1 = scanBl[iscan][ib][0]
            idSta2 = scanBl[iscan][ib][1]
            iscan1 = StatScan[idSta1][0].tolist().index(iscan)
            iscan2 = StatScan[idSta2][0].tolist().index(iscan)
            
            ista1 = StatScan[idSta1][1][iscan1]
            ista2 = StatScan[idSta2][1][iscan2]

    
            trsSta1 = results[idSta1].trs[iscan1]
            trsSta2 = results[idSta2].trs[iscan2]
            crsSta1 = results[idSta1].crs[iscan1]
            crsSta2 = results[idSta2].crs[iscan2]
            v1 = results[idSta1].vgeo[iscan1]
            v2 = results[idSta2].vgeo[iscan2]
            
            crsBL = crsSta2 - crsSta1
            trsBL = trsSta2 - trsSta1
            
                
            com_delay = comDelay(iscan, crsSta1, crsSta2, idSta1, idSta2, ephem, rqu, v1, v2)
            # delayScan.com.append([com_delay,rqu@(v2-v1)/const.c])
            #delayScan.com.extend([com_delay])

            # theoretical delay correct of tropsphere
            com_delay += results[idSta1].staObs[iscan1][7]*rqu@(v2-v1)/const.c # [s]
            com_delay += results[idSta2].staObs[iscan2][7] - results[idSta1].staObs[iscan1][7] # total delay
            # axis offset correct
            com_delay += results[idSta2].staObs[iscan2][5] - results[idSta1].staObs[iscan1][5]
            # gravity deformation correct
            com_delay += results[idSta2].staObs[iscan2][9] - results[idSta1].staObs[iscan1][9]


            #fid.writelines('%2d %2d %5.1f %5.1f %10.1f ps\n'%(idSta1,idSta2,(np.pi/2-results[idSta1].staObs[iscan1][4])*180/np.pi, \
            #                                                  (np.pi/2-results[idSta2].staObs[iscan2][4]) * 180 / np.pi,\
            #                                      (results[idSta2].staObs[iscan2][9] - results[idSta1].staObs[iscan1][9])*1E12))

                        
            if createFlag != 'CREATE':
                
                corcab = scanCabCal[iscan][ista2] - scanCabCal[iscan][ista1]
                for iband in range(bandNum):
                    oc_obs[iband].append(scanGD[iscan][iband][ib]+corcab-com_delay)
                    pObs[iband].append(scanGDSig[iscan][iband][ib])

                    #if iband == 1:
                    #    fid.writelines('%20.15f %20.15f %20.15f %20.15f %20.15f\n'%(scanGD[iscan][iband][ib]+corcab,com_delay,
                    #                                                                results[idSta2].staObs[iscan2][7] - results[idSta1].staObs[iscan1][7],
                    #                                                                results[idSta2].staObs[iscan2][5] - results[idSta1].staObs[iscan1][5],
                    #                                                                results[idSta2].staObs[iscan2][9] - results[idSta1].staObs[iscan1][9]))


                # delayScan.oc_obs.append(scanGD[iscan][ib]+corcab-com_delay)
                # delayScan.pObs.append(scanGDSig[iscan][ib])
            
            # partial derivatives
            beta = vearth/const.c
            b2 = (v2 + vearth)/const.c
            gam = 1/np.sqrt(1-beta@beta)
            rho = 1+rqr@b2
            dij = np.identity(3)
            
            psi = -(gam*(1-beta@b2)*rqr/rho+gam*beta)
            E = dij + ((gam-1)*beta/(beta@beta)-gam*b2)@beta
            K = E@psi
            B = K@t2c.trs2crs[iscan]
            M = (dij-rqr@b2/rho)@((-gam)*(1-b2@beta)*(E@crsBL/rho))
            
            
            # EOP partial
            delayScan.pEOP.append([K@(t2c.dxp[iscan]@trsBL)/const.c,\
                                   K@(t2c.dyp[iscan]@trsBL)/const.c,\
                                   K@(t2c.dut1[iscan]@trsBL)/const.c,\
                                   K@(t2c.ddX[iscan]@trsBL)/const.c,\
                                   K@(t2c.ddY[iscan]@trsBL)/const.c,\
                                   K@(t2c.dxp[iscan]@trsBL)*(scanMJD[iscan]-refMJD)/const.c,\
                                   K@(t2c.dyp[iscan]@trsBL)*(scanMJD[iscan]-refMJD)/const.c,\
                                   K@(t2c.dut1[iscan]@trsBL)*(scanMJD[iscan]-refMJD)/const.c])
            
            # station partial
            pxyz.append(B)
            delayScan.pxyz.append(B)
            
            # source partial from calc11
            psou = partialSource(vearth, v1, v2, rqu, crsBL, pRaDec[idSource])
            delayScan.psou.append(psou)

        delayScan.pxyzt.append(pxyz) #modify 2022.11.24
    #fid.close()
    delayScan.oc_obs = oc_obs
    delayScan.pObs = pObs
    
    return delayScan
    
def partialSource(vearth, v1, v2, rqu, crsBL, pRaDec):
    """
    Get the modified partial of source Ra and Dec

    Parameters
    ----------
    vearth : the velocity of earth in BCRS.
    v1 ,v2 : the velocity of station 1 and v2.
    rqu : the source direction.
    crsBL : the baseline position in CRS.
    pRaDec : partial of Ra and Dec.

    Returns
    -------
    Modified partial of source Ra and Dec of delay and rate (cm/mas, m/s**2).

    """
    
    vg = vearth + v2
    bv = v2 - v1
    tt = 1.0 + 1.0/const.c * rqu@vg
    
    #*np.pi/180/3.6E6
    pRa = (pRaDec[0,:]@crsBL/(const.c*tt) - (rqu@crsBL)*(vg@pRaDec[0,:])/const.c**2)*const.c # (m/rad)
    pRar = pRaDec[0,:]@bv/(const.c*tt) - (rqu@bv)*(vg@pRaDec[0,:])/const.c**2
    
    pDec = (pRaDec[1,:]@crsBL/(const.c*tt) - (rqu@crsBL)*(vg@pRaDec[1,:])/const.c**2)*const.c # (m/rad)
    pDecr = pRaDec[1,:]@bv/(const.c*tt) - (rqu@bv)*(vg@pRaDec[1,:])/const.c**2
    
    # return np.array([[pRa,pDec],[pRar,pDecr]])
    return np.array([pRa,pDec])

def getStatScan(num, Scan2Station):
    """
    Get the scan posit and station posit in scan of station

    Parameters
    ----------
    num : All station number.
    Scan2Station : scan and station relevance.

    Returns
    -------
    StatScan : scan posit and station posit in scan for all station.

    """

    StatScan = []
    for i in range(num):
        scanPosit = []
        scanInObs = []
        staScan = np.where(Scan2Station[:,i]!=0)
        
        for scanNum in staScan[0]:
            scanInObs.append(Scan2Station[scanNum,i]-1)
            temp = np.where(Scan2Station[scanNum,:i]!=0)
            if len(temp[0]):
                scanPosit.append(len(temp[0]))
            else:
                scanPosit.append(0)
            
        StatScan.append([staScan[0], scanPosit, scanInObs])
        
    return StatScan

def integrateResultSta(resultStation, StatScan, scanInfo, Scan2Station):
    
    scanMFW = []
    scanMFGE = []
    scanMFGN = []
    
    trs = []
    
    for i in range(len(scanInfo.scanMJD)):
        staPositINScan = np.where(Scan2Station[i,:]!=0)
        
        tempMFW = []
        tempMFGE = []
        tempMFGN = []
        temptrs = []
        
        for sta in staPositINScan[0]:
            scanPositInSta = StatScan[sta][0].tolist().index(i)
            tempMFW.append(resultStation[sta].mpf[scanPositInSta][1])
            tempMFGE.append(resultStation[sta].mpf[scanPositInSta][2])
            tempMFGN.append(resultStation[sta].mpf[scanPositInSta][3])
            temptrs.append(resultStation[sta].trs[scanPositInSta])
            
        scanMFW.append(tempMFW)
        scanMFGE.append(tempMFGE)
        scanMFGN.append(tempMFGN)
        trs.append(np.array(temptrs))
        
    scanInfo.scanMFW = scanMFW
    scanInfo.scanMFGE = scanMFGE
    scanInfo.scanMFGN = scanMFGN
    scanInfo.staTRS = trs
    
def integrateResultDelay(resultDelay, scanInfo, createFlag, parallelFlag):
    
    if parallelFlag == 'YES':
        com = []
        oc_obs = []
        pObs = []
        for i in range(len(resultDelay[0].oc_obs)):
            oc_obs.append([])
            pObs.append([])
        
        for i in range(len(resultDelay)):
            scanInfo.pEOP.extend(resultDelay[i].pEOP)
            for j in range(len(resultDelay[0].oc_obs)):
                oc_obs[j].extend(resultDelay[i].oc_obs[j])
                pObs[j].extend(resultDelay[i].pObs[j])
            com.extend(resultDelay[i].com)
            # scanInfo.pObs.extend(resultDelay[i].pObs)
            # scanInfo.oc_obs.extend(resultDelay[i].oc_obs)
            scanInfo.pxyz.extend(resultDelay[i].pxyz)
            scanInfo.psou.extend(resultDelay[i].psou)
            
        scanInfo.pObs = pObs
        scanInfo.oc_obs = oc_obs
    else:
        scanInfo.oc_obs = resultDelay.oc_obs
        scanInfo.pObs = resultDelay.pObs
        scanInfo.pEOP = resultDelay.pEOP
        scanInfo.pxyz = resultDelay.pxyz
        scanInfo.psou = resultDelay.psou
        com = resultDelay.com
    return com