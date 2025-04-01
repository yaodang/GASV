#!/usr/bin/env python3

from jplephem.spk import SPK
import numpy as np
import sys
sys.path.append("..//")

from MOD import *
from COMMON import *


def read_eph(filename, MJD):
    """
    Read the ephem file, the unit is km from ephem file
    ---------------------
    input: 
        filename    : the ephem file name
        MJD         : the observe MJD
    output: 
        ephem       : the class type
    ---------------------
    """
    deg2rad = np.pi/180
    
    data = SPK.open(filename)
    
    T = calc_T(MJD)
    
    temp = (357.528 + 35999.05 * T) * deg2rad
    TDB = 2451545.0 + T*36525 + (0.001658*np.sin(temp+0.0167*np.sin(temp)))/86400
    
    #----------------------------------------------------------------------
    #Earth
    em = PLANET()
    posit,vel = data[0,3].compute_and_differentiate(TDB)
    em.get_xv_bar(posit*1E3,vel*1E3/86400)
    
    posit_e,vel_e = data[3,399].compute_and_differentiate(TDB) #earth-moon system Barycenter to earth
    posit_m,vel_m = data[3,301].compute_and_differentiate(TDB) #earth-moon system Barycenter to moon
    
    #earth
    earth = PLANET()
    moon = PLANET()
    
    earth.get_xv_bar(em.xbar+posit_e*1E3,em.vbar+vel_e*1E3/86400)
    moon.get_xv_bar(em.xbar+posit_m*1E3,em.vbar+vel_m*1E3/86400)
    moon.get_xv_geo((posit_m-posit_e)*1E3,(vel_m-vel_e)*1E3/86400)
    
    ae = accEarth(TDB,data)
    earth.get_acc_bar(ae)
    #---------------------------------------------------------------
    
    #Mercury
    merc = PLANET()
    posit,vel = data[0,1].compute_and_differentiate(TDB)
    merc.get_xv_bar(posit*1E3,vel*1E3/86400)
    merc.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    #Venus
    venu = PLANET()
    posit,vel = data[0,2].compute_and_differentiate(TDB)
    venu.get_xv_bar(posit*1E3,vel*1E3/86400)
    venu.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)

    
    #Mars
    mars = PLANET()
    posit,vel = data[0,4].compute_and_differentiate(TDB)
    mars.get_xv_bar(posit*1E3,vel*1E3/86400)
    mars.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    #Jupiter
    jupi = PLANET()
    posit,vel = data[0,5].compute_and_differentiate(TDB)
    jupi.get_xv_bar(posit*1E3,vel*1E3/86400)
    jupi.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    #Saturn
    satu = PLANET()
    posit,vel = data[0,6].compute_and_differentiate(TDB)
    satu.get_xv_bar(posit*1E3,vel*1E3/86400)
    satu.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    #Uranus
    uran = PLANET()
    posit,vel = data[0,7].compute_and_differentiate(TDB)
    uran.get_xv_bar(posit*1E3,vel*1E3/86400)
    uran.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    #Neptune
    nept = PLANET()
    posit,vel = data[0,8].compute_and_differentiate(TDB)
    nept.get_xv_bar(posit*1E3,vel*1E3/86400)
    nept.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    #plut
    plut = PLANET()
    posit,vel = data[0,9].compute_and_differentiate(TDB)
    plut.get_xv_bar(posit*1E3,vel*1E3/86400)
    plut.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    #sun
    sun = PLANET()
    posit,vel = data[0,10].compute_and_differentiate(TDB)
    sun.get_xv_bar(posit*1E3,vel*1E3/86400)
    sun.get_xv_geo(posit*1E3-earth.xbar,vel*1E3/86400-earth.vbar)
    
    
    ephem = EPHEM(merc, venu, em, mars, jupi, satu, uran, nept, plut, sun, earth, moon)
    return ephem
    
def accEarth(TDB,data):
    """
    Get the acceleration by  velocity 1 second before and 1 second later

    Parameters
    ----------
    TDB : .
    data : DE421 data.

    Returns
    -------
    ae : the barycentric earth acceleration (m/s**2).
    """

    tminus1 = TDB - 1.0/86400
    tplus1 = TDB + 1.0/86400
    
    pm,vm = data[0,3].compute_and_differentiate(tminus1)
    pp,vp = data[0,3].compute_and_differentiate(tplus1)
    
    p_em,v_em = data[3,399].compute_and_differentiate(tminus1)
    p_ep,v_ep = data[3,399].compute_and_differentiate(tplus1)
    
    vem = vm + v_em
    vep = vp + v_ep
    
    ae = (vep*1E3/86400-vem*1E3/86400)/2   # acceleration
    
    return ae

    
