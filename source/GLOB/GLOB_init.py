#!/usr/bin/env python3

import os,sys
import numpy as np
from INIT import read_SNX
from INIT.read_discontinuous import *
from GLOB.GLOB_matrix import *
from GLOB.GLOB_check import *
from INIT.read_sourceFile import *

def globalPrepareNew(Param):
    print('    Global solution......')

    checkParam(Param)

    sitAll = []
    souAll = []

    sitDC = read_discontinue('/home/GeoAS/Work/GASV/APRIORI/vlbi_discontinuous.txt')
    vtpvSession = 0
    numObs = 0
    numRed = 0
    for isnx in range(len(Param.Arcs.session)):
        sessionName = Param.Arcs.session[isnx]
        print(sessionName)
        year = get_year(sessionName)
        # filePath = os.path.join(Param.Out.snxPath[1],'VLBI_IVS',sessionName)
        # filePath = os.path.join(Param.Out.snxPath[1],str(year),sessionName)
        filePath = os.path.join(Param.Out.snxPath[1], sessionName)
        sitEst, souEst, paramSession, Ns, bs, solutionStatics = read_SNX(filePath, 3)
        numObs += solutionStatics['NoO']
        updateSitNew(sitDC, sitEst, paramSession)

        # get all station and source of all sinex
        rmStaNum = 0
        rmSouNum = 0
        if isnx == 0:
            sitAll = sitEst
            sitAll['ObsNum'] = np.ones(len(sitEst['code']), dtype=int).tolist()
            deleteStation(sitAll, Param.Global.station)
            souAll = souEst
            souAll['ObsNum'] = np.ones(len(souEst['name']), dtype=int).tolist()
        else:
            numAdd = np.zeros(2, dtype=int)
            for i in range(len(sitEst['code'])):
                sit = sitEst['code'][i]
                osit = sitEst['ocode'][i]
                sitName = sitEst['name'][i]
                if sitName not in Param.Global.station:
                    try:
                        index = sitAll['name'].index(sitName)
                        sitAll['ObsNum'][index] += 1
                        sitAll['estEpoch'][index].extend(sitEst['estEpoch'][i])
                        sitAll['estPosit'][index].extend(sitEst['estPosit'][i])
                    except ValueError:
                        sitAll['code'].append(sit)
                        sitAll['ocode'].append(osit)
                        sitAll['dome'].append(sitEst['dome'][i])
                        sitAll['name'].append(sitEst['name'][i])
                        sitAll['oname'].append(sitEst['oname'][i])
                        sitAll['ObsNum'].append(1)
                        sitAll['estEpoch'].append([])
                        sitAll['estPosit'].append([])
                        sitAll['estEpoch'][-1].extend(sitEst['estEpoch'][i])
                        sitAll['estPosit'][-1].extend(sitEst['estPosit'][i])
                        if Param.Global.station[0] == 'YES':
                            numAdd[0] += 1
                else:
                    rmStaNum += 1

            for i in range(len(souEst['name'])):
                sou = souEst['name'][i]
                if sou not in Param.Global.source:
                    try:
                        index = souAll['name'].index(sou)
                        souAll['ObsNum'][index] += 1
                        souAll['estEpoch'][index].extend(souEst['estEpoch'][i])
                        souAll['estPosit'][index].extend(souEst['estPosit'][i])
                    except ValueError:
                        souAll['name'].append(sou)
                        souAll['ObsNum'].append(1)
                        souAll['estEpoch'].append([])
                        souAll['estPosit'].append([])
                        souAll['estEpoch'][-1].extend(souEst['estEpoch'][i])
                        souAll['estPosit'][-1].extend(souEst['estPosit'][i])
                        if Param.Global.source[0] == 'YES':
                            numAdd[1] += 1
                else:
                    rmSouNum += 1

        updateSitAll(sitAll,souAll,Param)
        positInSession, positInGlob, sitObsEpoch = searchIndexNew(sitAll, souAll, paramSession, Param)
        #if sessionName == '01MAY18XN_bkg2022a':
        #    print('yes')
        checkProcess(positInSession,sitEst['code'],souEst['name'], Param, rmStaNum, rmSouNum)

        NsNew, bsNew = matrixRebuild(Ns, bs, positInSession[2])
        Nr, br, vtpvReduce,redNum = matrixReduce(NsNew, bsNew, len(positInSession[2]))
        vtpvSession += solutionStatics['WSSoOC'] - vtpvReduce
        numRed += redNum
        checkNum = [len(positInSession[0]), len(positInSession[1])]

        if isnx == 0:
            Nrn, brn = matrixTransfer(Nr, br, sitObsEpoch, checkNum, Param, 0)
        else:
            Nrn, brn = matrixTransfer(Nr, br, sitObsEpoch, checkNum, Param, 1)

        numAll = np.array([len(sitAll['name']), len(souAll['name'])])
        if Param.Global.source[0] == 'NO':
            numAll = np.array([len(sitAll['name']), 0])
        if isnx == 0:
            NGlob = Nrn
            bGlob = brn
        else:
            if sum(numAdd) != 0:
                #NGlob, bGlob = matrixExtend(NGlob, bGlob, Param, numAll, numAdd)
                #'''
                NGlob, bGlob = matrixExtendNew(NGlob, bGlob, Param, sitAll['globEstSitPosit'],
                                               sitAll['globEstSitVelPosit'], numAll, numAdd,\
                                               sitAll['estNum'])
                #'''
            matrixStack(NGlob, Nrn, bGlob, brn, positInGlob[2])

    fid = open('souAll.txt','w')
    for name in souAll['name']:
        fid.writelines(name+'\n')
    fid.close()

    get_stationTRF(Param, sitAll)
    get_sourceCRF(Param, souAll)
    setGlobalConstrainFlag(sitAll, souAll, Param)

    return sitAll, souAll, NGlob, bGlob, vtpvSession,numObs-numRed


