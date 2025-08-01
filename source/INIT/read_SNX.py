#!/usr/bin/env python3

import sys
sys.path.append('..//')
import numpy as np
import gzip
from COMMON.time_transfer import *

def read_SNX(filePath,flag):
    
    if '.gz' in filePath:
        fid = gzip.open(filePath, 'rt')
    else:
        if '.snx' in filePath:
            fid = open(filePath, 'r')
        else:
            fid = open(filePath+'.snx','r')
        
    lines = fid.readlines()
    fid.close()
    
    blockPosit = get_posit(lines)
    # print(blockPosit)
    
    #if flag == 0:
    solutionStatistics = get_solutionStatistics(lines, blockPosit[3])
        #return solutionStatistics
    if flag > 0:
        sitID = get_siteID(lines, blockPosit[0])
        souID = get_souID(lines, blockPosit[1])
        paramInfo, souEst = get_solutionApriori(lines, blockPosit[4], souID)
        get_solutionEstimate(lines, blockPosit[5], paramInfo)
        addInfo(sitID, souEst, paramInfo)
        
    if flag > 1:
        normalMatrix = get_solutionNormalEquation(lines, blockPosit[6])
        normalVector = get_solutionNormalVector(lines, blockPosit[7])
    if flag == 0:
        return solutionStatistics
    elif flag == 1:
        return sitID, souEst
    elif flag == 2:
        # return paramInfo,normalMatrix
        return paramInfo,normalMatrix,normalVector
    elif flag == 3:
        return sitID, souEst, paramInfo,normalMatrix,normalVector,solutionStatistics

def addInfo(sitEst, souEst, paramInfo):
    
    # station
    for i in range(len(sitEst['name'])):
        index = paramInfo['code'].index(sitEst['code'][i])
        sitEst['estEpoch'][i].append(paramInfo['RefEpoch'][index])
        sitEst['estPosit'][i].append([paramInfo['estValue'][paramInfo['Nposit'][index][0]],\
                                      paramInfo['estValue'][paramInfo['Nposit'][index][1]],\
                                      paramInfo['estValue'][paramInfo['Nposit'][index][2]]])
            
    # source
    for i in range(len(souEst['name'])):
        index = paramInfo['code'].index(souEst['name'][i])
        souEst['estEpoch'][i].append(paramInfo['RefEpoch'][index])
        souEst['estPosit'][i].append([paramInfo['estValue'][paramInfo['Nposit'][index][0]],\
                                      paramInfo['estValue'][paramInfo['Nposit'][index][1]]])
        

def get_posit(lines):
    blockPosit = np.zeros((8,2),dtype=int)
    
    blockPosit[0,0],blockPosit[0,1] = findPosit(lines, 'SITE/ID')
    blockPosit[1,0],blockPosit[1,1] = findPosit(lines, 'SOURCE/ID')
    blockPosit[2,0],blockPosit[2,1] = findPosit(lines, 'SOLUTION/EPOCHS')
    blockPosit[3,0],blockPosit[3,1] = findPosit(lines, 'SOLUTION/STATISTICS')
    blockPosit[4,0],blockPosit[4,1] = findPosit(lines, 'SOLUTION/APRIORI')
    blockPosit[5,0],blockPosit[5,1] = findPosit(lines, 'SOLUTION/ESTIMATE')
    blockPosit[6,0],blockPosit[6,1] = findNormal(lines, ['SOLUTION/NORMAL_EQUATION_MATRIX U',\
                                                         'SOLUTION/NORMAL_EQUATION_MATRIX L',\
                                                         'SOLUTION/DECOMPOSED_NORMAL_MATRIX'])
    blockPosit[7,0],blockPosit[7,1] = findNormal(lines, ['SOLUTION/NORMAL_EQUATION_VECTOR',\
                                                         'SOLUTION/DECOMPOSED_NORMAL_VECTOR'])
            
    return blockPosit

def get_siteID(lines, posit):
    siteID = {'code':[],\
              'dome':[],\
              'name':[],\
              'estPosit':[],\
              'estEpoch':[]}
    
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line.split(" ")))
            siteID['code'].append(temp[0])
            siteID['dome'].append(temp[2])
            #siteID['name'].append(line[21:-1].strip())
            siteID['name'].append(temp[4])
            siteID['estPosit'].append([])
            siteID['estEpoch'].append([])
    
    return siteID
            
