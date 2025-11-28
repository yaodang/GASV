from PyQt5.QtCore import pyqtSignal as Signal, QThread
import numpy as np
from COMMON import *
import os,re

from INIT import *
from MOD import *
from SOLVE import *
from OUT import *
from MAKE import *
from GLOB import *

class ambigCorrThread(QThread):
    finished = Signal(object)
    
    def setParam(self, scanInfo, result, bandIndex, *args):
        self.scanInfo = scanInfo
        self.result = result
        self.bandIndex = bandIndex
        
    def run(self):
        staRefIndex = self.scanInfo.stationAll.index(self.scanInfo.refclk)
        staNum = len(self.scanInfo.stationAll)
        sigma = np.array(self.scanInfo.pObs[self.bandIndex])
        ambigSize = self.scanInfo.baseInfo[2][self.bandIndex]
        
        ambigNum = correctAmbiguty(staNum, self.scanInfo, self.result, sigma, ambigSize, staRefIndex)
        
        self.finished.emit(ambigNum)
        
class localFileThread(QThread):
    finished = Signal(object,object)
    
    def initSet(self):
        self.yearList = []
    
    def setParam(self,dirPath,startYear,stopYear,pattern):
        self.dir_file_Path = dirPath
        self.startYear = startYear
        self.stopYear = stopYear
        self.pattern = pattern
    
    def run(self):
        self.fileInfo = [[],[],[],[]] # [DName,type,SName,STime]
        self.fileList = []
        self.version = []
        self.ac = []
        self.fileType = []
        self.SName = []
        self.Stime = []
        self.station = []
        self.wrms = []
        self.chi = []
        self.obs = []
        
        nsCode = np.loadtxt(os.path.join(self.dir_file_Path[2],'ns-codes.txt'),dtype=str,comments='*',usecols=[0,1,2,3],unpack=False)
        
        if self.startYear == self.stopYear:
            yearList = np.array([self.startYear])
        else:
            yearList = np.linspace(self.startYear, self.stopYear, self.stopYear-self.startYear+1,dtype=int)
            
        for year in yearList:
            if year not in self.yearList:
                self.yearList.append(year)
            
            path = os.path.join(self.dir_file_Path[0], str(year))
            self.readMaster24h(self.dir_file_Path[1], year)
            self.readMaster1h(self.dir_file_Path[1], year)
            
            if not os.path.exists(path):
                os.mkdir(path)
                
            for filename in os.listdir(path):
                if os.path.isdir(os.path.join(path, filename)):
                    self.fileList.append(filename)
                    self.readDir(os.path.join(path, filename), nsCode)
                    
                    snxFile = os.path.join(self.dir_file_Path[9],str(year),filename+'.snx')
                    if os.path.exists(snxFile):
                        solutionStatistics = read_SNX(snxFile,0)
                        self.wrms.append(solutionStatistics['WoPR'])
                        self.obs.append(solutionStatistics['NoO'])
                        self.chi.append(solutionStatistics['VF'])
                    else:
                        self.wrms.append(0)
                        self.obs.append(0)
                        self.chi.append(0)
                    
                    try:
                        index = self.fileInfo[0].index(filename)
                        self.fileType.append(self.fileInfo[1][index])
                        self.SName.append(self.fileInfo[2][index])
                        self.Stime.append(self.fileInfo[3][index])
                    except:
                        self.fileType.append('other')
                        self.Stime.append('XX:XX')
                        self.SName.append('XXXXXX')
                    
        self.searchFile = []
        if self.pattern == 'All':
            for i in range(len(self.fileList)):
                self.searchFile.append([self.fileList[i],self.SName[i],self.Stime[i],self.version[i],\
                                        self.ac[i],self.obs[i],self.chi[i],self.wrms[i],self.station[i]])
        else:
            for i in range(len(self.fileList)):
                file = self.fileList[i]
                if self.fileType[i] in self.pattern:
                    self.searchFile.append([file,self.SName[i],self.Stime[i],self.version[i],\
                                            self.ac[i],self.obs[i],self.chi[i],self.wrms[i],self.station[i]])

        self.finished.emit(self.fileList, self.searchFile)

    def readDir(self, path, nsCode):
        wrpFile = []
        flag = []
        vAll = []
        tempSta = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                if '.wrp' in filename:
                    wrpFile.append(filename)
                    if '_V' in filename:
                        index = filename.index('_V')
                        vAll.append(int(filename[index+2:index+5]))
                    else:
                        vAll.append(0)

                    if '_i' in filename:
                        flag.append(1)
                    else:
                        flag.append(0)
            if os.path.isdir(os.path.join(path, filename)):
                if filename.isupper() and (not ' ' in filename):
                    nsCodeP = np.where(nsCode[:,1]==filename)[0]
                    if len(nsCodeP):
                        tempSta.append(nsCode[nsCodeP,0][0])
        
        self.station.append(''.join(tempSta))
        #tempFile = wrpFile[-1]
        #index1 = tempFile.index('_V')
        #version = int(tempFile[index1+2:index1+5])

        version = max(vAll)
        index1 = vAll.index(version)
        if flag[index1] == 1:
            file = wrpFile[index1]
            self.version.append(version)
        else:
            print(wrpFile[index1])
            print('Please change the name like: session_V***_i***_kall.wrp')
        
        #if flag[-1] == 1:
        #    file = tempFile
        #else:
        #    for i in range(len(flag)-2,-1,-1):
        #        if flag[i] == 1:
        #            tempIndex = wrpFile[i].index('_V')
        #            tempVersion = int(wrpFile[i][tempIndex+2:tempIndex+5])
        #            if version == tempVersion:
        #                file = wrpFile[i]
        #            break
            
        #self.version.append(version)
        
        try:
            index2 = file.index('_i')
            index3 = file.index('_k')
            if index2 < index3:
                self.ac.append(file[index2+2:index3])
            else:
                print(path)
                index3 = file.index('.')
                self.ac.append(file[index2+2:index3])
        except:
            self.ac.append('NONE')
            
    def readMaster24h(self, path, year):
        
        flag = 0
        masterFile = os.path.join(path,'master'+str(year)[2:4]+'.txt')
        if year >= 2023:
            flag = 1
            masterFile = os.path.join(path,'master'+str(year)+'.txt')

        fid = open(masterFile,'r')
        lines = fid.readlines()
        fid.close()
        
        for line in lines:
            if line[0] == '|':
                tempPos = [match.start() for match in re.finditer(re.escape('|'), line)]
                if flag == 0:
                    self.fileInfo[0].append(str(year)[2:4]+line[tempPos[2]+1:tempPos[3]]+line[tempPos[11]+1:tempPos[12]].strip())
                    self.fileInfo[2].append(line[tempPos[1] + 1:tempPos[2]].strip().lower())
                else:
                    self.fileInfo[0].append(line[tempPos[1]+1:tempPos[2]]+'-'+line[tempPos[2]+1:tempPos[3]].strip())
                    self.fileInfo[2].append(line[tempPos[2] + 1:tempPos[3]].strip().lower())

                self.fileInfo[3].append(line[tempPos[4]+1:tempPos[5]])
                
                if 'IVS-R' in line:
                    self.fileInfo[1].append('IVS_R')
                elif 'VGOS-' in line:
                    self.fileInfo[1].append('VGOS_24h')
                elif 'AOV' in line:
                    self.fileInfo[1].append('AOV')
                elif 'APSG' in line:
                    self.fileInfo[1].append('APSG')
                elif 'AUS-MIX' in line:
                    self.fileInfo[1].append('AUM')
                elif 'AUS-AST' in line:
                    self.fileInfo[1].append('AUA')
                elif 'IVS-T' in line:
                    self.fileInfo[1].append('TRF')
                elif 'IVS-CRF' in line:
                    self.fileInfo[1].append('CRF')
                elif 'CONT' in line:
                    self.fileInfo[1].append('CONT')
                else:
                    self.fileInfo[1].append('24h_other')
                        
    def readMaster1h(self, path, year):
        
        flag = 0
        masterFile = os.path.join(path,'master'+str(year)[2:4]+'-int.txt')
        if year >= 2023:
            flag = 1
            masterFile = os.path.join(path,'master'+str(year)+'-int.txt')

        if os.path.exists(masterFile):
            fid = open(masterFile,'r')
            lines = fid.readlines()
            fid.close()

            for line in lines:
                if line[0] == '|':
                    tempPos = [match.start() for match in re.finditer(re.escape('|'), line)]
                    if flag == 0:
                        self.fileInfo[0].append(str(year)[2:4]+line[tempPos[2]+1:tempPos[3]]+line[tempPos[11]+1:tempPos[12]].strip())
                        self.fileInfo[2].append(line[tempPos[1] + 1:tempPos[2]].strip().lower())
                        if 'INI' in line:
                            self.fileInfo[1].append('INT0')
                        elif '|IN1' in line:
                            self.fileInfo[1].append('INT1')
                        elif '|IN2' in line:
                            self.fileInfo[1].append('INT2')
                        elif '|IN3' in line:
                            self.fileInfo[1].append('INT3')
                        elif 'VGOS' in line:
                            self.fileInfo[1].append('VGOS_1h')
                        else:
                            self.fileInfo[1].append('1h_other')
                    else:
                        self.fileInfo[0].append(line[tempPos[1]+1:tempPos[2]]+'-'+line[tempPos[2]+1:tempPos[3]].strip())
                        self.fileInfo[2].append(line[tempPos[2] + 1:tempPos[3]].strip().lower())
                        if 'IVS-INT-00' in line:
                            self.fileInfo[1].append('INT0')
                        elif 'IVS-INT-1' in line:
                            self.fileInfo[1].append('INT1')
                        elif 'IVS-INT-2' in line:
                            self.fileInfo[1].append('INT2')
                        elif 'IVS-INT-3' in line:
                            self.fileInfo[1].append('INT3')
                        elif 'VGOS' in line:
                            self.fileInfo[1].append('VGOS_1h')
                        else:
                            self.fileInfo[1].append('1h_other')

                    self.fileInfo[3].append(line[tempPos[4]+1:tempPos[5]])
                
            
