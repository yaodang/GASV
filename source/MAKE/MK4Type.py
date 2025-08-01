#!/usr/bin/env python3

import struct, sys
import numpy as np

# sys.path.append('../COMMON')

# from time_transfer import *

from COMMON import *

def typeRootFile(file):
    
    fid = open(file,'r')
    lines = fid.readlines()
    fid.close()
    
    modePosit = lines.index('$MODE;\n')
    stationPosit = lines.index('$STATION;\n')
    antennaPosit = lines.index('$ANTENNA;\n')
    freqPosit = lines.index('$FREQ;\n')
    bbcPosit = lines.index('$BBC;\n')
    
    allStaAbbr = []
    allStaName =[]
    blank = '        '
    for line in lines[stationPosit:antennaPosit]:
        if 'def ' in line:
            index = line.index(';')
            allStaAbbr.append(line[index-2:index])
        if 'ref $SITE' in line:
            index1 = line.index('=')
            index2 = line.index(';')
            name = line[index1+2:index2]
            newName = name+blank[:8-len(name)]
            allStaName.append(newName)
    
    staAbbr = []
    staFreq = []
    staName = []
    for line in lines[modePosit:stationPosit]:
        if 'ref $FREQ' in line:
            index1 = line.index('=')
            index2 = line.index(':')
            index3 = line.index(';')
            staAbbr.append(line[index2+1:index3])
            staFreq.append(line[index1+2:index2])
            
            index4 = allStaAbbr.index(line[index2+1:index3])
            staName.append(allStaName[index4])
            
    
    staFreqStart = []
    staFreqStop = []
    staFreqIndex = []
    band = []
    for i in range(freqPosit,bbcPosit):
        if ' def ' in lines[i]:
            staFreqStart.append(i)
            index1 = lines[i].index('def')
            index2 = lines[i].index(';')
            staFreqIndex.append(staFreq.index(lines[i][index1+4:index2]))
            
        if 'chan_def' in lines[i]:
            index = lines[i].index('=')
            if lines[i][index+2] not in band:
                band.append(lines[i][index+2])
        
        if 'enddef;' in lines[i]:
            staFreqStop.append(i)
            
    staSampleRate = np.zeros(len(staAbbr))
    staChannelFreq = []
    for i in range(len(staAbbr)):
        staChannelFreq.append([])
        
    for i in range(len(staFreqStart)):
        if len(band) == 1:
            temp = [[]]
            uniqueFreq = [[]]
        elif len(band) == 2:
            temp = [[],[]]
            uniqueFreq = [[],[]]
            
        for j in range(staFreqStart[i],staFreqStop[i]):
            if 'sample_rate =' in lines[j]:
                index1 = lines[j].index('=')
                index2 = lines[j].index('Ms')
                staSampleRate[staFreqIndex[i]] = float(lines[j][index1+1:index2])
            
            if 'chan_def' in lines[j]:
                index  = lines[j].index('=')
                index1 = lines[j].index(': :')
                index2 = lines[j].index('MHz')
                # if len(band) == 1:
                #     temp.append(float(lines[j][index1+3:index2]))
                # else:
                bandIndex = band.index(lines[j][index+2])
                temp[bandIndex].append(float(lines[j][index1+3:index2]))
                
        # if len(band) == 1:
        #     uniqueFreq = np.unique(temp)
        # else:
        for k in range(len(band)):
            uniqueFreq[k] = np.unique(temp[k])
                
        staChannelFreq[staFreqIndex[i]] = uniqueFreq
                
    # print('YES')
    return staName, staSampleRate,staChannelFreq,band
        
    


