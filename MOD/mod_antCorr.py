#!/usr/bin/env python3

import sys
import numpy as np
from scipy.interpolate import splrep, splev

from COMMON import *

def antCorr(phi, az, zd, corz, de, LHAe, zdry, stationInfo, staP, staTemp):
    """
    Get the axis offset, thermal deformation and gravity deformation correct for each antenna.
    ---------------------
    input:
        phi            : 
        az             : azimuth [rad]
        zd             : zenith distance [rad]
        corz           : correction to zenith distance due to trop. refract. [rad]
        de             : 
        LHAe           : source local hour angle east of the meridian [rad]
        zdry           : apriori zenith delay
        stationInfo    : station struct
        staP           : the station position in stationInfo
        staTemp        : the temperature of station
    output: 
        axCor          : axis offset delay [s]
        thermalCor     : thermal deformation delay [s]
        gravCor        : gravity deformation delay [s]
    ---------------------
    """ 
       
    caz = np.cos(az)
    saz = np.sin(az)
    sz = np.sin(zd-corz)
    cz = np.cos(zd-corz)
    se = np.sin(np.pi/2-(zd-corz))
    ce = np.cos(np.pi/2-(zd-corz))
    cd = np.cos(de)
    
    
    #staTemp = scanInfo.scanT[iscan][istat]
    axtype = stationInfo.axtype[staP]
    offset = stationInfo.axoffset[staP]
    phigd = cart2phigd(stationInfo.posit[staP])
    
    
    thermpar = stationInfo.thermpar[staP]
    focus = stationInfo.foctype[staP]
    
    # thermal deformation parameter
    if focus == 'FO_PRIM':
        focfac = 0.9
    else:
        focfac = 1.8
        
    axCor,daxCor,aoalt = axisCorr(axtype, offset, phi, az, caz, cz, saz, sz, se, ce, phigd, LHAe, zdry)
    thermCor = thermdefCorr(caz,saz,cz,sz,cd,axtype,offset,staTemp,focfac,thermpar,staTemp)
    gravCor = gravdefCorr(stationInfo,staP,staTemp,zd)
    
    return axCor,aoalt, daxCor, thermCor, gravCor

def axisCorr(axtype,offset,phi,az,caz,cz,saz,sz,se,ce,phigd,LHAe,zdry):
    """
    Get the axis offset correct for each antenna.
    ---------------------
    input:
        axtype         : the axis type
        offset         : the axis offset
        corz           : correction to zenith distance due to trop. refract. [rad]
        phi            : 
        caz            :
        saz            : 
        sz             : 
        LHAe           : source local hour angle east of the meridian [rad]
        zdry           : apriori zenith delay
    output: 
        axkt           : axis offset delay [s]
        daxkt          : the partial derivative of axis offset [s/m]
        aoalt          : Antenna axis offset altitude correction [m]
    ---------------------
    """ 
    DTSH = 8600 # [m] ~8.6km Dry Troposphere Scale Height
    if axtype == 'none':
        axkt = 0
        daxkt = 0
        psifac = 0
    else:
        if axtype == 'AZEL':
            axkt = -(offset*sz)/const.c
            daxkt = -sz
            
            psifac = 0
        elif axtype == 'EQUA':
            csx = sz*caz*np.cos(phi) + cz*np.sin(phi)
            sn = np.arccos(csx)
            snx = np.sin(sn)
            
            axkt = -(offset*snx)/const.c
            daxkt = -snx
            
            psifac = np.cos(phigd)*np.cos(LHAe)
        elif axtype == 'X-Y1' or axtype == 'X-YN' or axtype == 'XYNO':
            axkt = -(offset*np.sqrt(1-(sz*caz)**2))/const.c
            daxkt = -np.sqrt(1-(sz*caz)**2)
            psifac = se/np.sqrt(1-(caz*ce)**2)
        elif axtype == 'X-Y2' or axtype == 'X-YE' or axtype == 'XYEA':
            axkt = -(offset*np.sqrt(1-(sz*saz)**2))/const.c
            daxkt = -np.sqrt(1-(sz*saz)**2)
            psifac = se/np.sqrt(1-(saz*ce)**2)
            
        elif axtype == 'RICH':
            axkt = -(offset*np.sqrt(1-(cz*np.sin(0.6817256)+sz*np.cos(0.6817256)*
                                       (caz*np.cos(0.0020944)-saz*np.sin(0.0020944)))**2))/const.c
            daxkt = -np.sqrt(1-(cz*np.sin(0.6817256)+sz*np.cos(0.6817256)*
                                       (caz*np.cos(0.0020944)-saz*np.sin(0.0020944)))**2)
        
            E = 0.12/180*np.pi
            phiW = 39.06/180*np.pi
            LHA_Rich = np.arctan2(ce*np.sin(az-E),np.cos(phiW)*se-np.sin(phiW)*ce*np.cos(az+E))
            psifac = np.cos(phiW)*np.cos(LHA_Rich)
        else:
            axkt = 0
            daxkt = 0
            psifac = 0
    
    # Antenna axis offset altitude correction
    aoalt = -zdry*(axkt*const.c/DTSH)*psifac  #[m]
    
    return axkt,daxkt/const.c,aoalt

