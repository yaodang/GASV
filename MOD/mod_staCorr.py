#!/usr/bin/env python3

import sys,bisect
import numpy as np
np.set_printoptions(precision=15)

from MOD.mod_trp import GPT3
from MOD.mod_trp import GPT
from MOD import *

class STASCAN():
    def __init__(self):
        self.id = -1
        self.trs = []
        self.crs = []
        self.staObs = []
        self.vgeo = []
        self.mpf = []

def staPositCorr(args):
    t2c, rqu, moonxgeo, sunxgeo, earthvbar, scanMJD, scanTime, p_sta, eopXP, eopYP, stationInfo, \
        creatv2Flag, scanPress, scanTemp, GPT3Data= \
        args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args[9],args[10],\
            args[11],args[12],args[13],args[14]
    
    
    staScan = STASCAN()
    staScan.id = p_sta
    
    for i in range(len(scanMJD)):
        mjd = scanMJD[i]
        xp = eopXP[i]
        yp = eopYP[i]
        date = scanTime[i]
        doy = date2doy(int(date[0]), int(date[1]), int(date[2]))
        tim = [date[0], doy, date[3], date[4], date[5]]
        
        moon_xgeo = moonxgeo[:,i]
        sun_xgeo = sunxgeo[:,i]
        vearth = earthvbar[:,i]
        
        sta_xgeo = stationInfo.posit[p_sta]
        lam,phi,hell = stationInfo.ell[p_sta]
        
        psd_phi = cart2phigd(sta_xgeo)
        psd_lam = np.arctan2(sta_xgeo[1],sta_xgeo[0])
        
        cts = soild_tidal_corr(mjd, t2c[i], sta_xgeo, moon_xgeo, sun_xgeo)
        cto = ocean_tidal_corr(mjd, stationInfo.cto[p_sta], lam, phi)
        ctp = pole_tidal(tim, lam, phi, xp, yp, stationInfo.opp[p_sta])
        # print(p_sta,stationInfo.opp[p_sta])
        cta = atmosphere_tidal_corr(mjd, lam, phi, stationInfo.ap[p_sta])
        
        cpsd = [0,0,0]
        if stationInfo.psdFlag[p_sta] > 0:
            cpsd = psd_corr(mjd, stationInfo.psd[p_sta], psd_phi, psd_lam)
            # print(cpsd)            
        
        # if p_sta == 1 and i == 0:
            # print(cts,cto,ctp,ctop)
        p_corr = cts + cto + ctp + cta + cpsd
        # p_corr = 0
        
        t_obs = (mjd - stationInfo.epoch[p_sta])/365.25
        sta_xgeo = sta_xgeo + stationInfo.vel[p_sta]*t_obs
        
        sta_trs = sta_xgeo + p_corr
        sta_crs = np.dot(t2c[i], sta_trs)
        
        # velocity of station
        v = np.dot(t2c[i], np.array([-const.omega*sta_trs[1], const.omega*sta_trs[0], 0]))
        
        # aberrated source vector
        ka = rqu[i] + (vearth + v)/const.c - np.dot(rqu[i],np.dot(rqu[i],vearth+v))/const.c
        
        # the station information after correct
        lam, phi, hell = xyz2ell(sta_trs.tolist())
        az,zd,corz,de,LHAe = locsource(lam, phi, ka, t2c[i])
        
        # apriori zenith delay
        if creatv2Flag != 'CREATE':
            press = scanPress[i]
            if press == -999:
                press, temperature = GPT(scanMJD[i], phi, lam, hell)
                
            if scanTemp[i] != -999:
                temperature = scanTemp[i]
        else:
                press, temperature = GPT(scanMJD[i], phi, lam, hell)
                
        zdry = 0.0022768*press / (1-0.00266*np.cos(2*phi)-(0.28e-6*hell))
        zwet = 0
        
        # axis offset correct
        axCor, aoalt, daxCor, thermCor, gravCor = antCorr(phi, az, zd, corz, de, LHAe, zdry, stationInfo, p_sta, temperature)
        
        # GPT3 mapping function for dry, wet, and gradient
        mfh,mfw = GPT3(scanMJD[i],phi,lam,hell,0,GPT3Data,zd)

        ell = np.pi / 2 - zd
        mge = np.sin(az) / (np.tan(ell) * np.sin(ell) + 0.0032)
        mgn = np.cos(az) / (np.tan(ell) * np.sin(ell) + 0.0032)
        
        trp = ((zdry+aoalt)*mfh+zwet*mfw)/const.c
        
        staScan.trs.append(sta_trs)
        staScan.crs.append(sta_crs)
        staScan.staObs.append([lam,phi,hell,az,zd,axCor,daxCor,trp,thermCor,gravCor])
        staScan.vgeo.append(v)
        staScan.mpf.append([mfh,mfw,mge,mgn])
        
        
    return staScan

def axisCorrect(phi,az,zd,corz,axtype,axoffset):
    """
    Corrections to the delay due to axis offset
    ---------------------
    input: 
      mjd            : Modify Journal Date
      az             : azimuth [rad]
      zd             : zenith distance [rad]
      corz           : correction to zenith distance due to trop. refract. [rad]
      axtype         : type of the axis ['char']
      axoffset       : axis offset of the antenna [m]
    output: 
      axCor          : correction due to axis offset [s]
    ---------------------
    """
    caz = np.cos(az)
    saz = np.sin(az)
    sz = np.sin(zd-corz)
    cz = np.cos(zd-corz)
    
    if axtype == 'AZEL':
        axCor = -(axoffset*sz)/const.c
        daxCor = -sz
    elif axtype == 'EQUA':
        csx = sz*caz*np.cos(phi) + cz*np.sin(phi)
        sn = np.arccos(csx)
        snx = np.sin(sn)
        axCor = -axoffset*snx/const.c
        daxCor = -snx
    elif axtype == 'X-Y1' or axtype == 'X-YN' or axtype == 'XYNO':
        axCor = -(axoffset*np.sqrt(1-(sz*caz)**2))/const.c
        daxCor = -np.sqrt(1-(sz*caz)**2)
    elif axtype == 'X-Y2' or axtype == 'X-YE' or axtype == 'XYEA':
        axCor = -(axoffset*np.sqrt(1-(sz*saz)**2))/const.c
        daxCor = -np.sqrt(1-(sz*saz)**2)
    elif axtype == 'RICH':
        axCor = -(axoffset*np.sqrt(1-(cz*np.sin(0.6817256) \
                  + sz*np.cos(0.6817256)*(caz*np.cos(0.0020944)-saz*np.sin(0.0020944)))**2))/const.c
        daxCor = -np.sqrt(1-(cz*np.sin(0.6817256) \
                  + sz*np.cos(0.6817256)*(caz*np.cos(0.0020944)-saz*np.sin(0.0020944)))**2)
    elif axtype == 'NONE':
        axCor = 0
        daxCor = 0
        
    return axCor     