def type200(Bytes, posit):
    '''
    Read th type 200 (general information).
    
    Field           type            bytes   Description
    -----           ----            -----   -----------
    Type            ascii           3       200
    Version         ascii           2       0-99 
    Unused          ascii           3       Spaces
    Revision        i*2 x 10        20      Revision levels for many progs
    Experiment      i*4             4       Experiment number
    Program         ascii           32      Observing program name
    Scan name       ascii           32      Name of scan
    Correlator      ascii           8       Correlator indentification
    Scantime        date            12      Scan time to 1 second
    Start offset    i*4             4       Baseline start (sec) rel. to scan
    Stop offset     i*4             4       Baseline stop (sec) rel. to scan
    Corr_date       date            12      Date of correlation
    FPT             date            12      Fourfit processing date
    FRT             date            12      Fourfit reference time
    
    Record length is fixed at 160 bytes.

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    scanTime : the observer source

    '''
    # posit = Bytes[64:].find(b'201')+64
    
    byte = [[2,2,2,2,4],['>h','>h','>h','>h','>f']]
    

    scanTime = []
    for i in range(len(byte[0])):
        temp = posit-12+sum(byte[0][:i])
        scanTime.append(struct.unpack(byte[1][i],Bytes[temp:temp+byte[0][i]])[0])
    
    md = doy2day(scanTime[1],scanTime[0])
    MJD = modjuldat(np.array([scanTime[0]]),np.array([md[0]]),np.array([md[1]]),\
                    np.array([scanTime[2]]),np.array([scanTime[3]]),np.array([scanTime[4]]))
    scanTime.extend([md[0],md[1],MJD[0]])
    
    return scanTime

def type201(Bytes, posit):
    '''
    Read th type 201 (source information).

    Field           type            bytes   Description
    -----           ----            -----   -----------
    Type            ascii           3       201
    Version         ascii           2       0-99 
    Unused          ascii           3       Spaces
    Source          ascii           32      Source name
    Coord           sky_coord       16      Source coordinates of epoch
    Epoch of ra/dec i*2             2       1950 or 2000
    Unused2         ascii           2       Padding
    Coord_date      date            12      Ref date for proper motion
    R.A. rate       r*8             8       Proper motion (rad/sec)
    Dec. rate       r*8             8       Proper motion (rad/sec)
    Pulsar phase    r*8 x 4         32      Polynomial of pulse timing
    Pulsar epoch    r*8             8       reference time for polynomial
    Dispersion      r*8             8       Pulsar dispersion measure
    
    Record length is fixed at 128 bytes.

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    sou : the observer source

    '''
    blank = '        '
    # posit = Bytes[64:].find(b'201')+64
    sou = Bytes[posit+8:posit+8+32].decode()
    
    temp = sou.index('\x00')
    return sou[:temp]+blank[:8-len(sou[:temp])]
    
    
def type202(Bytes, posit):
    '''
    Read th type 202 (baseline information).

    Field           type            bytes   Description
    -----           ----            -----   -----------
    Type            ascii           3       202
    Version         ascii           2       0-99 
    Unused          ascii           3       Spaces
    Baseline        ascii           2       Standard baseline ID
    Ref intl_id     ascii           2       International 2-char ID
    Rem intl_id     ascii           2       International 2-char ID
    Ref name        ascii           8       Station names
    Rem name        ascii           8       
    Ref tape        ascii           8       Tape VSNs
    Rem tape        ascii           8       
    Nlags           i*2             2       Number of correlated lags
    Ref xpos        r*8             8       Station X coords (meters)
    Rem xpos        r*8             8       
    Ref ypos        r*8             8       Station Y coords (meters)
    Rem ypos        r*8             8       
    Ref zpos        r*8             8       Station Z coords (meters)
    Rem zpos        r*8             8       
    U               r*8             8       fringes/arcsec E-W at 1GHz at FRT
    V               r*8             8       fringes/arcsec N-S at 1GHz at FRT
    UF              r*8             8       mHz/arcsec/GHz in R.A. at FRT
    VF              r*8             8       mHz/arcsec/GHz in dec. at FRT
    Ref clock       r*4             4       Clock offsets (usec) at FRT
    Rem clock       r*4             4       
    Ref clockrate   r*4             4       Clock rates (sec/sec)
    Rem clockrate   r*4             4       
    Ref idelay      r*4             4       Instrumental delays (usec)
    Rem idelay      r*4             4       
    Ref zatm del.   r*4             4       Zenith atmospheric delay (nsec)
    Rem zatm del.   r*4             4       
    Ref elev        r*4             4       Elevation of source at FRT (deg)
    Rem elev        r*4             4
    Ref az          r*4             4       Azimuth of source at FRT (deg)
    Rem az          r*4             4       
    
    Record length is fixed at 176 bytes.

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    sta1,sta2 : the station name

    '''
    # startP = 288
    # posit = Bytes[startP:].find(b'202')
    # id1 = Bytes[startP+posit+10:startP+posit+12].decode()
    # id2 = Bytes[startP+posit+12:startP+posit+14].decode()
    sta1 = Bytes[posit+14:posit+14+8].decode().replace('\x00',' ')
    sta2 = Bytes[posit+14+8:posit+14+8*2].decode().replace('\x00',' ')
   
    return [sta1,sta2]

