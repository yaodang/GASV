import sys

def checkParam(Param):
    if Param.Flags.vel[0] == 'YES' and Param.Global.station[0] == 'NO':
        print('Error: velocity is estimate but station not estimate!')
        sys.exit()

def checkProcess(posit, sitCode, souName, Param, rmStaNum, rmSouNum):
    if Param.Global.station[0] == 'YES':
        if len(posit[0]) != (len(sitCode) - rmStaNum) * 3:
            print('Error: station number is wrong in sinex!')
            sys.exit()
    if Param.Global.source[0] == 'YES':
        if len(posit[1]) != (len(souName) - rmSouNum) * 2:
            print('Error: source number is wrong in sinex!')
            sys.exit()