def get_souID(lines, posit):
    souID = {'code':[],\
             'iersName':[],\
             'ivsName':[]}
    
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line[:-1].split(" ")))
            souID['code'].append(temp[0])
            souID['iersName'].append(temp[1])
            if len(temp) == 5:
                souID['ivsName'].append(temp[4])
            elif len(temp) == 6:
                souID['ivsName'].append(temp[5])
            else:
                souID['ivsName'].append(temp[1])
            
    return souID
            
def get_solutionEpochs(lines, posit):
    solutionEpochs = {'code':[],\
                      'startTime':[],\
                      'stopTime':[],\
                      'meanTime':[]}
    
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line.split(" ")))
            solutionEpochs['code'].append(temp[0])
            solutionEpochs['startTime'].append(temp[4])
            solutionEpochs['stopTime'].append(temp[5])
            solutionEpochs['meanTime'].append(temp[6])
            
    return solutionEpochs
            
def get_solutionStatistics(lines, posit):
    solutionStatistics = {'NoO':0,\
                          'NoU':0,\
                          'WSSoOC':0,\
                          'VTPV':0,\
                          'VF':0,\
                          'WoPR':0}
    
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line.split(" ")))
            if 'NUMBER OF OBSERVATIONS' in line:
                solutionStatistics['NoO'] = int(temp[3])
            elif 'NUMBER OF UNKNOWNS' in line:
                solutionStatistics['NoU'] = int(temp[3])
            elif 'WEIGHTED SQUARE SUM OF O-C' in line:
                if 'D' in temp[5]:
                    temp[5] = temp[5].replace('D','E')
                solutionStatistics['WSSoOC'] = float(temp[5])
            elif 'SQUARE SUM OF RESIDUALS (VTPV)' in line:
                if 'D' in temp[5]:
                    temp[5] = temp[5].replace('D','E')
                solutionStatistics['VTPV'] = float(temp[5])    
            elif 'VARIANCE FACTOR' in line:
                if 'D' in temp[2]:
                    temp[2] = temp[2].replace('D','E')
                solutionStatistics['VF'] = float(temp[2])
            elif 'WRMS OF POSTFIT RESIDUALS' in line:
                if 'D' in temp[4]:
                    temp[4] = temp[4].replace('D','E')
                solutionStatistics['WoPR'] = float(temp[4])*1E12

    return solutionStatistics

def get_solutionApriori(lines, posit, souID):
    solutionApriori = {'code':[],\
                       'Nposit':[],\
                       'Param':[],\
                       'RefEpoch':[],\
                       'aprValue':[],\
                       'estValue':[]}
    souAll = {'name':[],\
             'estPosit':[],\
             'estEpoch':[]}
        
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line.split(" ")))
            number = int(temp[0])-1
            epochMJD = get_epochMJD(temp[5])
            value = float(temp[8].replace('D','E'))
            if temp[2] == '----':
                solutionApriori['code'].append(temp[1])
                solutionApriori['Nposit'].append([number])
                solutionApriori['Param'].append('eop')
                solutionApriori['RefEpoch'].append(epochMJD)
                solutionApriori['aprValue'].append([value])
                
            if 'STA' in temp[1]:
                if temp[2] not in solutionApriori['code']:
                    solutionApriori['code'].append(temp[2])
                    solutionApriori['Nposit'].append([number])
                    solutionApriori['Param'].append('xyz')
                    solutionApriori['RefEpoch'].append(epochMJD)
                    solutionApriori['aprValue'].append([value])
                else:
                    index = solutionApriori['code'].index(temp[2])
                    solutionApriori['Nposit'][index].append(number)
                    solutionApriori['aprValue'][index].append(value)
                    
            if 'RS_' in temp[1]:
                souPosit = souID['code'].index(temp[2])
                souName = souID['ivsName'][souPosit]
                
                if souName not in solutionApriori['code']:
                    souAll['name'].append(souName)
                    souAll['estPosit'].append([])
                    souAll['estEpoch'].append([])
                    
                    solutionApriori['code'].append(souName)
                    solutionApriori['Nposit'].append([number])
                    solutionApriori['Param'].append('sou')
                    solutionApriori['RefEpoch'].append(epochMJD)
                    solutionApriori['aprValue'].append([value])
                else:
                    index = solutionApriori['code'].index(souName)
                    solutionApriori['Nposit'][index].append(number)
                    solutionApriori['aprValue'][index].append(value)
                    
    return solutionApriori,souAll

