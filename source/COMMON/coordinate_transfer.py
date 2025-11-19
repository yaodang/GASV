#!/usr/bin/env python3

import sys
import numpy as np

from COMMON.constant import *

def cart2phigd(x):
    """
     Calculates geodetic latitude from cartesian coordinates
    ---------------------
    input: 
      x              : cartesian coordinates (x,y,z) [m], 1x3
    output: 
      phigd          : geodetic latitude angle [rad]
    ---------------------
    """
    
    f = 1/300
    e12 = 2*f - f**2
    e22 = e12/(1-e12)
    
    rsp = np.sqrt(x[0]**2+x[1]**2)
    teta = np.arctan2(x[2],rsp*(1-f))
    
    temp1 = x[2] + e22*const.Re*np.sin(teta)**3*(1-f)
    temp2 = rsp - e12*const.Re*np.cos(teta)**3
    
    phigd = np.arctan2(temp1, temp2)
    return phigd

def ell2xyz(ell):
    """
    Transformation from ellipsoidal coordinates lam,phi,elh to
    Cartesian coordinates X,Y,Z.
    ---------------------
    input: 
      ell            : ellipsoidal coordinates, nx3
    output: 
      x              : the Cartesian coordinates of station, nx3
    ---------------------
    """
    f = const.f
    e2 = 2*f - f**2
    N = const.ae/np.sqrt(1-e2*np.sin(ell[1])**2)
    
    x = (N+ell[2])*np.cos(ell[1])*np.cos(ell[0])
    y = (N+ell[2])*np.cos(ell[1])*np.sin(ell[0])
    z = (N*(1-e2)+ell[2])*np.sin(ell[1])
    
    return [x,y,z]

def locsource(lam,phi,rqu,t2c):
    """
    Computes local azimuth, zenith distance.
    ---------------------
    input:
        lam,phi        : station ellipsoidal coordinates [rad]
        t2c            : transfer matrix from TRS to CRS
        rqu            : unit source vector barycentrum-source [m]
    output: 
        az,zd          : local azimuth and zenith distance [rad]
        corz           : correction to zenith distance due to trop. refract. [rad]
        de             : local declination [rad]
        LHAe           : source local hour angle east of the meridian [rad]
    ---------------------
    """ 
    rq_trs = np.dot(t2c.T, rqu)
    rq = rq_trs/np.linalg.norm(rq_trs)
    
    de = np.arctan2(rq[2],np.sqrt(rq[0]**2+rq[1]**2))
    LHAe = np.arctan2(rq[1],rq[0]) - lam
    
    temp = np.array([[1,0,0],[0,-1,0],[0,0,1]])
    tranf = np.dot(np.dot(temp, rotm(np.pi/2-phi,2)),rotm(lam,3))
    lq = np.dot(tranf,rq)
    
    zd = np.arccos(lq[2])
    
    saz = np.arctan2(lq[1],lq[0]) # south azimuth
    if lq[1] < 0:
        saz += 2*np.pi
        
    az = np.mod(saz+np.pi, 2*np.pi) # north azimuth
    
    corz = 313E-6*np.tan(zd)
    if corz > np.pi/2:
        corz = -corz
    
    return az,zd,corz,de,LHAe

def ren2xyz(dren, phi, lam):
    """
    Transformation of a displacement vector at a station (lam,phi) from a
    local coordinate system REN into geocentric system XYZ
    ---------------------
    input: 
      dren           : displacement in the local system REN, nx3
      phi            : latitude of the station     [rad]
      lam            : longitude of the station    [rad]
    output: 
      dxyz           : displacement in the geocentric system XYZ, nx3
    ---------------------
    """        
    
    cp = np.cos(phi)
    sp = np.sin(phi)
    cl = np.cos(lam)
    sl = np.sin(lam)
    
    if dren.ndim == 2:
        dx = cp*cl*dren[:,0] - sl*dren[:,1] - sp*cl*dren[:,2]
        dy = cp*sl*dren[:,0] + cl*dren[:,1] - sp*sl*dren[:,2]
        dz =    sp*dren[:,0] +                cp*dren[:,2]
    else:
        dx = cp*cl*dren[0] - sl*dren[1] - sp*cl*dren[2]
        dy = cp*sl*dren[0] + cl*dren[1] - sp*sl*dren[2]
        dz =    sp*dren[0] +                cp*dren[2]    
    
    return np.array([dx,dy,dz])

