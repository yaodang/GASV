#!/usr/bin/env python3

import numpy as np

class _const:
    class ConstError(TypeError) : pass
    class ConstCaseError(ConstError) : pass
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value 
        
        
const = _const()
const.c = 299792458 #light velocity, [m/s]
const.g = 6.67428e-11 #gravitation, [m^3/kg s^2]

const.omega = 7.292115e-5 #nominal earth rotation velocity [rad/sec]
const.gme = 3.986004418e14 #[m^3/s^2]
const.gms = 1.32712442076e20 #[m^3/s^2]
const.gmm = 4.904928372000000e+12
const.gmmerc = 2.203209000000012e+13 
const.gmvenu = 3.248585920000013e+14
const.gmmars = 4.282837521400020e+13
const.gmjupi = 1.267127648000003e+17
const.gmsatu = 3.794058520000017e+16
const.gmuran = 5.794548600000033e+15
const.gmnept = 6.836535000000019e+15
const.gmplut = 9.770000000000060e+11

const.Re = 6378136.55 #m
const.ae = 6378136.6  #Equatorial radius of the Earth, [m]
const.f = 1/298.25642  #Flattening factor of the Earth
const.MRs = 332945.943062 #mass ratio sun/earth
const.MRm = 0.012300034 #mass ratio moon/earth

const.a_tidefree = 6378136.6
const.ge_tidefree = 9.7803278
Hp = np.sqrt(8*np.pi/15)*const.omega**2*const.a_tidefree**4/const.gme
const.K_opp = 4*np.pi*const.g*const.a_tidefree*1025*Hp/3/const.ge_tidefree


