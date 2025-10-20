#!/usr/bin/env python3

import numpy as np
import os
import sys

# --------------------------- control file -----------------------------
class PARAMETER:
    def __init__(self):
        self.Setup   = SETUP()
        self.Flags   = FLAGS()
        self.Data    = DATA()
        self.Global  = GLOBAL()
        self.Map     = MAPPING()
        self.Const   = CONSTRAINTS()
        self.Arcs    = ARCS()
        self.Tie     = TIE()
        self.Out     = OUTPUT()

    def creatParam(self, ParamSetup, ParamFlags, ParamData, ParamGlobal, \
                   ParamMap, ParamCon, ParamArcs, ParamTie, ParamOut):
        self.Setup   = ParamSetup
        self.Flags   = ParamFlags
        self.Data    = ParamData
        self.Global  = ParamGlobal
        self.Map     = ParamMap
        self.Const   = ParamCon
        self.Arcs    = ParamArcs
        self.Tie     = ParamTie
        self.Out     = ParamOut
        
    def check(self):
        if self.Flags.type == 'POLY' and len(self.Const.erp):
            num = 0
            if self.Flags.ut1[0] == 'YES':
                num += 1
            if self.Flags.pm[0] == 'YES':
                num += 1
            if self.Flags.pmr[0] == 'YES':
                num += 1
            if self.Flags.lod == 'YES':
                num += 1
            
            if len(self.Const.erp) <= num:
                print('        The EOP FLAG and CONSTRAINTS not match, Please check!')
                sys.exit()
        
class SETUP:
    def __init__(self):
        self.name = 'SETUP'
        self.solution = 'INDEPENDENT'
        self.calctheroe = 'IN'
        self.weight = 'NO'
        self.vgosdbPath = ''
        self.qcodeLim = 5
        self.clkRef = 'Default'
        
    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                temp = list(filter(None,line.split(" ")))
                if 'SOLUTION' in line:
                    self.solution = temp[1][0:-1]
                if 'VGOSDB' in line:
                    if len(temp) < 2:
                        print('        The SETUP(VGOSDB) part is wrong!')
                        sys.exit()
                    self.vgosdbPath = temp[1][:-1]
                if 'CALTHEORE' in line:
                    self.calctheroe = temp[1][:-1]
                    
                if 'WEIGHT' in line:
                    self.weight = temp[1][:-1]
                
                if 'STALOG' in line:
                    if len(temp) < 2:
                        print('        The SETUP(STALOG) part is wrong!')
                        sys.exit()
                    self.staLogPath = temp[1][:-1]
                
                if 'QUALCODE_LIMIT' in line:
                    self.qcodeLim = int(temp[1][:-1])
                if 'CLOCKREF' in line:
                    self.clkRef = temp[1][:-1]
        print('        Reading the %-15s part OK.'%('SETUP'))   
                    
