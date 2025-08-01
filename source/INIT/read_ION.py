#!/usr/bin/env python3

import os
import numpy as np
from COMMON.time_transfer import *
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation,SkyCoord



def readAndCreateIONFile(Param, scanInfo, stationInfo,sourceInfo):
    
    tec_type = 'jpl'
    
    time1 = scanInfo.scanTime[0]
    time2 = scanInfo.scanTime[-1]
    DOY1  = date2doy(int(time1[0]),int(time1[1]),int(time1[2]))
    DOY2  = date2doy(int(time2[0]),int(time2[1]),int(time2[2]))
    
    if DOY1 == DOY2:
        get_TEC(int(time1[0]),DOY1, Param.Setup.vgosdbPath, tec_type)
    else:
        get_TEC(int(time1[0]), DOY1, Param.Setup.vgosdbPath, tec_type)
        get_TEC(int(time2[0]), DOY2, Param.Setup.vgosdbPath, tec_type)
    
    ionDelay = []
    for iobs in range(len(scanInfo.Obs2Scan)):
        staIndex1 = scanInfo.Obs2Baseline[iobs,0]-1
        staIndex2 = scanInfo.Obs2Baseline[iobs,1]-1
        souIndex = scanInfo.Obs2Source[iobs]-1
        
        sta1xyz = stationInfo.posit[staIndex1]
        sta2xyz = stationInfo.posit[staIndex2]
        rade = sourceInfo.rade[souIndex]*180/np.pi
        
        sta1 = EarthLocation.from_geocentric(x=sta1xyz[0]*u.m,y=sta1xyz[1]*u.m, z=sta1xyz[2]*u.m)
        sta2 = EarthLocation.from_geocentric(x=sta2xyz[0]*u.m,y=sta2xyz[1]*u.m, z=sta2xyz[2]*u.m)
    
        ymdhms = scanInfo.scanTime[scanInfo.Obs2Scan[iobs]-1]
        DOY = date2doy(int(ymdhms[0]),int(ymdhms[1]),int(ymdhms[2]))
        UTC = ymdhms[3]+ymdhms[4]/60.0+ymdhms[5]/3600.0
        T = Time("%04i-%02i-%02i %02i:%02i:%06.3f"%(ymdhms[0],ymdhms[1],ymdhms[2],ymdhms[3],ymdhms[4],ymdhms[5]))

        SAT_1      = SkyCoord(rade[0], rade[1], frame="icrs", unit="deg", obstime=T, location=sta1)
        SAT_2      = SkyCoord(rade[0], rade[1], frame="icrs", unit="deg", obstime=T, location=sta2)
        SAT_1_AZEL = SAT_1.altaz
        SAT_2_AZEL = SAT_2.altaz
        AZ_1       = SAT_1_AZEL.az.value
        EL_1       = SAT_1_AZEL.alt.value
        AZ_2       = SAT_2_AZEL.az.value
        EL_2       = SAT_2_AZEL.alt.value
        
        LAT_1      = sta1.lat.value
        LONG_1     = sta1.lon.value
        LAT_2      = sta2.lat.value
        LONG_2     = sta2.lon.value
        
        (STEC_1, E_STEC_2) = FDSTEC(LONG_1, LAT_1, EL_1, AZ_1, int(ymdhms[0]), DOY, UTC, tec_type, 0)
        (STEC_2, E_STEC_2) = FDSTEC(LONG_2, LAT_2, EL_2, AZ_2, int(ymdhms[0]), DOY, UTC, tec_type, 0)
     
        #calc baseline ionosphere delay
        #TEC, ETEC in unit of 0.1 TECU, change to TECU
        if len(scanInfo.baseInfo[0]) == 2:
            refFreq = scanInfo.baseInfo[1][1][0]*1E-3
        else:
            refFreq = scanInfo.baseInfo[1][0][0]*1E-3
        delay1 = stec2delay(STEC_1/10.0,refFreq)
        delay2 = stec2delay(STEC_2/10.0,refFreq)
     
        ionDelay.append(delay2-delay1)
        
    return ionDelay

