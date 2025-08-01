#!/usr/bin/env python3

import numpy as np

def NNRT2TRF(sitAll,Param):
    sitNum = len(sitAll['name'])
    
    normlize = 1
    # normlize = np.sqrt(sitNum)
    # sumAll = 0
    # for i in range(sitNum):
    #     sumAll += sum(sitAll['ITRF'][i][:3]**2)
    # earthRadius = np.sqrt(sumAll)
    
    number = 6
    if number == 6:
        earthRadius = 1
        # normlize = np.sqrt(sitNum)
    else:
        earthRadius = 1
        # normlize = 1
    Bsit = np.zeros((number,3*sitNum))
    
    for i in range(sitNum):
        if sitAll['nnrt'][i] == 1:
            xyz = sitAll['ITRF'][i][:3]/earthRadius
            # xyz = sitAll['ITRF'][i][:3]/np.sqrt(sum(sitAll['ITRF'][i][:3]**2))
            
            if number == 6:
                Bi = np.array([[      1/normlize,       0,      0],\
                               [      0,       1/normlize,      0],\
                               [      0,       0,      1/normlize],\
                               [      0,  xyz[2],-xyz[1]],\
                               [-xyz[2],       0, xyz[0]],\
                               [ xyz[1], -xyz[0],      0]])
            else:
                Bi = np.array([[      1/normlize,       0,      0],\
                               [      0,       1/normlize,      0],\
                               [      0,       0,      1/normlize],\
                               [      0, -xyz[2], xyz[1]],\
                               [ xyz[2],       0,-xyz[0]],\
                               [-xyz[1],  xyz[0],      0],\
                               [ xyz[0],  xyz[1], xyz[2]]])
                
            Bsit[:,3*i:3*(i+1)] = Bi
            
    if Param.Flags.vel[0] == 'YES':
        '''
        temp1 = np.hstack((Bsit,np.zeros((number,3*sitNum))))
        temp2 = np.hstack((np.zeros((number,3*sitNum)),Bsit))
        Bsit = np.vstack((temp1,temp2))
        '''

        deleteCol = []
        for i in range(len(sitAll['velUsedFlag'])):
            if sitAll['velUsedFlag'][i] == 0:
                deleteCol.extend([3*i,3*i+1,3*i+2])
        Bsitv = np.delete(Bsit,deleteCol,axis=1)
        temp1 = np.hstack((Bsit, np.zeros((number, 3 * sitAll['estNum'][1]))))
        temp2 = np.hstack((np.zeros((number, 3 * sitNum)), Bsitv))
        Bsit = np.vstack((temp1, temp2))
        #'''
        
    return Bsit


def velTieConst(B, sitAll, Param):
    sitEstParamNum = len(np.unique(sitAll['globEstSitPosit']))
    velEstParamNum = len(np.unique(sitAll['globEstSitVelPosit']))
    tieNum = len(Param.Tie.velTie)

    if tieNum:
        k = 0
        for i in range(tieNum):
            index = []

            for tieSit in Param.Tie.velTie[i]:
                try:
                    index.append(sitAll['name'].index(tieSit))
                except ValueError:
                    continue

            if len(index) >= 2:
                velZeros = np.zeros(((len(index) - 1) * 3, velEstParamNum))

                for ib in range(len(index) - 1):
                    if index[ib] == 0:
                        startp = 0
                        endp = 3
                    else:
                        startp = sitAll['globEstSitVelPosit'][3 * index[ib]] - sitEstParamNum
                        #startp = sitAll['globEstSitVelPosit'][3 * (index[ib] - 1)] - sitEstParamNum
                        #endp = sitAll['globEstSitVelPosit'][3 * index[ib]] - sitEstParamNum
                    velZeros[ib * 3:(ib + 1) * 3, startp:startp+3] = np.eye(3)

                    if index[ib+1] == 0:
                        startp = 0
                        endp = 3
                    else:
                        startp = sitAll['globEstSitVelPosit'][3 * index[ib+1]] - sitEstParamNum
                        #startp = sitAll['globEstSitVelPosit'][3 * (index[ib + 1] - 1)] - sitEstParamNum
                        #endp = sitAll['globEstSitVelPosit'][3 * index[ib+1]] - sitEstParamNum
                    velZeros[ib * 3:(ib + 1) * 3, startp:startp+3] = -np.eye(3)

                    #velZeros[ib * 3:(ib + 1) * 3, index[0] * 3:(index[0] + 1) * 3] = np.eye(3)
                    #velZeros[ib * 3:(ib + 1) * 3, index[ib + 1] * 3:(index[ib + 1] + 1) * 3] = -np.eye(3)

                tempB = np.hstack((np.zeros((velZeros.shape[0], sitEstParamNum)), velZeros))
                if k == 0:
                    Bvtie = tempB
                else:
                    Bvtie = np.vstack((Bvtie, tempB))
                k += 1

    try:
        return np.vstack((B, Bvtie))
    except UnboundLocalError:
        return B

def velTieConstold(B, sitAll, Param):
    
    sitNum = len(sitAll['name'])
    tieNum = len(Param.Tie.velTie)
    
    if tieNum:
        k = 0
        for i in range(tieNum):
            index = []

            for tieSit in Param.Tie.velTie[i]:
                try:
                    index.append(sitAll['name'].index(tieSit))
                except ValueError:
                    continue
                
            if len(index) >= 2:
                velZeros = np.zeros(((len(index)-1)*3,sitNum*3))
                
                for ib in range(len(index)-1):
                    velZeros[ib*3:(ib+1)*3,index[0]*3:(index[0]+1)*3]=np.eye(3)
                    velZeros[ib*3:(ib+1)*3,index[ib+1]*3:(index[ib+1]+1)*3]=-np.eye(3)
                
                
                tempB = np.hstack((np.zeros((velZeros.shape[0],sitNum*3)),velZeros))
                if k == 0:
                    Bvtie = tempB
                else:
                    Bvtie = np.vstack((Bvtie,tempB))
                k += 1
                
    try:
        return np.vstack((B, Bvtie))
    except UnboundLocalError:
        return B
    
    
def NNR2CRF(souAll):
    
    souNum = len(souAll['name'])
    Bsou = np.zeros((3,2*souNum))
    
    for i in range(souNum):
        if souAll['nnr'][i] == 1:
            ra = souAll['RaDe'][i][0]
            de = souAll['RaDe'][i][1]

            Bi = np.array([[ -np.cos(ra)*np.sin(de)*np.cos(de),  np.sin(ra)],\
                           [ -np.sin(ra)*np.sin(de)*np.cos(de), -np.cos(ra)],\
                           [                     np.cos(de)**2,           0]])
                
            Bsou[:,2*i:2*(i+1)] = Bi
    
    return Bsou