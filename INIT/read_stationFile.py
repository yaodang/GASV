#!/usr/bin/env python3

import os,sys
import numpy as np
sys.path.append("..//")
from scipy import interpolate
from COMMON import *

        
def read_station(stationFile, scanInfo):
    """
    Read the station file
    ---------------------
    input: 
        stationFile     : the station apriori file
        stationList     : the session observe source, list
    output: 
        stationInfo     : STATION class
    ---------------------
    """
    
    # read station file
    if not os.path.exists(stationFile):
        sys.stderr.write('Error: The apriori station file not exist!')
        sys.exit()
    
    station,ptype = np.loadtxt(stationFile, dtype='str',comments='$$',usecols=[0,8], unpack=True)
    staPosit = np.loadtxt(stationFile, dtype='float',comments='$$',usecols=[1,2,3,4,5,6,7], unpack=False)

    station = add_blank(station)
    
    stationInfo = STATION()
    for i in range(len(scanInfo.stationAll)):
        name = scanInfo.stationAll[i]

        if name in station:
            index = station.index(name)
            XYZ = staPosit[index, 0:3]
            vXYZ = staPosit[index,3:6]
            epoch = staPosit[index,6].tolist()
            staType = ptype[index]
        else:
            print('        The %s not in station file, using apriori posit in data and set velocity zeros!'%name)
            XYZ = scanInfo.staPosit[i]
            vXYZ = np.zeros(3)
            epoch = 0
            staType = 'fromSession'

            if XYZ[0] == 0 and XYZ[1] == 0 and XYZ[2] == 0:
                print('        Error: the posit of %s is wrong!' %name)
                sys.exit()

        stationInfo.addStation(name, XYZ, vXYZ, epoch,staType)
        lam, phi, hell = xyz2ell(XYZ)
        stationInfo.ell.append([lam, phi, hell])

        ps = np.where(scanInfo.Scan2Station[:, i] != 0)
        if np.any(ps):
            stationInfo.obsTimeRange.append([scanInfo.scanTime[ps[0][0]], scanInfo.scanTime[ps[0][-1]]])
            stationInfo.obsMJDRange.append([scanInfo.scanMJD[ps[0][0]], scanInfo.scanMJD[ps[0][-1]]])
        '''
        if name in station:
            index = station.index(name)
            stationInfo.addStation(name, staPosit[index, 0:3], staPosit[index,3:6], staPosit[index,6].tolist(),ptype[index])
            lam,phi,hell = xyz2ell(staPosit[index, 0:3])
            stationInfo.ell.append([lam,phi,hell])
            
            ps = np.where(scanInfo.Scan2Station[:,i] != 0)
            if np.any(ps):
                stationInfo.obsTimeRange.append([scanInfo.scanTime[ps[0][0]], scanInfo.scanTime[ps[0][-1]]])
                stationInfo.obsMJDRange.append([scanInfo.scanMJD[ps[0][0]], scanInfo.scanMJD[ps[0][-1]]])
            
        else:
            print('The station %s not in %s, please add!\n'%(name,stationFile))
            sys.exit()
        '''
    
    path = stationFile[0:stationFile.rfind('/')+1]
    read_antennaInfo(path,'antenna-info',stationInfo)
    read_gravity(path, 'gravity_deform_model.txt',stationInfo,scanInfo.scanMJD[0])
    read_ocean_tidal(path,'TPXO72',stationInfo)
    read_ocean_pole_tidal(path,stationInfo)
    read_psd(path, stationInfo, scanInfo.stationCode)

    return stationInfo    
    

