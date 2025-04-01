#!/usr/bin/env python3

import sys,os,time
import re,copy

from INIT.init import *
from MOD.mod import *
from SOLVE.solve import *
from GLOB.GLOB_glob import *
from OUT import *
from MAKE import *

# makedb -d 23JAN11XA -o /Users/dangyao/work/software/VIPS/vgosDb/2023 /Users/dangyao/Downloads/crf134
# plog -p /Users/dangyao/work/software/VIPS/STALOG -k log /Users/dangyao/work/software/VIPS/vgosDb/2022/22JUN24XG
# D:/software/V1.9.8/APRIORI/cnt.txt
# makedb -d 23OCT18NU -o D:/data/VLBI/vgosDB/2023 D:/data/VLBI/HOPS_OUT/U231018

def check():
    if len(sys.argv) == 1:
        print('\nUsage: VIPSR [OPTION]\n'+\
              "Try 'VIPSR --help' for more information\n")
        sys.exit()
        
    elif sys.argv[1] == '--help':
        printHelp()
        
    elif sys.argv[1] == 'init':
        creatPath()
        
    elif sys.argv[1] == 'makedb':
        runFlag = 1
        runInfo = {'ac':'','dbName':'','outPath':'','inPath':''}
        
        if len(sys.argv) != 9:
            print('Please input like: VIPSR makedb -a IVS -d 23MAR03XA -o /home/work /data/corr/i23001\n')
            sys.exit()
        
        index1 = sys.argv.index('-a')
        index2 = sys.argv.index('-d')
        index3 = sys.argv.index('-o')
        
        runInfo['ac'] = sys.argv[index1+1]
        runInfo['dbName'] = sys.argv[index2+1]
        runInfo['outPath'] = sys.argv[index3+1]
        runInfo['inPath'] = sys.argv[-1]

        return runFlag,runInfo
    
    elif sys.argv[1] == 'calc':
        runFlag = 2
        runInfo = [sys.argv[2]]
        
        return runFlag,runInfo
    
    elif sys.argv[1] == 'plog':
        runFlag = 3
        runInfo = {'inPath':'','type':'','outPath':''}
        
        if len(sys.argv) != 7:
            print('Please input like: VIPSR plog -p /data/session -k log /data/21DEC20XA\n')
            sys.exit()
        index1 = sys.argv.index('-p')
        index2 = sys.argv.index('-k')
        runInfo['inPath'] = sys.argv[index1+1]
        runInfo['type'] = sys.argv[index2+1]
        runInfo['outPath'] = sys.argv[-1]

        return runFlag, runInfo
    
    else:
        runFlag = 4
        runInfo = [sys.argv[1]]
        
        return runFlag,runInfo
             
def printHelp():
    print("VIPSR is a program that process VLBI data and estimate the parameter.\n"+\
          '\nUsage: VIPSR [OPTION]\n'+\
          "The OPTION can be:\n"+\
          "           --help: print help information\n\n"+\
          "             init: create the work path\n\n"+\
          "           makedb: create the vgosDB file from HOPS output, the parameter is:\n"+\
          "                   -a 'AnalysisName'\n"+\
          "                   -d 'databaseName'\n"+\
          "                   -o 'outputDir'\n"+\
          "                   'fringe data path'\n\n"+\
          "             calc: create the vgosDB version 2, the parameter is:\n"+\
          "                   <wrap file>-- the vgosDB wrap file\n\n"+\
          "             plog: read the station log or other file, the parameter is:\n"+\
          "                   -p 'log path'\n"+\
          "                   -k [log|met|cable]\n"+\
          "                   <absolute vgosDB path>\n\n"+\
          "         cnt_file: control file path, contain the setup for VLBI data process\n")
    sys.exit()
    
