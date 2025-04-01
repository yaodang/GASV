#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

def plot_stationGlobal(sitAll):
    m = Basemap(resolution='l')     # 实例化一个map
    m.drawcoastlines()  # 画海岸线
    # m.drawmapboundary(fill_color='aqua') 
    # m.drawcountries()
    #m.drawrivers()
    # m.fillcontinents(color='lightgray',lake_color='blue') # 画大洲，颜色填充为褐色
    
    parallels = np.arange(-90., 90., 30.)  # 这两行画纬度，范围为[-90,90]间隔为10
    m.drawparallels(parallels,labels=[False, True, True, False])
    meridians = np.arange(-180., 180., 60.)  # 这两行画经度，范围为[-180,180]间隔为10
    m.drawmeridians(meridians,labels=[True, False, False, True])
    
    sitNum = len(sitAll['name'])
    # lonlat = [[],[]]
    for i in range(sitNum):
        lon = np.arctan2(sitAll['ITRF'][i][1],sitAll['ITRF'][i][0])*180/np.pi
        temp = np.sqrt(sitAll['ITRF'][i][1]**2+sitAll['ITRF'][i][0]**2)
        lat = np.arctan2(sitAll['ITRF'][i][2],temp)*180/np.pi
        
        if sitAll['nnrt'][i] == 1:
            # lonlat[0].append(lon)
            # lonlat[1].append(lat)
            m.plot(lon,lat,marker='D',color='red')
        else:
            m.plot(lon,lat,marker='D',color='blue')
            
    
    plt.savefig('glob.png', bbox_inches='tight',dpi=600)

# plot_stationGlobal()