def FDSTEC(LONG,LAT,EL,AZ,YEAR,DOY,UT,MAP_TYPE,print_level):
    """
    inputs:
        LONG          station LONG in deg
        LAT           station LAT in deg
        EL            star/target in deg
        AZ            star/target AZ in deg
        YEAR          YEAR
        DOY           DOY day of year
        UT            UT in DOY
        MAP_TYPE      'jpl','cod','esa'
        print_level

    outputs:
        STEC 	      in unit of 0.1 TECU

    dependence:
        IONOS_intersection, FDZTEC, ZTEC2STEC
 
    Examples
      >>> import intertec_tst 
      >>> LONG = 141.132586
      >>> LAT = 39.133522
      >>> EL = 45.0
      >>> AZ = 135.0
      >>> YEAR=2015
      >>> DOY=208
      >>> UT=3.5
      >>> MAP_TYPE='cod'
      >>> (STEC, E_STEC) = intertec_tst.FDSTEC(LONG,LAT,EL,AZ,YEAR,DOY,UT,MAP_TYPE)
      
    """
    (IONOS_LONG,IONOS_LAT) = IONOS_intersection2(LONG, LAT, EL, AZ, ERAD=6371.0, IHEI = 450.0)
    TEC,E_TEC, IRET = FDZTEC(IONOS_LONG, IONOS_LAT, YEAR, DOY, UT, MAP_TYPE)
    (STEC,E_STEC) = ZTEC2STEC(TEC,E_TEC,EL)

    return STEC,E_STEC

def IONOS_intersection2(LONG,LAT,EL,AZ, ERAD=6371.0, IHEI = 450.0):
    """
    Purpose:
    Given the height 450 km of ionposhere, there are differences between
    startion LONG, LAT and intersection LONG, LAT, when EL != 90. Consider
    a line from statoin to star/target that intersect with ionosphere.
    This function is used to caluculate the LONG, LAT of the intersection
    point.
  
    At lower EL, this will cause a very large differences
    At EL = 20 deg, the delta_zenith  = 8.63 deg
    At EL = 10 deg, the delta_zenith  = 13.10 deg

    inputs:
          LONG		station LONG in deg
          LAT		station LAT in deg
          EL		star/target EL in deg
          AZ		star/target AZ in deg
          ERAD		Earth radius, default 6371 km
          IHEI		1 layer Ionosphere height, default 450 km

    outputs:
          IONOS_LONG	longitude of the intersection in ionosphere
          IONOS_LAT     latitude of the intersection in inonosphere
    
    Examples
      >>> import intertec_tst
      >>> LONG = 141.132586
      >>> LAT = 39.133522
      >>> EL = 45.0
      >>> AZ = 135.0
      >>> (IONOS_LONG, IONOS_LAT) = intertec_tst.IONOS_intersection2(LONG, LAT, EL, AZ)
      >>> (IONOS_LONG, IONOS_LAT) = intertec_tst.IONOS_intersection2(LONG, 50.0, 50, 2)

    """
    if EL > 90 or EL <0:
       print('       EL = %6.2f is not in [0, 90] deg'%EL)
       IONOS_LONG = np.nan
       IONOS_LAT = np.nan
    elif AZ<0 or AZ>360:
       print('       AZ = %6.2f, is not in [0, 360] deg'%AZ)
       IONOS_LONG = np.nan
       IONOS_LAT = np.nan
    elif LAT<-87.5 or LAT>87.5:
       print('       LAT= %6.2f, is not in [-87.5, 87.5] deg'%LAT)
       IONOS_LONG = np.nan
       IONOS_LAT = np.nan
    else:
        zenith = np.deg2rad(90.0-EL)
        az = np.deg2rad(AZ)
 
        IO_zenith = np.arcsin(ERAD*np.sin(zenith)/(ERAD+IHEI))
        delta_zenith = zenith - IO_zenith
        
        #using spherical law of cosines to solve new LAT
        b = delta_zenith
        a = np.deg2rad(90.0-LAT)
        C_ = az
  
        cos_c = np.cos(a)*np.cos(b)+np.sin(a)*np.sin(b)*np.cos(C_)
        c = np.arccos(cos_c)
        IONOS_LAT = 90.0-np.rad2deg(c)
 
        # IONOS_LONG = LONG + B_
        #using spherical law of cosines to solve B_
 
        cos_B_ = (np.cos(b) - np.cos(a)*np.cos(c))/(np.sin(a)*np.sin(c))
 
        ######## numpy.arccos will give nan when cos_B_ too small
        if np.abs(1.0- cos_B_)<=0.0001:
           B_ = 0
        elif np.rad2deg(C_)>180:
           B_ = -1.0*np.arccos(cos_B_)
        elif np.rad2deg(C_)<180:
           B_ =  1.0*np.arccos(cos_B_)
           
        IONOS_LONG = LONG+np.rad2deg(B_)
        
    return IONOS_LONG,IONOS_LAT

