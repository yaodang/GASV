#!/usr/bin/env python3

import sys
import math
import numpy as np

#from constant import const
#from time_transfer import *
from COMMON import *

def APG(phi,lam,az,el):
    """
    Determines the asymmetric delay in meters caused by gradients
    ---------------------
    input:
        phi            : Latitude [rad]
        lam            : Longitude [rad]
        az             : Azimuth from north [rad]
        el             : Elevation angle [rad]
    output: 
        d              : Gradient delay [m]
        grn,gre        : North gradient and East gradient [mm]
    ---------------------
    """ 
    a_n = np.array([ 2.8959E-02,-4.6440E-01,-8.6531E-03, 1.1836E-01,-2.4168E-02,\
                    -6.9072E-05, 2.6783E-01,-1.1697E-03,-2.3396E-03,-1.6206E-03,\
                    -7.4883E-02, 1.3583E-02, 1.7750E-03, 3.2496E-04, 8.8051E-05,\
                     9.6532E-02, 1.3192E-02, 5.5250E-04, 4.0507E-04,-5.4758E-06,\
                     9.4260E-06,-1.0872E-01, 5.7551E-03, 5.3986E-05,-2.3753E-04,\
                    -3.8241E-05, 1.7377E-06,-4.4135E-08, 2.1863E-01, 2.0228E-02,\
                    -2.0127E-04,-3.3669E-04, 8.7575E-06, 7.0461E-07,-4.0001E-08,\
                    -4.5911E-08,-3.1945E-03,-5.1369E-03, 3.0684E-04, 2.4459E-05,\
                     7.6575E-06,-5.5319E-07, 3.5133E-08, 1.1074E-08, 3.4623E-09,\
                    -1.5845E-01,-2.0376E-02,-4.0081E-04, 2.2062E-04,-7.9179E-06,\
                    -1.6441E-07,-5.0004E-08, 8.0689E-10,-2.3813E-10,-2.4483E-10])
    
    b_n = np.array([ 0.0000E+00, 0.0000E+00,-1.1930E-02, 0.0000E+00, 9.8349E-03,\
                    -1.6861E-03, 0.0000E+00, 4.3338E-03, 6.1707E-03, 7.4635E-04,\
                     0.0000E+00, 3.5124E-03, 2.1967E-03, 4.2029E-04, 2.4476E-06,\
                     0.0000E+00, 4.1373E-04,-2.3281E-03, 2.7382E-04,-8.5220E-05,\
                     1.4204E-05, 0.0000E+00,-8.0076E-03, 4.5587E-05,-5.8053E-05,\
                    -1.1021E-05, 7.2338E-07,-1.9827E-07, 0.0000E+00,-3.9229E-03,\
                    -4.0697E-04,-1.6992E-04, 5.4705E-06,-4.4594E-06, 2.0121E-07,\
                    -7.7840E-08, 0.0000E+00,-3.2916E-03,-1.2302E-03,-6.5735E-06,\
                    -3.1840E-06,-8.9836E-07, 1.1870E-07,-5.8781E-09,-2.9124E-09,\
                     0.0000E+00, 1.0759E-02,-6.6074E-05,-4.0635E-05, 8.7141E-06,\
                     6.4567E-07,-4.4684E-08,-5.0293E-11, 2.7723E-10, 1.6903E-10])
        
    a_e = np.array([-2.4104E-03, 1.1408E-04,-3.4621E-04, 1.6565E-03,-4.0620E-03,\
                    -6.8424E-03,-3.3718E-04, 7.3857E-03,-1.3324E-03,-1.5645E-03,\
                     4.6444E-03, 1.0296E-03, 3.6253E-03, 4.0329E-04, 3.1943E-04,\
                    -7.1992E-04, 4.8706E-03, 9.4300E-04, 2.0765E-04,-5.0987E-06,\
                    -7.1741E-06,-1.3131E-02, 2.9099E-04,-2.2509E-04, 2.6716E-04,\
                    -8.1815E-05, 8.4297E-06,-9.2378E-07,-5.8095E-04, 2.7501E-03,\
                     4.3659E-04,-8.2990E-06,-1.4808E-05, 2.2033E-06,-3.3215E-07,\
                     2.8858E-08, 9.9968E-03, 4.9291E-04, 3.3739E-05, 2.4696E-06,\
                    -8.1749E-06,-9.0052E-07, 2.0153E-07,-1.0271E-08, 1.8249E-09,\
                     3.0578E-03, 1.1229E-03,-1.9977E-04, 4.4581E-06,-7.6921E-06,\
                    -2.8308E-07, 1.0305E-07,-6.9026E-09, 1.5523E-10,-1.0395E-10])
        
    b_e = np.array([ 0.0000E+00, 0.0000E+00,-2.5396E-03, 0.0000E+00, 9.2146E-03,\
                    -7.5836E-03, 0.0000E+00, 1.2765E-02,-1.1436E-03, 1.7909E-04,\
                     0.0000E+00, 2.9318E-03,-6.8541E-04, 9.5775E-04, 2.4596E-05,\
                     0.0000E+00, 3.5662E-03,-1.3949E-03,-3.4597E-04,-5.8236E-05,\
                     5.6956E-06, 0.0000E+00,-5.0164E-04,-6.5585E-04, 1.1134E-05,\
                     2.3315E-05,-4.0521E-06,-4.1747E-07, 0.0000E+00, 5.1650E-04,\
                    -1.0483E-03, 5.8109E-06, 1.6406E-05,-1.6261E-06, 6.2992E-07,\
                     1.3134E-08, 0.0000E+00,-6.1449E-03,-3.2511E-04, 1.7646E-04,\
                     7.5326E-06,-1.1946E-06, 5.1217E-08, 2.4618E-08, 3.6290E-09,\
                     0.0000E+00, 3.6769E-03,-9.7683E-04,-3.2096E-07, 1.3860E-06,\
                    -6.2832E-09, 2.6918E-09, 2.5705E-09,-2.4401E-09,-3.7917E-11])
    
    nmax = 9
    
    V,W = VW(nmax, phi, lam)
           
    GRN = 0
    GRE = 0
    I = 0
    for n in range(0,nmax+1):
        for m in range(n+1):
            GRN += (a_n[I]*V[n,m] + b_n[I]*W[n,m])
            GRE += (a_e[I]*V[n,m] + b_e[I]*W[n,m])
            I += 1
            
    d = 1.0/(np.sin(el)*np.tan(el)+0.0031)*(GRN*np.cos(az)+GRE*np.sin(az))/1000  #[m]
    return d,GRN,GRE