def gravdefCorr(stationInfo,p_sta,temperature,zd):
    '''
    output:
        gravCor          : gravitational deformation [s]
    '''
    if len(stationInfo.gravpar[p_sta]) == 1:
        gravCor = 0
    else:
        cubicSpline = splrep(stationInfo.gravpar[p_sta][:, 0], stationInfo.gravpar[p_sta][:, 1])
        gravCor = splev((np.pi/2 - zd) * 180 / np.pi, cubicSpline)
        if stationInfo.stationName[p_sta] == 'ONSALA60':
            delay = (temperature - 19) * 0.47 * 1E-3  # [mm]
            gravCor += delay  # [mm]

    return gravCor*1E-3/const.c
def thermdefCorr(caz,saz,cz,sz,cd,axtype,offset,temp,focfac,thermpar,staTemp):
    """
    Get the thermal deformation for each antenna.
    ---------------------
    input:
        phi            : 
        az             : azimuth [rad]
        zd             : zenith distance [rad]
        corz           : correction to zenith distance due to trop. refract. [rad]
        LHAe           : source local hour angle east of the meridian [rad]
        zdry           : apriori zenith delay
        iscan          : the number of scan
        istat          : index of station
        stationInfo    : station struct
        scanInfo       : scan struct
    output: 
        axkt           : axis offset delay [s]
        daxkt          : axis offset partial
        aoalt          : altitude correction [m]
    ---------------------
    """ 
    ref_temp = thermpar[0]       # Reference temperature (degree C)
    hf       = thermpar[1]       # Height of foundation (m)
    hd       = thermpar[2]       # Depth of foundation (m)
    gf       = thermpar[3]       # Foundation thermal expansion coefficient (1/K)
    hp       = thermpar[4]       # Length of the fixed axis (m)
    ga       = thermpar[5]       # Fixed axis thermal expansion coefficient (1/K)
    hv       = thermpar[6]       # Distance from the movable axis to the antenna vertex (m)
    hs       = thermpar[7]       # Height of the sub-reflector above the vertex (m)
    
    

    if ref_temp != 999:
        temp0 = ref_temp
    else:
        temp0 = staTemp
        
    if temp == -999:
        temp = temp0
        
    if axtype == 'NONE':
        thermCor = 0
    elif axtype =='AZEL':
        thermCor = (gf*(temp-temp0)*hf*cz + \
                    ga*(temp-temp0)*(hp*cz+hv-focfac*hs))/const.c + \
                   ga*(temp-temp0)*offset*sz/const.c
    elif axtype == 'EQUA':
        thermCor = (gf*(temp-temp0)*hf*cz + \
                    ga*(temp-temp0)*(hp*cz+hv-focfac*hs+hd*cd))/const.c + \
                   ga*(temp-temp0)*offset*cd/const.c
    elif axtype == 'X-Y1' or axtype == 'X-YN' or axtype == 'XYNO':
        thermCor = (gf*(temp-temp0)*hf*cz + \
                    ga*(temp-temp0)*(hp*cz+hv-focfac*hs))/const.c + \
                   ga*(temp-temp0)*offset*np.sqrt(1-(sz*caz)**2)/const.c
    elif axtype == 'X-Y2' or axtype == 'X-YE' or axtype == 'XYEA':
        thermCor = (gf*(temp-temp0)*hf*cz + \
                    ga*(temp-temp0)*(hp*cz+hv-focfac*hs))/const.c + \
                   ga*(temp-temp0)*offset*np.sqrt(1-(sz*saz)**2)/const.c
    elif axtype == 'RICH':
        thermCor = (gf*(temp-temp0)*hf*cz + \
                    ga*(temp-temp0)*(hp*cz+hv-focfac*hs))/const.c + \
                   ga*(temp-temp0)*offset*np.sqrt(1-(cz*np.sin(0.6817256)+\
                                                     sz*np.cos(0.6817256)*(caz*np.cos(0.0020944)-\
                                                                           saz*np.sin(0.0020944)))**2)/const.c
    else:
        thermCor = 0
        
    return thermCor
