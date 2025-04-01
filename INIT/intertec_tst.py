####################################################################
# a pacakge to download ionex file and solve zenith VTEC at any given
# (long,lat, YEAR, DOY, UT) and line of sight STEC at any given 
# (lon,lat,EL, AZ, YERA, DOY, UTC)
#
# how to use ?
#     import intertec_tst
#     help(intertec_tst) 
#
# writer: yuanwei Wu NAOJ 2015 05 18
# version 2.0 2015-05-27 add capability of rms estimation
# version 2.1 2015-09-17 fix time interval bugs
# version 2.2 2015-09-18 change ERAD, IHEI variables
#             2015-09-18 IONOS_intersection is not right
#                        should re write with spherical trigonometry
# version 2.3 2019-12-03 for c1p and c2p, do not calculate error of TEC
# version 2.4 2020-04-29 from STEC to DISP second/m/m
####################################################################
# reference: Stefan Schaer 1998
#            "IONEX: The IONosphere Map EXchange Format"
#
####################################################################
#import matplotlib.pyplot plt
import os, sys, subprocess
import numpy as np
from astropy.time import Time

# global variables 
c = 299792458.0
path_xyz = './xyz/'   # do not change path_xyz
path_ionex = './ionex/'
logfile = 'solve_stec.log'
if os.path.exists(path_xyz)==False:
   os.mkdir(path_xyz)
if os.path.exists(path_ionex)==False:
   os.mkdir(path_ionex)
##### Start defination of functions ########################
#
#
def mprint(intext,logfile):
    """
    print log info. to screen and logfile
    """
    print(intext)
    f=open(logfile, 'a')
    f.writelines(intext+'\n')
    f.close()

# Get the day-of-year integer from the year/month/day
def get_day_of_year(year, month, day):
    """
    Get the day-of-year integer from the year/month/day
    """
    day_of_year_list = [0,31,59,90,120,151,181,212,243,273,304,334]
    doy = day_of_year_list[month-1] + day
    if(month>2):
        if((year&0x3)==0):
            if((year % 100 != 0) or (year % 400 == 0)):
                doy = doy+1
#   doy='%03i'%(doy)
    return doy

##############################################################################
#  
def get_TEC(year,doy,tec_type):
    year=str(year)[2:4]
    if doy<10:
        doy='00'+str(doy)
    elif doy<100:
        doy='0'+str(doy)
    else:
        doy=str(doy)
    name=tec_type+'g'+doy+'0.'+year+'i'
    if os.path.exists(path_ionex+name):
        print(path_ionex+name+' already there.')
    else:
        path='ftp://gssc.esa.int/gnss/products/ionex/20'+year+'/'+doy+'/'
        os.popen(r'wget -t 30 -O '+name+'.Z '+path+name+'.Z')
        print(r'wget -t 30 -O '+name+'.Z '+path+name+'.Z')
        os.popen(r'uncompress '+name+'.Z')
        os.popen(r'cp '+name+' ./ionex/ ')

#       cmd='wget -t 30 -O '+name+'.Z '+path+name+'.Z'
#       proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#       cmd='uncompress '+name+'.Z'
#       proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#       cmd='cp '+name+' ./ionex/ '
#       proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def get_TEC_igmas(year,doy,tec_type):
    year=str(year)[2:4]
    if doy<10:
        doy='00'+str(doy)
    elif doy<100:
        doy='0'+str(doy)
    else:
        doy=str(doy)
    name=tec_type+'g'+doy+'0.'+year+'i'
    if os.path.exists(name):
        print('File already there.')
    else:
#       path='ftp://igmas.ntsc.ac.cn/ionex/20'+year+'/'+doy+'/'
        path='ftp://113.200.79.163:/ionex/20'+year+'/'+doy+'/'
        os.popen(r'wget --no-passive-ftp '+name+'.Z '+path+name+'.Z')
        os.popen(r'zcat -f '+name+'.Z >'+name)