def get_solutionEstimate(lines, posit, paramInfo):
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line.split(" ")))
            paramInfo['estValue'].append(float(temp[8].replace('D','E')))
            
def get_solutionNormalEquation(lines, posit):
        
    temp = list(filter(None,lines[posit[1]-1].split(" ")))
    num = int(temp[0])
    normalMatrix = np.zeros((num,num))
    
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line.split(" ")))
            if '\n' in temp:
                temp.remove('\n') #like bkg sinex 10APR12XA_bkg2022a
            row = int(temp[0]) - 1
            col = int(temp[1]) - 1
            
            for j in range(0,len(temp)-2):
                temp[j+2] = temp[j+2].replace('D','E')
            
                normalMatrix[row,col+j] = float(temp[j+2])
                normalMatrix[col+j,row] = float(temp[j+2])
            
    return normalMatrix

def get_solutionNormalVector(lines, posit):
    temp = list(filter(None,lines[posit[1]-1].split(" ")))
    num = int(temp[0])
    normalVector = np.zeros(num)
    
    for i in range(posit[0],posit[1]):
        line = lines[i]
        if line[0] != '*':
            temp = list(filter(None,line[:-1].split(" ")))
            row = int(temp[0]) - 1
            
            # for k in range(len(temp)-1,-1,-1):
            #     if temp[k] != ' ':
            #         break
            temp[-1] = temp[-1].replace('D','E')
            normalVector[row] = float(temp[-1])
            
    return normalVector

def get_epochMJD(timeStr):
    
    temp = list(filter(None,timeStr.split(":")))
    if int(temp[0]) > 60:
        year = 1900 + int(temp[0])
    else:
        year = 2000 + int(temp[0])
    md = doy2day(int(temp[1]), year)
    mjd = modjuldatNew(year,md[0],md[1],int(temp[2]))
    
    return mjd

def findPosit(lines, block):
    flag = 0
    start,stop = 0,0

    try:
        start = lines.index('+'+block+'\n') + 1
    except ValueError:
        for i in range(len(lines)):  #like bkg sinex 10APR12XA_bkg2022a
            if '+'+block in lines[i]:
                start = i + 1
                break

    try:
        stop = lines.index('-'+block+'\n')
    except ValueError:
        for i in range(start,len(lines)):
            if '-' + block in lines[i]:
                stop = i
                break

    if start == 0  or stop == 0:
        print('    %s read error!'%block)
            
    return start,stop

def findNormal(lines, block):
    flag = 0
    start,stop = 0,0
    
    for blockStr in block:
        try:
            start = lines.index('+'+blockStr+'\n') + 1
            flag = 0
        except ValueError:
            for i in range(len(lines)):
                if '+'+blockStr in lines[i]:
                    start = i + 1
                    break
        if start == 0:
            continue
        else:
            break
            
    if flag == 0:
        for blockStr in block:
            try:
                stop = lines.index('-'+blockStr+'\n')
            except ValueError:
                for i in range(start, len(lines)):
                    if '-' + blockStr in lines[i]:
                        stop = i
                        break
            if stop == 0:
                continue
            else:
                break
            
    return start, stop
    
# ab = '21:308:16538'
# get_epochMJD(ab)
# filePath = 'IGS1R03SNX_20140260000_07D_07D_SOL.SNX'
# startTime = time.time()
# paramInfo,normalMatrix = read_SNX(filePath, 2)
# stopTime = time.time()
# print(stopTime-startTime)
#sitEst,souEst,paramSession,Ns,bs = read_SNX('/data/VLBI/SINEX/bkg/10APR12XA_bkg2022a',3)
#print('yes')