def FDZTEC(LONG, LAT, YEAR,DOY,UT,TYPE='jpl'):
    """
    Function to interpolate final TEC from maps of T1 and T2

    inputs: 
          IONEXF        Global tec map at T1 used to find TEC
                               T1<TIME<T2, T2=T1 + 2hours
          LAT 		Latitude (deg)
          LONG		Longitude (deg) 
          YEAR
          DOY
          UT
          TYEPE         TEC map type: 'cod', 'jpl', or 'esa'

    outputs:
          TEC		Zenith TEC in unit of 0.1 TECU
          E_TEC  	error of zenith TEC in unit of 0.1 TECU
          IRET		Return status:
			True - TEC valid
			False - data not available
    dependence:
         TEC_4POINT
 
    Examples
      >>> import intertec_tst
      >>> LONG = 141.132586
      >>> LAT = 39.133522
      >>> YEAR=2015
      >>> DOY=208
      >>> UT=3
      >>> MAP_TYPE='cod'
      >>> (TEC, E_TEC, IRET) = intertec_tst.FDZTEC(LONG, LAT, YEAR,DOY,UT,TYPE='jpl')
    """
    doy = '%03i'%(DOY)
    #inputs check
    if LAT>87.5 or LAT<-87.5:
       print('! Error LAT value. LAT = %+5.1f!'%(LAT))
       print('! Reset LAT within [-87.5,87.5]')
       TEC = np.nan
       IRET = False

    elif LONG > 180 or LONG <-180:
       print('! Error LONG value. LONG = %+5.1f!'%(LONG))
       print('! Reset LONG within [-180.0,180.0]')
       TEC = np.nan
       IRET = False
    
    elif YEAR<2000:
       print('! Error YEAR value. YEAR = %4i'%(YEAR))
       print('! Global TEC map data before 2000 not available.')
       TEC = np.nan
       IRET = False
    elif DOY<0 or DOY>366:
       print('! Error DOY value. DOY = %3i'%(DOY))
       print('! Reset DOY within [0,366]')
       TEC = np.nan
       IRET = False
    else:
        year=str(YEAR)[2:4]
#       hour = np.int(UT-np.mod(UT,2))
        T = UT
        IONEXF = TYPE+'g'+doy+'0.'+year+'i'
#       print("! INPUT IONEX FILE: %s"%IONEXF)
        (DT, T1, T2) = TEC_time_info(UT, IONEXF)

        IONEXF1 = IONEXF+'-'+'%02i'%(T1)+'-xyz.txt'
        IONEXF2 = IONEXF+'-'+'%02i'%(T2)+'-xyz.txt'
        if os.path.exists(path_ionex+IONEXF1)==False:
            IXFILE2MAP(IONEXF,T1,IONEXF1)
        if os.path.exists(path_ionex+IONEXF2)==False:
            IXFILE2MAP(IONEXF,T2,IONEXF2)
        DT1 = T - T1 #unit hr
        DT2 = T2 - T #unit hr
 
        TLONG1 = LONG + DT1*15.0
        TLONG2 = LONG - DT2*15.0
 
        if (TLONG1<-180.0):
           TLONG1 = TLONG1+360.0
        elif (TLONG1>+180.0):
           TLONG1 = TLONG1-360.0
 
        if (TLONG2<-180.0):
           TLONG2 = TLONG2+360.0
        elif (TLONG2>+180.0):
           TLONG2 = TLONG2-360.0
 
        TEC1,E_TEC1,IRET1 = TEC_4POINT(IONEXF1,LAT,TLONG1)
        TEC2,E_TEC2,IRET2 = TEC_4POINT(IONEXF2,LAT,TLONG2) 
        
        if IRET1 and IRET2:
           TEC = (DT2*TEC1 + DT1*TEC2) /(DT1+DT2)
           E_TEC = (DT2*E_TEC1 + DT1*E_TEC2) /(DT1+DT2)
           IRET = True
        else:
           TEC = np.nan
           E_TEC = np.nan
           IRET = False

    return TEC, E_TEC, IRET