def GPT(mjd, phi, lam, hell):
    """
    Get Global Pressure and Temperature (Boehm et al. 2007)
    ---------------------
    input:
        mjd            : Modified Julian Date
        phi            : Latitude [rad]
        lam            : Longitude [rad]
        hell           : Height in [m]
    output: 
        P              : pressure [hPa]
        T              : temperature [C]
    ---------------------
    reference:
        Boehm, J., Heinkelmann, R. and Schuh, H., 2007, "Short Note: A
        Global model of pressure and temperature for geodetic applications",
        Journal of Geodesy, 81(10), pp. 679-683.
    """ 
    a_geoid = np.array([-5.6195E-001,-6.0794E-002,-2.0125E-001,-6.4180E-002,-3.6997E-002,\
                        +1.0098E+001,+1.6436E+001,+1.4065E+001,+1.9881E+000,+6.4414E-001,\
                        -4.7482E+000,-3.2290E+000,+5.0652E-001,+3.8279E-001,-2.6646E-002,\
                        +1.7224E+000,-2.7970E-001,+6.8177E-001,-9.6658E-002,-1.5113E-002,\
                        +2.9206E-003,-3.4621E+000,-3.8198E-001,+3.2306E-002,+6.9915E-003,\
                        -2.3068E-003,-1.3548E-003,+4.7324E-006,+2.3527E+000,+1.2985E+000,\
                        +2.1232E-001,+2.2571E-002,-3.7855E-003,+2.9449E-005,-1.6265E-004,\
                        +1.1711E-007,+1.6732E+000,+1.9858E-001,+2.3975E-002,-9.0013E-004,\
                        -2.2475E-003,-3.3095E-005,-1.2040E-005,+2.2010E-006,-1.0083E-006,\
                        +8.6297E-001,+5.8231E-001,+2.0545E-002,-7.8110E-003,-1.4085E-004,\
                        -8.8459E-006,+5.7256E-006,-1.5068E-006,+4.0095E-007,-2.4185E-008])
    
    b_geoid = np.array([+0.0000E+000,+0.0000E+000,-6.5993E-002,+0.0000E+000,+6.5364E-002,\
                        -5.8320E+000,+0.0000E+000,+1.6961E+000,-1.3557E+000,+1.2694E+000,\
                        +0.0000E+000,-2.9310E+000,+9.4805E-001,-7.6243E-002,+4.1076E-002,\
                        +0.0000E+000,-5.1808E-001,-3.4583E-001,-4.3632E-002,+2.2101E-003,\
                        -1.0663E-002,+0.0000E+000,+1.0927E-001,-2.9463E-001,+1.4371E-003,\
                        -1.1452E-002,-2.8156E-003,-3.5330E-004,+0.0000E+000,+4.4049E-001,\
                        +5.5653E-002,-2.0396E-002,-1.7312E-003,+3.5805E-005,+7.2682E-005,\
                        +2.2535E-006,+0.0000E+000,+1.9502E-002,+2.7919E-002,-8.1812E-003,\
                        +4.4540E-004,+8.8663E-005,+5.5596E-005,+2.4826E-006,+1.0279E-006,\
                        +0.0000E+000,+6.0529E-002,-3.5824E-002,-5.1367E-003,+3.0119E-005,\
                        -2.9911E-005,+1.9844E-005,-1.2349E-006,-7.6756E-009,+5.0100E-008])
        
    ap_mean = np.array([+1.0108E+003,+8.4886E+000,+1.4799E+000,-1.3897E+001,+3.7516E-003,\
                        -1.4936E-001,+1.2232E+001,-7.6615E-001,-6.7699E-002,+8.1002E-003,\
                        -1.5874E+001,+3.6614E-001,-6.7807E-002,-3.6309E-003,+5.9966E-004,\
                        +4.8163E+000,-3.7363E-001,-7.2071E-002,+1.9998E-003,-6.2385E-004,\
                        -3.7916E-004,+4.7609E+000,-3.9534E-001,+8.6667E-003,+1.1569E-002,\
                        +1.1441E-003,-1.4193E-004,-8.5723E-005,+6.5008E-001,-5.0889E-001,\
                        -1.5754E-002,-2.8305E-003,+5.7458E-004,+3.2577E-005,-9.6052E-006,\
                        -2.7974E-006,+1.3530E+000,-2.7271E-001,-3.0276E-004,+3.6286E-003,\
                        -2.0398E-004,+1.5846E-005,-7.7787E-006,+1.1210E-006,+9.9020E-008,\
                        +5.5046E-001,-2.7312E-001,+3.2532E-003,-2.4277E-003,+1.1596E-004,\
                        +2.6421E-007,-1.3263E-006,+2.7322E-007,+1.4058E-007,+4.9414E-009])

    bp_mean = np.array([+0.0000E+000,+0.0000E+000,-1.2878E+000,+0.0000E+000,+7.0444E-001,\
                        +3.3222E-001,+0.0000E+000,-2.9636E-001,+7.2248E-003,+7.9655E-003,\
                        +0.0000E+000,+1.0854E+000,+1.1145E-002,-3.6513E-002,+3.1527E-003,\
                        +0.0000E+000,-4.8434E-001,+5.2023E-002,-1.3091E-002,+1.8515E-003,\
                        +1.5422E-004,+0.0000E+000,+6.8298E-001,+2.5261E-003,-9.9703E-004,\
                        -1.0829E-003,+1.7688E-004,-3.1418E-005,+0.0000E+000,-3.7018E-001,\
                        +4.3234E-002,+7.2559E-003,+3.1516E-004,+2.0024E-005,-8.0581E-006,\
                        -2.3653E-006,+0.0000E+000,+1.0298E-001,-1.5086E-002,+5.6186E-003,\
                        +3.2613E-005,+4.0567E-005,-1.3925E-006,-3.6219E-007,-2.0176E-008,\
                        +0.0000E+000,-1.8364E-001,+1.8508E-002,+7.5016E-004,-9.6139E-005,\
                        -3.1995E-006,+1.3868E-007,-1.9486E-007,+3.0165E-010,-6.4376E-010])

    ap_amp = np.array([-1.0444E-001,+1.6618E-001,-6.3974E-002,+1.0922E+000,+5.7472E-001,\
                       -3.0277E-001,-3.5087E+000,+7.1264E-003,-1.4030E-001,+3.7050E-002,\
                       +4.0208E-001,-3.0431E-001,-1.3292E-001,+4.6746E-003,-1.5902E-004,\
                       +2.8624E+000,-3.9315E-001,-6.4371E-002,+1.6444E-002,-2.3403E-003,\
                       +4.2127E-005,+1.9945E+000,-6.0907E-001,-3.5386E-002,-1.0910E-003,\
                       -1.2799E-004,+4.0970E-005,+2.2131E-005,-5.3292E-001,-2.9765E-001,\
                       -3.2877E-002,+1.7691E-003,+5.9692E-005,+3.1725E-005,+2.0741E-005,\
                       -3.7622E-007,+2.6372E+000,-3.1165E-001,+1.6439E-002,+2.1633E-004,\
                       +1.7485E-004,+2.1587E-005,+6.1064E-006,-1.3755E-008,-7.8748E-008,\
                       -5.9152E-001,-1.7676E-001,+8.1807E-003,+1.0445E-003,+2.3432E-004,\
                       +9.3421E-006,+2.8104E-006,-1.5788E-007,-3.0648E-008,+2.6421E-010])

    bp_amp = np.array([+0.0000E+000,+0.0000E+000,+9.3340E-001,+0.0000E+000,+8.2346E-001,\
                       +2.2082E-001,+0.0000E+000,+9.6177E-001,-1.5650E-002,+1.2708E-003,\
                       +0.0000E+000,-3.9913E-001,+2.8020E-002,+2.8334E-002,+8.5980E-004,\
                       +0.0000E+000,+3.0545E-001,-2.1691E-002,+6.4067E-004,-3.6528E-005,\
                       -1.1166E-004,+0.0000E+000,-7.6974E-002,-1.8986E-002,+5.6896E-003,\
                       -2.4159E-004,-2.3033E-004,-9.6783E-006,+0.0000E+000,-1.0218E-001,\
                       -1.3916E-002,-4.1025E-003,-5.1340E-005,-7.0114E-005,-3.3152E-007,\
                       +1.6901E-006,+0.0000E+000,-1.2422E-002,+2.5072E-003,+1.1205E-003,\
                       -1.3034E-004,-2.3971E-005,-2.6622E-006,+5.7852E-007,+4.5847E-008,\
                       +0.0000E+000,+4.4777E-002,-3.0421E-003,+2.6062E-005,-7.2421E-005,\
                       +1.9119E-006,+3.9236E-007,+2.2390E-007,+2.9765E-009,-4.6452E-009])

    at_mean = np.array([+1.6257E+001,+2.1224E+000,+9.2569E-001,-2.5974E+001,+1.4510E+000,\
                        +9.2468E-002,-5.3192E-001,+2.1094E-001,-6.9210E-002,-3.4060E-002,\
                        -4.6569E+000,+2.6385E-001,-3.6093E-002,+1.0198E-002,-1.8783E-003,\
                        +7.4983E-001,+1.1741E-001,+3.9940E-002,+5.1348E-003,+5.9111E-003,\
                        +8.6133E-006,+6.3057E-001,+1.5203E-001,+3.9702E-002,+4.6334E-003,\
                        +2.4406E-004,+1.5189E-004,+1.9581E-007,+5.4414E-001,+3.5722E-001,\
                        +5.2763E-002,+4.1147E-003,-2.7239E-004,-5.9957E-005,+1.6394E-006,\
                        -7.3045E-007,-2.9394E+000,+5.5579E-002,+1.8852E-002,+3.4272E-003,\
                        -2.3193E-005,-2.9349E-005,+3.6397E-007,+2.0490E-006,-6.4719E-008,\
                        -5.2225E-001,+2.0799E-001,+1.3477E-003,+3.1613E-004,-2.2285E-004,\
                        -1.8137E-005,-1.5177E-007,+6.1343E-007,+7.8566E-008,+1.0749E-009])
    
    bt_mean = np.array([+0.0000E+000,+0.0000E+000,+1.0210E+000,+0.0000E+000,+6.0194E-001,\
                        +1.2292E-001,+0.0000E+000,-4.2184E-001,+1.8230E-001,+4.2329E-002,\
                        +0.0000E+000,+9.3312E-002,+9.5346E-002,-1.9724E-003,+5.8776E-003,\
                        +0.0000E+000,-2.0940E-001,+3.4199E-002,-5.7672E-003,-2.1590E-003,\
                        +5.6815E-004,+0.0000E+000,+2.2858E-001,+1.2283E-002,-9.3679E-003,\
                        -1.4233E-003,-1.5962E-004,+4.0160E-005,+0.0000E+000,+3.6353E-002,\
                        -9.4263E-004,-3.6762E-003,+5.8608E-005,-2.6391E-005,+3.2095E-006,\
                        -1.1605E-006,+0.0000E+000,+1.6306E-001,+1.3293E-002,-1.1395E-003,\
                        +5.1097E-005,+3.3977E-005,+7.6449E-006,-1.7602E-007,-7.6558E-008,\
                        +0.0000E+000,-4.5415E-002,-1.8027E-002,+3.6561E-004,-1.1274E-004,\
                        +1.3047E-005,+2.0001E-006,-1.5152E-007,-2.7807E-008,+7.7491E-009])

    at_amp = np.array([-1.8654E+000,-9.0041E+000,-1.2974E-001,-3.6053E+000,+2.0284E-002,\
                       +2.1872E-001,-1.3015E+000,+4.0355E-001,+2.2216E-001,-4.0605E-003,\
                       +1.9623E+000,+4.2887E-001,+2.1437E-001,-1.0061E-002,-1.1368E-003,\
                       -6.9235E-002,+5.6758E-001,+1.1917E-001,-7.0765E-003,+3.0017E-004,\
                       +3.0601E-004,+1.6559E+000,+2.0722E-001,+6.0013E-002,+1.7023E-004,\
                       -9.2424E-004,+1.1269E-005,-6.9911E-006,-2.0886E+000,-6.7879E-002,\
                       -8.5922E-004,-1.6087E-003,-4.5549E-005,+3.3178E-005,-6.1715E-006,\
                       -1.4446E-006,-3.7210E-001,+1.5775E-001,-1.7827E-003,-4.4396E-004,\
                       +2.2844E-004,-1.1215E-005,-2.1120E-006,-9.6421E-007,-1.4170E-008,\
                       +7.8720E-001,-4.4238E-002,-1.5120E-003,-9.4119E-004,+4.0645E-006,\
                       -4.9253E-006,-1.8656E-006,-4.0736E-007,-4.9594E-008,+1.6134E-009])
    
    bt_amp = np.array([+0.0000E+000,+0.0000E+000,-8.9895E-001,+0.0000E+000,-1.0790E+000,\
                       -1.2699E-001,+0.0000E+000,-5.9033E-001,+3.4865E-002,-3.2614E-002,\
                       +0.0000E+000,-2.4310E-002,+1.5607E-002,-2.9833E-002,-5.9048E-003,\
                       +0.0000E+000,+2.8383E-001,+4.0509E-002,-1.8834E-002,-1.2654E-003,\
                       -1.3794E-004,+0.0000E+000,+1.3306E-001,+3.4960E-002,-3.6799E-003,\
                       -3.5626E-004,+1.4814E-004,+3.7932E-006,+0.0000E+000,+2.0801E-001,\
                       +6.5640E-003,-3.4893E-003,-2.7395E-004,+7.4296E-005,-7.9927E-006,\
                       -1.0277E-006,+0.0000E+000,+3.6515E-002,-7.4319E-003,-6.2873E-004,\
                       -8.2461E-005,+3.1095E-005,-5.3860E-007,-1.2055E-007,-1.1517E-007,\
                       +0.0000E+000,+3.1404E-002,+1.5580E-002,-1.1428E-003,+3.3529E-005,\
                       +1.0387E-005,-1.9378E-006,-2.7327E-007,+7.5833E-009,-9.2323E-009])
    nmax = 9
    doy = mjd - 44239 + 1 - 28
    V,W = VW(nmax, phi, lam)
    
    # geoidal height
    undu = 0.0E0
    # surface pressure on the geoid
    apm = 0.0
    apa = 0.0
    # surface temperature on the geoid
    atm = 0.0
    ata = 0.0
    
    I = 0
    for n in range(nmax+1):
        for m in range(n+1):
            undu += a_geoid[I]*V[n,m] + b_geoid[I]*W[n,m]
            apm += ap_mean[I]*V[n,m] + bp_mean[I]*W[n,m]
            apa += ap_amp[I]*V[n,m] + bp_amp[I]*W[n,m]
            atm += at_mean[I]*V[n,m] + bt_mean[I]*W[n,m]
            ata += at_amp[I]*V[n,m] + bt_amp[I]*W[n,m]
            I += 1
            
    hort = hell - undu
    press = (apm+apa*np.cos(2*np.pi*doy/365.25)) * (1-0.0000226*hort)**5.225        
    temp = atm + ata*np.cos(2*np.pi*doy/365.25) - 0.0065*hort
    
    return press, temp