class FLAGS:
    def __init__(self):
        self.name = 'FLAGS'
        self.type = 'NO'
        self.clk = 'NO'
        self.blClk = 'NO'
        self.zwd = 'NO'
        self.gradient = ['NO']
        self.ut1 = ['NO']
        self.lod = ['NO']
        self.pm = ['NO']
        self.pmr = ['NO']
        self.nut = ['NO']
        self.xyz = ['NO']
        self.sou = ['NO']
        self.vel = ['NO']
        self.eopTime = 'MIDDEL'
        self.segConstr = [0,0]
        
    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        lineNum = posit[p]+1
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                temp = list(filter(None,line[1:-1].split(" ")))
                if 'CLOCKS' in line:
                    if len(temp)==4 and 'ORDER'==temp[2]:
                        self.clk = [int(temp[1]),int(temp[3])]
                    elif len(temp)==2 and temp[1][0:-1].isdigit():
                        self.clk = [int(temp[1]),0]
                    else:
                        print('        The clock estimate interval set error!')
                        sys.exit()
                if 'BL_CLOCK' in line:
                    self.blClk = temp[1]
                
                if 'ATMOSPHERES' in line:
                    if temp[1].isdigit():
                        self.zwd = int(temp[1])
                    elif temp[1] != 'NO':
                        print('        The atmosphere estimate interval set error!')
                        sys.exit()
                if 'GRADIENTS' in line:
                    self.gradient = temp[1:]
                        
                if 'UT1/PM' in line:
                    self.getEOPParam(temp[1:])
                    
                if 'NUTATION' in line:
                    self.nut = temp[1:]
                        
                if 'SOURCES' in line:
                    self.sou = getExcept(lines, lineNum, temp, 1)

                if 'STATIONS' in line:
                    self.xyz = getExcept(lines, lineNum, temp, 1)
                    
                if 'VELOCITIES' in line:
                    self.vel = temp[1:]
            lineNum += 1
        print('        Reading the %-15s part OK.'%('FLAGS'))
        
    def getEOPParam(self, inList):
        if len(inList):
            if inList[0] == 'NO':
                self.type = 'NO'
            if inList[0] == 'SEGMENT':
                if len(inList) != 7:
                    print('        The UT1/PM set of FLAG error!\n')
                    sys.exit()
                else:
                    errFlag = 0
                    self.type = 'SEGMENT'
                    if 'INTERVAL' in inList:
                        if inList[2].isdigit():
                            self.pm = ['YES', inList[2]]
                            self.ut1 = ['YES', inList[2]]
                        else: 
                            errFlag = 1
                    else:
                        errFlag = 1
                    
                    if 'PM_RATE_CONSTR' in inList:
                        try:
                            self.segConstr[0] = float(inList[4])
                        except ValueError:
                            if inList[4] == '-':
                                self.pm[0] = 'NO'
                            else:
                                errFlag = 1
                    else:
                        errFlag = 1
                        
                    if 'UT1_RATE_CONSTR' in inList:
                        try:
                            self.segConstr[1] = float(inList[6])
                        except ValueError:
                            if inList[4] == '-':
                                self.ut1[0] = 'NO'
                            else:
                                errFlag = 1
                    else:
                        errFlag = 1
                    
                    if errFlag == 1:
                        print('        The UT1/PM set of FLAG error!\n')
                        sys.exit()
                                                    
            elif inList[0] == 'POLY':
                if len(inList) != 6:
                    print('        The UT1/PM set of FLAG error!\n')
                    sys.exit()
                else:
                    self.type = 'POLY'
                    if inList[2][0] != '-':
                        self.pm = ['YES']
                    if inList[2][1] != '-':
                        self.ut1 = ['YES']
                    if inList[4][0] != '-':
                        self.pmr = ['YES']
                    if inList[4][1] != '-':
                        self.lod = ['YES']
                    self.eopTime = inList[5]   
        else:
            print('        The UT1/PM set error!\n')
            sys.exit()             
                    
class DATA:
    def __init__(self):
        self.name = 'DATA'
        self.sou = []
        self.sta = []
        self.bl = []
        self.outlier = ['NO']
        
    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        lineNum = posit[p]+1
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                temp = list(filter(None,line[1:-1].split(" ")))
                if 'SOURCE' in line:
                    self.sou = getExcept(lines, lineNum, temp, 1)
                if 'STATIONS' in line:
                    self.sta = getExcept(lines, lineNum, temp, 1)
                if 'BASELINE' in line:
                    self.bl = getExcept(lines, lineNum, temp, 1)
                if 'OUTLIER' in line:
                    temp = list(filter(None,line[1:-1].split(" ")))
                    if len(temp) == 3 and temp[1] == 'YES':
                       if temp[2].isdigit():
                           self.outlier = temp[1:]
                    else:
                        self.outlier = ['NO']
            lineNum += 1
        print('        Reading the %-15s part OK.'%('DATA'))
        
class GLOBAL:
    def __init__(self):
        self.name = 'GLOBAL'
        self.source = ['NO']
        self.station = ['NO']
        
    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        lineNum = posit[p]+1
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                if 'SOURCE' in line:
                    temp = list(filter(None,line[:-1].split(" ")))
                    self.source = temp[1:]
                if 'STATION' in line:
                    temp = list(filter(None,line[:-1].split(" ")))
                    self.station = getExcept(lines, lineNum, temp, 1)
            lineNum += 1
           
