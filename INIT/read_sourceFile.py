#!/usr/bin/env python3
"""
This program use to pick the source information(name,ra,de) from the apriori source file.
"""

import os
import sys
import numpy as np
from scipy.constants import arcminute

sys.path.append("..//")
from COMMON import *

def read_source(sourceFile, sourceList, sourceApriori, meanMJD):
    """
    Read the source file
    ---------------------
    input: 
        sourceFile     : the source apriori file
        sourceList     : the session observe source, list
        sourceApriori  : the apriori source posit
        meanMJD        : the mean obs MJD
    output: 
        sourceInfo     : SOURCE class
    ---------------------
    """
    if not os.path.exists(sourceFile):
        sys.stderr.write('Error: The apriori source file not exist!')
        sys.exit()
        
    # sou_iers,sou_ivs,flag = np.loadtxt(sourceFile,comments='%',usecols=[0,1,2],dtype=str,unpack=True)
    # RaDec = np.loadtxt(sourceFile,comments='%',usecols=[3,4,5,6,7,8],dtype=float,unpack=False)
    # Ra = ((RaDec[:,0]+RaDec[:,1]/60+RaDec[:,2]/3600)*np.pi/12).tolist()
    # De = []
    # for i in range(len(Ra)):
    #     if '-' in str(RaDec[i,3]):
    #         De.append((RaDec[i,3]-RaDec[i,4]/60-RaDec[i,5]/3600)*np.pi/180)
    #     else:
    #         De.append((RaDec[i,3]+RaDec[i,4]/60+RaDec[i,5]/3600)*np.pi/180)
    sou_iers,sou_icrf,sou_iau,sou_ivs,flag,Ra,De = readSourceFile(sourceFile)
    Ra,De = correct_GA(Ra, De, meanMJD)
    
    sourceInfo = SOURCE()
    blank = '        '
    for i in range(len(sourceList)):
        name = sourceList[i]
        #index = -1
        if name.strip() in sou_iers:
            index = sou_iers.index(name.strip())
            souIERSName = name
            souIVSName = name
            souICFName = sou_icrf[index]
            souIAUName = sou_iau[index]
            if sou_ivs[index] != 'X':
                souIVSName = sou_ivs[index] + blank[:8-len(sou_ivs[index])]
            souRa = Ra[index]
            souDe = De[index]
            souFlag = flag[index]
        elif name.strip() in sou_ivs:
            index = sou_ivs.index(name.strip())
            souIERSName = sou_iers[index] + blank[:8-len(sou_iers[index])]
            souIVSName = name
            souICFName = sou_icrf[index]
            souIAUName = sou_iau[index]
            souRa = Ra[index]
            souDe = De[index]
            souFlag = flag[index]
        else:
            print('        The %s not in source file, using apriori posit in data!'%name)
            souRa,souDe = correct_GA(sourceApriori[i][0], sourceApriori[i][1], meanMJD)
            if souRa == 0 and souDe == 0:
                print('        Error: the posit of %s is wrong.' % name)
                sys.exit()
            souFlag = 'other'
            souIERSName = name
            souIVSName = name
            raICFName,raIAUName = ra2hms(sourceApriori[i][0])
            decICFName, decIAUName = dec2dms(sourceApriori[i][1])
            souICFName = raICFName + decICFName
            souIAUName = raIAUName + decIAUName

        #if index != -1:
        rq, pRaDec = partialSource(souRa, souDe)
        if souFlag == 'define':
            sourceInfo.addSource(souIERSName, souIVSName, souICFName, souIAUName, np.array([souRa,souDe]), rq, pRaDec,1)
        else:
            sourceInfo.addSource(souIERSName, souIVSName, souICFName, souIAUName, np.array([souRa,souDe]), rq, pRaDec,0)
        #else:
        #    print('        Error: the observe source %s not in source file\n        Please added!'%name)
        #    sys.exit()
            
    return sourceInfo