def GMF(mjd, phi, lam, hell, zd):
    """
    Global Mapping Function (Boehm et al. 2006)
    ---------------------
    input:
        mjd            : Modified Julian Date
        phi            : Latitude [rad]
        lam            : Longitude [rad]
        hell           : Height in [m]
        zd             : Zenith distance [rad]
    output: 
        mh,mw          : Hydrostatic and Wet mapping function
    ---------------------
    """ 
    ah_mean = np.array([+1.2517E+02, +8.503E-01, +6.936E-02, -6.760E+00, +1.771E-01,\
                         +1.130E-02, +5.963E-01, +1.808E-02, +2.801E-03, -1.414E-03,\
 			             -1.212E+00, +9.300E-02, +3.683E-03, +1.095E-03, +4.671E-05,\
     			         +3.959E-01, -3.867E-02, +5.413E-03, -5.289E-04, +3.229E-04,\
     			         +2.067E-05, +3.000E-01, +2.031E-02, +5.900E-03, +4.573E-04,\
     			         -7.619E-05, +2.327E-06, +3.845E-06, +1.182E-01, +1.158E-02,\
     			         +5.445E-03, +6.219E-05, +4.204E-06, -2.093E-06, +1.540E-07,\
     			         -4.280E-08, -4.751E-01, -3.490E-02, +1.758E-03, +4.019E-04,\
     			         -2.799E-06, -1.287E-06, +5.468E-07, +7.580E-08, -6.300E-09,\
     			         -1.160E-01, +8.301E-03, +8.771E-04, +9.955E-05, -1.718E-06,\
     			         -2.012E-06, +1.170E-08, +1.790E-08, -1.300E-09, +1.000E-10])
    
    bh_mean = np.array([+0.000E+00, +0.000E+00, +3.249E-02, +0.000E+00, +3.324E-02,\
                        +1.850E-02, +0.000E+00, -1.115E-01, +2.519E-02, +4.923E-03,\
                        +0.000E+00, +2.737E-02, +1.595E-02, -7.332E-04, +1.933E-04,\
                        +0.000E+00, -4.796E-02, +6.381E-03, -1.599E-04, -3.685E-04,\
                        +1.815E-05, +0.000E+00, +7.033E-02, +2.426E-03, -1.111E-03,\
                        -1.357E-04, -7.828E-06, +2.547E-06, +0.000E+00, +5.779E-03,\
                        +3.133E-03, -5.312E-04, -2.028E-05, +2.323E-07, -9.100E-08,\
                        -1.650E-08, +0.000E+00, +3.688E-02, -8.638E-04, -8.514E-05,\
                        -2.828E-05, +5.403E-07, +4.390E-07, +1.350E-08, +1.800E-09,\
                        +0.000E+00, -2.736E-02, -2.977E-04, +8.113E-05, +2.329E-07,\
                        +8.451E-07, +4.490E-08, -8.100E-09, -1.500E-09, +2.000E-10])
    
    ah_amp =np.array([-2.738E-01, -2.837E+00, +1.298E-02, -3.588E-01, +2.413E-02,\
                      +3.427E-02, -7.624E-01, +7.272E-02, +2.160E-02, -3.385E-03,\
                      +4.424E-01, +3.722E-02, +2.195E-02, -1.503E-03, +2.426E-04,\
                      +3.013E-01, +5.762E-02, +1.019E-02, -4.476E-04, +6.790E-05,\
                      +3.227E-05, +3.123E-01, -3.535E-02, +4.840E-03, +3.025E-06,\
                      -4.363E-05, +2.854E-07, -1.286E-06, -6.725E-01, -3.730E-02,\
                      +8.964E-04, +1.399E-04, -3.990E-06, +7.431E-06, -2.796E-07,\
                      -1.601E-07, +4.068E-02, -1.352E-02, +7.282E-04, +9.594E-05,\
                      +2.070E-06, -9.620E-08, -2.742E-07, -6.370E-08, -6.300E-09,\
                      +8.625E-02, -5.971E-03, +4.705E-04, +2.335E-05, +4.226E-06,\
                      +2.475E-07, -8.850E-08, -3.600E-08, -2.900E-09, +0.000E+00])
    
    bh_amp = np.array([+0.000E+00, +0.000E+00, -1.136E-01, +0.000E+00, -1.868E-01,\
                       -1.399E-02, +0.000E+00, -1.043E-01, +1.175E-02, -2.240E-03,\
                       +0.000E+00, -3.222E-02, +1.333E-02, -2.647E-03, -2.316E-05,\
                       +0.000E+00, +5.339E-02, +1.107E-02, -3.116E-03, -1.079E-04,\
                       -1.299E-05, +0.000E+00, +4.861E-03, +8.891E-03, -6.448E-04,\
                       -1.279E-05, +6.358E-06, -1.417E-07, +0.000E+00, +3.041E-02,\
                       +1.150E-03, -8.743E-04, -2.781E-05, +6.367E-07, -1.140E-08,\
                       -4.200E-08, +0.000E+00, -2.982E-02, -3.000E-03, +1.394E-05,\
                       -3.290E-05, -1.705E-07, +7.440E-08, +2.720E-08, -6.600E-09,\
                       +0.000E+00, +1.236E-02, -9.981E-04, -3.792E-05, -1.355E-05,\
                       +1.162E-06, -1.789E-07, +1.470E-08, -2.400E-09, -4.000E-10])
    
    aw_mean = np.array([+5.640E+01, +1.555E+00, -1.011E+00, -3.975E+00, +3.171E-02,\
                        +1.065E-01, +6.175E-01, +1.376E-01, +4.229E-02, +3.028E-03,\
                        +1.688E+00, -1.692E-01, +5.478E-02, +2.473E-02, +6.059E-04,\
                        +2.278E+00, +6.614E-03, -3.505E-04, -6.697E-03, +8.402E-04,\
                        +7.033E-04, -3.236E+00, +2.184E-01, -4.611E-02, -1.613E-02,\
                        -1.604E-03, +5.420E-05, +7.922E-05, -2.711E-01, -4.406E-01,\
                        -3.376E-02, -2.801E-03, -4.090E-04, -2.056E-05, +6.894E-06,\
                        +2.317E-06, +1.941E+00, -2.562E-01, +1.598E-02, +5.449E-03,\
                        +3.544E-04, +1.148E-05, +7.503E-06, -5.667E-07, -3.660E-08,\
                        +8.683E-01, -5.931E-02, -1.864E-03, -1.277E-04, +2.029E-04,\
                        +1.269E-05, +1.629E-06, +9.660E-08, -1.015E-07, -5.000E-10])
    
    bw_mean = np.array([+0.000E+00, +0.000E+00, +2.592E-01, +0.000E+00, +2.974E-02,\
                        -5.471E-01, +0.000E+00, -5.926E-01, -1.030E-01, -1.567E-02,\
                        +0.000E+00, +1.710E-01, +9.025E-02, +2.689E-02, +2.243E-03,\
                        +0.000E+00, +3.439E-01, +2.402E-02, +5.410E-03, +1.601E-03,\
                        +9.669E-05, +0.000E+00, +9.502E-02, -3.063E-02, -1.055E-03,\
                        -1.067E-04, -1.130E-04, +2.124E-05, +0.000E+00, -3.129E-01,\
                        +8.463E-03, +2.253E-04, +7.413E-05, -9.376E-05, -1.606E-06,\
                        +2.060E-06, +0.000E+00, +2.739E-01, +1.167E-03, -2.246E-05,\
                        -1.287E-04, -2.438E-05, -7.561E-07, +1.158E-06, +4.950E-08,\
                        +0.000E+00, -1.344E-01, +5.342E-03, +3.775E-04, -6.756E-05,\
                        -1.686E-06, -1.184E-06, +2.768E-07, +2.730E-08, +5.700E-09])
    
    aw_amp = np.array([+1.023E-01, -2.695E+00, +3.417E-01, -1.405E-01, +3.175E-01,\
                       +2.116E-01, +3.536E+00, -1.505E-01, -1.660E-02, +2.967E-02,\
                       +3.819E-01, -1.695E-01, -7.444E-02, +7.409E-03, -6.262E-03,\
                       -1.836E+00, -1.759E-02, -6.256E-02, -2.371E-03, +7.947E-04,\
                       +1.501E-04, -8.603E-01, -1.360E-01, -3.629E-02, -3.706E-03,\
                       -2.976E-04, +1.857E-05, +3.021E-05, +2.248E+00, -1.178E-01,\
                       +1.255E-02, +1.134E-03, -2.161E-04, -5.817E-06, +8.836E-07,\
                       -1.769E-07, +7.313E-01, -1.188E-01, +1.145E-02, +1.011E-03,\
                       +1.083E-04, +2.570E-06, -2.140E-06, -5.710E-08, +2.000E-08,\
                       -1.632E+00, -6.948E-03, -3.893E-03, +8.592E-04, +7.577E-05,\
                       +4.539E-06, -3.852E-07, -2.213E-07, -1.370E-08, +5.800E-09])
    
    bw_amp = np.array([+0.000E+00, +0.000E+00, -8.865E-02, +0.000E+00, -4.309E-01,\
                       +6.340E-02, +0.000E+00, +1.162E-01, +6.176E-02, -4.234E-03,\
                       +0.000E+00, +2.530E-01, +4.017E-02, -6.204E-03, +4.977E-03,\
                       +0.000E+00, -1.737E-01, -5.638E-03, +1.488E-04, +4.857E-04,\
                       -1.809E-04, +0.000E+00, -1.514E-01, -1.685E-02, +5.333E-03,\
                       -7.611E-05, +2.394E-05, +8.195E-06, +0.000E+00, +9.326E-02,\
                       -1.275E-02, -3.071E-04, +5.374E-05, -3.391E-05, -7.436E-06,\
                       +6.747E-07, +0.000E+00, -8.637E-02, -3.807E-03, -6.833E-04,\
                       -3.861E-05, -2.268E-05, +1.454E-06, +3.860E-07, -1.068E-07,\
                       +0.000E+00, -2.658E-02, -1.947E-03, +7.131E-04, -3.506E-05,\
                       +1.885E-07, +5.792E-07, +3.990E-08, +2.000E-08, -5.700E-09])
    
    ap,bp = calcApBp(phi,lam)
    sine = math.sin(np.pi/2-zd)
    
    # Compute mapping function
    bh = 0.0029
    bw = 0.00146
    cw = 0.04391
    
    # hydrostatic 
    if phi < 0: # southern hemisphere
        phh = np.pi
        c11h = 0.007
        c10h = 0.002
    else:
        phh = 0
        c11h = 0.005
        c10h = 0.001
    
    doy = mjd - 44239 + 1 - 28
    ch = 0.062 + ((math.cos(doy*2*np.pi/365.25+phh)+1)*c11h/2+c10h)*(1-math.cos(phi))
    ah = (np.dot(ah_mean,ap)+np.dot(bh_mean,bp))*1E-5 + \
         (np.dot(ah_amp,ap)+np.dot(bh_amp,bp))*1E-5*math.cos(doy*2*np.pi/365.25)
    
    beta = bh/(sine+ch) 
    gamma = ah/(sine+beta)    
    gmfh = (1+ah/(1+bh/(1+ch)))/(sine+gamma)
    
    # Height correction for hydrostatic
    aht = 2.53E-5
    bht = 5.49E-3
    cht = 1.14E-3
    
    h_km = hell/1000
    beta = bht/(sine+cht)
    gamma = aht/(sine+beta)
    h_corr_coef = 1/sine - (1+aht/(1+bht/(1+cht)))/(sine+gamma)
    h_corr = h_corr_coef*h_km
    gmfh += h_corr
    
    # wet
    aw = (np.dot(aw_mean,ap)+np.dot(bw_mean,bp))*1E-5 + \
         (np.dot(aw_amp,ap)+np.dot(bw_amp,bp))*1E-5*math.cos(doy*2*np.pi/365.25)    
    
    beta = bw/(sine+cw)
    gamma = aw/(sine+beta)
    gmfw = (1+aw/(1+bw/(1+cw)))/(sine+gamma)

    return gmfh,gmfw