class MAPPING:
    def __init__(self):
        self.name = 'MAPPING'
        self.stationFile = ''
        self.sourceFile = ''
        self.eopFile = ''
        self.ephemFile = ''
        self.mapFun = 'GPT3'
        # self.heopm = 'Desai'
        self.heopm = 'None'
        self.tidalCorrect = 'IERS'
        
    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                if 'STATIONS' in line:
                    temp = list(filter(None,line.split(" ")))
                    self.stationFile = temp[1][0:-1]
                if 'SOURCES' in line:
                    temp = list(filter(None,line.split(" ")))
                    self.sourceFile = temp[1][0:-1]
                if 'EARTH_ORIENTATION' in line:
                    temp = list(filter(None,line.split(" ")))
                    self.eopFile = temp[1][0:-1]
                if 'EPHEM' in line:
                    temp = list(filter(None,line.split(" ")))
                    self.ephemFile = temp[1][0:-1]
                if 'MAPFUNCTION' in line:
                    temp = list(filter(None,line.split(" ")))
                    self.mapFun = temp[1][0:-1]
                if 'HI_FREQ_EOP' in line:
                    temp = list(filter(None,line.split(" ")))
                    self.heopm = temp[1][0:-1]
                if 'TIDALCORRECT' in line:
                    temp = list(filter(None, line.split(" ")))
                    self.tidalCorrect = temp[1][0:-1]
        print('        Reading the %-15s part OK.'%('MAPPING'))
class CONSTRAINTS:
    def __init__(self):
        self.name = 'CONSTRAINTS'
        self.atm = 50.0
        self.clk = 43.0
        self.grad = [0.05,0.2]
        self.erp = []
        self.nnr_nnt_sta = [['NO'],['NO']]
        self.nnr_nnt_stav = [['NO'],['NO']]
        self.nnr_sou = ['NO']
        
        self.nut = 0
        self.tie = 'NO'
        self.sta = ['NO',0.01]
        self.sou = ['NO',1E-6]
        self.sigma_nnr_nnt_sta = [0.01,0.01]
        self.sigma_nnr_nnt_stav = [0.01,0.01]
        self.sigma_nnr_sou = 1E-11
        
    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        lineNum = posit[p]+1
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                temp = list(filter(None,line[1:-1].split(" ")))
                if 'ATMOSPHERE' in line:
                    self.atm = float(temp[1])   # [ps/hour]
                if 'CLOCKS' in line:
                    self.clk = float(temp[1])   # [ps/hour]
                if 'GRADIENTS' in line:
                    self.grad = [float(temp[1]),float(temp[2])]
                if 'UT1/PM' in line:
                    self.getEOPConstr(temp[1:])
                if 'NUTATION' in line:
                    self.nut = float(temp[1])
                if 'STATIONS' in line:
                    self.sta[0] = temp[1]
                    sigma = self.getSigma(temp[1:])
                    if sigma != 0:
                        self.sta[1] = sigma
                        
                if 'SOURCES' in line:
                    self.sou[0] = temp[1]
                    sigma = self.getSigma(temp[1:])
                    if sigma != 0:
                        self.sou[1] = sigma

                if 'NNR_POSITION' in line:
                    value = getExcept(lines, lineNum, temp, 1)
                    self.nnr_nnt_sta[0] = value
                    self.getNNNNRSigma(value, 0)
                if 'NNT_POSITION' in line:
                    value = getExcept(lines, lineNum, temp, 1)
                    self.nnr_nnt_sta[1] = value
                    self.getNNNNRSigma(value, 1)
                if 'NNR_VELOCITY' in line:
                    value = getExcept(lines, lineNum, temp, 1)
                    self.nnr_nnt_stav[0] = value
                    self.getNNNNRSigma(value, 2)
                if 'NNT_VELOCITY' in line:
                    value = getExcept(lines, lineNum, temp, 1)
                    self.nnr_nnt_stav[1] = value
                    self.getNNNNRSigma(value, 3)
                if 'NNR_SOURCE' in line:
                    value = getExcept(lines, lineNum, temp, 1)
                    self.nnr_sou = value
                    self.getNNNNRSigma(value, 4)
                    
                if 'STATIE' in line:
                    if temp[1] != 'NO':
                        try:
                            float(temp[1])
                        except ValueError:
                            print('The STATIE set in $CONSTRAINTS is wrong!')
                            sys.exit()
                        else:
                            self.tie = float(temp[1])
            lineNum += 1
        print('        Reading the %-15s part OK.'%("CONSTRAINTS"))
        
    def getEOPConstr(self, inList):
        if inList[0] != 'NO':
            for i in range(len(inList)):
                self.erp.append(float(inList[i]))
    
    def getSigma(self,value):
        sigma = 0
        if 'SIGMA' in value:
            index = value.index('SIGMA')
            if 'D' in value[index+1]:
                try:
                    temp = value[index+1].replace('D','E')
                    sigma = float(temp)
                except ValueError:
                    sys.exit()
            else:
                try:
                    sigma = float(value[index+1])
                except ValueError:
                    sys.exit()
                    
        return sigma
    
    def getNNNNRSigma(self,value,flag):
        sigma = self.getSigma(value)
                    
        if sigma !=0:
            if flag == 0:
                self.sigma_nnr_nnt_sta[0] = sigma
            elif flag == 1:
                self.sigma_nnr_nnt_sta[1] = sigma
            elif flag == 2:
                self.sigma_nnr_nnt_stav[0] = sigma
            elif flag == 3:
                self.sigma_nnr_nnt_stav[1] = sigma
            elif flag == 4:
                self.sigma_nnr_sou = sigma