def creatPath():
    temp1 = os.path.abspath(__file__)
    runPath = temp1[0:temp1.rfind('/')+1]
    temp2 = os.getcwd()
    workPath = temp2+'/VIPS_WORK'
    
    if os.path.exists(workPath):
        choice = input('\nThe work path already exists in '+temp2+'\n Remove and create new(y/n)?:')
    else:
        choice = input('\nCreate work path in '+temp2+' (y/n/c)?:')
        if choice == 'c':
            temp3 = input('\nInput the new work Dir:')
            workPath = temp3+'/VIPS_WORK'
        
    
    if choice == 'y' or choice == 'c':
        if os.path.exists(workPath):
            os.system('rm -rf '+workPath)
            
        os.mkdir(workPath)
        fileDirs = ['SNX','EOP','PNG','ARC']
        
        for fileDir in fileDirs:
            os.mkdir(os.path.join(workPath,fileDir))
            
        os.system('cp -r '+runPath+'APRIORI '+workPath)
    
    sys.exit()

def main():
    runFlag,runInfo = check()
    print('\n######################## START  ########################\n')
    
    if runFlag == 1:
        makedb(runInfo)
    
    Param = PARAMETER()
    if runFlag == 2:
        Param.Setup.calctheroe = 'CREATE'
        wrapName = sys.argv[2]
        if not os.path.isabs(wrapName):
            wrapName = os.getcwd()+'/'+wrapName
        if os.path.exists(wrapName):
            Param.Arcs.session = ['23OCT22XU']
            Param.Arcs.version = [1]
            Param.Arcs.AC = ['YAO']
            # Param.Arcs.session,Param.Arcs.version,Param.Arcs.AC = wrapSVA(wrapName)
            indexes = [m.start() for m in re.finditer('/', wrapName)]
            Param.Setup.vgosdbPath = wrapName[:indexes[-3]+1]
        else:
            print('    The wrap not exists!')
            sys.exit()
    
    if runFlag == 3:
        pLog(runInfo)
            
    if runFlag == 4:
        read_cnt(runInfo[0], Param)
        Param.check()
            
    if runFlag == 4 or runFlag == 2:
        process(Param)
    
def process(ParamApri):
    if ParamApri.Setup.solution == 'GLOB':
        GLOB(ParamApri)
    else:
        fid = open('log','w')
        for sessionNum in range(len(ParamApri.Arcs.session)):
            try:
                Param = copy.deepcopy(ParamApri)
                print('\n##################  Process '+Param.Arcs.session[sessionNum]+'  #################')
                scanInfo, sourceInfo, stationInfo, eopApri, ephem = init(Param,sessionNum)
                eopObs,res = mod(Param, eopApri, scanInfo, sourceInfo, stationInfo, ephem)

                # fid = open('com_yd.txt','w')
                # for i in range(len(res)):
                #     fid.writelines('%5d %17.15f\n'%(scanInfo.Obs2Scan[i], res[i]))
                # fid.close()

                if Param.Setup.calctheroe.upper() == 'CREATE':
                    createV2(Param, scanInfo, stationInfo, sourceInfo, eopObs, ephem)
                    sys.exit()

                index = scanInfo.baseInfo[0].index('X')
                result = RESULT()
                staObs = solve(Param, scanInfo, stationInfo, sourceInfo, result, index)

                print('\n---------------------  Write result  --------------------')
                plotResuidal(Param, scanInfo, staObs, result)
                out = collectResult(Param, scanInfo, stationInfo, sourceInfo, staObs, eopApri, result)
                writeSFF(Param, scanInfo, eopApri, result, out)

                writeEOP(Param, scanInfo, result, sessionNum, out)
                writeSNX(Param, scanInfo, sourceInfo, stationInfo, eopApri, result, out)
            except Exception as e:
                fid.writelines(f'Error:%s \n{e}'%Param.Arcs.session[sessionNum])
                continue
        fid.close()

if __name__ == "__main__":
    startTime = time.time()
    main()
    stopTime = time.time()
    print('\n##########################################################\n')
    print('    Using time:%6.1f s'%(stopTime-startTime))
    print('\n#####################    VIPS END     #####################\n')
