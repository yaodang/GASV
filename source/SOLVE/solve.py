#!/usr/bin/env python3

import sys
sys.path.append("..//")
from COMMON import *
from SOLVE import *

def solve(Param, scanInfo, stationInfo, sourceInfo, result, bandIndex, *args):
    
    print('\n------------------------  SOLVE  -----------------------')
    runFlag = 1
    outlierFlag = 0
    handFlag = 0
    
    handOut = []
    if len(args) == 1:
        handOut = args[0]
        handFlag = 1
 
    while runFlag or outlierFlag:
        if runFlag:
            staObs = pick_staObs(scanInfo,stationInfo)
        
        if len(handOut) and handFlag == 1:
            outlierFlag = getOutFlag(staObs, scanInfo, stationInfo, Param, \
                                     result, handOut, handFlag, bandIndex)
            handOut = []
            handFlag = 0
        
        print('    First solve to remove big clock diff......')
        
        # get baseline information and used in GUI
        sta_bl_sou_ResInfo(scanInfo)
        P_obs = np.diag(1/(np.array(scanInfo.pObs[bandIndex])*const.c)**2) # [m^-2]
        oc_obs = np.array(scanInfo.oc_obs[bandIndex])*const.c # [m]
        
        nobs = len(oc_obs)
        staNum = len(scanInfo.stationAll)
        result.preal = P_obs
        result.nObs = nobs
        
        ocObs,firstClk = firstSolution(scanInfo, stationInfo, P_obs, oc_obs, staObs)
        result.o_creal = ocObs
        
        # ambiguity remove
        # print('    Remove the ambiguity...')
        # staRefIndex = scanInfo.stationAll.index(scanInfo.refclk)
        # ambNum = np.zeros(len(scanInfo.Obs2Scan))
        # sigma = np.array(scanInfo.pObs[bandIndex])
        # # for i in range(10):
        # ambNum += correctAmbiguty(staNum, scanInfo, ocObs, sigma, scanInfo.baseInfo[2][bandIndex], staRefIndex)
        
        # correctIono(scanInfo, staObs)
            
        estFlag = check(Param)
        #print(staObs.oc_nob[0],staObs.oc_nob[3])
        if estFlag != 0:
            print('    Main solve: forming the matrix A......')
            estPara,Ablk,Hblk,Pobs,oc,staNNRT,souNNR = designMatrix(scanInfo, staObs, Param, stationInfo, sourceInfo, P_obs, ocObs)
            print('    Main solve: LSM the estimate parameter......')
            LSQSolution(estPara, Ablk, Hblk, Pobs, oc, ocObs, staNNRT, souNNR, nobs, result, bandIndex)

            if Param.Setup.weight == 'BL':
                print('\n    Reweight......')
                reweight(scanInfo, staObs, result, P_obs)
                P_obs = np.diag(1 / (np.array(scanInfo.pObs[bandIndex]) * const.c) ** 2)
                estPara, Ablk, Hblk, Pobs, oc, staNNRT, souNNR = designMatrix(scanInfo, staObs, Param, stationInfo,
                                                                              sourceInfo, P_obs, ocObs)
                LSQSolution(estPara, Ablk, Hblk, Pobs, oc, ocObs, staNNRT, souNNR, nobs, result, bandIndex)

            if handFlag == 0:
                outlierFlag,rmPosit = getOutFlag(staObs, scanInfo, stationInfo, Param, result, handOut, handFlag, bandIndex)
                # print(outlierFlag,rmPosit)
        else:
            outlierFlag = 0
        
        runFlag = 0
        '''
        if Param.Setup.weight == 'BL':
            print('\n    Reweight......')
            reweight(scanInfo, staObs, result, P_obs)
            P_obs = np.diag(1/(np.array(scanInfo.pObs[bandIndex])*const.c)**2)
            estPara,Ablk,Hblk,Pobs,oc,staNNRT,souNNR = designMatrix(scanInfo, staObs, Param, stationInfo, sourceInfo, P_obs, ocObs)
            LSQSolution(estPara, Ablk, Hblk, Pobs, oc, ocObs, staNNRT, souNNR, nobs, result, bandIndex)
        '''
        # iterNum = 10
        # while (result.chis > 1.05 or result.chis < 0.95) and iterNum:
        # #     print(result.chis)
        #     reweightValue = reweight(scanInfo, staObs, result, P_obs)
        #     # ocObs = firstSolution(scanInfo, stationInfo, P_obs, oc_obs, staObs)
        #     # result.o_creal = ocObs
            
        #     estPara,Ablk,Hblk,Pobs,oc,staNNRT,souNNR = designMatrix(scanInfo, staObs, Param, stationInfo, sourceInfo, P_obs, ocObs)
        #     LSQSolution(estPara, Ablk, Hblk, Pobs, oc, ocObs, staNNRT, souNNR, nobs, result, bandIndex)
            
        #     iterNum -= 1
    
    if estFlag != 0:
        reduceSNX(result, Param.Out.snxPath)
    elif estFlag == 0:
        result.VReal[bandIndex] = ocObs
        result.SReal[bandIndex] = np.array(scanInfo.pObs[bandIndex])*const.c-0.005 # [m]
        result.flag[bandIndex] = 1

    '''
    fid = open('/home/GeoAS/Work/Tools/20250828_clkout/clk_aips_jlkm.txt', 'a')
    fid.writelines('%11.5f %20.12e %20.12e %20.12e ' % (scanInfo.scanMJD[0], firstClk[0], firstClk[1], firstClk[2]))
    #fid.writelines(
    #    '%6.1f %6.1f %6.1f %20.12e %20.12e %20.12e\n' % (estPara.tmjd[0][0], estPara.tmjd[0][1], estPara.tmjd[0][2],
    #                                               result.para[0], result.para[1], result.para[2]))
    fid.writelines(
        '%6.1f %6.1f %20.12e %20.12e \n' % (estPara.tmjd[0][0], estPara.tmjd[0][1],
                                                         result.para[0], result.para[1]))
    fid.close()
    #'''
    return staObs



    
    
    