def soild_tidal_corr(mjd, t2c, sta_xgeo, moon_xgeo, sun_xgeo):
    """
    Soild tidal station correction
    ---------------------
    input: 
      mjd            : Modify Journal Date
      t2c            : TRF transfer to CRF
      sta_xgeo       : the station position in GTRF
      moon_xgeo      : the sun position in GTRF
      sun_xgeo       : the sun position in GTRF
    output: 
      cts            : soild tidal correction
    ---------------------
    """
    
    moon_xcrf = np.dot(t2c.T, moon_xgeo)
    sun_xcrf = np.dot(t2c.T, sun_xgeo)
    
    
    azm,elm,lm,Rum = get_unit_vector(moon_xcrf)
    azs,els,ls,Rus = get_unit_vector(sun_xcrf)
    lat,phi,lsta,Rusta = get_unit_vector(sta_xgeo)
    
    #---------------------in-phase:2 degree-----------------------------
    h_0 = 0.6078
    h_2 = -0.0006
    l_0 = 0.0847
    l_2 = 0.0002
    
    h2 = h_0 + h_2*(3*np.sin(phi)**2-1)/2
    l2 = l_0 + l_2*(3*np.sin(phi)**2-1)/2
    
    dotm = np.dot(Rum, Rusta)
    dots = np.dot(Rus, Rusta)
    
    #degree 2 coefficient: GMj*Re**4/(GMe*Rj**3
    c2m = const.MRm * const.Re**4 / lm**3
    c2s = const.MRs * const.Re**4 / ls**3
    
    #IERS2010 eq7.5
    corr_2_degree = c2m * (h2 * Rusta*(3*dotm**2-1)/2 + 3*l2*dotm*(Rum-dotm*Rusta)) + \
                    c2s * (h2 * Rusta*(3*dots**2-1)/2 + 3*l2*dots*(Rus-dots*Rusta))
    
    #---------------------in-phase:3 degree-----------------------------
    h3 = 0.292
    l3 = 0.015
    
    c3m = const.MRm * const.Re**5 / lm**4
    c3s = const.MRs * const.Re**5 / ls**4
    
    #IERS2010 eq7.6
    corr_3_degree = c3m * (h3 * Rusta*(2.5*dotm**3-1.5*dotm) + l3*(7.5*dotm**2-1.5)*(Rum-dotm*Rusta)) + \
                    c3s * (h3 * Rusta*(2.5*dots**3-1.5*dots) + l3*(7.5*dots**2-1.5)*(Rus-dots*Rusta))

    #---------------------out of phase: diurnal-----------------------------
    hi_d = -0.0025
    li_d = -0.0007
    r = np.array([1,0,0])
    e = np.array([0,1,0])
    n = np.array([0,0,1])
    
    #IERS2010 eq7.10
    corr_diurnal_r = -3/4*hi_d*c2m*np.sin(2*elm)*np.sin(2*phi)*np.sin(lat-azm) + \
                     -3/4*hi_d*c2s*np.sin(2*els)*np.sin(2*phi)*np.sin(lat-azs) 
                     
    corr_diurnal_t = -3/2*li_d*c2m*np.sin(2*elm)*(np.cos(2*phi)*np.sin(lat-azm)*n+np.sin(phi)*np.cos(lat-azm)*e) + \
                     -3/2*li_d*c2s*np.sin(2*els)*(np.cos(2*phi)*np.sin(lat-azs)*n+np.sin(phi)*np.cos(lat-azs)*e)
    
    corr_diurnal = corr_diurnal_r*r + corr_diurnal_t            
    
    #---------------------out of phase: semidiurnal-----------------------------
    hi_s = -0.0022
    li_s = -0.0007
    
    #IERS2010 eq7.11                 
    corr_semid_r =   -3/4*hi_s*c2m*np.cos(elm)**2*np.cos(phi)**2*np.sin(2*(lat-azm)) + \
                     -3/4*hi_s*c2s*np.cos(els)**2*np.cos(phi)**2*np.sin(2*(lat-azs))
                     
    corr_semid_t =   3/4*li_s*c2m*np.cos(elm)**2*(np.sin(2*phi)*np.sin(2*(lat-azm))*n-2*np.cos(phi)*np.cos(2*(lat-azm))*e) + \
                     3/4*li_s*c2s*np.cos(els)**2*(np.sin(2*phi)*np.sin(2*(lat-azs))*n-2*np.cos(phi)*np.cos(2*(lat-azs))*e)
                     
    corr_semid = corr_semid_r*r + corr_semid_t
                     
    #---------------------contribution: diurnal-----------------------------
    l_1 = 0.0012
    
    P21m = 3 * np.cos(elm) * np.sin(elm)
    P21s = 3 * np.cos(els) * np.sin(els)
    
    #IERS2010 eq7.8
    corr_con_diur = -l_1*np.sin(phi)*c2m*P21m*(np.sin(phi)*np.cos(lat-azm)*n-np.cos(2*phi)*np.sin(lat-azm)*e) + \
                      -l_1*np.sin(phi)*c2s*P21s*(np.sin(phi)*np.cos(lat-azs)*n-np.cos(2*phi)*np.sin(lat-azs)*e)
                      
    #---------------------contribution: semidiurnal-----------------------------
    l_1 = 0.0024
    
    P22m = 3 * np.cos(elm)**2
    P22s = 3 * np.cos(els)**2
    
    #IERS2010 eq7.9
    corr_con_semi = -1/2*l_1*np.sin(phi)*np.cos(phi)*c2m*P22m*(np.cos(2*(lat-azm))*n+np.sin(phi)*np.sin(2*(lat-azm))*e) + \
                      -1/2*l_1*np.sin(phi)*np.cos(phi)*c2s*P22s*(np.cos(2*(lat-azs))*n+np.sin(phi)*np.sin(2*(lat-azs))*e)
                      
                      
    #--------------------Corrections to be computed in the frequency domain------               
    TAB = np.array([[1, 3, 5, 6, 5, 5, -0.08,  0.00, -0.01,  0.01],\
                    [1, 4, 5, 5, 4, 5, -0.10,  0.00,  0.00,  0.00],\
                    [1, 4, 5, 5, 5, 5, -0.51,  0.00, -0.02,  0.03],\
                    [1, 5, 5, 6, 5, 5,  0.06,  0.00,  0.00,  0.00],\
                    [1, 6, 2, 5, 5, 6, -0.06,  0.00,  0.00,  0.00],\
                    [1, 6, 3, 5, 5, 5, -1.23, -0.07,  0.06,  0.01],\
                    [1, 6, 5, 5, 4, 5, -0.22,  0.01,  0.01,  0.00],\
                    [1, 6, 5, 5, 5, 5, 12.00, -0.78, -0.67, -0.03],\
                    [1, 6, 5, 5, 6, 5,  1.73, -0.12, -0.10,  0.00],\
                    [1, 6, 6, 5, 5, 4, -0.50, -0.01,  0.03,  0.00],\
                    [1, 6, 7, 5, 5, 5, -0.11, -0.11,  0.01,  0.00]])
    
    s,tau,h,p,zns,ps = doodarg(mjd)
    thetaf = TAB[:,0]*tau + (TAB[:,1]-5)*s + (TAB[:,2]-5)*h + (TAB[:,3]-5)*p + \
             (TAB[:,4]-5)*zns + (TAB[:,5]-5)*ps
    thetaf = thetaf*np.pi/180   #rad
    
    #IERS2010 eq7.12
    corr_freq_r = np.sum((TAB[:,6]*np.sin(thetaf+lat) + TAB[:,7]*np.cos(thetaf+lat))*np.sin(2*phi)*1E-3)*r #m
    corr_freq_t = np.sum((TAB[:,8]*np.cos(thetaf+lat) - TAB[:,9]*np.sin(thetaf+lat))*np.sin(phi)*1E-3)*e + \
                  np.sum((TAB[:,8]*np.sin(thetaf+lat) + TAB[:,9]*np.cos(thetaf+lat))*np.cos(2*phi)*1E-3)*n
    corr_freq = corr_freq_r + corr_freq_t
                  
                  
    TAB1 = np.array([[5, 5, 5, 6, 5,  0.47,  0.16,  0.23,  0.07],\
                     [5, 7, 5, 5, 5, -0.20, -0.11, -0.12, -0.05],\
                     [6, 5, 4, 5, 5, -0.11, -0.09, -0.08, -0.04],\
                     [7, 5, 5, 5, 5, -0.13, -0.15, -0.11, -0.07],\
                     [7, 5, 5, 6, 5, -0.05, -0.06, -0.05, -0.03]])
    thetafl = (TAB1[:,0]-5)*s + (TAB1[:,1]-5)*h + (TAB1[:,2]-5)*p + (TAB1[:,3]-5)*zns + \
              (TAB1[:,4]-5)*ps
    thetafl = thetafl*np.pi/180   #rad         
    
    #IERS2010 eq7.13
    corr_long_r = np.sum((3/2*np.sin(phi)**2-1/2)*(TAB1[:,5]*np.cos(thetafl) + TAB1[:,6]*np.sin(thetafl))*1E-3)*r #m
    corr_long_t = np.sum((TAB1[:,7]*np.cos(thetafl) + TAB1[:,8]*np.sin(thetafl))*np.sin(2*phi))*1E-3*n #m
    corr_long = corr_long_r + corr_long_t
    
    phigd = cart2phigd(sta_xgeo)
    phi_n = np.ones(6) * phigd
    lat_n = np.ones(6) * lat
    
    ren = np.vstack((corr_diurnal,corr_semid,corr_con_diur,corr_con_semi,corr_freq,corr_long))
    corr_ren = ren2xyz(ren,phi_n,lat_n)
    
    cts = np.sum(corr_ren,1)+corr_3_degree+corr_2_degree
    
    return cts