def read_SAT_AZEL(infile):
    f=open(infile,'r')
    lines=f.readlines()
    f.close()
    YEAR,DOY,UTC,AZ,EL,DIST,T=[],[],[],[],[],[],[]
    for i in range(len(lines)):
        if lines[i][0]!='!':
           temp=lines[i].split() 
           yr = int(temp[0])
           mn = int(temp[1])
           day= int(temp[2])
           hh = int(temp[3])
           mm = int(temp[4])
           ss = float(temp[5])
           x  = float(temp[6])
           y  = float(temp[7])
           z  = float(temp[8])
           #####################
           doy = get_day_of_year(yr, mn, day)
           utc = hh+mm/60.0+ss/3600.0
           t=Time("%04i-%02i-%02i %02i:%02i:%06.3f"%(yr,mn,day,hh,mm,ss))

           YEAR.append(yr)
           DOY.append(doy)
           UTC.append(utc)
           T.append(t)
           AZ.append(x)
           EL.append(y)
           DIST.append(z)
    return (YEAR,DOY,UTC,T,AZ,EL,DIST)

def read_SAT_AZEL2(infile):
    f=open(infile,'r')
    lines=f.readlines()
    f.close()
    T,YEAR,DOY,UTC = [],[],[],[]
    AZ_JL,EL_JL,AZ_SY,EL_SY,AZ_KS,EL_KS=[],[],[],[],[],[]
    for i in range(len(lines)):
        if lines[i][0]!='!':
           temp=lines[i].split() 
#          print(temp)
           yr = int(temp[0].split('-')[0])
           mn = int(temp[0].split('-')[1])
           day= int(temp[0].split('-')[2]) 
                                          
           hh = int(temp[1].split(':')[0])               
           mm = int(temp[1].split(':')[1])            
           ss = float(temp[1].split(':')[2])            
           az_jl  = float(temp[2])
           el_jl  = float(temp[3])
           az_sy  = float(temp[4])
           el_sy  = float(temp[5])
           az_ks  = float(temp[6])
           el_ks  = float(temp[7])
           #####################
           doy = get_day_of_year(yr, mn, day)
           utc = hh+mm/60.0+ss/3600.0
           t=Time("%s %s"%(temp[0],temp[1]))

           YEAR.append(yr)
           DOY.append(doy)
           UTC.append(utc)
           T.append(t)
           AZ_JL.append(az_jl)
           EL_JL.append(el_jl)
           AZ_SY.append(az_sy)
           EL_SY.append(el_sy)
           AZ_KS.append(az_ks)
           EL_KS.append(el_ks)
    return (YEAR,DOY,UTC,T,AZ_JL,EL_JL,AZ_SY,EL_SY,AZ_KS,EL_KS)


# Load data and index it
def IONOS_intersection(LONG,LAT,EL,AZ, ERAD=6371.0, IHEI = 450.0):
    """
    bugs in this function are found; should use spherical triangle law
    to get IONOS_LONG and IONOS_LAT
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
      >>> (IONOS_LONG, IONOS_LAT) = intertec_tst.IONOS_intersection(LONG, LAT, EL, AZ)

    """
    print('!\n!    call IONOS_intersection(LONG,LAT,EL,AZ)')
    print('!        Target_EL = %+6.1f deg  Target_AZ = %+6.1f deg'%(EL,AZ))
    print('!        Station_LONG = %+6.1f deg  Station_LAT = %+6.1f deg'%(LONG,LAT))
    zenith = np.deg2rad(90.0-np.float(EL))
    az = np.deg2rad(np.float(AZ))

    IO_zenith = np.arcsin(ERAD*np.sin(zenith)/(ERAD+IHEI))
    delta_zenith = zenith - IO_zenith
    delta_LONG = np.rad2deg(delta_zenith*np.sin(az))
    delta_LAT  = np.rad2deg(delta_zenith*np.cos(az))
    IONOS_LONG = delta_LONG+LONG
    IONOS_LAT = delta_LAT+LAT
    print('!    return IONOS_LONG = %+6.1f deg  IONOS_LAT = %+6.1f deg'%(IONOS_LONG,IONOS_LAT))
    return IONOS_LONG,IONOS_LAT

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
        print('!\n!    call IONOS_intersection2(LONG,LAT,EL,AZ)')
        print('!        Target_EL   = %+10.4f deg  Target_AZ = %+10.4f deg'%(EL,AZ))
        print('!        Stat_LONG   = %+10.4f deg  Stat_LAT  = %+10.4f deg\n'%(LONG,LAT))
        zenith = np.deg2rad(90.0-np.float(EL))
        az = np.deg2rad(np.float(AZ))
 
        IO_zenith = np.arcsin(ERAD*np.sin(zenith)/(ERAD+IHEI))
        delta_zenith = zenith - IO_zenith
        print('!        Delta_Zenith= %+10.4f deg'%(np.rad2deg(delta_zenith)))
        
        #using spherical law of cosines to solve new LAT
       
        b = delta_zenith
        a = np.deg2rad(90.0-LAT)
        C_ = az
 
        print('!        solving spherical trigonometry')
        print('!        cos(c) = cos(a)cos(b) + sin(a)sinb(b)cos(C)\n')
        print('!        a  = 90-Stat_LAT  = %10.4f deg'%(np.rad2deg(a)))
        print('!        b  = Delta_Zenith = %10.4f deg'%(np.rad2deg(b)))
        print('!        C  = Target_AZ    = %10.4f deg\n'%(np.rad2deg(C_)))
  
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
        #########################################
        IONOS_LONG = LONG+np.rad2deg(B_)
        print('!        c  = 90-IONOS_LAT = %10.4f deg'%(np.rad2deg(c)))
        print('!        B  = IONOS_LONG - Stat_LONG')
        print('!           =                %10.4f deg\n'%(np.rad2deg(B_)))
