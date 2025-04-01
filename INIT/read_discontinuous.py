#!/usr/bin/env python3

from COMMON.time_transfer import *

def read_discontinue(fileName):
    sta_DC = {'name':[],\
              'dcTime':[],\
              'dcMJD':[],\
              'newName':[],\
              'newCode':[]}

    fid = open(fileName,'r')
    lines = fid.readlines()
    fid.close()
    flags = ['A','B','C','D','E','F','G','H','I','J','K']

    for i in range(len(lines)):
        if lines[i][0] != '%':
            temp = list(filter(None,lines[i].split(" ")))
            temp[-1] = temp[-1][:-1]
            if temp[0] not in sta_DC['name']:
                sta_DC['name'].append(temp[0])
                sta_DC['dcTime'].append(temp[1:])

                dcMJD = []
                for timeStr in temp[1:]:
                    year = int(timeStr[:4])
                    doy = int(timeStr[4:7])
                    seconds = int(timeStr[7:])

                    mon,day = doy2day(doy,year)
                    hour,minute,second = sec2hms(seconds)
                    mjd = modjuldatNew(year,mon,day,hour,minute,second)
                    dcMJD.append(mjd)
                sta_DC['dcMJD'].append(dcMJD)

                newName = []
                newCode = []
                if len(temp[0]) == 8:
                    tempName = temp[0][:-1]
                else:
                    tempName = temp[0]
                for j in range(len(temp[1:])+1):
                    newName.append(tempName+str(j))
                    newCode.append(flags[j])
                sta_DC['newName'].append(newName)
                sta_DC['newCode'].append(newCode)

    return sta_DC

#fileName = '/home/GeoAS/Work/GATV/APRIORI/vlbi_discontinuous.txt'
#sta_DC = read_discontinue(fileName)
#print('yes')