def read_antennaInfo(path,filename,stationInfo):
    """
    Read antenna information file
    ---------------------
    input: 
        path              : the apriori file path
        filename          : the antenna-info file name
    output: 
        eccStation        : station in eccentricity file
    ---------------------
    """
    antinfoPath = os.path.join(path,filename+'.txt')
    if os.path.exists(antinfoPath):
        # delete the first line and end line with '$'
        fid = open(antinfoPath,'r')
        lines = fid.readlines()
        fid.close()
        
        flag = 0
        if '$' in lines[0]:
            del lines[0]
            flag = 1
        if '$' in lines[-1]:
            del lines[-1]
            flag = 1
            
        if flag == 1:
            fid = open(antinfoPath,'w')
            fid.writelines(lines)
            fid.close()
        
        staName,foctype,axtype = np.loadtxt(antinfoPath,comments='#',dtype='str',usecols=[1,2,3],unpack=True)
        axoffset = np.loadtxt(antinfoPath,comments='#',dtype='float',usecols=[16],unpack=True)
        thermpar = np.loadtxt(antinfoPath,comments='#',dtype='float',usecols=[6,11,12,13,14,15,18,20],unpack=False)
        staName = add_blank(staName)
        
        if len(staName) != len(axoffset):
            print('The antenna-info file read wrong, please check!')
            sys.exit()
        
        for sta in stationInfo.stationName:
            if sta in staName:
                posit = staName.index(sta)
                stationInfo.axtype.append(axtype[posit][3:])
                stationInfo.axoffset.append(axoffset[posit])
                stationInfo.thermpar.append(thermpar[posit])
                stationInfo.foctype.append(foctype[posit])
            else:
                stationInfo.axtype.append('none')
                stationInfo.axoffset.append(0)
                stationInfo.thermpar.append(np.zeros(8))
                stationInfo.foctype.append('none')
    else:
        for i in range(len(stationInfo.stationName)):
            stationInfo.axtype.append('none')
            stationInfo.axoffset.append(0)
            stationInfo.thermpar.append(np.zeros(8))
            stationInfo.foctype.append('none')

def read_gravity(path,fileName, stationInfo, refMJD):
    gravityPath = os.path.join(path, fileName)
    gravSta = {'station':[],'epoch':[],'data':[]}
    if os.path.exists(gravityPath):
        # delete the first line and end line with '$'
        fid = open(gravityPath, 'r')
        lines = fid.readlines()
        fid.close()

        staList = []
        posit = []
        for i in range(1,len(lines)):
            line = lines[i]
            if line[0] == '#':
                continue
            if line[0] != ' ' and 'EPOCH' not in line:
                temp = list(filter(None,line[:-1].split(" ")))
                staList.append(temp)
                posit.append(i)
        posit.append(len(lines))

        for i in range(len(staList)):
            if staList[i][0] not in gravSta['station']:
                gravSta['station'].append(staList[i][0])
                epoch,data = getData(lines[posit[i]+1:posit[i+1]])
                gravSta['epoch'].append([epoch])
                gravSta['data'].append([data])
            else:
                index = gravSta['station'].index(staList[i][0])
                epoch, data = getData(lines[posit[i] + 1:posit[i + 1]])
                gravSta['epoch'][index].append(epoch)
                gravSta['data'][index].append(data)

    for sta in stationInfo.stationName:
        #sta =
        if sta in gravSta['station']:
            index = gravSta['station'].index(sta)
            k = 0
            for i in range(len(gravSta['epoch'][index])):
                if refMJD >= gravSta['epoch'][index][i][0] and refMJD <= gravSta['epoch'][index][i][1]:
                    stationInfo.gravpar.append(np.array(gravSta['data'][index][i]))
                    k += 1
            if k == 0:
                stationInfo.gravpar.append([0])
        else:
            stationInfo.gravpar.append([0])

def getData(lines):
    epoch = []
    data = []

    if 'EPOCH' not in lines[0]:
        epoch = [0,99999]
    else:
        temp = list(filter(None,lines[0].split(" ")))
        startMJD = modjuldatNew(int(temp[1][:4]),int(temp[1][4:6]),int(temp[1][6:8]))
        stopMJD = modjuldatNew(int(temp[2][:4]),int(temp[2][4:6]),int(temp[2][6:8]))
        epoch = [startMJD,stopMJD]

    for line in lines:
        if line[0] == ' ':
            temp = list(filter(None, line[:-1].split(" ")))
            data.append([float(temp[0]),float(temp[1])])

    return epoch,data

def read_ecc(filename):
    """
    Read station eccentricity file
    ---------------------
    input: 
        filename          : the eccentricity file name
    output: 
        eccStation        : station in eccentricity file
        ecc               : parameter of station
    ---------------------
    """
    eccStation = []
    ecc = []