##      print('! delta LONG: %6.1f, delta LAT: %6.1f'%(delta_LONG,delta_LAT))
        print('!        IONOS_LONG = %+6.1f deg  IONOS_LAT = %+6.1f deg'%(IONOS_LONG,IONOS_LAT))
    return IONOS_LONG,IONOS_LAT

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
    global path_xyz,path_ionex
    t = np.int(t)
    (DT,T1,T2) = TEC_time_info(t,ixfile)
    DT = np.int(DT)
    TYPE = ixfile[0:3]
#   print "DT = %6.2f, T1=%6.2f, T2=%6.2f"%(DT,T1,T2)
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
 
      x = np.arange(np.float(lon[0]), np.float(lon[1])+np.float(lon[2]), np.float(lon[2]))
      y = np.arange(np.float(lat[0]), np.float(lat[1])+np.float(lat[2]), np.float(lat[2]))
      dim_x = len(x)
      dim_y = len(y)
      X, Y = np.meshgrid(x,y)
      X=np.resize(X,(1,dim_x*dim_y))
      X=X[0]
      Y=np.resize(Y,(1,dim_x*dim_y))
      Y=Y[0]
      Z1=[]
      Z2=[]
      print('! Return 2D ionex map at %2i hour. Dimension [%3.0f, %3.0f]'%(t,dim_x,dim_y))
      #use index to find start and ended lines of data blocks
      start_indx = lines.index("%6i%74s\n"%(t/DT+1,'START OF TEC MAP    '))
      ended_indx = lines.index("%6i%74s\n"%(t/DT+1,'END OF TEC MAP      '))
      print('! TEC map Start from line %6i, ended at line %6i'%(start_indx+1,ended_indx+1))
      outfile = open(path_xyz+xyzfile,'w')
      outfile.writelines('!lon     lat      TEC    RMS\n')
      count = 0
      for i in lines[start_indx:ended_indx+1]:
          if ('MAP' in i) or  ('LAT' in i):
              pass
          else:
              line_data = i[0:-1].split()
              for j in line_data:
                  z=np.float(j)
                  Z1.append(z)
                  count=count+1
      print("TEC_TYPE:%s"%TYPE)        

      if TYPE=='c1p' or TYPE=='c2p':
           Z2=np.zeros(len(Z1))
      else:
          #use index to find start and ended lines of rms blocks
          start_indx = lines.index("%6i%74s\n"%(t/DT+1,'START OF RMS MAP    '))
          ended_indx = lines.index("%6i%74s\n"%(t/DT+1,'END OF RMS MAP      '))
          print('! rms map Start from line %6i, ended at line %6i'%(start_indx+1,ended_indx+1))
          count = 0
          for i in lines[start_indx:ended_indx+1]:
              if ('MAP' in i) or  ('LAT' in i):
                  pass
              else:
                  line_data = i[0:-1].split()
                  for j in line_data:
                      z=np.float(j)
                      Z2.append(z)