def globalPrepare(Param):
    print('    Global solution......')
    sitAll = []
    souAll = []

    sitDC = read_discontinue('/home/GeoAS/Work/GATV/APRIORI/vlbi_discontinuous.txt')
    for isnx in range(len(Param.Arcs.session)):
        sessionName = Param.Arcs.session[isnx]
        print(sessionName)
        year = get_year(sessionName)
        # filePath = os.path.join(Param.Out.snxPath[1],'VLBI_IVS',sessionName)
        # filePath = os.path.join(Param.Out.snxPath[1],str(year),sessionName)
        filePath = os.path.join(Param.Out.snxPath[1], sessionName)
        sitEst, souEst, paramSession, Ns, bs = read_SNX(filePath, 3)

        updateSit(sitDC, sitEst)

        # get all station and source of all sinex
        if isnx == 0:
            sitAll = sitEst
            sitAll['ObsNum'] = np.ones(len(sitEst['code']), dtype=int).tolist()
            deleteStation(sitAll, Param.Global.station)
            souAll = souEst
            souAll['ObsNum'] = np.ones(len(souEst['name']), dtype=int).tolist()
        else:
            numAdd = np.zeros(2, dtype=int)
            for i in range(len(sitEst['code'])):
                sit = sitEst['code'][i]
                sitName = sitEst['name'][i]
                if sitName not in Param.Global.station:
                    try:
                        index = sitAll['name'].index(sitName)
                        sitAll['ObsNum'][index] += 1
                        sitAll['estEpoch'][index].extend(sitEst['estEpoch'][i])
                        sitAll['estPosit'][index].extend(sitEst['estPosit'][i])
                    except ValueError:
                        sitAll['code'].append(sit)
                        sitAll['dome'].append(sitEst['dome'][i])
                        sitAll['name'].append(sitEst['name'][i])
                        sitAll['oname'].append(sitEst['oname'][i])
                        sitAll['ObsNum'].append(1)
                        sitAll['estEpoch'].append([])
                        sitAll['estPosit'].append([])
                        sitAll['estEpoch'][-1].extend(sitEst['estEpoch'][i])
                        sitAll['estPosit'][-1].extend(sitEst['estPosit'][i])
                        if Param.Global.station[0] == 'YES':
                            numAdd[0] += 1

            for i in range(len(souEst['name'])):
                sou = souEst['name'][i]
                if sou not in Param.Global.source:
                    try:
                        index = souAll['name'].index(sou)
                        souAll['ObsNum'][index] += 1
                        souAll['estEpoch'][index].extend(souEst['estEpoch'][i])
                        souAll['estPosit'][index].extend(souEst['estPosit'][i])
                    except ValueError:
                        souAll['name'].append(sou)
                        souAll['ObsNum'].append(1)
                        souAll['estEpoch'].append([])
                        souAll['estPosit'].append([])
                        souAll['estEpoch'][-1].extend(souEst['estEpoch'][i])
                        souAll['estPosit'][-1].extend(souEst['estPosit'][i])
                        if Param.Global.source[0] == 'YES':
                            numAdd[1] += 1

        positInSession, positInGlob, sitObsEpoch = searchIndex(sitAll, souAll, paramSession, Param)
        NsNew, bsNew = matrixRebuild(Ns, bs, positInSession[2])
        Nr, br = matrixReduce(NsNew, bsNew, len(positInSession[2]))

        checkNum = [len(positInSession[0]), len(positInSession[1])]

        if isnx == 0:
            Nrn, brn = matrixTransfer(Nr, br, sitObsEpoch, checkNum, Param, 0)
        else:
            Nrn, brn = matrixTransfer(Nr, br, sitObsEpoch, checkNum, Param, 1)

        numAll = np.array([len(sitAll['name']), len(souAll['name'])])
        if Param.Global.source[0] == 'NO':
            numAll = np.array([len(sitAll['name']), 0])
        if isnx == 0:
            NGlob = Nrn
            bGlob = brn
        else:
            if sum(numAdd) != 0:
                NGlob, bGlob = matrixExtend(NGlob, bGlob, Param, numAll, numAdd)
            matrixStack(NGlob, Nrn, bGlob, brn, positInGlob[2])

    get_stationTRF(Param, sitAll)
    get_sourceCRF(Param, souAll)
    setGlobalConstrainFlag(sitAll, souAll, Param)

    return sitAll, souAll, NGlob, bGlob