def stec2delay(stec,freq):
    """
    inputs:
        stec	slant TEC in unit of TECU
        freq 	frequency in unit of GHz

    outputs:
        ionos delay in unit of seconds at given freq.
    
    dependence:
 
    Examples
      >>> ionos_delay = stec2delay(stec,freq)
      
    """
    delay_cm = 40.28*stec/(freq*freq)
    delay = delay_cm/100.0/299792458
    return delay

def TEC_time_info(UT, ixfile):
    """
    Purpose
          find T1, T2, DT from global TEC map at given UT

    inputs: 
          IONEXF        global tec map in ionex format
          UT		

    outputs:
          T1            T1<=UT
          T2            T2>=UT
          DT		time interval of GIM

    Examples
      >>> import intertec_tst
      >>> (DT, T1, T2) = intertec_tst.TEC_time_info(9.7,'codg2080.15i')
    """

    if  (UT<0 or UT>24):
        print('T = %3i, which should within [0, 24] #unit hour'%(UT))
    else:
        infile = open(path_ionex+ixfile,'r')
        lines = infile.readlines()
        for line in lines:
            if '# OF MAPS IN FILE' in line:
                nmaps = int(line[2:6])
        DT = 24.0/(nmaps-1.0)
        times = np.arange(0,25,DT)
        for i in range(len(times)-1):
            if times[i]<=UT and times[i+1]:
                T1 = times[i]
                T2 = times[i+1]

        return DT, T1, T2

def TEC_4POINT(IONEXF, LAT, LONG):
    """
    Purpose
          function to do 4-point interpolation

    inputs: 
          IONEXF        Global tec map in xyz format used to find TEC
          LAT 		Latitude (deg)
          LONG		Longitude (deg) 

    outputs:
          TEC		Zenith TEC in unit of 0.1 TECU
          E_TEC		error of zenith TEC in unit of 0.1 TECU
          IRET		Return status:
			True - TEC valid
			False - data not available
    Examples
      >>> import intertec_tst
      >>> (TEC, E_TEC, IRET) = intertec_tst.TEC_4POINT('codg0010.14i-02-xyz.txt',+39.1335, 141.1326)

    """
    infile =path_ionex+IONEXF
    if os.path.exists(infile)==False:
       print('Warning: '+ infile+' do not exists!')
       TEC = np.nan
       E_TEC = np.nan
       IRET = False
    else:
       #read lines in string
       f=open(infile,'r')
       lines = f.readlines()
       f.close()
       #read x,y,z in float
       x,y,z = np.loadtxt(infile,usecols=(0,1,2),comments='!',dtype=float,unpack=True)
       xi,yi = [],[]
       for i in range(len(x)):
         if x[i] not in xi:
            xi.append(x[i])
         if y[i] not in yi:
            yi.append(y[i])
       xi=np.array(xi)
       yi=np.array(yi)
       DLONG= (xi.max()-xi.min())/(len(xi)-1)
       DLAT = (yi.max()-yi.min())/(len(yi)-1)

       for i in range(len(x)):
           if 0<=(LAT-y[i])<=DLAT:
              if 0<=(LONG-x[i])<=DLONG:
                 str_00 = '%+7.1f%+7.1f'%(x[i],y[i])
                 point00=[x[i],y[i],z[i]]
                 weight_x =(LONG-x[i])/DLONG
                 weight_y =(LAT-y[i])/DLAT
                 break

#      calculate weights
       weight00 = (1-weight_x)*(1-weight_y)
       weight01 = (1-weight_x)*weight_y
       weight10 = weight_x*(1-weight_y)
       weight11 = weight_x*weight_y
 
#      get points position of other 3 points, calculate weights
#      point 11
       point11=[point00[0]+DLONG,point00[1]+DLAT]
       if (point11[0]<-180.0):
          str_11 = '%+7.1f%+7.1f'%(point11[0]+360.0,point11[1])
       elif (point11[0]>+180.0):
          str_11 = '%+7.1f%+7.1f'%(point11[0]-360.0,point11[1])
       else:
          str_11 = '%+7.1f%+7.1f'%(point11[0],point11[1])
       # if LAT_11 > 87.5, pappens when LAT > 85.0, set  TEC = 0
       if (point11[1]>87.5):
          point11.append(0)
       