def pole_tidal(tim, lam, phi, xp, yp, opp):
    """
    Pole tidal station correction
    ---------------------
    input:
      tim            : [Year,Doy,Hour,Minute,Second]
      lam,phi        : the station ellipsoial position
      xp,yp          : Pole motion parameter
      opp            : ocean pole load tide coefficients from Desai (2002)
    output: 
      ctp            : station correction of pole tidal and ocean pole tidal, [m]
    ---------------------
    """
    clt = np.pi/2 - phi
    
    IFAC = 365
    if np.mod(tim[0],4) == 0:
        IFAC = 366
        
    t = tim[0] + (tim[1]+tim[2]/23.93447+tim[3]/1440+tim[4]/86400)/(IFAC+0.2422)
    
    xpm,ypm = meanPole(t)
    
    m1 =   xp*3600*180/np.pi - xpm/1000 # [as]
    m2 = -(yp*3600*180/np.pi - ypm/1000) # [as]
    
    # pole tidal
    dr = -0.033*np.sin(2*clt)*(m1*np.cos(lam)+m2*np.sin(lam))
    de =  0.009*np.cos(clt)*(m1*np.sin(lam)-m2*np.cos(lam))
    dn =  0.009*np.cos(2*clt)*(m1*np.cos(lam)+m2*np.sin(lam))
    
    # ocean pole tidal
    part1 = (m1*0.6870 + m2*0.0036)/3600/180*np.pi #rad
    part2 = (m2*0.6870 - m1*0.0036)/3600/180*np.pi #rad
    
    oppR = opp[[0,2,4]]
    oppI = opp[[1,3,5]]
    ctop = const.K_opp*(part1*oppR + part2*oppI)
    ctop = [ctop[0],ctop[2],ctop[1]]
    
    ctp = ren2xyz(np.array([dr,de,dn]),phi,lam) + \
          ren2xyz(np.array(ctop), phi, lam)
          
    temp = ren2xyz(np.array([dr,de,dn]), phi, lam)
          
    return ctp
    
def meanPole(t):
    """
    Compute mean Pole coordinates
    ---------------------
    input: 
      t              : time
    output: 
      xpm,ypm        : mean Pole coordinate, [mas]
    ---------------------
    """
    t0 = 2000
    
    x0 = 55.0   # [mas]
    x1 = 1.677  # [mas/year]
    
    y0 = 320.5
    y1 = 3.460
    
    xpm = x0 + x1*(t-t0)
    ypm = y0 + y1*(t-t0)
    
    """
    # IERS Conv. 2010
    if t < 2010:
        x0 = 55.974  #mas
        x1 = 1.8243
        x2 = 0.18413
        x3 = 0.007024
        
        y0 = 346.346
        y1 = 1.7896
        y2 = -0.10729
        y3 = -0.000908
    else:
        x0 = 23.513
        x1 = 7.6141
        x2 = 0
        x3 = 0
        
        y0 = 358.891
        y1 = -0.6287
        y2 = 0
        y3 = 0
   
    xpm = x0 + x1*(t-t0) + x2*(t-t0)**2 + x3*(t-t0)**3
    ypm = y0 + y1*(t-t0) + y2*(t-t0)**2 + y3*(t-t0)**3
    """
    
    return xpm,ypm

def atmosphere_tidal_corr(mjd, lam, phi, ap):
    """
    Atmosphere tidal station correction
    ---------------------
    input:
      mjd            : Modified Julian Date
      lam,phi        : the station position
      ap             : atmosphere tide coefficients
    output: 
      cta            : station correction of atmosphere tidal, [m]
    ---------------------
    """
    UTJ = (mjd - np.floor(mjd))*2*np.pi
    
    dr = ap[0]*np.cos(UTJ) + ap[1]*np.sin(UTJ) + ap[2]*np.cos(2*UTJ) + ap[3]*np.sin(2*UTJ)
    dn = ap[4]*np.cos(UTJ) + ap[5]*np.sin(UTJ) + ap[6]*np.cos(2*UTJ) + ap[7]*np.sin(2*UTJ)
    de = ap[8]*np.cos(UTJ) + ap[9]*np.sin(UTJ) + ap[10]*np.cos(2*UTJ) + ap[11]*np.sin(2*UTJ)
    
    cta = ren2xyz(np.array([dr,de,dn])/1000, phi, lam)
    
    return cta