class TIE:
    def __init__(self):
        self.name = 'TIE'
        self.velTie = []

    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        # lineNum = posit[p]+1
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                temp = list(filter(None,line[:-1].split(" ")))
                self.velTie.append(temp)
                
class ARCS:
    def __init__(self):
        self.name = 'ARCS'
        self.session = []
        self.version = []
        self.AC = []
        
    def getValue(self, lines, keyword, posit):
        k = 0
        p = keyword.index(self.name)
        for line in lines[posit[p]+1:posit[p+1]]:
            if line[0] != '*':
                k = k + 1
                if k == 2:
                    print('        The ARCS part is wrong! exist too many type.')
                    sys.exit()
                if 'ARCFILE' in line:
                    temp = list(filter(None,line.split(" ")))
                    self.read_arcsfile(temp[1][0:-1])
                else:
                    temp = list(filter(None,line.split(" ")))
                    if len(temp) != 3:
                        print('        The ARCS part is wrong! please check!')
                        sys.exit()
                    self.session = [temp[0][1:]]
                    self.version = [int(temp[1])]
                    if '\n' in temp[2]:
                        self.AC = [temp[2][:-1]]
                    else:
                        self.AC = [temp[2]]
        print('        Reading the %-15s part OK.'%('ARCS'))          
                    
    def read_arcsfile(self, filename):
        session = []
        version = []
        ac      = []
        if not os.path.exists(filename):
            print('        Error: The arc file not exists!')
            sys.exit()
            
        fid = open(filename, 'r')
        lines = fid.readlines()
        fid.close()
        
        for line in lines:
            if line[0] == '$':
                temp = list(filter(None,line.split(" ")))
                session.append(temp[0][1:])
                version.append(int(temp[1]))
                if '\n' in temp[2]:
                    ac.append(temp[2][:-1])
                else:
                    ac.append(temp[2])
        if not session:
            print('        The ARCS(ARCFILE) part is wrong! no session in file.')
            sys.exit()
        self.session = session
        self.version = version
        self.AC = ac
        
class OUTPUT:
    def __init__(self):
        self.name = 'OUTPUT'
        self.residualPath = ''
        self.snxPath = ['NO']
        self.reportPath = ['NO']
        self.eopPath = ['NO']
    
    def getValue(self, lines, keyword, posit):
        p = keyword.index(self.name)
        for line in lines[posit[p]+1:]:
            if line[0] != '*':
                if '\n' in line:
                    temp = list(filter(None,line[1:-1].split(" ")))
                else:
                    temp = list(filter(None, line[1:].split(" ")))
                if 'RESIDUAL' in line:
                    if temp[1] == 'YES' and len(temp) == 3:
                        self.residualPath = temp[2]
                    else:
                        self.residualPath = 'None'
                if 'SNX' in line:
                    if temp[1] == 'YES':
                        if len(temp) == 2:
                            print('SNX of $OUTPUT set wrong!')
                            sys.exit()
                        elif len(temp) >= 3:
                            self.snxPath = temp[1:]
                if 'REPORT' in line:
                    if temp[1] == 'YES':
                        if len(temp) == 2:
                            print('REPORT of $OUTPUT set wrong!')
                            sys.exit()
                        elif len(temp) == 3:
                            self.reportPath = temp[1:]
                        
                if 'EOP' in line:
                    errFlag = 0
                    if len(temp) == 3:
                        if temp[1] != 'YES' and temp[1] != 'NO':
                            errFlag += 1
                        #if not os.path.exists(temp[2]):
                        #    errFlag += 1
                        self.eopPath = temp[1:]
                    else:
                        errFlag = 1

                    if errFlag != 0:
                        print('        The EOP output set wrong! Please modify!')
                        sys.exit()
                        
        print('        Reading the %-15s part OK.'%('OUTPUT'))