class runThread(QThread):
    finished = Signal(object,object,object,object,object,object,object,object)
    error = Signal(object)
    
    def setParam(self, scanInfo, Param, wrpInfo, handOutlierFlag, rmOutlier, runFlag, bandIndex, *args):
        self.scanInfo = scanInfo
        self.Param = Param
        self.wrpInfo = wrpInfo
        self.handOutlierFlag = handOutlierFlag
        self.rmOutlier = rmOutlier
        self.runFlag = runFlag
        self.bandIndex = bandIndex

        if len(args) == 2:
            self.sourceInfo = args[0]
            self.stationInfo = args[1]
            # self.staObs = args[2]
        
    def run(self):
        if self.runFlag == 0:
            print('    Reading station file......')
            self.stationInfo = read_station(self.Param.Map.stationFile, self.scanInfo)
    
            updateScanInfo(self.scanInfo, self.Param, self.wrpInfo, 0)
            makeScan(0,self.scanInfo)
    
            print('    Reading source file......')
            meanMJD = np.mean(self.scanInfo.scanMJD)
            self.sourceInfo = read_source(self.Param.Map.sourceFile, self.scanInfo.sourceAll, self.scanInfo.souPosit, meanMJD)
    
            print('    Reading eop file......')
            self.eopApri = read_eop(self.Param.Map.eopFile, self.scanInfo.scanMJD)
    
            print('    Reading ephem file......')
            ephem = read_eph(self.Param.Map.ephemFile,self.scanInfo.scanMJD)
    
            if self.Param.Map.mapFun == 'GPT3':
                read_trpgrid(self.Param)
                
            mod(self.Param, self.eopApri, self.scanInfo, self.sourceInfo, self.stationInfo, ephem)
            
            self.result = RESULT()
            
            self.runFlag = 1
        
        errorType = 0
        if self.handOutlierFlag == 0:
            try:
                self.staObs = solve(self.Param, self.scanInfo, self.stationInfo, self.sourceInfo, self.result, self.bandIndex)
            except IndexError:
                errorType = 'IndexError'
            except ValueError:
                errorType = 'ValueError'
                
        elif self.handOutlierFlag == 1:
            try:
                self.staObs = solve(self.Param, self.scanInfo, self.stationInfo, self.sourceInfo, self.result, self.bandIndex, self.rmOutlier)
            except IndexError:
                errorType = 'IndexError'
            except ValueError:
                errorType = 'ValueError'
        
        if len(self.result.para):
            out = collectResult(self.Param, self.scanInfo, self.stationInfo, self.sourceInfo, self.staObs, self.eopApri, self.result)
        else:
            out = OUTRESULT()
        
        if errorType == 0:
            self.finished.emit(self.scanInfo,self.Param, self.sourceInfo, self.stationInfo, self.result, self.staObs, out, self.runFlag)
        else:
            self.error.emit(errorType)
            