#####                 outfile.writelines('%+7.1f%+7.1f%7.0f\n'%(X[count],Y[count],z))
                      count=count+1

      for i in range(len(X)):
                  outfile.writelines('%+7.1f%+7.1f%7.0f%7.0f\n'%(X[i],Y[i],Z1[i],Z2[i]))

      infile.close()
      outfile.close()
              
      Z1=np.array(Z1)
      Z2=np.array(Z2)
      ionos_map = np.resize(Z1,(dim_y,dim_x))
      rms_map = np.resize(Z2,(dim_y,dim_x))
      return ionos_map,rms_map,X,Y,Z1,Z2

###############################################
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
    global path_ionex

    t = np.float(UT)
    if  (t<0 or t>24):
        print('T = %3i, which should within [0, 24] #unit hour'%(t))
    else:
      if os.path.exists(path_ionex+ixfile)==False:
        print('! '+ixfile+' does not exists! Start Download.')
        year = ixfile[-3:-1]
        year=int('20'+year)
        doy = int(ixfile[4:7])
        tec_type = ixfile[0:3]
       
        get_TEC(year,doy,tec_type)
#       if os.path.exists()==True:

#     os.popen(r'mv '+ixfile+' ./ionex/ ')
      infile = open(path_ionex+ixfile,'r')
      lines = infile.readlines()
      ##get useful header info.
      for line in lines:
#         print line
          if '# OF MAPS IN FILE' in line:
#            print line
             nmaps = np.int(line[2:6])
      DT = 24.0/(nmaps-1.0)
      times = np.arange(0,25,DT)
      for i in range(len(times)-1):
          if times[i]<=t and times[i+1]:
             T1 = times[i]
             T2 = times[i+1]

      return DT, T1, T2
###############################################
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
    global path_xyz
    infile =path_xyz+IONEXF
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
#      print '!\n! call TEC_4POINT(IONEXF, LAT=%7.1f, LONG=%7.1f)'%(LAT,LONG)

#      find 00 position
#      point00=[999,999,0]
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
              point00.append(np.float(str_01[21:]))
           elif str_01 in i:
              str_01 = i
              point01.append(np.float(str_01[14:21]))
              point01.append(np.float(str_01[21:]))
           elif str_10 in i:
              str_10 = i
              point10.append(np.float(str_10[14:21]))
              point10.append(np.float(str_01[21:]))
           elif str_11 in i:
              str_11 = i
              point11.append(np.float(str_11[14:21]))
              point11.append(np.float(str_01[21:]))

#      print '! 4-points interpolation'
#      print '! weight_x:%6.3f, weight_y:%6.3f'%(weight_x,weight_y)
#      print '!     lon    lat    TEC    weight'
#      print '! %+7.1f%+7.1f%7.0f %8.3f'%(point00[0],point00[1],point00[2],weight00)
#      print '! %+7.1f%+7.1f%7.0f %8.3f'%(point01[0],point01[1],point01[2],weight01)
#      print '! %+7.1f%+7.1f%7.0f %8.3f'%(point10[0],point10[1],point10[2],weight10)
#      print '! %+7.1f%+7.1f%7.0f %8.3f'%(point11[0],point11[1],point11[2],weight11)
#      print '! ----------------------------------------------'

       TEC = (point00[2]*weight00+point01[2]*weight01+point10[2]*weight10+point11[2]*weight11)/(weight00+weight01+weight10+weight11)
       E_TEC =  (point00[3]*weight00+point01[3]*weight01+point10[3]*weight10+point11[3]*weight11)/(weight00+weight01+weight10+weight11)
       IRET = True
    
    return TEC,E_TEC,IRET