def getExcept(lines, lineNum, temp, startP):
    '''
    

    Parameters
    ----------
    lines : TYPE
        DESCRIPTION.
    lineNum : TYPE
        DESCRIPTION.
    temp : TYPE
        DESCRIPTION.
    startP : TYPE
        DESCRIPTION.

    Returns
    -------
    out : TYPE
        DESCRIPTION.

    '''
    out = temp[startP:]
    if os.path.exists(out[-1]) and len(out[-1]) > 1:
        fid = open(out[-1])
        lines = fid.readlines()
        fid.close()
        
        flag = True
        out.pop(-1)
        
        outt = getLine(flag, lines, -1, 0)
        
    else:
        flag = False
        if '\\' in out:
            flag = True
            out.pop(-1)
        outt = getLine(flag, lines, lineNum, startP)
        
        
    if outt:
        outt = list(set(outt))
        out.extend(outt)

    return out

def getLine(flag, lines, lineNum, startP):
    
    k = 1
    outt = []
    while flag:
        if lines[lineNum+k][-1] == '\n':
            temp = list(filter(None,lines[lineNum+k][startP:-1].split(" ")))
        else:
            temp = list(filter(None,lines[lineNum+k][startP:].split(" ")))
        if '\\' in temp:
            if not '*' in temp:
                temp.pop(-1)
                outt.extend(temp)
            k += 1
        else:
            outt.extend(temp)
            flag = False
            
    return outt

# -------------------------- mk4 struct ------------------------
class MK4STRUCT():
    def __init__(self):
        self.band = []
        
        self.scanTime = []
        self.scanSou = []
        self.scanSta = []
        self.scanBL = []
        
        self.quality = []
        self.delay = []
        self.sbdelay = []
        self.delaySig = []
        self.sbdelaySig = []
        self.ambig = []
        self.snr = []
        #self.phase = []
        #self.phaseSig = []
        
        self.sampleRate = []
        self.ampp = []
        self.apNum = []
        self.channelFreq = []
        
    def reBuild(self):
        bandNum = len(self.band)
        
        self.keys = list(self.__dict__.keys())
        index = self.keys.index('quality')
        keys = self.keys[index:]
        
        for key in keys:
            self.__dict__[key] = [[]*bandNum for i in range(bandNum)]
        
    def integrateResult(self, result):
        for i in range(len(result)):
            self.addScan(result[i], 1)
            
            for ib in range(len(self.band)):
                self.addBandInfo(result[i],'quality',ib,1)
                
    def addScan(self, Struct, flag):
        self.scanTime.extend(Struct.scanTime)
        self.scanSou.extend(Struct.scanSou)
        if flag == 0:
            self.scanSta.append(Struct.scanSta)
            self.scanBL.append(Struct.scanBL)
        else:
            self.scanSta.extend(Struct.scanSta)
            self.scanBL.extend(Struct.scanBL)
                
    def addBandInfo(self, Struct, param, iband, flag):
        
        index = self.keys.index(param)
        keys = self.keys[index:]
        
        if type(Struct) == list:
            for ik in range(len(keys)):
                self.__dict__[keys[ik]][iband].append(Struct[ik])
        elif type(Struct) == MK4STRUCT:
            for key in keys:
                if flag == 0:
                    self.__dict__[key][iband].append(getattr(Struct, key)[iband])
                else:
                    self.__dict__[key][iband].extend(getattr(Struct, key)[iband])