#      point 01
       point01=[point00[0],point00[1]+DLAT]
       if (point01[0]<-180.0):
          str_01 = '%+7.1f%+7.1f'%(point01[0]+360.0,point01[1])
       elif (point01[0]>+180.0):
          str_01 = '%+7.1f%+7.1f'%(point01[0]-360.0,point01[1])
       else:
          str_01 = '%+7.1f%+7.1f'%(point01[0],point01[1])
       # if LAT_01 > 87.5, pappens when LAT > 85.0, set  TEC = 0
       if (point01[1]>87.5):
          point01.append(0)

#      point 10
       point10=[point00[0]+DLONG,point00[1]]
       if (point10[0]<-180.0):
          str_10 = '%+7.1f%+7.1f'%(point10[0]+360.0,point10[1])
       elif (point10[0]>+180.0):
          str_10 = '%+7.1f%+7.1f'%(point10[0]-360.0,point10[1])
       else:
          str_10 = '%+7.1f%+7.1f'%(point10[0],point10[1])
         
       #get value for 01,10,11     
       for i in lines:
           if str_00 in i:
              str_00 = i
              point00.append(float(str_01[21:]))
           elif str_01 in i:
              str_01 = i
              point01.append(float(str_01[14:21]))
              point01.append(float(str_01[21:]))
           elif str_10 in i:
              str_10 = i
              point10.append(float(str_10[14:21]))
              point10.append(float(str_01[21:]))
           elif str_11 in i:
              str_11 = i
              point11.append(float(str_11[14:21]))
              point11.append(float(str_01[21:]))

       TEC = (point00[2]*weight00+point01[2]*weight01+point10[2]*weight10+point11[2]*weight11)/(weight00+weight01+weight10+weight11)
       E_TEC =  (point00[3]*weight00+point01[3]*weight01+point10[3]*weight10+point11[3]*weight11)/(weight00+weight01+weight10+weight11)
       IRET = True
    
    return TEC,E_TEC,IRET

def IXFILE2MAP(ixfile,t,xyzfile):
    """
    Purpose
          take GIM maps and transfer ionex files into eily read xyz format.

    inputs:
          ixfile	file name of ionex format GIM files
          t		hour 
          xyzfile	output file name
    outputs:
          ionos_map	2D GIM map
          rms_map	2D rms of GIM map
          X		longitude for 2D gride
	  Y		latitude for 2D gride
          Z1		TEC at (X, Y)
	  Z2		error of TEC at (X, Y)
          write xyzfile in ./xyz/
    
     return: ionos_map,rms_map,X,Y,Z1,Z2

    Examples
      >>> import intertec_tst
      >>> ionos_map,rms_map,X,Y,Z1,Z2 = intertec_tst.IXFILE2MAP('codg2080.15i',7,'codeg2080.15i-07-xyz.txt')
    """
    t = int(t)
    (DT,T1,T2) = TEC_time_info(t,ixfile)
    DT = int(DT)
    TYPE = ixfile[0:3]
    
    if  (t<0 or t>24):
        print('T = %3i, which should within [0, 2, 4, .., 22] #unit hour'%(t))
    else:
        infile = open(path_ionex+ixfile,'r')
        lines = infile.readlines()
        ##get useful header info.
        for line in lines:
            if line[60:78] == 'LAT1 / LAT2 / DLAT':
                temp = line[2:20]
                lat = temp.split()
            elif line[60:78] == 'LON1 / LON2 / DLON':
                temp = line[2:20]
                lon = temp.split()
 
        x = np.arange(float(lon[0]), float(lon[1])+float(lon[2]), float(lon[2]))
        y = np.arange(float(lat[0]), float(lat[1])+float(lat[2]), float(lat[2]))
        dim_x = len(x)
        dim_y = len(y)
        X, Y = np.meshgrid(x,y)
        X = np.resize(X,(1,dim_x*dim_y))
        X = X[0]
        Y = np.resize(Y,(1,dim_x*dim_y))
        Y = Y[0]
        Z1 = []
        Z2 = []
        start_indx = lines.index("%6i%74s\n"%(t/DT+1,'START OF TEC MAP    '))
        ended_indx = lines.index("%6i%74s\n"%(t/DT+1,'END OF TEC MAP      '))
        outfile = open(path_ionex+xyzfile,'w')
        outfile.writelines('!lon     lat      TEC    RMS\n')
        count = 0
        
        for i in lines[start_indx:ended_indx+1]:
            if ('MAP' in i) or  ('LAT' in i):
                pass
            else:
                line_data = i[0:-1].split()
                for j in line_data:
                    z = float(j)
                    Z1.append(z)
                    count = count+1

        if TYPE=='c1p' or TYPE=='c2p':
             Z2=np.zeros(len(Z1))
        else:
            #use index to find start and ended lines of rms blocks
            start_indx = lines.index("%6i%74s\n"%(t/DT+1,'START OF RMS MAP    '))
            ended_indx = lines.index("%6i%74s\n"%(t/DT+1,'END OF RMS MAP      '))
            count = 0
            for i in lines[start_indx:ended_indx+1]:
                if ('MAP' in i) or  ('LAT' in i):
                    pass
                else:
                    line_data = i[0:-1].split()
                    for j in line_data:
                        z = float(j)
                        Z2.append(z)
                        count = count+1

        for i in range(len(X)):
            outfile.writelines('%+7.1f%+7.1f%7.0f%7.0f\n'%(X[i],Y[i],Z1[i],Z2[i]))
  
        infile.close()
        outfile.close()
                
        Z1=np.array(Z1)
        Z2=np.array(Z2)
        ionos_map = np.resize(Z1,(dim_y,dim_x))
        rms_map = np.resize(Z2,(dim_y,dim_x))
        
        return ionos_map,rms_map,X,Y,Z1,Z2
    