def GPT3(mjd,lat,lam,hell,choice,GPT3Data,zd):
    """
    GPT3 module for tropsphere
    ---------------------
    input:
        mjd            : Modified Julian Date
        phi            : Latitude given in radians
        lam            : Longitude given in radians
        hell           : Height in meters
        choice         : 1-no time variation but static quantities
                       : 0-with time variation (annual and semiannual terms)
        param          : the param struct
    output: 
        ah,aw          : mapping function coefficient
    ---------------------
    """
    grid = GPT3Data.trpGrid
    pvmf3 = GPT3Data.vmf3p
    
    [year,mon,day,hour,minute,sec] = mjd2date(mjd)
    doyd = date2doy(year,mon,day)
    pdoy = doyd/sum(month(year))
    doy = doyd + mjd - np.floor(mjd)
    
    ah = []
    aw = []
    T = []
    P = []
    
    if choice == 1:
        cfy = 0
        chy = 0
        sfy = 0
        shy = 0
    else:
        cfy = np.cos(doy/365.25*2*np.pi)
        chy = np.cos(doy/365.25*4*np.pi)
        sfy = np.sin(doy/365.25*2*np.pi)
        shy = np.sin(doy/365.25*4*np.pi)
        

    if lam < 0:
        plon = (lam+2*np.pi)*180/np.pi
    else:
        plon = lam*180/np.pi
        
    ppod = (-lat+np.pi/2)*180/np.pi
    ipod = np.floor((ppod+5)/5)
    ilon = np.floor((plon+5)/5)
    
    diffpod = (ppod-(ipod*5-2.5))/5
    difflon = (plon-(ilon*5-2.5))/5
    #print(ipod,ilon)
    if ipod == 37:
        ipod = 36
    if ilon == 73:
        ilon = 1
    if ilon == 0:
        ilon = 72
    #print(ipod-1)
    indxe = [int((ipod-1)*72 + ilon)-1]
    
    biliner = 0
    if ppod > 2.5 and ppod < 177.5:
        biliner = 1
        
    if biliner == 0:
        indx = indxe[0]
        undu = grid.u[indx]
        hgt = hell - undu
        
        ah.append(grid.ah[indx,0] + grid.ah[indx,1]*cfy + grid.ah[indx,2]*sfy + grid.ah[indx,3]*chy + grid.ah[indx,4]*shy)
        aw.append(grid.aw[indx,0] + grid.aw[indx,1]*cfy + grid.aw[indx,2]*sfy + grid.aw[indx,3]*chy + grid.aw[indx,4]*shy)
        
    else:
        ipod1 = ipod + np.sign(diffpod)
        ilon1 = ilon + np.sign(difflon)
        
        if ilon1 == 73:
            ilon1 = 1
        if ilon1 == 0:
            ilon1 = 72
        
        indxe.append(int((ipod1-1)*72+ilon)-1)
        indxe.append(int((ipod -1)*72+ilon1)-1)
        indxe.append(int((ipod1-1)*72+ilon1)-1)
        
        
        undul = grid.u[indxe]
        hgt = hell-undul
        
        ahl = grid.ah[indxe,0] + grid.ah[indxe,1]*cfy + grid.ah[indxe,2]*sfy + grid.ah[indxe,3]*chy + grid.ah[indxe,4]*shy
        awl = grid.aw[indxe,0] + grid.aw[indxe,1]*cfy + grid.aw[indxe,2]*sfy + grid.aw[indxe,3]*chy + grid.aw[indxe,4]*shy

        dnpod1 = abs(diffpod)
        dnpod2 = 1 - dnpod1
        dnlon1 = abs(difflon)
        dnlon2 = 1 - dnlon1
        
        R1 = dnpod2*ahl[0] + dnpod1*ahl[1]
        R2 = dnpod2*ahl[2] + dnpod1*ahl[3]
        ah.append(dnlon2*R1 + dnlon1*R2)
        
        R1 = dnpod2*awl[0] + dnpod1*awl[1]
        R2 = dnpod2*awl[2] + dnpod1*awl[3]
        aw.append(dnlon2*R1 + dnlon1*R2)
        
    mfh,mfw = VMF3_ht(pdoy,ah,aw,mjd,lat,lam,hell,zd,pvmf3)
            
    return mfh,mfw