def ocean_tidal_corr(mjd, cto, lam, phi):
    """
    Ocean tidal station correction
    ---------------------
    input: 
      mjd            : Modified Julian Date
      cto            : data in the BLQ format used by Scherneck and Bos for ocean loading
    output: 
      cto_corr       : station correction
    ---------------------
    """
    F_lsr,P_lsr,TAMPL,IDD1 = tidal_admit(mjd)
    D,DD = tdfrph(mjd)
    
    IDT = np.array([[2, 0, 0, 0, 0, 0],\
                    [2, 2,-2, 0, 0, 0],\
                    [2,-1, 0, 1, 0, 0],\
                    [2, 2, 0, 0, 0, 0],\
                    [1, 1, 0, 0, 0, 0],\
                    [1,-1, 0, 0, 0, 0],\
                    [1, 1,-2, 0, 0, 0],\
                    [1,-2, 0, 1, 0, 0],\
                    [0, 2, 0, 0, 0, 0],\
                    [0, 1, 0,-1, 0, 0],\
                    [0, 0, 2, 0, 0, 0]])
    TAMPT = np.array([ 0.6322,0.2941,0.1210,0.0799,0.3686,-0.2622,-0.1220,-0.0502,-0.0666,-0.0352,-0.0310])
    
    TAMP = cto[0:3,0:]
    TPH = -cto[3:,0:]
    TPH = TPH * np.pi/180
    
    RL = TAMP * np.cos(TPH)/abs(TAMPT)
    AIM = TAMP * np.sin(TPH)/abs(TAMPT)
    RF = np.dot(IDT, DD)
    
    key = np.argsort(RF)
    
    RF = RF[key]
    AIM = AIM[:,key]
    RL = RL[:,key]
    
    # vertical
    AZ,PZ = admint(RF,RL[0],AIM[0],F_lsr,P_lsr,TAMPL,IDD1)
    # West
    AW,PW = admint(RF,RL[1],AIM[1],F_lsr,P_lsr,TAMPL,IDD1)
    # South
    AS,PS = admint(RF,RL[2],AIM[2],F_lsr,P_lsr,TAMPL,IDD1)
    
    DZ = sum(AZ*np.cos(PZ))
    DS = sum(AS*np.cos(PS))
    DW = sum(AW*np.cos(PW))
    
    cto = ren2xyz(np.array([DZ,-DW,-DS]), phi, lam)
    
    return cto

def psd_corr(mjd, psd, phi, lam):
    '''
    Correct the post-seismic deformation.

    '''
    
    #index  = psd_getENU(mjd, psd[0])
    index = bisect.bisect_left(psd[0],mjd) - 1

    cpsd = np.zeros(3)
    if index != -1:
        #for i in range(index+1):
        Epsd = psd_compute((mjd - psd[0][index])/365.25, psd[1][index][0])
        Npsd = psd_compute((mjd - psd[0][index])/365.25, psd[1][index][1])
        Upsd = psd_compute((mjd - psd[0][index])/365.25, psd[1][index][2])
        
            # print(Epsd,Npsd,Upsd, phi, lam)
    
        cpsd += ren2xyz(np.array([Upsd, Epsd, Npsd]), phi, lam)
    
    return cpsd
    
def psd_getENU(mjd, MJD):
    
    index = -1
    if len(MJD) == 1:
        if mjd >= MJD[0]:
            index = 0
            
    elif len(MJD) >= 2:
        for i in range(len(MJD)-1):
            if mjd >= MJD[i] and mjd < MJD[i+1]:
                index = i
        if mjd >= MJD[-1]:
            index = len(MJD)-1
            
    return index

def psd_compute(mjd, value):
    
    nvalue = [int(value[0])]
    for i in value[1:]:
        nvalue.append(float(i))
    
    if nvalue[0] == 0:
        psdValue = 0
    elif nvalue[0] == 1:
        psdValue = nvalue[1]*np.log(1+mjd/nvalue[2])
    elif nvalue[0] == 2:
        psdValue = nvalue[1]*(1-np.exp(-mjd/nvalue[2]))
    elif nvalue[0] == 3:
        psdValue = nvalue[1]*np.log(1+mjd/nvalue[2]) + nvalue[3]*(1-np.exp(-mjd/nvalue[4]))
    elif nvalue[0] == 4:
        psdValue = nvalue[1]*(1-np.exp(-mjd/nvalue[2])) + nvalue[3]*(1-np.exp(-mjd/nvalue[4]))
    elif nvalue[0] == 5:
        psdValue = nvalue[1]*np.log(1+mjd/nvalue[2]) + nvalue[3]*np.log(1+mjd/nvalue[4])
        
    return psdValue*1E-3
    
def admint(RF,RL, AIM, F, P, TAMP, IDD):
    
    temp = np.where(RF<0.5)                 # Long periods
    NLP = len(temp[0])
    temp = np.where((RF>0.5) & (RF<1.5))     # diurnal
    NDI = len(temp[0])
    temp = np.where((RF>1.5) & (RF<2.5))     # semidiurnal
    NSD = len(temp[0])
    
    if NLP != 0:
        ZDR = spline(NLP, RF, RL)
        ZDI = spline(NLP, RF, AIM)
        
    DR = spline(NDI, RF[NLP:], RL[NLP:])
    DI = spline(NDI, RF[NLP:], AIM[NLP:])
    SDR = spline(NDI, RF[NLP+NDI:], RL[NLP+NDI:])
    SDI = spline(NDI, RF[NLP+NDI:], AIM[NLP+NDI:])
    
    
    SF = F[IDD==0]
    RE_lp = lib_eval(SF, NLP, RF, RL, ZDR)
    AM_lp = lib_eval(SF, NLP, RF, AIM, ZDI)
    
    SF = F[IDD==1]
    RE_diu = lib_eval(SF, NDI, RF[NLP:], RL[NLP:], DR)
    AM_diu = lib_eval(SF, NDI, RF[NLP:], AIM[NLP:], DI)
    
    SF = F[IDD==2]
    RE_smd = lib_eval(SF, NSD, RF[NLP+NDI:], RL[NLP+NDI:], SDR)
    AM_smd = lib_eval(SF, NSD, RF[NLP+NDI:], AIM[NLP+NDI:], SDI)
    
    AMP1 = TAMP[IDD==2]*np.sqrt(RE_smd**2+AM_smd**2)
    AMP2 = TAMP[IDD==1]*np.sqrt(RE_diu**2+AM_diu**2)
    AMP3 = TAMP[IDD==0]*np.sqrt(RE_lp**2+AM_lp**2)
    AMP = np.hstack((AMP1,AMP2,AMP3))
    
    dP = np.hstack((np.arctan2(AM_smd,RE_smd)*180/np.pi,\
                   np.arctan2(AM_diu,RE_diu)*180/np.pi,\
                   np.arctan2(AM_lp,RE_lp)*180/np.pi))
    
    P_l = []
    for i in range(342):
        if IDD[i] == 0:
            P_l.append(P[i]+180)
        elif IDD[i] == 1:
            P_l.append(P[i]+90)
        else:
            P_l.append(P[i])
    
    P_l = P_l + dP
    
    temp = np.where(P_l>180)
    P_l[temp[0]] = P_l[temp[0]] - 360
    
    return AMP,P_l*np.pi/180
    
    
