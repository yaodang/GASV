#!/usr/bin/env python3

import numpy as np
import math
np.set_printoptions(precision=15)

def calc_T(MJD):
    """
    Calculate Julian centuries of TDB/TT since J2000
    ---------------------
    input: 
        MJD          : 
    output: 
        T            : Julian centuries of TDB/TT since J2000
    ---------------------
    Reference: IERS Conventions 2010
    """
    taiut = leap_second(MJD)
    MJDTT = MJD + (32.184 + taiut)/86400
    #Julian centuries from J2000.0
    T = (MJDTT - 51544.5) / 36525.0
    return T

def doodarg(mjd):
    """
    Computes Doodson's fundamental arguments
    ---------------------
    input: 
        MJD          : 
    output: 
      tau            :   mean lunar time [deg]
      s              :   mean tropic longitude of the Moon [deg]
      h              :   mean tropic longitude of the Sun [deg]
      p              :   mean tropic longitude of the lunar perigee [deg]
      zns            :   mean tropic longitude of the ascending lunar node
                         (decreasing in time)(N') [deg]
      ps             :   mean tropic longitude of the perihelion [deg]
    ---------------------
    Reference: IERS Conventions 2010
    """
    T = calc_T([mjd])
    T2 = T**2
    T3 = T**3
    T4 = T**4
    fhr = (mjd - np.floor(mjd)) * 24
    
    #mean tropic longitude of the Moon
    s = 218.31664563 + 481267.88194*T - 0.0014663889*T2 + 0.00000185139*T3
    #mean lunar time [deg]
    tau = fhr*15 + 280.4606184 + 36000.7700536 * T + 0.00038793*T2 - 0.0000000258*T3 - s
    PR = 1.396971278*T + 0.000308889*T2 + 0.000000021*T3 + 0.000000007*T4
    s = s + PR
    #mean tropic longitude of the Sun [deg]
    h = 280.46645 + 36000.7697489*T + 0.00030322222*T2 + 0.000000020*T3 - 0.00000000654*T4
    #mean tropic longitude of the lunar perigee [deg]
    p = 83.35324312 + 4069.01363525 *T - 0.01032172222*T2 - 0.0000124991*T3 + 0.00000005263*T4
    #mean tropic longitude of the ascending lunar node [deg]
    zns = 234.95544499 + 1934.13626197*T - 0.00207561111*T2 - 0.00000213944*T3 + 0.00000001650*T4
    #mean tropic longitude of the perihelion [deg]
    ps = 282.93734098 + 1.71945766667*T + 0.00045688889*T2 - 0.00000001778*T3 - 0.00000000334*T4
    
    return [s,tau,h,p,zns,ps]    
    
def month(year):
	lmonth = np.array(np.zeros(12,dtype=int))
	
	for i in np.arange(0,12):
		lmonth[i-1] = 31
		if i == 2:
			lmonth[i-1] = 28
		if (i==4) | (i==6) | (i==9) | (i==11):
			lmonth[i-1] = 30

	if year%4 == 0 or year%400 == 0 and year%100 != 0:
		lmonth[1] = 29
	return lmonth

def doy2day(doy, year):
	lmonth = month(year)
	#print lmonth
	for i in range(0,12):
		if doy>sum(lmonth[0:i]) and doy<=sum(lmonth[0:i+1]):
			mon = i + 1
			day = doy - sum(lmonth[0:i])
		elif doy == sum(lmonth[0:i]):
			mon = i
			day = lmonth[i-1]
	return [mon,day]

def date2doy(year,m,d):
	lmonth = month(year)

	doy = sum(lmonth[0:m-1])+d
	
	return doy

def add_time(y,m,d,h,mi,s,time):
#y---year
#m---month
#d---day
#h---hour
#mi--minute
#s---second
#time---add time(unite:second)
	lmonth = month(y)
	if (s+time)/60 >= 1:
		mi = mi + (s+time)/60		
		s = (s+time)%60
		if mi/60 >= 1:
			h = h + mi/60
			mi = mi%60
			if h/24 >= 1:
				d = d + h/24				
				h = 0
				if d > lmonth[m-1]:
					d = 1
					m = m + 1
					if m > 12:
						m = 1
						y = y + 1
	out = ''	
	if len(str(h)) == 1:
		out = out + '0'+str(h)
	else:
		out = out + str(h)
	out = out + ':'

	if len(str(mi)) == 1:
		out = out + '0'+str(mi)
	else:
		out = out + str(mi)
	out = out + ':'
	
	if len(str(s)) == 1:
		out = out + '0'+str(s)
	else:
		out = out + str(s)

	zeros = '0'
	return [str(y),zeros[0:2-len(str(m))]+str(m),zeros[0:2-len(str(d))]+str(d),out]
		