def read_ocean_tidal(path,filename,stationInfo):
    """
    Read and add ocean tidal loading parameter
    ---------------------
    input: 
        path              : the apriori file path
        filename          : the ocean tidal loading file name
        stationInfo       : the station information struct
    output: 
        stationInfo       : the station information struct
    ---------------------
    """
    oceanStation = []
    oceanCto = []
    
    oceanPath = path+'ocean_loading_'+filename+'.TXT'
    if os.path.exists(oceanPath):
        fid = open(oceanPath,'r')
        lines = fid.readlines()
        fid.close()
        
        nlines = []
        oceanStation = []
        oceanCto = []
        for line in lines:
            if not '$$' in line:
                nlines.append(line)
                
        nL = len(nlines)
        for i in range(int(nL/7)):
            oceanStation.append(nlines[i*7][2:10])
            oceanCto.append(strSplit(nlines[i*7+1:i*7+7]))
    else:
        print('The %s file not exists!\n'%oceanPath)
        sys.exit()
            
    if len(oceanStation) != nL/7:
        print('The ocean tidal read wrong!\n')
        sys.exit()
        
    if len(oceanStation) != len(oceanCto):
        print('The ocean tidal read wrong!\n')
        sys.exit()

    for name in stationInfo.stationName:
        if name in oceanStation:
            index = oceanStation.index(name)
            stationInfo.cto.append(oceanCto[index])
        else:
            stationInfo.cto.append(np.zeros((6,11)))

def read_ocean_pole_tidal(path,stationInfo):
    """
    Read ocean pole tidal parameter
    ---------------------
    input: 
        path              : the apriori file path
        stationInfo       : the station information struct
    output:
        opp               : the ocean pole tidal parameter
    ---------------------
    """
    station = np.loadtxt(path+'ocean_pole_tidal_file.txt',dtype='str',usecols=[0],unpack=False)
    data_opp = np.loadtxt(path+'ocean_pole_tidal_file.txt',dtype='float',usecols=[1,2,3,4,5,6],unpack=False)
    data_ap = np.loadtxt(path+'atmosphere_tidal_file.txt',dtype='float',usecols=[1,2,3,4,5,6,7,8,9,10,11,12],unpack=False)

    station = add_blank(station)
    noOppApSta = []
    for i in range(len(stationInfo.stationName)):
        if stationInfo.stationName[i] not in station:
            noOppApSta.append(i)
    if len(noOppApSta):
        creat_opp_ap_File(path, noOppApSta, stationInfo)
    

    for name in stationInfo.stationName:
        if name in station:
            posit = station.index(name)
            stationInfo.opp.append(data_opp[posit,:])
            stationInfo.ap.append(data_ap[posit,:])
            
def read_psd(path, station, nsCode):
    '''
    Get the post-seismic deformation value.
    '''
    
    fid = open(path+'ITRF2020-psd-vlbi.dat','r')
    lines = fid.readlines()
    fid.close()
    
    staID = []
    startMJD = []
    E = []
    N = []
    U = []
    for i in range(int(len(lines)/3)):
        staID.append(int(lines[3*i][:5]))
        if int(lines[3*i][19:21]) > 72:
            year = 1900 + int(lines[3*i][19:21])
        else:
            year = 2000 + int(lines[3*i][19:21])
        doy = int(lines[3*i][22:25])
        seconds = int(lines[3*i][26:31])
        hour,minute,sec = time_transfer.sec2hms(seconds)
        mon,day = time_transfer.doy2day(doy, year)
        
        
        startMJD.append(time_transfer.modjuldat(np.array([year]),np.array([mon]),np.array([day]),hour,minute,sec)[0])
        E.append(list(filter(None,lines[3*i][34:67].split(" "))))

        if '\n' in lines[3*i+1]:
            N.append(list(filter(None,lines[3*i+1][34:-1].split(" "))))
        else:
            N.append(list(filter(None, lines[3 * i + 1][34:].split(" "))))

        if '\n' in lines[3*i+2]:
            U.append(list(filter(None,lines[3*i+2][34:-1].split(" "))))
        else:
            U.append(list(filter(None, lines[3 * i + 2][34:].split(" "))))

    #check ENU
    if [] in E or [] in N or [] in U:
        print('\n    Error: psd file read wrong! please check file.\n')
        sys.exit()

    psd = []
    psdFlag = np.zeros(len(nsCode),dtype=int)
    for i in range(len(nsCode)):
        if nsCode[i][3] == '----':
            psd.append([])
        else:
            iID = int(nsCode[i][3])
            if iID in staID:
                posit = np.where(np.array(staID)==iID)[0]
                psdFlag[i] = len(posit)

                temp = [[],[]]
                for ip in posit:
                    temp[0].append(startMJD[ip])
                    temp[1].append([E[ip],N[ip],U[ip]])

                # resort the temp by first mjd list
                sorted_temp = list(zip(*sorted(zip(*temp))))
                sorted_temp = [list(item) for item in sorted_temp]

                psd.append(sorted_temp)
            else:
                psd.append([])

    station.psd = psd
    station.psdFlag = psdFlag
        