class GLOBThread(QThread):
    finished = Signal(object,object)
    
    def setParam(self, Param):
        self.Param = Param
        
    def run(self):
        NGlob, bGlob, sitAll, souAll = GLOB(self.Param)
        
        self.finished.emit(sitAll, souAll)
        
 
class resultThread(QThread):
    finished = Signal(list)
    
    def setParam(self, scanInfo, wrpInfo, Param, result, stationInfo, sourceInfo, path, sessionNum, out, outFlag):
        self.scanInfo = scanInfo
        self.wrpInfo = wrpInfo
        self.Param = Param
        self.result = result
        self.stationInfo = stationInfo
        self.sourceInfo = sourceInfo
        self.vgosPath = path
        self.sessionNum = sessionNum
        self.sessionName = Param.Arcs.session[sessionNum]
        self.out = out
        self.outFlag = outFlag
        
        if self.outFlag[0] == 1 or self.outFlag[2] == 1: 
            self.eopApri = read_eop(self.Param.Map.eopFile, self.scanInfo.scanMJD)

    def run(self):
        checkFlag = [0, 0, 0]

        if self.outFlag[0]:
            try:
                writeSFF(self.Param, self.scanInfo, self.eopApri, self.result, self.out)
            except:
                checkFlag[0] -= 1
            else:
                checkFlag[0] += 1
        if self.outFlag[1]:
            writeEOP(self.Param, self.scanInfo, self.result, self.sessionNum, self.out)
        #if self.outFlag[1]:
        #    try:
        #        writeEOP(self.Param, self.scanInfo, self.result, self.sessionName, self.out)
        #    except:
        #        checkFlag[1] -= 1
        #    else:
        #        checkFlag[1] += 1
                
        if self.outFlag[2]:
            try:
                writeSNX(self.Param, self.scanInfo, self.sourceInfo, self.stationInfo, self.eopApri, self.result, self.out)
            except:
                checkFlag[2] -= 1
            else:
                checkFlag[2] += 1
                
        if self.outFlag[3]:
            #if len(self.sessionName) == 9:
            #    year = 2000 + int(self.sessionName[:2])
            #elif len(self.sessionName) == 15:
            #    year = int(self.sessionName[:4])
            year = sessionNameCheck(self.sessionName)
            
            sessionPath = self.vgosPath + '/'+str(year) + '/'+self.sessionName
            create_result(sessionPath, self.scanInfo, self.wrpInfo, self.Param.Arcs)
                
        self.finished.emit(checkFlag)