def spline(N,X,U):
    
    if N <= 3:
        S = np.zeros(N)
        return S
        
    U1 = U[1] - U[0]
    X1 = X[1] - X[0]
    U2 = U[2] - U[0]
    X2 = X[2] - X[0]
    Q1 = (U1/(X1**2) - U2/(X2**2))/(1.0/X1-1.0/X2)
    
    
    U1 = U[N-2] - U[N-1]
    X1 = X[N-2] - X[N-1]
    U2 = U[N-3] - U[N-1]
    X2 = X[N-3] - X[N-1]
    QN = (U1/(X1**2) - U2/(X2**2))/(1.0/X1-1.0/X2)
    
    A = np.zeros(N)    
    S = np.zeros(N)
    S[0] = 6.0*((U[1]-U[0])/(X[1]-X[0])-Q1)

    for i in range(1, N-1):
        S[i] = (U[i-1]/(X[i]-X[i-1]) - U[i]*(1.0/(X[i]-X[i-1])+1.0/(X[i+1]-X[i]))+\
                U[i+1]/(X[i+1]-X[i]))*6.0
    S[N-1] = 6.0*(QN + (U[N-2]-U[N-1])/(X[N-1]-X[N-2]))
    A[0] = 2.0*(X[1]-X[0])
    A[1] = 1.5*(X[1]-X[0]) + 2.0*(X[2]-X[1])
    S[1] = S[1] - 0.5*S[0]
    
    for i in range(2, N-1):
        C = (X[i]-X[i-1])/A[i-1]
        A[i] = 2.0*(X[i+1]-X[i-1]) - C*(X[i]-X[i-1])
        S[i] = S[i] - C*S[i-1]

    C = (X[N-1]-X[N-2])/A[N-2]
    A[N-1] = (2.0-C)*(X[N-1]-X[N-2])
    S[N-1] = S[N-1] - C*S[N-2]
    
    S[N-1] = S[N-1]/A[N-1]
    
    for j in range(N-1):
        i = N - 2 - j
        S[i] = (S[i]-(X[i+1]-X[i])*S[i+1])/A[i]
        
    return S

def lib_eval(Y, N, X, U, S):
    
    nt = len(Y)
    EVAL = np.zeros(nt)
    
    id1 = np.where(Y <= X[0])
    if len(id1[0]) != 0:
        EVAL[id1[0]] = U[0]
        
    id2 = np.where(Y >= X[N-1])
    if len(id2[0]) != 0:
        EVAL[id2[0]] = U[N-1]
        
    aid = np.append(id1,id2)
        
    Y = np.delete(Y,aid)
    
    NY = len(Y)
    K1 = np.zeros(NY, dtype=int)
    K2 = np.zeros(NY, dtype=int)
    
    for i in range(NY):
        for k in range(1,N):
            if (X[k-1] < Y[i]) & (X[k] >= Y[i]):
                K1[i] = k-1
                K2[i] = k
                
    DY = X[K2] - Y
    DY1 = Y - X[K1]
    DK = X[K2] - X[K1]
    DELI = 1.0/(6.0*DK)
    FF1 = S[K1]*DY**3
    FF2 = S[K2]*DY1**3
    
    F1 = (FF1+FF2)*DELI
    F2 = DY1*((U[K2]/DK)-(S[K2]*DK)/6.0)
    F3 = DY*((U[K1]/DK)-(S[K1]*DK)/6.0)
    EVAL1 = F1+F2+F3
    
    nid = np.ones(nt)
    nid[aid] = 0
        
    EVAL[nid==1] = EVAL1
    
    return EVAL
        