def deleteStation(sitAll, rmStation):
    
    rmPosit = []
    for i in range(len(sitAll['name'])):
        if sitAll['name'][i] in rmStation:
            rmPosit.append(i)
    
    if len(rmPosit):
        for i in range(len(rmPosit)):
            temp = rmPosit[i] - i
            
            for key in sitAll.keys():
                del sitAll[key][temp]

def get_sourceCRF(Param, souAll):
    
    souAll['RaDe'] = []
    iersName,icrfName,iauName,ivsName,flag,Ra,De = readSourceFile(Param.Map.sourceFile)
 
    for isou in range(len(souAll['name'])):
        index = -1
        souName = souAll['name'][isou]
        if souName in iersName:
            index = iersName.index(souAll['name'][isou])
        elif souName in ivsName:
            index = ivsName.index(souAll['name'][isou])
        else:
            print('Error: %s not in source file!'%souName)
            sys.exit()
            
        souAll['RaDe'].append([Ra[index],De[index]])

def get_stationTRF(Param, sitAll):
    
    sitAll['ITRF'] = []
    stationFile = Param.Map.stationFile
    station = np.loadtxt(stationFile, dtype='str',comments='$$',usecols=[0], unpack=True)
    station = station.tolist()
    staPosit = np.loadtxt(stationFile, dtype='float',comments='$$',usecols=[1,2,3,4,5,6,7], unpack=False)
 
    for isit in range(len(sitAll['oname'])):
        try:
            index = station.index(sitAll['oname'][isit])
        except ValueError:
            index = -1
            
        if index != -1:
            sitAll['ITRF'].append(staPosit[index])
            
    
    
def get_year(name):
    
    # if len(name) == 9:
    #     year = 2000 + int(name[:2])
    # else:
    #     if '-' in name:
    #         index = name.index('-')
    #         if index == 8:
    #             year = int(name[0:4])
    #         elif index == 7:
    #             year = 2000 + int(name[1:3])
                
    year = 2000 + int(name[:2])
                
    return year


def searchIndex(sitAll, souAll, paramSession, Param):
    '''
    Get the parameter position in global solution

    Parameters
    ----------
    sitAll : list
        all station code list.
    souAll : list
        all source name list.
    paramInfo : Dictionary
        the session parameter.

    Returns
    -------
    None.

    '''
    positInSession = [[], [], []]  # first is sit position, second is sou position,third is all
    positInGlob = [[], [], []]  # first is sit position and vel, second is sou position,third is all
    sitEpoch = []

    # station search
    if Param.Global.station[0] == 'YES':
        numSit = len(sitAll['code'])
        for isit in range(numSit):
            sit = sitAll['code'][isit]

            try:
                index = paramSession['code'].index(sit)
                positInSession[0].extend(paramSession['Nposit'][index])
                sitEpoch.append(paramSession['RefEpoch'][index])

                if Param.Flags.vel[0] == 'YES':
                    positInGlob[0].extend([isit * 3, isit * 3 + 1, isit * 3 + 2, \
                                           numSit * 3 + isit * 3, numSit * 3 + isit * 3 + 1, numSit * 3 + isit * 3 + 2])
                else:
                    positInGlob[0].extend([isit * 3, isit * 3 + 1, isit * 3 + 2])
            except ValueError:
                continue

    # source search
    if Param.Global.source[0] == 'YES':
        numSou = len(souAll['name'])
        for isou in range(numSou):
            sou = souAll['name'][isou]

            try:
                index = paramSession['code'].index(sou)
                positInSession[1].extend(paramSession['Nposit'][index])
                # sitEpoch.append(paramSession['RefEpoch'][index])

                if Param.Global.station[0] == 'YES' and Param.Flags.vel[0] == 'YES':
                    positInGlob[1].extend([numSit * 6 + isou * 2, numSit * 6 + isou * 2 + 1])
                else:
                    positInGlob[1].extend([numSit * 3 + isou * 2, numSit * 3 + isou * 2 + 1])

            except ValueError:
                continue

    for i in range(2):
        positInSession[2].extend(positInSession[i])
        positInGlob[2].extend(positInGlob[i])

    return positInSession, positInGlob, sitEpoch

