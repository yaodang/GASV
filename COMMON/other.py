#!/usr/bin/env python3

import os,sys,re
# import platform

def changeBlank(strList):
    # 2025.02.12
    temp_staName = ''.join(strList)
    if ' ' in temp_staName.strip():
        staName1 = temp_staName.strip().replace(' ', '_')
        staName = staName1 + ' ' * (8 - len(staName1))
    else:
        staName = temp_staName

    return staName
        
def getVersion(path,string):
    files = os.listdir(path)
    #pattern = re.compile('^'+string+'*')
    pattern = re.compile('^'+string)
    
    version = []
    for file in files:
        result = pattern.search(file)
        if result:
            try:
                index = file.index('_V')
                version.append(int(file[index+2:index+5]))
            except ValueError:
                version.append(0)
    return version
    # print(version)

def makeFile(ncFile):
    if os.path.exists(ncFile):
        os.remove(ncFile)

    fid = open(ncFile, 'w')
    fid.close()

    if sys.platform[:3] != 'win':
        os.system('chmod 777 ' + ncFile)

def sessionNameCheck(name):
    #20250213
    year = 0
    if bool(re.match(r'^\d{8}',name)):
        year = int(name[:4])
    elif bool(re.match(r'^\d{2}[A-Z]{3}\d{2}',name)):
        if int(name[:2]) >= 50:
            year = 1900 + int(name[:2])
        else:
            year = 2000 + int(name[:2])

    if year == 0:
        print('    The year from session name wrong!')
        sys.exit()
    else:
        return year

def ncCreateSamePart(path, string, fileList, *args):
    "the same part for solve"
    if len(args) == 1:
        fileName = string + '_b'+args[0]+'.nc'
    else:
        fileName = string + '.nc'
        strLen = len(string)
    posit = -1
    
    for i in range(len(fileList)):
        file = fileList[i]
        if len(args) == 1:
            if string in file and ('_b'+args[0]) in file:
                posit = i
        else:
            if string in file[:strLen]:
                posit = i
    
    if not os.path.exists(path):
        os.mkdir(path)

    if len(args) == 1:
        version = getVersion(path, string+'_b'+args[0])
        if len(version):
            fileName = string+'_b'+args[0] + '_V%03d.nc' % (max(version) + 1)
    else:
        version = getVersion(path, string)
        if len(version):
            fileName = string + '_V%03d.nc' % (max(version) + 1)
    #version = getVersion(path,string)
    #if len(version):
    #    fileName = string+'_V%03d.nc'%(max(version)+1)
        
    if posit == -1:
        fileList.append(fileName)
    else:
        fileList[posit] = fileName
    
    ncFile = path+'/'+fileName
    makeFile(ncFile)
    
    return ncFile

def searchWrp(path):
    
    dirFiles = os.listdir(path)    
    version = []
    
    for file in dirFiles:
        if '.wrp' in file:
            try:
                index = file.index('_V')
                version.append(int(file[index+2:index+5]))
            except ValueError:
                version.append(0)
    return max(version)
    
#path = '/data/VLBI/vgosDB/2017/17SEP28XU/ObsEdit'
#version = getVersion(path,'GroupDelayFull_bX')
#print(version)