def tidal_admit(mjd):
    """
    contains amplitudes and Doodson numbers for 342 tidal constituents
    ---------------------
    input: 
      mjd            : 
    output: 
      F              : frequencies of tidal constituents
      P              : phases of tidal constituents
      TAMP           : Cartwright-Edden amplitudes of tidal constituents
      IDD1           : first digit of the Doodson number (used in libiers_hardisp/libiers_admint)
    ---------------------
    """
    TAMP = np.array([ .632208, .294107, .121046, .079915, .023818,-.023589, .022994,\
                      .019333,-.017871, .017192, .016018, .004671,-.004662,-.004519,\
                      .004470, .004467, .002589,-.002455,-.002172, .001972, .001947,\
                      .001914,-.001898, .001802, .001304, .001170, .001130, .001061,\
                     -.001022,-.001017, .001014, .000901,-.000857, .000855, .000855,\
                      .000772, .000741, .000741,-.000721, .000698, .000658, .000654,\
                     -.000653, .000633, .000626,-.000598, .000590, .000544, .000479,\
                     -.000464, .000413,-.000390, .000373, .000366, .000366,-.000360,\
                     -.000355, .000354, .000329, .000328, .000319, .000302, .000279,\
                     -.000274,-.000272, .000248,-.000225, .000224,-.000223,-.000216,\
                      .000211, .000209, .000194, .000185,-.000174,-.000171, .000159,\
                      .000131, .000127, .000120, .000118, .000117, .000108, .000107,\
                      .000105,-.000102, .000102, .000099,-.000096, .000095,-.000089,\
                     -.000085,-.000084,-.000081,-.000077,-.000072,-.000067, .000066,\
                      .000064, .000063, .000063, .000063, .000062, .000062,-.000060,\
                      .000056, .000053, .000051, .000050, .368645,-.262232,-.121995,\
                     -.050208, .050031,-.049470, .020620, .020613, .011279,-.009530,\
                     -.009469,-.008012, .007414,-.007300, .007227,-.007131,-.006644,\
                      .005249, .004137, .004087, .003944, .003943, .003420, .003418,\
                      .002885, .002884, .002160,-.001936, .001934,-.001798, .001690,\
                      .001689, .001516, .001514,-.001511, .001383, .001372, .001371,\
                     -.001253,-.001075, .001020, .000901, .000865,-.000794, .000788,\
                      .000782,-.000747,-.000745, .000670,-.000603,-.000597, .000542,\
                      .000542,-.000541,-.000469,-.000440, .000438, .000422, .000410,\
                     -.000374,-.000365, .000345, .000335,-.000321,-.000319, .000307,\
                      .000291, .000290,-.000289, .000286, .000275, .000271, .000263,\
                     -.000245, .000225, .000225, .000221,-.000202,-.000200,-.000199,\
                      .000192, .000183, .000183, .000183,-.000170, .000169, .000168,\
                      .000162, .000149,-.000147,-.000141, .000138, .000136, .000136,\
                      .000127, .000127,-.000126,-.000121,-.000121, .000117,-.000116,\
                     -.000114,-.000114,-.000114, .000114, .000113, .000109, .000108,\
                      .000106,-.000106,-.000106, .000105, .000104,-.000103,-.000100,\
                     -.000100,-.000100, .000099,-.000098, .000093, .000093, .000090,\
                     -.000088, .000083,-.000083,-.000082,-.000081,-.000079,-.000077,\
                     -.000075,-.000075,-.000075, .000071, .000071,-.000071, .000068,\
                      .000068, .000065, .000065, .000064, .000064, .000064,-.000064,\
                     -.000060, .000056, .000056, .000053, .000053, .000053,-.000053,\
                      .000053, .000053, .000052, .000050,-.066607,-.035184,-.030988,\
                      .027929,-.027616,-.012753,-.006728,-.005837,-.005286,-.004921,\
                     -.002884,-.002583,-.002422, .002310, .002283,-.002037, .001883,\
                     -.001811,-.001687,-.001004,-.000925,-.000844, .000766, .000766,\
                     -.000700,-.000495,-.000492, .000491, .000483, .000437,-.000416,\
                     -.000384, .000374,-.000312,-.000288,-.000273, .000259, .000245,\
                     -.000232, .000229,-.000216, .000206,-.000204,-.000202, .000200,\
                      .000195,-.000190, .000187, .000180,-.000179, .000170, .000153,\
                     -.000137,-.000119,-.000119,-.000112,-.000110,-.000110, .000107,\
                     -.000095,-.000095,-.000091,-.000090,-.000081,-.000079,-.000079,\
                      .000077,-.000073, .000069,-.000067,-.000066, .000065, .000064,\
                     -.000062, .000060, .000059,-.000056, .000055,-.000051])
    IDD = np.array([[2, 0, 0, 0, 0, 0],   [2, 2,-2, 0, 0, 0],   [2,-1, 0, 1, 0, 0],\
                    [2, 2, 0, 0, 0, 0],   [2, 2, 0, 0, 1, 0],   [2, 0, 0, 0,-1, 0],\
                    [2,-1, 2,-1, 0, 0],   [2,-2, 2, 0, 0, 0],   [2, 1, 0,-1, 0, 0],\
                    [2, 2,-3, 0, 0, 1],   [2,-2, 0, 2, 0, 0],   [2,-3, 2, 1, 0, 0],\
                    [2, 1,-2, 1, 0, 0],   [2,-1, 0, 1,-1, 0],   [2, 3, 0,-1, 0, 0],\
                    [2, 1, 0, 1, 0, 0],   [2, 2, 0, 0, 2, 0],   [2, 2,-1, 0, 0,-1],\
                    [2, 0,-1, 0, 0, 1],   [2, 1, 0, 1, 1, 0],   [2, 3, 0,-1, 1, 0],\
                    [2, 0, 1, 0, 0,-1],   [2, 0,-2, 2, 0, 0],   [2,-3, 0, 3, 0, 0],\
                    [2,-2, 3, 0, 0,-1],   [2, 4, 0, 0, 0, 0],   [2,-1, 1, 1, 0,-1],\
                    [2,-1, 3,-1, 0,-1],   [2, 2, 0, 0,-1, 0],   [2,-1,-1, 1, 0, 1],\
                    [2, 4, 0, 0, 1, 0],   [2,-3, 4,-1, 0, 0],   [2,-1, 2,-1,-1, 0],\
                    [2, 3,-2, 1, 0, 0],   [2, 1, 2,-1, 0, 0],   [2,-4, 2, 2, 0, 0],\
                    [2, 4,-2, 0, 0, 0],   [2, 0, 2, 0, 0, 0],   [2,-2, 2, 0,-1, 0],\
                    [2, 2,-4, 0, 0, 2],   [2, 2,-2, 0,-1, 0],   [2, 1, 0,-1,-1, 0],\
                    [2,-1, 1, 0, 0, 0],   [2, 2,-1, 0, 0, 1],   [2, 2, 1, 0, 0,-1],\
                    [2,-2, 0, 2,-1, 0],   [2,-2, 4,-2, 0, 0],   [2, 2, 2, 0, 0, 0],\
                    [2,-4, 4, 0, 0, 0],   [2,-1, 0,-1,-2, 0],   [2, 1, 2,-1, 1, 0],\
                    [2,-1,-2, 3, 0, 0],   [2, 3,-2, 1, 1, 0],   [2, 4, 0,-2, 0, 0],\
                    [2, 0, 0, 2, 0, 0],   [2, 0, 2,-2, 0, 0],   [2, 0, 2, 0, 1, 0],\
                    [2,-3, 3, 1, 0,-1],   [2, 0, 0, 0,-2, 0],   [2, 4, 0, 0, 2, 0],\
                    [2, 4,-2, 0, 1, 0],   [2, 0, 0, 0, 0, 2],   [2, 1, 0, 1, 2, 0],\
                    [2, 0,-2, 0,-2, 0],   [2,-2, 1, 0, 0, 1],   [2,-2, 1, 2, 0,-1],\
                    [2,-1, 1,-1, 0, 1],   [2, 5, 0,-1, 0, 0],   [2, 1,-3, 1, 0, 1],\
                    [2,-2,-1, 2, 0, 1],   [2, 3, 0,-1, 2, 0],   [2, 1,-2, 1,-1, 0],\
                    [2, 5, 0,-1, 1, 0],   [2,-4, 0, 4, 0, 0],   [2,-3, 2, 1,-1, 0],\
                    [2,-2, 1, 1, 0, 0],   [2, 4, 0,-2, 1, 0],   [2, 0, 0, 2, 1, 0],\
                    [2,-5, 4, 1, 0, 0],   [2, 0, 2, 0, 2, 0],   [2,-1, 2, 1, 0, 0],\
                    [2, 5,-2,-1, 0, 0],   [2, 1,-1, 0, 0, 0],   [2, 2,-2, 0, 0, 2],\
                    [2,-5, 2, 3, 0, 0],   [2,-1,-2, 1,-2, 0],   [2,-3, 5,-1, 0,-1],\
                    [2,-1, 0, 0, 0, 1],   [2,-2, 0, 0,-2, 0],   [2, 0,-1, 1, 0, 0],\
                    [2,-3, 1, 1, 0, 1],   [2, 3, 0,-1,-1, 0],   [2, 1, 0, 1,-1, 0],\
                    [2,-1, 2, 1, 1, 0],   [2, 0,-3, 2, 0, 1],   [2, 1,-1,-1, 0, 1],\
                    [2,-3, 0, 3,-1, 0],   [2, 0,-2, 2,-1, 0],   [2,-4, 3, 2, 0,-1],\
                    [2,-1, 0, 1,-2, 0],   [2, 5, 0,-1, 2, 0],   [2,-4, 5, 0, 0,-1],\
                    [2,-2, 4, 0, 0,-2],   [2,-1, 0, 1, 0, 2],   [2,-2,-2, 4, 0, 0],\
                    [2, 3,-2,-1,-1, 0],   [2,-2, 5,-2, 0,-1],   [2, 0,-1, 0,-1, 1],\
                    [2, 5,-2,-1, 1, 0],   [1, 1, 0, 0, 0, 0],   [1,-1, 0, 0, 0, 0],\
                    [1, 1,-2, 0, 0, 0],   [1,-2, 0, 1, 0, 0],   [1, 1, 0, 0, 1, 0],\
                    [1,-1, 0, 0,-1, 0],   [1, 2, 0,-1, 0, 0],   [1, 0, 0, 1, 0, 0],\
                    [1, 3, 0, 0, 0, 0],   [1,-2, 2,-1, 0, 0],   [1,-2, 0, 1,-1, 0],\
                    [1,-3, 2, 0, 0, 0],   [1, 0, 0,-1, 0, 0],   [1, 1, 0, 0,-1, 0],\
                    [1, 3, 0, 0, 1, 0],   [1, 1,-3, 0, 0, 1],   [1,-3, 0, 2, 0, 0],\
                    [1, 1, 2, 0, 0, 0],   [1, 0, 0, 1, 1, 0],   [1, 2, 0,-1, 1, 0],\
                    [1, 0, 2,-1, 0, 0],   [1, 2,-2, 1, 0, 0],   [1, 3,-2, 0, 0, 0],\
                    [1,-1, 2, 0, 0, 0],   [1, 1, 1, 0, 0,-1],   [1, 1,-1, 0, 0, 1],\
                    [1, 4, 0,-1, 0, 0],   [1,-4, 2, 1, 0, 0],   [1, 0,-2, 1, 0, 0],\
                    [1,-2, 2,-1,-1, 0],   [1, 3, 0,-2, 0, 0],   [1,-1, 0, 2, 0, 0],\
                    [1,-1, 0, 0,-2, 0],   [1, 3, 0, 0, 2, 0],   [1,-3, 2, 0,-1, 0],\
                    [1, 4, 0,-1, 1, 0],   [1, 0, 0,-1,-1, 0],   [1, 1,-2, 0,-1, 0],\
                    [1,-3, 0, 2,-1, 0],   [1, 1, 0, 0, 2, 0],   [1, 1,-1, 0, 0,-1],\
                    [1,-1,-1, 0, 0, 1],   [1, 0, 2,-1, 1, 0],   [1,-1, 1, 0, 0,-1],\
                    [1,-1,-2, 2, 0, 0],   [1, 2,-2, 1, 1, 0],   [1,-4, 0, 3, 0, 0],\
                    [1,-1, 2, 0, 1, 0],   [1, 3,-2, 0, 1, 0],   [1, 2, 0,-1,-1, 0],\
                    [1, 0, 0, 1,-1, 0],   [1,-2, 2, 1, 0, 0],   [1, 4,-2,-1, 0, 0],\
                    [1,-3, 3, 0, 0,-1],   [1,-2, 1, 1, 0,-1],   [1,-2, 3,-1, 0,-1],\
                    [1, 0,-2, 1,-1, 0],   [1,-2,-1, 1, 0, 1],   [1, 4,-2, 1, 0, 0],\
                    [1,-4, 4,-1, 0, 0],   [1,-4, 2, 1,-1, 0],   [1, 5,-2, 0, 0, 0],\
                    [1, 3, 0,-2, 1, 0],   [1,-5, 2, 2, 0, 0],   [1, 2, 0, 1, 0, 0],\
                    [1, 1, 3, 0, 0,-1],   [1,-2, 0, 1,-2, 0],   [1, 4, 0,-1, 2, 0],\
                    [1, 1,-4, 0, 0, 2],   [1, 5, 0,-2, 0, 0],   [1,-1, 0, 2, 1, 0],\
                    [1,-2, 1, 0, 0, 0],   [1, 4,-2, 1, 1, 0],   [1,-3, 4,-2, 0, 0],\
                    [1,-1, 3, 0, 0,-1],   [1, 3,-3, 0, 0, 1],   [1, 5,-2, 0, 1, 0],\
                    [1, 1, 2, 0, 1, 0],   [1, 2, 0, 1, 1, 0],   [1,-5, 4, 0, 0, 0],\
                    [1,-2, 0,-1,-2, 0],   [1, 5, 0,-2, 1, 0],   [1, 1, 2,-2, 0, 0],\
                    [1, 1,-2, 2, 0, 0],   [1,-2, 2, 1, 1, 0],   [1, 0, 3,-1, 0,-1],\
                    [1, 2,-3, 1, 0, 1],   [1,-2,-2, 3, 0, 0],   [1,-1, 2,-2, 0, 0],\
                    [1,-4, 3, 1, 0,-1],   [1,-4, 0, 3,-1, 0],   [1,-1,-2, 2,-1, 0],\
                    [1,-2, 0, 3, 0, 0],   [1, 4, 0,-3, 0, 0],   [1, 0, 1, 1, 0,-1],\
                    [1, 2,-1,-1, 0, 1],   [1, 2,-2, 1,-1, 0],   [1, 0, 0,-1,-2, 0],\
                    [1, 2, 0, 1, 2, 0],   [1, 2,-2,-1,-1, 0],   [1, 0, 0, 1, 2, 0],\
                    [1, 0, 1, 0, 0, 0],   [1, 2,-1, 0, 0, 0],   [1, 0, 2,-1,-1, 0],\
                    [1,-1,-2, 0,-2, 0],   [1,-3, 1, 0, 0, 1],   [1, 3,-2, 0,-1, 0],\
                    [1,-1,-1, 0,-1, 1],   [1, 4,-2,-1, 1, 0],   [1, 2, 1,-1, 0,-1],\
                    [1, 0,-1, 1, 0, 1],   [1,-2, 4,-1, 0, 0],   [1, 4,-4, 1, 0, 0],\
                    [1,-3, 1, 2, 0,-1],   [1,-3, 3, 0,-1,-1],   [1, 1, 2, 0, 2, 0],\
                    [1, 1,-2, 0,-2, 0],   [1, 3, 0, 0, 3, 0],   [1,-1, 2, 0,-1, 0],\
                    [1,-2, 1,-1, 0, 1],   [1, 0,-3, 1, 0, 1],   [1,-3,-1, 2, 0, 1],\
                    [1, 2, 0,-1, 2, 0],   [1, 6,-2,-1, 0, 0],   [1, 2, 2,-1, 0, 0],\
                    [1,-1, 1, 0,-1,-1],   [1,-2, 3,-1,-1,-1],   [1,-1, 0, 0, 0, 2],\
                    [1,-5, 0, 4, 0, 0],   [1, 1, 0, 0, 0,-2],   [1,-2, 1, 1,-1,-1],\
                    [1, 1,-1, 0, 1, 1],   [1, 1, 2, 0, 0,-2],   [1,-3, 1, 1, 0, 0],\
                    [1,-4, 4,-1,-1, 0],   [1, 1, 0,-2,-1, 0],   [1,-2,-1, 1,-1, 1],\
                    [1,-3, 2, 2, 0, 0],   [1, 5,-2,-2, 0, 0],   [1, 3,-4, 2, 0, 0],\
                    [1, 1,-2, 0, 0, 2],   [1,-1, 4,-2, 0, 0],   [1, 2, 2,-1, 1, 0],\
                    [1,-5, 2, 2,-1, 0],   [1, 1,-3, 0,-1, 1],   [1, 1, 1, 0, 1,-1],\
                    [1, 6,-2,-1, 1, 0],   [1,-2, 2,-1,-2, 0],   [1, 4,-2, 1, 2, 0],\
                    [1,-6, 4, 1, 0, 0],   [1, 5,-4, 0, 0, 0],   [1,-3, 4, 0, 0, 0],\
                    [1, 1, 2,-2, 1, 0],   [1,-2, 1, 0,-1, 0],   [0, 2, 0, 0, 0, 0],\
                    [0, 1, 0,-1, 0, 0],   [0, 0, 2, 0, 0, 0],   [0, 0, 0, 0, 1, 0],\
                    [0, 2, 0, 0, 1, 0],   [0, 3, 0,-1, 0, 0],   [0, 1,-2, 1, 0, 0],\
                    [0, 2,-2, 0, 0, 0],   [0, 3, 0,-1, 1, 0],   [0, 0, 1, 0, 0,-1],\
                    [0, 2, 0,-2, 0, 0],   [0, 2, 0, 0, 2, 0],   [0, 3,-2, 1, 0, 0],\
                    [0, 1, 0,-1,-1, 0],   [0, 1, 0,-1, 1, 0],   [0, 4,-2, 0, 0, 0],\
                    [0, 1, 0, 1, 0, 0],   [0, 0, 3, 0, 0,-1],   [0, 4, 0,-2, 0, 0],\
                    [0, 3,-2, 1, 1, 0],   [0, 3,-2,-1, 0, 0],   [0, 4,-2, 0, 1, 0],\
                    [0, 0, 2, 0, 1, 0],   [0, 1, 0, 1, 1, 0],   [0, 4, 0,-2, 1, 0],\
                    [0, 3, 0,-1, 2, 0],   [0, 5,-2,-1, 0, 0],   [0, 1, 2,-1, 0, 0],\
                    [0, 1,-2, 1,-1, 0],   [0, 1,-2, 1, 1, 0],   [0, 2,-2, 0,-1, 0],\
                    [0, 2,-3, 0, 0, 1],   [0, 2,-2, 0, 1, 0],   [0, 0, 2,-2, 0, 0],\
                    [0, 1,-3, 1, 0, 1],   [0, 0, 0, 0, 2, 0],   [0, 0, 1, 0, 0, 1],\
                    [0, 1, 2,-1, 1, 0],   [0, 3, 0,-3, 0, 0],   [0, 2, 1, 0, 0,-1],\
                    [0, 1,-1,-1, 0, 1],   [0, 1, 0, 1, 2, 0],   [0, 5,-2,-1, 1, 0],\
                    [0, 2,-1, 0, 0, 1],   [0, 2, 2,-2, 0, 0],   [0, 1,-1, 0, 0, 0],\
                    [0, 5, 0,-3, 0, 0],   [0, 2, 0,-2, 1, 0],   [0, 1, 1,-1, 0,-1],\
                    [0, 3,-4, 1, 0, 0],   [0, 0, 2, 0, 2, 0],   [0, 2, 0,-2,-1, 0],\
                    [0, 4,-3, 0, 0, 1],   [0, 3,-1,-1, 0, 1],   [0, 0, 2, 0, 0,-2],\
                    [0, 3,-3, 1, 0, 1],   [0, 2,-4, 2, 0, 0],   [0, 4,-2,-2, 0, 0],\
                    [0, 3, 1,-1, 0,-1],   [0, 5,-4, 1, 0, 0],   [0, 3,-2,-1,-1, 0],\
                    [0, 3,-2, 1, 2, 0],   [0, 4,-4, 0, 0, 0],   [0, 6,-2,-2, 0, 0],\
                    [0, 5, 0,-3, 1, 0],   [0, 4,-2, 0, 2, 0],   [0, 2, 2,-2, 1, 0],\
                    [0, 0, 4, 0, 0,-2],   [0, 3,-1, 0, 0, 0],   [0, 3,-3,-1, 0, 1],\
                    [0, 4, 0,-2, 2, 0],   [0, 1,-2,-1,-1, 0],   [0, 2,-1, 0, 0,-1],\
                    [0, 4,-4, 2, 0, 0],   [0, 2, 1, 0, 1,-1],   [0, 3,-2,-1, 1, 0],\
                    [0, 4,-3, 0, 1, 1],   [0, 2, 0, 0, 3, 0],   [0, 6,-4, 0, 0, 0]])
    
    D,DD = tdfrph(mjd)
    
    F = np.dot(IDD, DD)
    P = np.dot(IDD,  D)
    P = np.mod(P, 360)
    
    return F,P,TAMP,IDD[:,0]

    