# --------------------------------------------------------
class SCAN:
    def __init__(self):
        #----------------------- reading from vgosDB --------------------------
        self.baseInfo         = []    # band,reFreq,ambigSize
        self.cableCal         = []    # Cable cal of station
        self.delayFlag        = []    # Delay unweight flag

        self.gdApri           = []    # Group Delay only include ambiguity
        self.gd               = []    # Group Delay include ambiguity and ionosphere
        self.gdSig            = []    # Group Delay Sigma
        # self.iondl            = []    # ionosphere delay
        # self.iondlSig         = []    # ionosphere delay sigma
        
        self.Obs2Scan         = []    # Cross reference from observation to scan
        self.Obs2Baseline     = []    # Cross reference from observation to baseline, station start from 1
        self.Obs2MJD          = []    # Cross reference from observation to MJD
        self.Obs2Source       = []    # the observe source index for each obs
        
        self.T                = []    # temperature of station
        self.P                = []    # pressure of station
        self.H                = []    # humidity of station
        
        self.stationAll       = []    # the observe station in session
        self.stationCode      = []    # the code of station from ns-code.txt and station plate from sitpl.dat
        self.sourceAll        = []    # the observe source in session
        self.refSta           = ''    # the reference station, default is first station in stationAll
        self.noEstSta         = []    # the station position not estimate
        self.estSou           = []    # the estimate source index
        self.refclk           = ''    # the reference clock, default is first station in stationAll
        self.rmSta            = []    # the station data not used
        self.rmScanNum        = []    # the scan to remove, use to reprocess
        self.ambigNum         = []    # the ambiguity correction number
        
        self.sessionName      = ''    # the session name
        self.expName          = ''    # the experiment name
        self.expDescrip       = ''    # the experiment description
        
        self.scanTime         = []    # the YMDHMS of each scan
        self.scanNum          = []    # the scan number
        self.scanMJD          = []    # the MJD of each sacn
        self.refMJD           = []    # the session reference MJD
        self.blClkList        = []    # the baseline list which clock is estimate, station start from 0

        
        #--------------------- rebuild for each scan --------------------------
        self.scanObsNum       = []    # the observe number in scan
        self.scanBl           = []    # the baseline in each scan
        self.scanStation      = []    # the station in each scan 
        self.Scan2Station     = []
        self.scan2Source      = []    # the source in each scan
        self.scanSource       = []    # the observe source name in scan
        self.scanT            = []    # the temperature of station in scan
        self.scanP            = []    # the pressure of station in scan
        self.scanH            = []    # the humidity of station in scan
        self.scanCabCal       = []    # the cable cal of station in scan
        self.scanMFW          = []    # store the wet mapping function for each station of each scan
        self.scanMFGE         = []    # store the east gradient mapping function for each station of each scan
        self.scanMFGN         = []    # store the north gradient mapping function for each station of each scan
        self.scanTRP          = []    # store the tropsphere delay for each station of each scan
        self.scanState        = []    # store the ellipsoidal coordinates lam,phi,elh for each station of each scan
                                      # after station correct
        self.Fmout_GNSS       = []    # the station clock offset between fmout and GNSS
        self.scanGD           = []    # Group Delay in scan
        self.scanGDSig        = []    # Group Delay Sigma in scan
        
        self.staUsed          = []    # the station used in session
        self.staBlList        = []    # the earch station join the baseline
        self.blResPosit       = []    # the posit of earch baseline in residual
        self.blUsed           = []    # all the baseline in session, station start from 1
        self.blMJD            = []    # the MJD of earch baseline
        self.reversePosit     = []    # the reverse baseline posit of Obs2Baseline (used)
        self.reverseBlPosit   = []    # the posit of blUsed
        
        #--------------------- creat in mod --------------------------
        # self.staCRS           = []    # the CRF position in scan
        # self.staTRS           = []    # the TRF position in scan
        self.com              = []    # the consensus theory delay and atmospheric refraction
        self.oc_obs           = []    # the observe delay (remove the cab)
        self.pObs             = []    # the weight
        self.effFreq          = []    # the effect freq
        
        self.pEOP             = []    # the all EOP partial
        self.pxyz             = []    # partial for coordinate
        self.pxyzt            = []
        self.psou             = []    # partial for source
        
    def initMatrix(self):
        self.scanObsNum = []
        self.scanGD = []
        self.scanGDSig = []
        self.scanBl = []
        self.scanT =[]
        self.scanP = []
        self.scanH = []
        self.scanCabCal = []
        self.scanStation = []
        self.scanMFW = []
        self.scanTRP = []
    
        
class CLKBRK:
    def __init__(self):
        self.staName          = []
        self.brkFlag          = []
        self.brkMJD           = []
    def initBrk(self,stations):
        self.staName = stations
        self.brkFlag = np.zeros(len(stations),dtype=int)
        for i in range(len(stations)):
            self.brkMJD.append([])

