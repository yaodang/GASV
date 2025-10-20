####################################################################
# a script to download ionex file and solve zenith TEC of
# any given # (lat,lon,UTC)

# writer: yuanwei Wu NAOJ 2015 05 18
# reference: Stefan Schaer 1998
#            "IONEX: The IONosphere Map EXchange Format"
#
# may function FDZTEC, find the zenith TEC for LAT, LONG at TIME.
#
# for interpolation method, follow AIPS Task TECOR.FOR
#      (1) for UT at time T, find grid time T1 and T2, T1 < T < T2
#      (2) use 4-point grid to interpolate maps of T1 and T2,
#          solve two TEC1 and TEC2 at given lat, lon and UT
#      (3) weighted average TEC1 and TEC2 
####################################################################
#import matplotlib.pyplot as plt
import sys, os
import numpy as np
import subprocess
import matplotlib.pyplot as plt
from intertec_tst import *
#import astropy.units as u
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation,SkyCoord, AltAz,ICRS, GCRS, FK5
from astropy.coordinates import get_body_barycentric, get_body, get_moon
###################################################################
def read_source_coordinates(SU_file):
    sources, ra, dec = np.loadtxt(SU_file,usecols=(2,3,4),skiprows = 5, dtype=str,unpack=True)
    sources_dict = {}
    for i in range(len(sources)):
        sources_dict.update({sources[i] : ra[i].replace('D','E')+' '+dec[i].replace('D','E')})
    return sources_dict
###############################
#constant
freq = 8.385     #GHz
c = 299792458.0  #m/s

#station coordinates
JL = EarthLocation.from_geocentric(x=-2730771.75748*u.m,y=3713280.20958*u.m, z=4394196.34058*u.m)
SY = EarthLocation.from_geocentric(x=-1997654.55200*u.m,y=5718679.21500*u.m, z=1990021.26400*u.m)
KS = EarthLocation.from_geocentric(x= 1190830.46200*u.m,y=4786201.48500*u.m, z=4032514.38000*u.m)
 
# directories to save results
#
path_xyz = './xyz/'   # do not change path_xyz
if os.path.exists(path_xyz)==False:
   os.mkdir(path_xyz)
#
path_ionex = './ionex/'
if os.path.exists(path_ionex)==False:
   os.mkdir(path_ionex)
#
path = './2023UT1sessions/'
if os.path.exists(path)==False:
   os.mkdir(path)
#################################################################
#
tec_type = sys.argv[1]
inputs_delays = sys.argv[2]
SU_file = sys.argv[3]
#################################################################
infile1=path+inputs_delays
infile2=path+SU_file
f=open(infile1,'r')
lines=f.readlines()
T=[]
YEAR,DOY,UTC=[],[],[]
SOURCES = []
for i in range(len(lines)):
    if lines[i][0]!='#':
       temp=lines[i].split() 
       yr = int(temp[0])
       mn = int(temp[1])
       day= int(temp[2])
       hh = int(temp[3])
       mm = int(temp[4])
       ss = float(temp[5])
       source  = str(temp[6])
       #####################
       t=Time("%04i-%02i-%02i %02i:%02i:%06.3f"%(yr,mn,day,hh,mm,ss))
       T.append(t)
       SOURCES.append(source)

       doy = get_day_of_year(yr, mn, day)

       utc = hh+mm/60.0+ss/3600.0
       t=Time("%04i-%02i-%02i %02i:%02i:%06.3f"%(yr,mn,day,hh,mm,ss))
       YEAR.append(yr)
       DOY.append(doy)
       UTC.append(utc)

       ionos_file=tec_type+'g0'+str(doy)+'0.'+str(yr)[2:]+'i'
       if os.path.exists(path_ionex+ionos_file):
             pass
       else:
              get_TEC(yr,doy,tec_type)
              if os.path.exists(ionos_file+'.Z'):
                 os.popen(r'uncompress '+ionos_file+'.Z')
                 if os.path.exists(ionos_file):
                    os.popen(r'mv '+ionos_file+' '+path_ionex+ionos_file)
                    print('mv '+ionos_file+' '+path_ionex+ionos_file)

sources_dict = read_source_coordinates(infile2)
RA,DEC = [],[]
for i in range(len(SOURCES)):
    RA.append(np.float64(sources_dict[SOURCES[i]].split()[0]))
    DEC.append(np.float64(sources_dict[SOURCES[i]].split()[1]))
#if False:
if True:
 ######################################################################################################### 
 SAT_JL=SkyCoord(RA, DEC, frame="icrs", unit="deg",obstime=T,location=JL)
 SAT_SY=SkyCoord(RA, DEC, frame="icrs", unit="deg",obstime=T,location=SY)
 SAT_KS=SkyCoord(RA, DEC, frame="icrs", unit="deg",obstime=T,location=KS)
 ################################
 SAT_JL_AZEL=SAT_JL.altaz
 SAT_SY_AZEL=SAT_SY.altaz
 SAT_KS_AZEL=SAT_KS.altaz
 ###############################
 JL_AZ=SAT_JL_AZEL.az.value
 JL_EL=SAT_JL_AZEL.alt.value
 SY_AZ=SAT_SY_AZEL.az.value
 SY_EL=SAT_SY_AZEL.alt.value
 KS_AZ=SAT_KS_AZEL.az.value
 KS_EL=SAT_KS_AZEL.alt.value
 #
 ##################################################################
 #
 start_line = 0
 outfile = 'stec_'+inputs_delays+'.txt'
 f = open(path+outfile,'w')
 f.writelines('!UTC                     JL_delay     KS_delay     SY_delay       JL-KS         JL-SY         KS-SY\n')
 f.writelines('!                         (sec)        (sec)        (sec)         (sec)         (sec)         (sec)\n')
 #####################################3
 JL_LAT  = JL.latitude.value
 JL_LONG = JL.longitude.value
 SY_LAT  = SY.latitude.value
 SY_LONG = SY.longitude.value
 KS_LAT  = KS.latitude.value  
 KS_LONG = KS.longitude.value 
 #
 #for i in range(start_line, start_line+24*60):
 for i in range(len(UTC)):
 #for i in range(start_line, start_line+3):
    (JL_STEC, JL_E_STEC) = FDSTEC(JL_LONG,JL_LAT,JL_EL[i],JL_AZ[i],YEAR[i],DOY[i],UTC[i],tec_type,0)
    (SY_STEC, SY_E_STEC) = FDSTEC(SY_LONG,SY_LAT,SY_EL[i],SY_AZ[i],YEAR[i],DOY[i],UTC[i],tec_type,0)
    (KS_STEC, KS_E_STEC) = FDSTEC(KS_LONG,KS_LAT,KS_EL[i],KS_AZ[i],YEAR[i],DOY[i],UTC[i],tec_type,0)
 
    #calc baseline ionosphere delay
    #TEC, ETEC in unit of 0.1 TECU, change to TECU
    jl_delay = stec2delay(JL_STEC/10.0,freq)
    ks_delay = stec2delay(KS_STEC/10.0,freq)
    sy_delay = stec2delay(SY_STEC/10.0,freq)
 
    jl_sy_delay = sy_delay-jl_delay
    jl_ks_delay = ks_delay-jl_delay
    ks_sy_delay = sy_delay-ks_delay
 
    line = '%s %12.4e %12.4e %12.4e %12.4e %12.4e %12.4e'%(T[i],jl_delay, ks_delay, sy_delay, jl_ks_delay, jl_sy_delay, ks_sy_delay)
    f.writelines(line+'\n')
 f.close()    