def VMF3_ht(doy,ah,aw,mjd,lat,lam,hell,zd,pvmf3):
    el = np.pi/2 - zd
    polDist = np.pi/2 - lat
    nmax = 12
    
    V,W = VW(nmax, lat, lam)
    
    result = np.zeros(20)
    
    i = 0
    for n in range(nmax+1):
        for m in range(n+1):
            for j in range(5):
                result[j] = result[j] + (pvmf3.abh[:,j][i]*V[n,m] + pvmf3.bbh[:,j][i]*W[n,m])
            for j in range(5):
                result[5+j] = result[5+j] + (pvmf3.abw[:,j][i]*V[n,m] + pvmf3.bbw[:,j][i]*W[n,m])
            for j in range(5):
                result[10+j] = result[10+j] + (pvmf3.ach[:,j][i]*V[n,m] + pvmf3.bch[:,j][i]*W[n,m])
            for j in range(5):
                result[15+j] = result[15+j] + (pvmf3.acw[:,j][i]*V[n,m] + pvmf3.bcw[:,j][i]*W[n,m])
            i = i + 1
    
    bh = result[0] + result[1]*np.cos(2*doy*np.pi) + result[2]*np.sin(2*doy*np.pi) + result[3]*np.cos(4*doy*np.pi) + result[4]*np.sin(4*doy*np.pi)
    bw = result[5] + result[6]*np.cos(2*doy*np.pi) + result[7]*np.sin(2*doy*np.pi) + result[8]*np.cos(4*doy*np.pi) + result[9]*np.sin(4*doy*np.pi)
    ch = result[10] + result[11]*np.cos(2*doy*np.pi) + result[12]*np.sin(2*doy*np.pi) + result[13]*np.cos(4*doy*np.pi) + result[14]*np.sin(4*doy*np.pi)
    cw = result[15] + result[16]*np.cos(2*doy*np.pi) + result[17]*np.sin(2*doy*np.pi) + result[18]*np.cos(4*doy*np.pi) + result[19]*np.sin(4*doy*np.pi)

    vmf3_h = (1+(ah/(1+bh/(1+ch)))) / (np.sin(el)+(ah/(np.sin(el)+bh/(np.sin(el)+ch))))
    vmf3_w = (1+(aw/(1+bw/(1+cw)))) / (np.sin(el)+(aw/(np.sin(el)+bw/(np.sin(el)+cw))))
    
    a_ht = 2.53E-5
    b_ht = 5.49E-3
    c_ht = 1.14E-3
    h_ell_km = hell/1000
    ht_corr_coef = 1/np.sin(el)   -   (1+(a_ht/(1+b_ht/(1+c_ht))))  /  (np.sin(el)+(a_ht/(np.sin(el)+b_ht/(np.sin(el)+c_ht))))
    ht_corr      = ht_corr_coef * h_ell_km
    vmf3_h       = vmf3_h + ht_corr
    
    return vmf3_h[0],vmf3_w[0]