def ZTEC2STEC(TEC,E_TEC, EL,ERAD=6371.0,IHEI=450.0):
     """
     Using mapping function to calculate Slant TEC
     STEC = TEC*sec(chai)
     chai = arcsin(6371*cos(EL))
     
     inputs: 
           TEC	Zenith TEC, float in unit of 0.1 TECU
           EL	float or float list, in unit of deg

     outputs:
           STEC  slant TEC in unit of 0.1 TECU
           E_STEC  error of slant TEC in unit of 0.1 T
     Examples
      >>> import intertec_tst
      >>> LONG = 141.132586
      >>> LAT = 39.133522
      >>> EL = 45.0
      >>> AZ = 135.0
      >>> YEAR=2015
      >>> DOY=208
      >>> UT=3
      >>> MAP_TYPE='cod'
      >>> (IONOS_LONG, IONOS_LAT) = intertec_tst.IONOS_intersection2(LONG, LAT, EL, AZ)
      >>> (TEC, E_TEC, IRET) = intertec_tst.FDZTEC(IONOS_LONG, IONOS_LAT, YEAR,DOY,UT,TYPE='jpl')
      >>> (STEC, E_STEC) = intertec_tst.ZTEC2STEC(TEC, E_TEC, EL)
     
     """
     if (EL<0 or EL>90)==True:
        print('!         EL should within [0,90] deg')
     else:
         EL = np.deg2rad(EL)
         TEC = float(TEC)
         E_TEC = float(E_TEC)
         chai = np.arcsin(ERAD*np.cos(EL)/(ERAD+IHEI))
         sec_chai = 1.0/np.cos(chai)
         STEC = TEC*sec_chai
         E_STEC = E_TEC*sec_chai
         
         return STEC, E_STEC
  
def get_TEC(year, doy, path, tec_type):    
    
    global path_ionex
    path_ionex = path+'ionex/'
    
    year = str(year)[2:4]
    if doy < 10:
        doy = '00'+str(doy)
    elif doy < 100:
        doy = '0'+str(doy)
    else:
        doy = str(doy)
        
    name = tec_type+'g'+doy+'0.'+year+'i'
    if os.path.exists(path_ionex+name):
        print('        '+name+' already there.')
    else:
        netpath='ftp://gssc.esa.int/gnss/products/ionex/20'+year+'/'+doy+'/'
        os.system(r'wget -t 30 -O '+name+'.Z '+netpath+name+'.Z')
        print(r'wget -t 30 -O '+name+'.Z '+netpath+name+'.Z')
        os.system(r'uncompress '+name+'.Z')
        os.system(r'cp '+name+' '+path_ionex)
    