def searchIndexNew(sitAll, souAll, paramSession, Param):
    '''
    Get the parameter position in global solution

    Parameters
    ----------
    sitAll : list
        all station code list.
    souAll : list
        all source name list.
    paramInfo : Dictionary
        the session parameter.

    Returns
    -------
    None.

    '''
    positInSession = [[],[],[]] #first is sit position, second is sou position,third is all
    positInGlob = [[],[],[]] #first is sit position and vel, second is sou position,third is all
    sitEpoch = []
    
    # station search
    if Param.Global.station[0] == 'YES':
        numSit = len(sitAll['code'])
        for isit in range(numSit):
            sit = sitAll['code'][isit]
            
            try:
                index = paramSession['code'].index(sit)
                positInSession[0].extend(paramSession['Nposit'][index])
                sitEpoch.append(paramSession['RefEpoch'][index])
                
                if Param.Flags.vel[0] == 'YES':
                    positInGlob[0].extend([sitAll['globEstSitPosit'][isit*3],\
                                           sitAll['globEstSitPosit'][isit*3 + 1],\
                                           sitAll['globEstSitPosit'][isit*3 + 2],\
                                           sitAll['globEstSitVelPosit'][isit*3],\
                                           sitAll['globEstSitVelPosit'][isit*3 + 1],\
                                           sitAll['globEstSitVelPosit'][isit*3 + 2]])
                else:
                    positInGlob[0].extend([sitAll['globEstSitPosit'][isit * 3], \
                                           sitAll['globEstSitPosit'][isit * 3 + 1], \
                                           sitAll['globEstSitPosit'][isit * 3 + 2]])
            except ValueError:
                continue
    
    # source search
    if Param.Global.source[0] == 'YES':
        numSou = len(souAll['name'])
        for isou in range(numSou):
            sou = souAll['name'][isou]
    
            try:
                index = paramSession['code'].index(sou)
                positInSession[1].extend(paramSession['Nposit'][index])
                # sitEpoch.append(paramSession['RefEpoch'][index])

                '''
                if Param.Global.station[0] == 'YES' and Param.Flags.vel[0] == 'YES':
                    positInGlob[1].extend([numSit*6+isou*2,numSit*6+isou*2+1])
                else:
                    positInGlob[1].extend([numSit*3+isou*2,numSit*3+isou*2+1])
                '''
                positInGlob[1].extend([sum(sitAll['estNum'])*3+isou*2,sum(sitAll['estNum'])*3+isou*2+1])
                
            except ValueError:
                continue
            
    for i in range(2):
        positInSession[2].extend(positInSession[i])
        positInGlob[2].extend(positInGlob[i])

    return positInSession, positInGlob, sitEpoch
    
def setGlobalConstrainFlag(sitAll, souAll, Param):
    '''
    set the global NNR and NNT constrain for station.
    the global NNR and NNT constrain of velocity of station is the same.
    set the global NNR constrain for source.

    Parameters
    ----------
    sitAll : Dict
        all station information.
    souAll : Dict
        all source information.
    Param : Class
        control file information.

    Returns
    -------
    None.

    '''
    sitNum = len(sitAll['name'])
    sitAll['nnrt'] = np.zeros(sitNum,dtype=int)
    
    if Param.Global.station[0] == 'YES':
        for i in range(len(sitAll['name'])):
            sitName = sitAll['name'][i]
            
            if Param.Const.nnr_nnt_sta[0][0] == 'YES' and Param.Const.nnr_nnt_sta[1][0] == 'YES':
                if sitName not in Param.Const.nnr_nnt_sta[0]:
                    sitAll['nnrt'][i] = 1
            else:
                if sitName in Param.Const.nnr_nnt_sta[0]:
                    sitAll['nnrt'][i] = 1
    
    souNum = len(souAll['name'])
    souAll['nnr'] = np.zeros(souNum,dtype=int)

    if Param.Global.source[0] == 'YES':
        for i in range(souNum):
            souName = souAll['name'][i]
            
            if Param.Const.nnr_sou[0] == 'YES':
                if souName not in Param.Const.nnr_sou:
                    souAll['nnr'][i] = 1
            else:
                if souName in Param.Const.nnr_sou:
                    souAll['nnr'][i] = 1

