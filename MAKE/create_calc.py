#!/usr/bin/env python3

# from OUT.createScan import *
# from OUT.createObsPart import *
# from OUT.createApriori import *
# from OUT.createStation import *
# from OUT.createObsTheoretical import *

from MAKE import *

def createV2(Param, scanInfo, stationInfo, sourceInfo, eopObs, ephem):
    
    path = Param.Setup.vgosdbPath + '/21DEC20XA' 
    numSta = len(scanInfo.stationAll)
    numScan = len(scanInfo.scanMJD)
    numSou = len(scanInfo.sourceAll)
    numObs = len(scanInfo.Obs2Scan)    
    
    # Apriori path
    souList = scanInfo.sourceAll
    staList = scanInfo.stationAll
    # createSource(path, scanInfo.expName, numSou, souList, sourceInfo)
    # createAntenna(path, scanInfo.expName, numSta, staList, stationInfo)
    # createStation(path, scanInfo.expName, numSta, staList, stationInfo)
    
    # Scan path
    # createERPApriori(path, scanInfo.expName, numScan, eopObs)
    # createEphemeris(path, scanInfo.expName, numScan, ephem.sun, ephem.moon, ephem.earth)
    
    # ObsPart path
    # createPartXYZ(path, scanInfo.expName, numObs, scanInfo.pxyz)
    # createPartERP(path, scanInfo.expName, numObs, scanInfo.pdx, scanInfo.pdy, scanInfo.pdut1)
    # CreatePartRaDec(path, scanInfo.expName, numObs, scanInfo.psou)
    # pRefract = np.array(scanInfo.com)[:,1]
    # CreatePartDelayAtmRefract(path, scanInfo.expName, numObs, pRefract)
    
    
    # ObsTheoretical path
    # delayTheory = np.array(scanInfo.com)[:,0]
    # createDelayTheoretical(path, scanInfo.expName, numObs, delayTheory)
    
    # Station path
    Scan2Station = scanInfo.Scan2Station
    StatScan = getStatScan(numSta, Scan2Station)
    mfWet = scanInfo.scanMFW
    mfGE = scanInfo.scanMFGE
    mfGN = scanInfo.scanMFGN
    
    for i in range(numSta):
        createAzEl(path, scanInfo.expName, staList[i], StatScan[i], scanInfo.scanState)
        createCalAxisOffset(path, scanInfo.expName, staList[i], StatScan[i], scanInfo.scanState)
        createPartAxisOffset(path, scanInfo.expName, staList[i], StatScan[i], scanInfo.scanState)
        createPartZenithWet(path, scanInfo.expName, staList[i], StatScan[i], mfWet)
        createPartHorizonGrd(path, scanInfo.expName, staList[i], StatScan[i], mfGE, mfGN)
        
def getStatScan(num, Scan2Station):
    """
    Get the scan posit and station posit in scan of station

    Parameters
    ----------
    num : All station number.
    Scan2Station : scan and station relevance.

    Returns
    -------
    StatScan : scan posit and station posit in scan for all station.

    """
    
    StatScan = []
    for i in range(num):
        scanPosit = []
        staScan = np.where(Scan2Station[:,i]!=0)
        
        for scanNum in staScan[0]:
            temp = np.where(Scan2Station[scanNum,:i]!=0)
            if len(temp[0]):
                scanPosit.append(len(temp[0]))
            else:
                scanPosit.append(0)
            
        StatScan.append([staScan[0], scanPosit])    
        
    return StatScan