def type203(Bytes, posit):
    '''
    Read the type 203 (channel information).
    
    Field           type            bytes   Description
    -----           ----            -----   -----------
    Type            ascii           3       203
    Version         ascii           2       0-99 
    Unused          ascii           3       Spaces
    Channels x 32
        index       i*2             2       Index number in type-1 file (0=empty)
        Sample rate i*2             2       ksamp/sec
        refsb       ascii           1       Ref station sideband (U/L)
        remsb       ascii           1       Rem station sideband (U/L)
        refpol      ascii           1       Ref station polarization (R/L)
        rempol      ascii           1       Rem station polarization
        ref_freq    r*8             8       Ref station LO freq (Hz)
        rem_freq    r*8             8       Rem station LO freq (Hz)
        ref_chan_id ascii           8       Ref station channel id
        rem_chan_id ascii           8       Rem station channel id
        
    Record length is fixed at 1288 bytes.

    Parameters
    ----------
    Bytes : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
            
    # posit = Bytes[64:].find(b'203')+64
            
    version = int(Bytes[posit+3:posit+5].decode())
    
    if version == 0:
        ch = 32
    elif version == 1:
        ch = 8*64
    
    sampleRate = []
    refFreq = []
    for i in range(ch): 
        sampleRate.append(struct.unpack('>H', Bytes[posit+8+40*i+2:posit+8+40*i+4])[0])
        refFreq.append(struct.unpack('>d', Bytes[posit+8+40*i+8:posit+8+40*i+16])[0])
        
    return sampleRate, refFreq

def type205(Bytes, posit):
    version = int(Bytes[posit+3:posit+5].decode())
    
    if version == 0:
        ch = 16
    elif version == 1:
        ch = 64
    else:
        print('    type205 version wrong!')
    
    ffit_chan = []
    for i in range(ch):
        ffit_chan_id = Bytes[posit+120:posit+121].decode()
        
        channel = []
        for j in range(4):
            channel.append(struct.unpack('>h', Bytes[posit+120+10*i+2+2*j:posit+120+10*i+2+2*(j+1)])[0])
            
        ffit_chan.append(channel)
        
    return ffit_chan
    
        
def type206(Bytes, posit):
    '''
    Read the type 206 (data filtering)
    
    Field           type            bytes   Description
    -----           ----            -----   -----------
    Type            ascii           3       206
    Version         ascii           2       0-99 
    Unused          ascii           3       Spaces
    Start           date            12      Time at start of 0th AP
    first_ap        i*2             2       Number of 1st valid AP
    last_ap         i*2             2       Number of last valid AP
    Accepted        i*2 x 2 x 16    64      APs accepted by channel/sband
    Intg time       r*4             4       Effective integration time (secs)
    Accept ratio    r*4             4       % ratio of min/max data accepted
    discard         r*4             4       % of data discarded
    ????????        i*2 x 2 x 16    64      Discards due to reason 1 (?)
    ????????        i*2 x 2 x 16    64      Discards due to reason 2 (?)
    ????????        i*2 x 2 x 16    64      Discards due to reason 3 (?)
    ????????        i*2 x 2 x 16    64      Discards due to reason 4 (?)
    ????????        i*2 x 2 x 16    64      Discards due to reason 5 (?)
    ????????        i*2 x 2 x 16    64      Discards due to reason 6 (?)
    ????????        i*2 x 2 x 16    64      Discards due to reason 7 (?)
    ????????        i*2 x 2 x 16    64      Discards due to reason 8 (?)
    ratesize        i*2             2       Size of fringe rate transform
    MBD size        i*2             2       Size of MBD transform
    SBD size        i*2             2       Size of SBD transform
    Unused2         ascii           6       Padding
    
    Record length is fixed at 556 bytes.

    Parameters
    ----------
    Bytes : TYPE
        the type 2 file bytes.

    Returns
    -------
    None.

    '''
    
    # posit = Bytes.find(b'206')
    
    version = int(Bytes[posit+3:posit+5].decode())
    if version == 0:
        ch = 16
    elif version == 1:
        ch = 16
    elif version == 2:
        ch = 64
    
    apNum = []
    for i in range(ch*2):
        apNum.append(struct.unpack('>h',Bytes[posit+24+2*i:posit+24+2*(i+1)])[0])
    apNum = np.array(apNum).reshape((ch,2))
    
    return apNum[:,[1,0]]
    

def type208(Bytes, posit):
    '''
    Read the type 208 (solution parameter).

    Parameters
    ----------
    Bytes : the type 2 file bytes.

    Returns
    -------
    quality : 

    '''
    
    # posit = Bytes.find(b'208')
    quality = Bytes[posit+8:posit+8+1].decode()
    
    delay = struct.unpack('>d', Bytes[posit+64:posit+72])[0] * 1E-6
    sbdelay = struct.unpack('>d', Bytes[posit+72:posit+80])[0] * 1E-6

    delaySig = struct.unpack('>f', Bytes[posit+100:posit+104])[0] * 1E-6
    sbdelaySig = struct.unpack('>f', Bytes[posit+104:posit+108])[0] * 1E-6
    
    ambig = struct.unpack('>f', Bytes[posit+112:posit+116])[0] * 1E-6
    snr = struct.unpack('>f',Bytes[posit+128:posit+132])[0]
    
    # phase = struct.unpack('>f',Bytes[posit+140:posit+144])[0]*np.pi/180
    # phaseSig = struct.unpack('>f',Bytes[posit+144:posit+148])[0]*np.pi/180

    return [quality,delay,sbdelay,delaySig,sbdelaySig,ambig,snr]

def type210(Bytes, posit):
    '''
    Read the type 210 (channel data)
    
    Field           type            bytes   Description
    -----           ----            -----   -----------
    Type            ascii           3       210
    Version         ascii           2       0-99 
    Unused          ascii           3       Spaces
    Amp-phase       r*4 x 2 x 16    128     Amp/phase by channel resid to model

    Record length is fixed at 134 bytes.

    Parameters
    ----------
    Bytes : byte
        the type2 file bytes.

    Returns
    -------
    None.

    '''
    
    # posit = Bytes.find(b'210')

    version = int(Bytes[posit+3:posit+5].decode())
    if version == 0:
        ch = 16
    elif version == 1:
        ch = 64
        
    ampp = []
    for i in range(2*ch):
        ampp.append(struct.unpack('>f',Bytes[posit+8+4*i:posit+8+4*(i+1)])[0])
        
    ampp = np.array(ampp).reshape((ch,2))
    
    return ampp
        
    