def updateSit(sitDC, sitEst):
    '''
    Change the name of station which has discontinuous caused by earthquake or rebuild.

    Parameters
    ----------
    sitDC : Dict
        discontinuous station information.
    sitEst : Dict
        station information from sinex.

    '''
    sitEst['oname'] = []

    for i in range(len(sitEst['name'])):
        sit = sitEst['name'][i]
        sitEst['oname'].append(sit)
        if sit in sitDC['name']:
            index = sitDC['name'].index(sit)
            sitEpoch = sitEst['estEpoch'][i]

            if sitEpoch <= sitDC['dcMJD'][index][0]:
                sitName = sitDC['newName'][index][0]
                sitCode = sitDC['newCode'][index][0]
            elif sitEpoch > sitDC['dcMJD'][index][-1]:
                sitName = sitDC['newName'][index][-1]
                sitCode = sitDC['newCode'][index][-1]
            else:
                for j in range(1,len(sitDC['dcMJD'][index])):
                    if sitEpoch <= sitDC['dcMJD'][index][j]:
                        sitName = sitDC['newName'][index][j]
                        sitCode = sitDC['newCode'][index][j]
            sitEst['name'][i] = sitName

def updateSitNew(sitDC, sitEst, paramSession):
    '''
    Change the name of station which has discontinuous caused by earthquake or rebuild.

    Parameters
    ----------
    sitDC : Dict
        discontinuous station information.
    sitEst : Dict
        station information from sinex.

    '''
    sitEst['oname'] = []
    sitEst['ocode'] = []
    #paramSession['oldCode'] = []

    for i in range(len(sitEst['name'])):
        sit = sitEst['name'][i]
        sitEst['oname'].append(sit)
        sitEst['ocode'].append( sitEst['code'][i])
        if sit in sitDC['name']:
            index = sitDC['name'].index(sit)
            sitEpoch = sitEst['estEpoch'][i]

            if sitEpoch <= sitDC['dcMJD'][index][0]:
                sitName = sitDC['newName'][index][0]
                sitCode = sitDC['newCode'][index][0]
            elif sitEpoch > sitDC['dcMJD'][index][-1]:
                sitName = sitDC['newName'][index][-1]
                sitCode = sitDC['newCode'][index][-1]
            else:
                for j in range(1,len(sitDC['dcMJD'][index])):
                    if sitEpoch <= sitDC['dcMJD'][index][j]:
                        sitName = sitDC['newName'][index][j]
                        sitCode = sitDC['newCode'][index][j]
            sitEst['name'][i] = sitName
            paramSession['code'][i] = paramSession['code'][i] + sitCode
            sitEst['code'][i] = sitEst['code'][i] + sitCode


def updateSitAll(sitAll,souAll,Param):
    sitAll['globEstSitPosit'] = []
    sitAll['globEstSitVelPosit'] = []
    souAll['globEstRaDePosit'] = []
    sitAll['velUsedFlag'] = []
    sitAll['estNum'] = [0,0]

    if Param.Global.station[0] == 'YES':
        sitNum = len(sitAll['code'])
        sitAll['estNum'][0] = sitNum
        if Param.Flags.vel[0] == 'YES':
            uniqueCode = []
            #for code in sitAll['code']:
            for code in sitAll['ocode']:
                if code not in uniqueCode:
                    uniqueCode.append(code)
                    sitAll['velUsedFlag'].append(1)
                else:
                    sitAll['velUsedFlag'].append(0)
            velNum = len(uniqueCode)
            sitAll['estNum'][1] = velNum
        for i in range(sitNum):
            sitAll['globEstSitPosit'].extend([i*3,i*3+1,i*3+2])
            if Param.Flags.vel[0] == 'YES':
                #index = uniqueCode.index(sitAll['code'][i])
                index = uniqueCode.index(sitAll['ocode'][i])
                sitAll['globEstSitVelPosit'].extend([sitNum*3+index * 3,\
                                                  sitNum*3+index * 3 + 1,\
                                                  sitNum*3+index * 3 + 2])

    if Param.Global.source[0] == 'YES':
        souNum = len(souAll['name'])
        souStartNum = sum(sitAll['estNum'])
        for i in range(souNum):
            souAll['globEstRaDePosit'].extend([souStartNum + i*2,\
                                               souStartNum + i*2+1])