def date2mjd(y,m,d,h,mi,s):
	jd = 367.000000*y\
	     - np.floor((7*(y+np.floor((m+9)/12.000000)))*0.250000)\
	     + np.floor(275*m/9.000000)\
	     +d+1721013.500000+h/24.000000+mi/1440.000000+s/86400.000000
	mjd = jd - 2400000.500000
	return mjd

def hms(dmjd):
    h = int(dmjd*24)
    m = int((dmjd*24-h)*60)
    s = ((dmjd*24-h)*60-m)*60
    
    return h,m,s

def modjuldatNew(y,m,d,*args):
    '''
    Get the Modified Julian Day from date.

    Parameters
    ----------
    y : array or int
        year.
    m : array or int
        month.
    d : array or int
        day.

    Returns
    -------
    tmjd : TYPE
        DESCRIPTION.

    '''    
    yn = y + 0
    mn = m + 0
    
    if type(yn) == int:
        if mn <= 2:
            mn = mn + 12
            yn = yn - 1
        b = 0
        if yn<=1582 and mn<=10 and d<=4:
            b = -2
        else:
            b = np.floor(yn/400) - np.floor(yn/100)
            
        
    elif type(yn) == np.ndarray:
        ind = np.where(mn <= 2)
        if len(ind[0]):
            mn[ind[0]] = mn[ind[0]] + 12
            yn[ind[0]] = yn[ind[0]] - 1
        
        b = np.zeros(len(yn))
        ind = np.where(np.logical_and(yn<=1582,mn<=10, d<=4)==True)
        if len(ind[0]):
            b[ind[0]] = -2
        ind = np.where(np.logical_and(yn<=1582,mn<=10, d<=4)==False)
        if ind[0].size != 0:
            b[ind[0]] = np.floor(yn[ind[0]]/400) - np.floor(yn[ind[0]]/100)
        
    jd = np.floor(365.25*yn) - 2400000.5
    
    
    if len(args) == 0:
        tmjd = jd + np.floor(30.6001*(mn+1))+b+1720996.5 + d
    if len(args) == 1:
        tmjd = jd + np.floor(30.6001*(mn+1))+b+1720996.5 + d + args[0]/86400.0
    elif len(args) == 3:
        tmjd = jd + np.floor(30.6001*(mn+1))+b+1720996.5 + d + args[0]/24.0 + \
               args[1]/1440.0 + args[2]/86400.0
    
    return tmjd


def modjuldat(y,m,d,h,mi,s):
    '''
    Get the Modified Julian Day from date.

    Parameters
    ----------
    y : array
        year.
    m : array
        month.
    d : array
        day.
    h : int or float or array
        hour.
    mi : int or float or array
        minute.
    s : int or float or array
        second.

    Returns
    -------
    tmjd : TYPE
        DESCRIPTION.

    '''
    
    yn = y + 0
    mn = m + 0
    
    ind = np.where(mn <= 2)
    if len(ind[0]):
        mn[ind[0]] = mn[ind[0]] + 12
        yn[ind[0]] = yn[ind[0]] - 1
    
    b = np.zeros(len(yn))
    ind = np.where(np.logical_and(yn<=1582,mn<=10, d<=4)==True)
    if len(ind[0]):
        b[ind[0]] = -2
    ind = np.where(np.logical_and(yn<=1582,mn<=10, d<=4)==False)
    if ind[0].size != 0:
        b[ind[0]] = np.floor(yn[ind[0]]/400) - np.floor(yn[ind[0]]/100)
    
    jd = np.floor(365.25*yn) - 2400000.5
    tmjd = jd + np.floor(30.6001*(mn+1))+b+1720996.5 + d + h/24.0 + mi/1440.0 + s/86400.0
    
    return tmjd