def rotm(angle, flag):
    """
    Gives the rotational matrix.
    ---------------------
    input: 
      angle          : the rotational angle
      flag           : which axis to rotate,1-x,2-y,3-z
    output: 
      R              : rotational matrix
    ---------------------
    """
    ca = np.cos(angle)
    sa = np.sin(angle)
    
    R = np.zeros([3,3])
    
    if flag == 1:
        R[0,0] = 1
        R[1,1] = ca
        R[1,2] = sa
        R[2,1] = -sa
        R[2,2] = ca
    elif flag == 2:
        R[0,0] = ca
        R[0,2] = -sa
        R[1,1] = 1
        R[2,0] = sa
        R[2,2] = ca
    elif flag == 3:
        R[0,0] = ca
        R[0,1] = sa
        R[1,0] = -sa
        R[1,1] = ca
        R[2,2] = 1
        
    return R

def xyz2ell(x):
    """
    Transformation from Cartesian coordinates X,Y,Z to ellipsoidal
    coordinates lam,phi,elh.
    ---------------------
    input: 
      x              : the Cartesian coordinates of station, nx3
    output: 
      ell            : ellipsoidal coordinates, nx3
    ---------------------
    """
    f = const.f
    e2 = 2*f - f**2
    
    lon = np.arctan2(x[1],x[0])
    
    lat0 = np.arctan2(x[2],np.sqrt(x[0]**2+x[1]**2))
    N = const.ae/np.sqrt(1-e2*np.sin(lat0)**2)
    lat1 = np.arctan2(x[2]+N*e2*np.sin(lat0), np.sqrt(x[0]**2+x[1]**2))
    
    while abs(lat0-lat1) > 1E-9:
        lat0 = lat1
        N = const.ae/np.sqrt(1-e2*np.sin(lat0)**2)
        lat1 = np.arctan2(x[2]+N*e2*np.sin(lat0), np.sqrt(x[0]**2+x[1]**2))
    
    lat = lat1
    N = const.ae/np.sqrt(1-e2*np.sin(lat)**2)
    h = np.sqrt(x[0]**2+x[1]**2)/np.cos(lat) - N
    
    return [lon, lat, h]

def xyz2ren(x, phi, lam):
    '''
    Transformation from Cartesian coordinates X,Y,Z to REN

    Parameters
    ----------
    x : array(1*3)
        Cartesian coordinates.
    phi : float
        DESCRIPTION.
    lam : float
        DESCRIPTION.

    Returns
    -------
    ren : array
        DESCRIPTION.

    '''
    
    rot = np.array([[np.cos(phi)*np.cos(lam), -np.sin(lam), -np.sin(phi)*np.cos(lam)],\
                    [np.cos(phi)*np.sin(lam),  np.cos(lam), -np.sin(phi)*np.sin(lam)],\
                    [np.sin(phi)            ,            0, np.cos(phi)             ]])
    
    ren = np.linalg.inv(rot)@x.T
    
    return ren

'''
lam = -2.786678495303264
phi = 0.386179303324234
rqu = np.array([0.343866000648711,-0.582732623386430,0.736327964548150])
t2c = np.array([[  -0.672851472655050,  -0.739774797310116,   0.002035929936796],\
                [   0.739776341558968,  -0.672852854942444,   0.000008089049053],\
                [   0.001363897195813,   0.001511575528881,   0.999997927459782]])
az,zd,corz,de,LHAe = locsource(lam,phi,rqu,t2c)
print(az*180/np.pi,zd*180/np.pi)
#R = rotm(np.pi/3, 3)
#'''
