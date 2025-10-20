#!/usr/bin/env python3

import math
def writeTRFResult(sitAll,result,Param):
    
    sitNum = len(sitAll['name'])
    fid = open('TRF.txt','w')
    fid.writelines('*name       Sessions  startMJD    stopMJD       X(mm)       Y(mm)       Z(mm)\n'+\
                   '*                                           Vx(mm/yr)   Vx(mm/yr)   Vx(mm/yr)\n')
    for i in range(sitNum):
        sitName = sitAll['name'][i]
        fid.writelines('%8s   %6d  %10.4f  %10.4f  %10.1f  %10.1f  %10.1f\n'%(sitName,sitAll['ObsNum'][i],min(sitAll['estEpoch'][i]),\
                                                                             max(sitAll['estEpoch'][i]),result[i*3,0]*1E3,\
                                                              result[i*3+1,0]*1E3,\
                                                              result[i*3+2,0]*1E3,))
            
        if Param.Flags.vel[0] == 'YES':
            #fid.writelines('           %10.1f  %10.1f  %10.1f\n'%(result[sitNum*3+i*3,0]*1E3,\
            #                                                   result[sitNum*3+i*3+1,0]*1E3,\
            #                                                   result[sitNum*3+i*3+2,0]*1E3))

            paramPosit = [sitAll['globEstSitVelPosit'][i * 3], \
                          sitAll['globEstSitVelPosit'][i * 3 + 1], \
                          sitAll['globEstSitVelPosit'][i * 3 + 2]]
            fid.writelines('                                           %10.1f  %10.1f  %10.1f\n' % (result[paramPosit[0], 0] * 1E3, \
                                                                    result[paramPosit[1], 0] * 1E3, \
                                                                    result[paramPosit[2], 0] * 1E3))
    fid.close()

def writeCRFResult(sitAll,souAll,result):
    '''
    if Param.Global.station[0] == 'YES' and Param.Flags.vel[0] == 'YES':
        startNum = len(sitAll['name'])*6
    elif Param.Global.station[0] == 'YES':
        startNum = len(sitAll['name']) * 3
    '''
    startNum = sum(sitAll['estNum'])*3
    souNum = len(souAll['name'])
    fid = open('CRF_1.txt', 'w')

    fid.writelines('%name       obsNum      type     dRa(mas)     dDe(mas)\n')
    for i in range(souNum):
        souName = souAll['name'][i]
        if souAll['nnr'][i] == 1:
            flag = 'define'
        else:
            flag = 'none'

        fid.writelines('%8s    %6d    %6s    %9.4f    %9.4f\n' % (souName, souAll['ObsNum'][i],flag,\
                                                              result[startNum + i*2, 0]*180/math.pi*3600*1000, \
                                                              result[startNum + i*2 + 1, 0]*180/math.pi*3600*1000))

    fid.close()