# source
class SOURCE:
    def __init__(self):
        self.sourceName = []
        self.ivsName = []
        self.icfName = []
        self.iauName = []
        self.j2000Name = []
        self.rade       = []        # right ascension, declination
        self.rq         = []        # BCRS
        self.pRaDec     = []        # the partial derivatives of right ascension and declination
        self.flag       = []        # the flag of ICRF3 defined source
        
    def addSource(self, iersName, ivsName, icfName, iauName, rade, rq, pRaDec, flag):
        self.sourceName.append(iersName)
        self.ivsName.append(ivsName)
        self.icfName.append(icfName)
        self.iauName.append(iauName)
        self.rade.append(rade)
        self.rq.append(rq)
        self.pRaDec.append(pRaDec)
        self.flag.append(flag)

# station
class STATION:
    def __init__(self):
        self.stationName   = []    
        self.posit         = []         # coordinate [m]
        self.ell           = []         # ellipsoidal coordinates [rad,rad,m]
        self.vel           = []         # the station velocity
        self.epoch         = []         # the velocity start time
        self.obsTimeRange  = []         # the start and stop time
        self.obsMJDRange   = []         # the start and stop MJD
        self.ptype         = []         # the position type, ITRF or other use for NNR/NNT
        self.cto           = []         # the ocean tidal loading parameter
        self.axtype        = []         # the type of the axis
        self.foctype       = []         # the focus of antenna
        self.axoffset      = []         # the axis offset [m]
        self.axisCorr      = []         # the axis offset correct [s]
        self.thermpar      = []         # the thermal deformation parameter
        self.gravpar       = []         # the gravity deformation parameter
        self.ecc           = []         # 
        self.opp           = []         # the ocean pole tidal parameter
        self.ap            = []         # the atmosphere tidal parameter
        self.psdFlag       = []
        self.psd           = []         # the post-seismic deformation correct
        
    def addStation(self, stationName, posit, vel, epoch, ptype):
        self.stationName.append(stationName)
        self.posit.append(posit)
        self.vel.append(vel)
        self.epoch.append(epoch)
        self.ptype.append(ptype)
        
# eop
class EOP:
    def __init__(self, mjd, xp, yp, ut1,dx,dy):
        self.MJD = mjd
        self.XP = xp
        self.YP = yp
        self.UT1 = ut1
        self.DX = dx
        self.DY = dy
        
# ephem
class EPHEM:
    def __init__(self, merc, venu, em, mars, jupi, satu, uran, nept, plut, sun, earth, moon):
        self.merc = merc
        self.em = em
        self.venu = venu
        self.earth = earth
        self.mars = mars
        self.jupi = jupi
        self.satu = satu
        self.uran = uran
        self.nept = nept
        self.plut = plut
        self.sun = sun
        self.moon = moon

class PLANET:
    def get_xv_bar(self, x, v):
        self.xbar = x
        self.vbar = v
    def get_xv_geo(self, x, v):
        self.xgeo = x
        self.vgeo = v
    def get_acc_bar(self, a):
        self.acc = a
        
# GPT
class GPTGRID():
    def __init__(self):
        self.lat    = []  # latitude in degree
        self.lon    = []  # longitude in degree
        self.p      = []  # pressure in Pascal
        self.T      = []  # temperature in Kelvin
        self.Q      = []  # specific humidity in kg/kg
        self.dT     = []  # temperature lapse rate in Kelvin/m
        self.u      = []  # geoid undulation in m
        self.Hs     = []  # orthometric grid height in m
        self.ah     = []  # hydrostatic mapping function coefficient, dimensionless
        self.aw     = []  # wet mapping function coefficient, dimensionless
        self.la     = []  # water vapor decrease factor, dimensionless
        self.Tm     = []  # mean temperature in Kelvin
        self.gn_h   = []  # hydrostatic north gradient in m
        self.ge_h   = []  # hydrostatic east gradient in m
        self.gn_w   = []  # wet north gradient in m
        self.ge_w   = []  # wet east gradient in m
        
class VMF3PARAM():
    def __init__(self):
        self.abh = []
        self.abw = []
        self.ach = []
        self.acw = []
        self.bbh = []
        self.bbw = []
        self.bch = []
        self.bcw = []


# --------------------------- mod -----------------------------
class T2C:
    def __init__(self, trs2crs, pxp, pyp, put1, pdX, pdY):
        self.trs2crs = trs2crs
        self.dxp = pxp
        self.dyp = pyp
        self.dut1 = put1
        self.ddX = pdX
        self.ddY = pdY