'''
def GPT3(mjd,lat,lam,hell,choice,grid):
    """
    GPT3 module for tropsphere
    ---------------------
    input:
        mjd            : Modified Julian Date
        phi            : Latitude given in radians
        lam            : Longitude given in radians
        hell           : Height in meters
        choice         : 1-no time variation but static quantities
                       : 0-with time variation (annual and semiannual terms)
        grid           : a cell containing all entries of the grid 'gpt3_5.grd'
    output: 
        ah,aw          : mapping function coefficient
    ---------------------
    """ 
    [year,mon,day] = mjd2date(mjd)
    doy = date2doy(year,mon,day)
    
    ah = []
    aw = []
    T = []
    P = []
    
    if choice == 1:
        cfy = 0
        chy = 0
        sfy = 0
        shy = 0
    else:
        cfy = np.cos(doy/365.25*2*np.pi)
        chy = np.cos(doy/365.25*4*np.pi)
        sfy = np.sin(doy/365.25*2*np.pi)
        shy = np.sin(doy/365.25*4*np.pi)
        
    nstat = len(lat)
    for i in range(nstat):
        if lam[i] < 0:
            plon = (lam[i]+2*np.pi)*180/np.pi
        else:
            plon = lam[i]*180/np.pi
            
        ppod = (-lat[i]+np.pi/2)*180/np.pi
        ipod = np.floor((ppod+5)/5)
        ilon = np.floor((plon+5)/5)
        
        diffpod = (ppod-(ipod*5-2.5))/5
        difflon = (plon-(ilon*5-2.5))/5
        
        if ipod == 37:
            ipod = 36
        if ilon == 73:
            ilon = 1
        if ilon == 0:
            ilon = 72
        
        indxe = [(ipod-1)*72 + ilon]
        
        biliner = 0
        if ppod > 2.5 and ppod < 177.5:
            biliner = 1
            
        if biliner == 0:
            indx = indxe[0]
            undu = grid.u[indx]
            hgt = hell[i] - undu
            
            ah.append(grid.ah[indx,0] + grid.ah[indx,1]*cfy + grid.ah[indx,2]*sfy + grid.ah[indx,3]*chy + grid.ah[indx,4]*shy)
            aw.append(grid.aw[indx,0] + grid.aw[indx,1]*cfy + grid.aw[indx,2]*sfy + grid.aw[indx,3]*chy + grid.aw[indx,4]*shy)
            
        else:
            ipod1 = ipod + np.sign(diffpod)
            ilon1 = ilon + np.sign(difflon)
            
            if ilon1 == 73:
                ilon1 = 1
            if ilon1 == 0:
                ilon1 = 72
            
            indxe.append((ipod1-1)*72+ilon)
            indxe.append((ipod -1)*72+ilon1)
            indxe.append((ipod1-1)*72+ilon1)
            
            undul = grid.u[indxe]
            hgt = hell[i]-undul
            
            ahl = grid.ah[indx,0] + grid.ah[indx,1]*cfy + grid.ah[indx,2]*sfy + grid.ah[indx,3]*chy + grid.ah[indx,4]*shy
            awl = grid.aw[indx,0] + grid.aw[indx,1]*cfy + grid.aw[indx,2]*sfy + grid.aw[indx,3]*chy + grid.aw[indx,4]*shy

            dnpod1 = abs(diffpod)
            dnpod2 = 1 - dnpod1
            dnlon1 = abs(diffpod)
            dnlon2 = 1 - dnlon1
            
            R1 = dnpod2*ahl[0] + dnpod1*ahl[1]
            R2 = dnpod2*ahl[2] + dnpod1*ahl[3]
            ah.append(dnlon2*R1 + dnlon1*R2)
            
            R1 = dnpod2*awl[0] + dnpod1*awl[1]
            R2 = dnpod2*awl[2] + dnpod1*awl[3]
            aw.append(dnlon2*R1 + dnlon1*R2)
            
    return ah,aw
'''    