def readSourceFile(sourceFile):
      
    sou_iers,sou_icrf,sou_iau,sou_ivs,flag = np.loadtxt(sourceFile,comments='%',usecols=[0,1,2,3,4],dtype=str,unpack=True)
    RaDec = np.loadtxt(sourceFile,comments='%',usecols=[5,6,7,8,9,10],dtype=float,unpack=False)
    Ra = ((RaDec[:,0]+RaDec[:,1]/60+RaDec[:,2]/3600)*np.pi/12).tolist()
    De = []
    for i in range(len(Ra)):
        if '-' in str(RaDec[i,3]):
            De.append((RaDec[i,3]-RaDec[i,4]/60-RaDec[i,5]/3600)*np.pi/180)
        else:
            De.append((RaDec[i,3]+RaDec[i,4]/60+RaDec[i,5]/3600)*np.pi/180)
            
    return sou_iers.tolist(),sou_icrf.tolist(),sou_iau.tolist(),sou_ivs.tolist(),flag,Ra,De

def add_blank(source):
    """
    Add blank to source name if the length is not equal to 8
    ---------------------
    input: 
        source         : the source name array
    output: 
        source         : new source name array
    ---------------------
    """
    blank = '        '
    for i in range(len(source)):
        if len(source[i]) != 8:
            source[i] = source[i] + blank[0:8-len(source[i])]
    if type(source) == list:
        return source
    else:
        return source.tolist()    
    
def correct_GA(ra, de, meanMJD):
    '''
    Correct the source position
    reference: MacMillan 2019, Galactocentric acceleration in VLBI analysis

    Parameters
    ----------
    ra : rad
        Right ascension.
    de : rad
        declination.
    meanMJD : TYPE
        the session mean MJD.

    Returns
    -------
    ra_ga : TYPE
        the right ascension after correct.
    de_ga : TYPE
        the declination after correct.

    '''
    
    
    deg2rad = np.pi/180
    ra_gal = 266.4*deg2rad
    de_gal = -28.94*deg2rad
    
    ga_val = 5.8 # [muas/year]
    ga_ref = 57023 # 20150101
    ga_val = ga_val*1E-6/3600.0*deg2rad
    ga_vec = [np.cos(de_gal)*np.cos(ra_gal),np.cos(de_gal)*np.sin(ra_gal),np.sin(de_gal)]
    
    time_delta = (meanMJD-ga_ref)/365.25
    
    delta_ra = (-ga_vec[0]*np.sin(ra)   +   ga_vec[1]*np.cos(ra))/np.cos(de)
    delta_de = -ga_vec[0]*np.sin(de)*np.cos(ra) - ga_vec[1]*np.sin(de)*np.sin(ra) + ga_vec[2]*np.cos(de)
    
    delta_ra = delta_ra*ga_val
    delta_de = delta_de*ga_val
    
    ra_ga = ra + delta_ra*time_delta
    de_ga = de + delta_de*time_delta
    
    return ra_ga, de_ga

def partialSource(Ra, Dec):
    """
    Get the direction in BCRF, partial derivative of right ascension and declination

    Parameters
    ----------
    Ra : the right ascension of source.
    Dec : the declination of source.

    Returns
    -------
    rq : source direction of source in BCRF.
    pRaDec : the partial derivative of right ascension and declination.

    """
    
    sind = np.sin(Dec)
    cosd = np.cos(Dec)
    
    sinr = np.sin(Ra)
    cosr = np.cos(Ra)
    
    ss = sind*sinr
    sc = sind*cosr
    cs = cosd*sinr
    cc = cosd*cosr
    
    rq = np.array([cc, cs, sind])
    pRaDec = np.array([[-cs, cc, 0],[-sc, -ss, cosd]])
    
    return rq, pRaDec

def ra2hms(ra_radians):

    ra_hours = ra_radians * 180 / np.pi /15
    hours = int(ra_hours)
    remain = ra_hours - hours
    minutes = int(remain * 60)
    seconds = (remain * 60 - minutes) * 60

    raICRFName = 'J%02d%02d%04.1f'%(hours,minutes,seconds)
    raIAUName = 'J%02d%02d'%(hours,minutes)
    return raICRFName,raIAUName

def dec2dms(dec_radians):

    dec_degrees = dec_radians * 180 / np.pi
    degrees = int(dec_degrees)
    remain = abs(dec_degrees - degrees)
    arcminutes = int(remain * 60)
    arcseconds = (remain * 60 - arcminutes) * 60

    sign = '+' if dec_degrees >= 0 else '-'

    decICRFName = '%s%02d%02d%04.1f' % (sign, abs(degrees), arcminutes, int(arcseconds))
    decIAUName = '%s%02d%02d' % (sign, abs(degrees), arcminutes)
    return decICRFName, decIAUName