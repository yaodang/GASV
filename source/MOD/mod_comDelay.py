#!/usr/bin/env python3

import sys
import numpy as np

from COMMON import *

def comDelay(iscan, crsSta1, crsSta2, idSta1, idSta2, ephem, rqu, v1, v2):
    """
    Calculates time delay following the consensus model
    ---------------------
    input:
        iscan          : number of scan
        crsSta1,crsSta2: CRS coordiantes of station
        idSta1,idSta2  : index of station
        rqu            : unit source vector barycentrum-source [m]
        ephem          : ephemerides
        v1,v2          : velocity of station
    output: 
        com_delay      : compute delay
    ---------------------
    """ 
    crsB = crsSta2 - crsSta1
    earth = ephem.earth.xbar[:,iscan]
    vearth = ephem.earth.vbar[:,iscan]
    sun = ephem.sun.xgeo[:,iscan]
    
    xb1 = earth + crsSta1
    xb2 = earth + crsSta2
    
    Tgrav = grav_delay(iscan,xb1,xb2,vearth,crsB,rqu,ephem)
    # gravitational delay due to the earth
    Tgrav = Tgrav + 2*const.gme/const.c**3 * np.log((np.linalg.norm(crsSta1) + rqu@crsSta1)/ \
                                                    (np.linalg.norm(crsSta2) + rqu@crsSta2))
    
    U = const.gms / np.linalg.norm(sun)
    gamma = 1
    fac1 = rqu@crsB/const.c
    term1 = 1-(1+gamma)*U/const.c**2-(np.linalg.norm(vearth))**2/(2*const.c**2)-vearth@v2/const.c**2
    fac2 = vearth@crsB/const.c**2
    term2 = 1+rqu@vearth/(2*const.c)
    quot = 1+rqu@(vearth+v2)/const.c

    com_delay = (Tgrav - fac1*term1 - fac2*term2)/quot
    
    return com_delay
    
def grav_delay(iscan,xb1,xb2,vearth,crsB,rqu,ephem):
    """
    Calculates the gravitational delay due to celestial bodies
    ---------------------
    input:
        iscan          : number of scan
        xb1,xb2        : barycentric station vector [m]
        vearth         : barycentric earth velocity
        crsB           : baseline GCRS
        rqu            : unit source vector barycentrum-source [m]
        ephem          : ephemerides 
    output: 
        Tgrav          : gravitaional delay
    ---------------------
    """
    
    Tgrav = 0
    for i in range(10):
        if i == 0:
            xbody_bar = ephem.sun.xbar[:,iscan]
            vbody_bar = ephem.sun.vbar[:,iscan]
            gg = const.gms
        if i == 1:
            xbody_bar = ephem.moon.xbar[:,iscan]
            vbody_bar = ephem.moon.vbar[:,iscan]
            gg = const.gmm
        if i == 2:
            xbody_bar = ephem.merc.xbar[:,iscan]
            vbody_bar = ephem.merc.vbar[:,iscan]
            gg = const.gmmerc
        if i == 3:
            xbody_bar = ephem.venu.xbar[:,iscan]
            vbody_bar = ephem.venu.vbar[:,iscan]
            gg = const.gmvenu  
        if i == 4:
            xbody_bar = ephem.mars.xbar[:,iscan]
            vbody_bar = ephem.mars.vbar[:,iscan]
            gg = const.gmmars
        if i == 5:
            xbody_bar = ephem.jupi.xbar[:,iscan]
            vbody_bar = ephem.jupi.vbar[:,iscan]
            gg = const.gmjupi
        if i == 6:
            xbody_bar = ephem.satu.xbar[:,iscan]
            vbody_bar = ephem.satu.vbar[:,iscan]
            gg = const.gmsatu
        if i == 7:
            xbody_bar = ephem.uran.xbar[:,iscan]
            vbody_bar = ephem.uran.vbar[:,iscan]
            gg = const.gmuran
        if i == 8:
            xbody_bar = ephem.nept.xbar[:,iscan]
            vbody_bar = ephem.nept.vbar[:,iscan]
            gg = const.gmnept
        if i == 9:
            xbody_bar = ephem.plut.xbar[:,iscan]
            vbody_bar = ephem.plut.vbar[:,iscan]
            gg = const.gmplut
            
        #time of closest approach
        dt = np.linalg.norm(xbody_bar - xb1)/const.c
        xbody = xbody_bar - dt*vbody_bar
        dt = np.linalg.norm(xbody - xb1)/const.c
        xbody = xbody_bar - dt*vbody_bar   
        dt = np.linalg.norm(xbody - xb1)/const.c
        xbody = xbody_bar - dt*vbody_bar
        
        R1b = xb1 - xbody
        R2b = xb2 - vearth/const.c*(rqu@crsB) - xbody
        gamma = 1
        Tgrav = Tgrav + (1+gamma)*gg/const.c**3 * np.log((np.linalg.norm(R1b) + rqu@R1b)/\
                                                         (np.linalg.norm(R2b) + rqu@R2b))
        
    return Tgrav