#   return TEC,IRET

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
    DOY=np.int(DOY)
    doy = '%03i'%(DOY)
    YEAR = np.int(YEAR)
    UT = np.float(UT)
    LAT=np.float(LAT)
    LONG = np.float(LONG)
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
        if os.path.exists(path_xyz+IONEXF1)==False:
           print('run IXFILE2MAP(%s, %2i, %s)'%(IONEXF,T1,IONEXF1))
           IXFILE2MAP(IONEXF,T1,IONEXF1)
        if os.path.exists(path_xyz+IONEXF2)==False:
           print('run IXFILE2MAP(%s, %2i, %s)'%(IONEXF,T2,IONEXF2))
           IXFILE2MAP(IONEXF,T2,IONEXF2)
        print('!\n! FDZTEC(LONG=%+6.1f, LAT=%+6.1f, YEAR=%4i, DOY = %3i, UT=%5.2f, TYPE=\'%s\')'%(LONG,LAT,YEAR,DOY, T,TYPE))
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
        print('! At %5.2f hr, TEC1 = %6.1f +- %6.1f (DT1 = %5.2f hr, TLONG1 = %+6.1f deg)'%(T1, TEC1, E_TEC1, DT1, TLONG1))
        print('! At %5.2f hr, TEC2 = %6.1f +- %6.1f (DT2 = %5.2f hr, TLONG2 = %+6.1f deg)'%(T2, TEC2, E_TEC2, DT2, TLONG2))
########
        if IRET1 and IRET2:
           TEC = (DT2*TEC1 + DT1*TEC2) /(DT1+DT2)
           E_TEC = (DT2*E_TEC1 + DT1*E_TEC2) /(DT1+DT2)
           IRET = True
           print('! At %05.2f hr, TEC  = %6.1f +- %6.1f'%(T, TEC,E_TEC))
        else:
           TEC = np.nan
           E_TEC = np.nan
           IRET = False

    return TEC, E_TEC, IRET

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
     print('!\n!    call ZTEC2STEC(TEC=%5.1f, EL=%4.1f)'%(TEC,EL))
     if (EL<0 or EL>90)==True:
        print('!         EL should within [0,90] deg')
     else:
         EL = np.deg2rad(EL)
         TEC = np.float(TEC)
         E_TEC = np.float(E_TEC)
         chai = np.arcsin(ERAD*np.cos(EL)/(ERAD+IHEI))
         sec_chai = 1.0/np.cos(chai)
         STEC = TEC*sec_chai
         E_STEC = E_TEC*sec_chai
###      chai = np.rad2deg(chai)
         
         print('!    return slant TEC: %5.1f +- %5.1f'%(STEC,E_STEC))
         return STEC, E_STEC

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
    if print_level == 3:
        print('! -----------------------------------------------------------------')
        print('!\n! Run main procedure FDSTEC(LONG,LAT,EL,AZ,YEAR,DOY,UT,MAP_TYPE)')
        print('! ')
        print('!    inputs:')
        print('!          YEAR = %3i yr'%(YEAR))
        print('!          DOY  = %3i day'%(DOY))
        print('!          UT   = %5.2f hr'%(UT))
        print('!          MAP_TYPE     = %s'%(MAP_TYPE) )
        print('!          Station_LONG = %+6.1f deg'%(LONG))
        print('!          Station_LAT  = %+6.1f deg'%(LAT))
        print('!          Satellite_EL = %+6.1f deg'%(EL))
        print('!          Satellite_AZ = %+6.1f deg'%(AZ))
        print('!\n! --- solve start ---')

    (IONOS_LONG,IONOS_LAT) = IONOS_intersection2(LONG, LAT, EL, AZ, ERAD=6371.0, IHEI = 450.0)
    TEC,E_TEC, IRET = FDZTEC(IONOS_LONG, IONOS_LAT, YEAR, DOY, UT, MAP_TYPE)
    (STEC,E_STEC) = ZTEC2STEC(TEC,E_TEC,EL)
    if print_level == 3:
        print('!\n! ---- solve end -------')
        print('!\n!    outputs:')
        print('!           TEC = %6.1f +- %6.1f\n'%(STEC,E_STEC))
        print('!           TEC = %6.1f +- %6.1f\n')
        print('! ---------------------- the end ----------------------------------')
    if print_level == 0:
        print('! ---------------------- the end ----------------------------------')
    return STEC,E_STEC

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
    delay = delay_cm/100.0/c
    return delay

def stec2disp(stec):
    """
    inputs:
        stec	slant TEC in unit of TECU

    outputs:
        dispersive delay: ionos delay in unit of seconds at wavelength of 1m
    
    dependence:
 
    Examples
      >>> disp = stec2disp(stec)
      
    """
    disp = 40.28*1E16*stec/(c**3)
    return disp