def calcApBp(phi,lam):
    """
    Calculate spherical harmonics
    ---------------------
    input:

        phi            : Latitude given in radians
        lam            : Longitude given in radians
        hell           : Height in meters
    output: 
        ap,bp          : harmonics
    ---------------------
    """
    pnm = calcPnm(phi)
    ap = []
    bp = []
    for n in range(10):
        for m in range(n+1):
            ap.append(pnm[n,m]*np.cos(m*lam))
            bp.append(pnm[n,m]*np.sin(m*lam))
            
    return np.array(ap),np.array(bp)
            
def calcPnm(phi):
    pnm = np.zeros([10,10])
    for i in range(10):
        for j in range(min(i,9)+1):
            sum1 = 0
            for k in range(int((i-j)/2+1)):
                sum1 += (-1)**k*math.factorial(2*i-2*k+1)*np.sin(phi)**(i-j-2*k)/\
                     (math.factorial(k+1)*math.factorial(i-k+1)*math.factorial(i-j-2*k+1))
            pnm[i,j] = 0.5**i*math.sqrt((1-math.sin(phi)**2)**j)*sum1
            
    return pnm

def VW(num, phi, lam):
    """
    Calculate Legendre polynomials
    ---------------------
    input:
        num            : the 
        phi            : Latitude [rad]
        lam            : Longitude [rad]
    output: 
        V,W            : Legendre polynomials
    ---------------------
    """

    nmax = num
    mmax = num
    V = np.zeros([num+1,num+1])
    W = np.zeros([num+1,num+1])
    
    X = np.cos(phi)*np.cos(lam)
    Y = np.cos(phi)*np.sin(lam)
    Z = np.sin(phi)
    
    V[0,0] = 1.0
    V[1,0] = Z*V[0,0]
    
    for n in range(1,nmax):
        V[n+1,0] = ((2*n+1) * Z * V[n,0] - (n) * V[n-1,0]) / (n+1)
        
    for m in range(mmax):
        V[m+1,m+1] = (2*m+1) * (X*V[m,m] - Y*W[m,m])
        W[m+1,m+1] = (2*m+1) * (X*W[m,m] + Y*V[m,m])
        if m < mmax-1:
            V[m+2,m+1] = (2*m+3) * Z * V[m+1,m+1]
            W[m+2,m+1] = (2*m+3) * Z * W[m+1,m+1]
        for n in range(m+2,nmax):
            V[n+1,m+1] = ((2*n+1)*Z*V[n,m+1] - (n+m+1)*V[n-1,m+1]) / (n-m)
            W[n+1,m+1] = ((2*n+1)*Z*W[n,m+1] - (n+m+1)*W[n-1,m+1]) / (n-m)

    return V,W

#press,temp = GPT(55055,0.6708665767,-1.393397187,812.546)        
#gmfh,gmfw = GMF(55055, 0.6708665767, -1.393397187, 844.715, 1.278564131)
#d,grn,gre = APG(0.6274877539940092, 2.454994088489240, 0.2617993877991494, 0.8726646259971648)