def tdfrph(mjd):
    """
    Get the frequency and phase of a tidal constituent
    ---------------------
    input: 
      IDD            : 
      mjd
    output: 
      D              : frequencies of tidal constituents
      DD             : phases of tidal constituents
    ---------------------
    """
    T = calc_T([mjd])
    
    day = mjd - np.floor(mjd)
    
    F1 =     134.9634025100E0 + \
     T*( 477198.8675605000E0 + \
     T*(      0.0088553333E0 + \
     T*(      0.0000143431E0 + \
     T*(     -0.0000000680E0 ))))
    F2 =     357.5291091806E0 + \
     T*(  35999.0502911389E0 + \
     T*(     -0.0001536667E0 + \
     T*(      0.0000000378E0 + \
     T*(     -0.0000000032E0 ))))
    F3 =      93.2720906200E0 + \
     T*( 483202.0174577222E0 + \
     T*(     -0.0035420000E0 + \
     T*(     -0.0000002881E0 + \
     T*(      0.0000000012E0 ))))
    F4 =     297.8501954694E0 + \
     T*( 445267.1114469445E0 + \
     T*(     -0.0017696111E0 + \
     T*(      0.0000018314E0 + \
     T*(     -0.0000000088E0 ))))
    F5 =     125.0445550100E0 + \
     T*(  -1934.1362619722E0 + \
     T*(      0.0020756111E0 + \
     T*(      0.0000021394E0 + \
     T*(     -0.0000000165E0 ))))
     
    D = np.array([360*day - F4,\
                  F3 + F5     ,\
                  F3 + F5 - F4,\
                  F3 + F5 - F1,\
                  -F5         ,\
                  F3 + F5 - F4 -F2])
    
    FD1 =  0.0362916471E0 + 0.0000000013E0*T
    FD2 =  0.0027377786E0
    FD3 =  0.0367481951E0 - 0.0000000005E0*T
    FD4 =  0.0338631920E0 - 0.0000000003E0*T
    FD5 = -0.0001470938E0 + 0.0000000003E0*T
    
    DD = np.array([  1 - FD4,\
                   FD3 + FD5,\
                   FD3 + FD5 - FD4,\
                   FD3 + FD5 - FD1,\
                   -FD5           ,\
                   FD3 + FD5 - FD4 - FD2])
    return D.reshape(6),DD.reshape(6)
     
    