def mjd2date(mjd):
    """
    Get the year/month/day from MJD
    ---------------------
    input: 
        MJD                 : 
    output: 
        [year,month,day]    : 
    ---------------------
    """
    hour = math.floor((mjd - math.floor(mjd)) * 24)
    minu = math.floor((((mjd - math.floor(mjd)) * 24) - hour) * 60)
    sec = (((((mjd - math.floor(mjd)) * 24) - hour) * 60) - minu) * 60
    if sec == 60:
        minu = minu + 1
        sec = 0
	    
    if minu == 60:
	    hour = hour + 1
	    minu = 0

    jd = mjd + 2400000.5
    if hour ==24:
        jd = jd + 1
        hour = 0
	    
    jd_int = math.floor(jd + 0.5)
    a = jd_int + 32044
    b = math.floor((4*a + 3) / 146097)
    c = a - math.floor((b * 146097) / 4)

    d = math.floor((4*c + 3) / 1461)
    e = c - math.floor((1461*d) / 4)
    m = math.floor((5*e + 2) / 153)

    day = int(e - math.floor((153*m + 2) / 5) + 1)
    month = int(m + 3 - 12*math.floor(m/10))
    year = int(b * 100 + d - 4800 + math.floor(m/10))

    return [year, month, day, hour, minu, sec]

def mjd2ymdhms(mjd):
    """
    Get the year/month/day from MJD
    ---------------------
    input: 
        MJD                 : 
    output: 
        [year,month,day]    : 
    ---------------------
    """
    hour = math.floor((mjd - math.floor(mjd)) * 24)
    minu = math.floor((((mjd - math.floor(mjd)) * 24) - hour) * 60)
    sec = (((((mjd - math.floor(mjd)) * 24) - hour) * 60) - minu) * 60
    if sec == 60:
        minu = minu + 1
        sec = 0
	    
    if minu == 60:
	    hour = hour + 1
	    minu = 0

    jd = mjd + 2400000.5
    if hour ==24:
        jd = jd + 1
        hour = 0
	    
    jd_int = math.floor(jd + 0.5)
    a = jd_int + 32044
    b = math.floor((4*a + 3) / 146097)
    c = a - math.floor((b * 146097) / 4)

    d = math.floor((4*c + 3) / 1461)
    e = c - math.floor((1461*d) / 4)
    m = math.floor((5*e + 2) / 153)

    day = int(e - math.floor((153*m + 2) / 5) + 1)
    month = int(m + 3 - 12*math.floor(m/10))
    year = int(b * 100 + d - 4800 + math.floor(m/10))

    return [year, month, day, hour, minu, sec]

def sec2hms(seconds):
    
    h = int(seconds/3600)
    m = int((seconds-h*3600)/60)
    si = seconds - h*3600 - m*60
    
    return h,m,si
    
def leap_second(MJD):
    """
    Get the leap seconds
    ---------------------
    input: 
        MJD          : 
    output: 
        tmu          : leap seconds
    ---------------------
    """
    
    tmu = np.zeros(len(MJD))
    
    leap_sec = np.array([57754, 57204,56109,54832,53736,51179,50630,50083,49534,49169,48804,48257,\
        47892,47161,46247,45516,45151,44786,44239,43874,43509,\
        43144,42778,42413,42048,41683,41499,41317])
    
    sec = np.array([37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,\
       16,15,14,13,12,11,10])
    
    for i in range(len(MJD)):
        temp = sec[MJD[i] >= leap_sec]
        tmu[i] = temp[0]
        
    return tmu
    
def getMon(mon):
    if mon == 1:
        return 'JAN'
    if mon == 2:
        return 'FEB'
    if mon == 3:
        return 'MAR'
    if mon == 4:
        return 'APR'
    if mon == 5:
        return 'MAY'
    if mon == 6:
        return 'JUN'
    if mon == 7:
        return 'JUL'
    if mon == 8:
        return 'AUG'
    if mon == 9:
        return 'SEP'
    if mon == 10:
        return 'OCT'
    if mon == 11:
        return 'NOV'
    if mon == 12:
        return 'DEC'
                                   
# print(doy2day(115, 2000))
# mjd = modjuldatNew(2023,10,10)
# y = np.array([2023])
# m = np.array([10])
# d = np.array([10])
# h = np.array([1])
# mi = np.array([10])
# s = np.array([0])
# mjd1 = modjuldatNew(y,m,d,h,mi,s)