# --------------------------- solve -----------------------------
class RESULT:
    def __init__(self):
        self.flag   = [0,0]     # the flag if the band if solve
        self.P      = []    # the weight matrix
        self.N      = []    # the constrained normal equation matrix
        self.b      = []    # the constrained normal equation matrix
        self.V      = []    # residuals
        self.VReal  = [[],[]]    # residuals over the observation
        self.SReal  = [[],[]]    # sigma of residuals over the observation
        self.dof    = 0     # degrees of freedom
        self.nObs   = 0     # the number of observation
        self.nConst = 0     # the number of constrain
        self.nEst   = 0     # the number of estimate parameter
        self.chis   = 0     # the chi-square
        self.para   = []     # the estimate parameter list
        
class STAOBS:
    def __init__(self):
        self.mjd = []
        self.oc_nob = []
        self.zd = []
        self.first = []
        self.other = []
        self.mf = []
        self.mge = []
        self.mgn = []
        self.pcoor = []
        self.scanbl = []
        self.meanTime = []
        self.meanPosit = []
    def addParam(self, mjd, oc_nob, first, mf, mge, mgn, other, pcoor, scanbl, meanTime, meanPosit):
        self.mjd.append(mjd)
        self.oc_nob.append(oc_nob)
        self.first.append(first)
        self.other.append(other)
        self.mf.append(mf)
        self.mge.append(mge)
        self.mgn.append(mgn)
        self.pcoor.append(pcoor)
        self.scanbl.append(scanbl)
        self.meanTime.append(meanTime)
        self.meanPosit.append(meanPosit)

# matrix
class LABEL:
    def __init__(self):
        self.zwd = []
        self.clk = []
        self.rqclk = []
        self.blclk = []
        self.xyz = []
        self.ut1 = []
        self.lod = []
        self.pmx = []
        self.pmy = []
        self.pmxr = []
        self.pmyr = []
        self.nutx = []
        self.nuty = []
        self.sou = []
        self.ngr = []
        self.egr = []
        
class ESTPARAM():
    def __init__(self):
        self.param = ['clk','zwd','ngr','egr','blclk','ut1','lod','pmx','pmy','pmxr','pmyr','nutx','nuty','xyz','sou']
        self.num = np.zeros(len(self.param), dtype=int)
        self.tmjd = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        self.clkinfo = [[],[]]
        self.zwdinfo = [[],[]]
        self.ngrinfo = [[],[]]
        self.egrinfo = [[],[]]
        
class OUTRESULT():
    def __init__(self):
        self.param = ['ut1','lod','pmx','pmy','pmxr','pmyr','nutx','nuty','xyz','sou']
        self.snxName = ['UT1','LOD','XPO','YPO','XPOR','YPOR','NUT_X','NUT_Y','XYZ','SOU']
        self.estFlag = np.zeros(len(self.param),dtype=int)
        self.unit = ['ms','ms','mas','mas','masD','masD','mas','mas','cm','mas']
        self.mjd = np.zeros(len(self.param)).tolist()
        self.aprioriValue = np.zeros(len(self.param)).tolist()
        self.estValue = np.zeros(len(self.param)).tolist()
        self.formalErr = np.zeros(len(self.param)).tolist()
        self.nscode = []
        self.souName = []

class NNRNNT():
    def __init__(self):
        self.aprX = []
        self.aprY = []
        self.aprZ = []
        self.nnrnnt = []
        self.nntrFlag = 0
    def norm(self):
        X = np.array(self.aprX)
        Y = np.array(self.aprY)
        Z = np.array(self.aprZ)
        
        temp = np.sqrt(np.dot(X,X)+np.dot(Y,Y)+np.dot(Z,Z))
        
        self.normX = X/temp
        self.normY = Y/temp
        self.normZ = Z/temp
        
class NNRSOU():
    def __init__(self):
        self.nnrMatrix = [[],[],[]]
        self.nnrFlag = 0
    #     self.readNNRSou()
        
    # def readNNRSou(self):
    #     fid = open('/Users/dangyao/Desktop/V1.4/COMMON/nnr_sou.txt','r')
    #     lines = fid.readlines()
    #     fid.close()
        
    #     temp = list(filter(None,lines[0][0:-1].split(" ")))
    #     self.nnrRef = getExcept(lines, 0, temp, 0)
        
class REWEI():
    def __init__(self):
        self.combinList = []
        self.useBlP = []