def add_blank(station):
    """
    Add blank to station name if the length is not equal to 8
    ---------------------
    input: 
        station         : the station name array
    output: 
        station         : new station name array
    ---------------------
    """
    blank = '        '
    if type(station) == np.ndarray:
        for i in range(len(station)):
            if len(station[i]) != 8:
                station[i] = station[i] + blank[0:8-len(station[i])]
                
        return station.tolist()
    elif type(station) == str:
        nstation = station + blank[0:8-len(station)]
        return nstation

def strSplit(lines):
    """
    Get the ocean tidal loading parameter
    ---------------------
    input: 
        lines           : ocean tidal loading lines
    output: 
        cto             : parameter, 6*11 array
    ---------------------
    """
    cto = []
    for line in lines:
        temp = line[:-1].split()
        cto.append(list(map(float,temp)))
        
    return np.array(cto)

def creat_opp_ap_File(path,posit,stationInfo):
    """
    Creat ocean pole tidal and atmposhpere pole tiddal
    ---------------------
    input: 
        path              : the apriori file path
        posit             : the posit of station which no opp and ap information
        stationInfo       : the station information struct
    output:
    ---------------------
    """
    print('        Creating the ocean pole tidal and atmosphere pole tidal...')
    lon_opt = np.linspace(0.25, 359.75, 720)
    lat_opt = np.linspace(-89.75, 89.75, 360)
    
    lon_at = np.linspace(0,360,361)
    lat_at = np.linspace(90,-90,181)
    
    #print('Reading ocean pole tidal file......')
    opt = np.loadtxt(path+'opoleloadcoefcmcor.txt',dtype='float',skiprows=14,usecols=[2,3,4,5,6,7],unpack=False)
    
    #print('Reading atmosphere tidal file......')
    at = np.loadtxt(path+'s1_s2_def_cm.dat',dtype='float',usecols=[2,3,4,5,6,7,8,9,10,11,12,13],unpack=False)

    fid_opp = open(path+'ocean_pole_tidal_file.txt','a')
    fid_ap = open(path+'atmosphere_tidal_file.txt','a')
    
    for i in range(len(posit)):
        
        lam,phi,h = stationInfo.ell[posit[i]]
        lam = lam*180/np.pi
        if lam < 0:
            lam = lam + 360
        phi = phi*180/np.pi
        
        # ocean pole tidal parameter
        u6 = [0,0,0,0,0,0]
        for j in range(6):
            data_opt = np.reshape(opt[:,j], (360,720))
            f_opt = interpolate.interp2d(lon_opt, lat_opt, data_opt, kind='cubic')
            temp = f_opt(lam,phi)
            u6[j] = temp[0]
        fid_opp.writelines('%-8s  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f\n'\
                           %(stationInfo.stationName[posit[i]],u6[0],u6[1],u6[2],u6[3],u6[4],u6[5]))
        
            
        # atmosphere tidal loading
        a12 = [0,0,0,0,0,0,0,0,0,0,0,0]
        for j in range(12):
            data_at = np.reshape(at[:,j], (361,181))
            f_at = interpolate.interp2d(lon_at, lat_at, data_at.T, kind='linear')
            temp = f_at(lam,phi)
            a12[j] = temp[0]
        fid_ap.writelines('%-8s  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f\n'\
                           %(stationInfo.stationName[posit[i]],a12[0],a12[1],a12[2],a12[3],a12[4],a12[5],a12[6],a12[7],a12[8],\
                             a12[9],a12[10],a12[11]))

    fid_opp.close()
    fid_ap.close()
    
# def findPosit(MJD, sMJD):
    
#     index = -1
#     if len(MJD) == 1:
#         if sMJD >= MJD:
            
#     elif len(MJD) >= 2:
#         for i in range(len(MJD)-1):
#             if sMJD >= MJD[i] and sMJD < MJD[i+1]:
#                 index = i
    
    