def get_unit_vector(crf):
    az = np.arctan2(crf[1],crf[0])
    el = np.arctan2(crf[2],np.sqrt(crf[0]**2+crf[1]**2))
    
    length = np.sqrt(crf[0]**2+crf[1]**2+crf[2]**2)
    return az,el,length,crf/length

'''    
mjd = 5.928877206018518e+04
cto = np.array([[  .01271, .00487, .00241, .00134, .01239, .00691, .00381, .00110, .00054, .00036, .00032],\
                [  .00274, .00127, .00053, .00036, .00215, .00144, .00067, .00028, .00001, .00001, .00001],\
                [  .00436, .00178, .00078, .00049, .00195, .00129, .00061, .00024, .00010, .00006, .00006],\
                [  -120.9, -116.4, -127.3, -126.8,   60.3,   53.8,   59.1,   51.6, -138.3, -152.1, -175.7],\
                [   160.2, -172.0,  157.0, -175.4,   39.6,   13.8,   37.0,   -0.9, -150.9,   86.4,    6.2],\
                [    97.0,  124.9,   93.6,  118.9,  112.8,   94.5,  109.6,   85.4,    0.0,    2.2,    0.4]])
ocean_tidal_corr(mjd, cto)
'''
  
  
'''
mjd = 5.933077106481482e+04
t2c = np.array([[-0.672851472655050,  -0.739774797310116,   0.002035929936796],\
               [0.739776341558968,  -0.672852854942444,   0.000008089049053],\
               [0.001363897195813,   0.001511575528881,   0.999997927459782]])
sta_xgeo = np.array([-5543831.709100000,  -2054585.942300000,   2387828.789800000])
moon_xgeo = np.array([-306130430.9003060,-177688316.1142268,-54380302.3253487])
sun_xgeo = np.array([1.211009947938485,0.820702753379182,0.355770853927402])*1E11

soild_tide_corr(mjd, t2c, sta_xgeo, moon_xgeo, sun_xgeo)
'''
