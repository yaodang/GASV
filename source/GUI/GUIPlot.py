import matplotlib
from matplotlib.lines import drawStyles, lineStyles
from scipy.sparse.csgraph import bellman_ford

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from matplotlib.pyplot import MultipleLocator
from matplotlib.widgets import RectangleSelector
from PyQt5.QtCore import pyqtSignal as Signal
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER,LATITUDE_FORMATTER
import numpy as np
from COMMON import *

class PlotMapSou(FigureCanvas):
    def __init__(self, width, height):
        self.fig = Figure(figsize=(width, height), tight_layout=True)
        self.axes = self.fig.add_subplot(111, projection='mollweide')
        FigureCanvas.__init__(self, self.fig)

        self.markers = []

        self.initMap()

    def initMap(self):
        self.axes.set_xticks(np.radians([-180,-150,-120,-90,-60,-30,0,30,60,90,120,150]))
        self.axes.set_xticklabels(['12h','','','','','','','','','','',''], ha='right')
        self.axes.set_yticks(np.radians([90,60,30,0,-30,-60,-90]))
        self.axes.set_yticklabels(['+90','','','','','','-90'])
        self.axes.grid(True, alpha=0.3)

        self.draw()

    def plotSource(self, radec):
        for i in range(len(radec)):
            if radec[i][0] > np.pi:
                radec[i][0] -= 2*np.pi
            marker = self.axes.plot(radec[i,0], radec[i,1], color='black', marker='o', linestyle='None', markersize=5)[0]
            self.markers.append(marker)

        self.draw()

    def clearMap(self):
        if len(self.markers):
            for marker in self.markers:
                marker.remove()
            self.markers = []
            self.draw()

class PlotMapSta(FigureCanvas):

    def __init__(self, width, height):
        self.fig = Figure(figsize=(width, height), tight_layout=True)
        self.axes = self.fig.add_subplot(111, projection=ccrs.PlateCarree())
        FigureCanvas.__init__(self, self.fig)

        self.markers = []
        self.labels = []
        self.initMap()

    def initMap(self):
        self.axes.set_global()
        self.axes.add_feature(cfeature.COASTLINE, linewidth=0.5)
        self.axes.add_feature(cfeature.BORDERS, linestyle='--', linewidth=0.3)
        gl = self.axes.gridlines(crs=ccrs.PlateCarree(),
                                 draw_labels=True,
                                 linewidth=0.5,
                                 color='gray',
                                 linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 10}
        gl.ylabel_style = {'size': 10}

        self.draw()

    def plotStation(self, lat, lon, stationList):
        for i in range(len(lat)):
            marker = self.axes.plot(lon[i], lat[i], marker='o',transform=ccrs.PlateCarree(),
                              color='red',linestyle='None')[0]
            label = self.axes.text(lon[i]+2, lat[i]+2,
                                   stationList[i],
                                   transform = ccrs.PlateCarree(),
                                   fontsize = 8,
                                   color = 'red')
                                   #bbox=dict(facecolor='white',alpha=0.4))

            self.markers.append(marker)
            self.labels.append(label)
        self.draw()

    def clearMap(self):
        if len(self.markers):
            for marker in self.markers:
                marker.remove()
            self.markers = []
            for  label in self.labels:
                label.remove()
            self.labels = []
            self.draw()

class PlotRes(FigureCanvas):
    finished_clk = Signal(object)
    signal_dbclick = Signal(object, object)
    
    def __init__(self, width,height):
        self.outlierFlag = 0
        self.clkbkFlag = 0
        self.typeFlag = 0
        self.rmMark = [[],[],[]] # first is baseline index, second is xData index, third is residual index
        self.getColor()
    
        self.fig = Figure(figsize=(width,height),tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.figInit()


        # self.background = None
        #self.canvas = FigureCanvas(self.fig)

        self.chid1 = self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        #self.chid3 = self.canvas.mpl_connect("button_release_event", self.onRelease)
        # self.chid4 = self.canvas.mpl_connect("scroll_event", self.do_scrollZoom)

    def initParam(self, scanInfo, stationInfo, result, session):
        self.scanInfo = scanInfo
        self.stationInfo = stationInfo
        self.result = result
        if self.typeFlag == 0:
            self.result = result[0]
            self.resultErr = result[1]
        self.blUsed = np.array(scanInfo.blUsed)
        self.useObs = np.where(self.scanInfo.Obs2Scan!=0)
        self.session = session
            
    def plotAll(self):
        
        blNum = len(self.scanInfo.blUsed)
        self.xbl = np.linspace(0,blNum-1,blNum,dtype=int).tolist()
        self.xData = []
        self.yData = []
        self.yDataErr = []
        self.plotColor = []
        for i in range(blNum):
            self.xData.append(self.scanInfo.blMJD[i])
            if self.typeFlag == 0:
                self.yData.append(self.result[self.scanInfo.blResPosit[i]]/const.c*1E9)
                self.yDataErr.append(self.resultErr[self.scanInfo.blResPosit[i]]/const.c*1E9)
            else:
                self.yData.append(self.result[self.scanInfo.blResPosit[i]])
            if blNum > 150:
                self.plotColor.append('#e78ea5')
            else:
                self.plotColor.append(self.color[i])
            
        self.title = self.session+' (ALL)'
        self.plotData()
        
    def plotStation(self, stationID, listIndex):
        
        staIndex = self.scanInfo.staUsed[stationID]
        self.xbl = self.scanInfo.staBlList[stationID][listIndex].tolist()
        # self.xbl = blPosit

        self.xData = []
        self.yData = []
        self.yDataErr = []
        self.plotColor = []
        
        # for ibl in self.scanInfo.staBlList[stationID]:
        for i in range(len(self.xbl)):
            ibl = self.xbl[i]
        # for ibl in self.xbl:
            self.xData.append(self.scanInfo.blMJD[ibl])
            if self.typeFlag == 0:
                self.yData.append(self.result[self.scanInfo.blResPosit[ibl]]/const.c*1E9)
                self.yDataErr.append(self.resultErr[self.scanInfo.blResPosit[ibl]]/const.c*1E9)
            else:
                self.yData.append(self.result[self.scanInfo.blResPosit[ibl]])
            
            if len(self.scanInfo.blUsed) > 150:
                self.plotColor.append(self.color[i])
            else:
                self.plotColor.append(self.color[ibl])
            # self.plotColor.append(self.color[ibl])
        
        self.title = self.session+' (%s)'%self.scanInfo.stationAll[staIndex-1]
        self.plotData()

    def plotSource(self, sourceID):
        self.resPosit = self.scanInfo.souResPosit[sourceID]
        self.xbl = [sourceID]

        self.xData = [self.scanInfo.souMJD[sourceID]]

        if self.typeFlag == 0:
            self.yData = [self.result[self.scanInfo.souResPosit[sourceID]]/const.c*1E9]
            self.yDataErr = [self.resultErr[self.scanInfo.souResPosit[sourceID]]/const.c*1E9]
        else:
            self.yData = [self.result[self.scanInfo.souResPosit[sourceID]]]

        if len(self.scanInfo.sourceAll)>150:
            self.plotColor = ['#e78ea5']
        else:
            self.plotColor = [self.color[sourceID]]

        #self.title = self.session + ' (%s)' % self.scanInfo.sourceAll[sourceID]
        self.title = self.session

        self.plotData()
        
    def plotBaseline(self, baselineID):
        
        self.resPosit = self.scanInfo.blResPosit[baselineID]
        self.xbl = [baselineID]
        
        self.xData = [self.scanInfo.blMJD[baselineID]]
        if self.typeFlag == 0:
            self.yData = [self.result[self.scanInfo.blResPosit[baselineID]]/const.c*1E9]
            self.yDataErr = [self.resultErr[self.scanInfo.blResPosit[baselineID]]/const.c*1E9]
        else:
            self.yData = [self.result[self.scanInfo.blResPosit[baselineID]]]
        if len(self.scanInfo.blUsed)>150:
            self.plotColor = ['#e78ea5']
        else:
            self.plotColor = [self.color[baselineID]]
        # self.plotColor = [self.color[baselineID]]
        
        self.title = self.session+' (%s-%s)'%(self.scanInfo.stationAll[self.blUsed[baselineID][0]-1],\
                                              self.scanInfo.stationAll[self.blUsed[baselineID][1]-1])
        self.plotData()
    
                            
    def plotData(self):

        matplotlib.rcParams['path.simplify'] = True
        matplotlib.rcParams['path.simplify_threshold'] = 0.1
        matplotlib.rcParams['agg.path.chunksize'] = 10000

        fontSize = 15
        useDay = np.round(self.scanInfo.scanMJD[-1] - self.scanInfo.scanMJD[0])

        if useDay == 0:
            xlabel = '%02d.%02d.%4d'%(self.scanInfo.scanTime[0][2],self.scanInfo.scanTime[0][1],\
                                      self.scanInfo.scanTime[0][0])
        elif useDay == 1:
            xlabel = '%02d.%02d.%4d-%02d.%02d.%4d'%(self.scanInfo.scanTime[0][2],self.scanInfo.scanTime[0][1],self.scanInfo.scanTime[0][0],\
                                                    self.scanInfo.scanTime[-1][2],self.scanInfo.scanTime[-1][1],self.scanInfo.scanTime[-1][0])
        else:
            xlabel = ''
        maxValue = 0
        minValue = 0
        for i in range(len(self.xData)):
            if self.typeFlag == 1:
                self.axes.plot(self.xData[i],self.yData[i],color=self.plotColor[i],marker='o',linestyle='None')
            else:
                self.axes.errorbar(self.xData[i],self.yData[i],yerr=self.yDataErr[i],color=self.plotColor[i],marker='o',linestyle='None')
                
                            
            if max(self.yData[i]) > maxValue:
                maxValue = max(self.yData[i])
            if min(self.yData[i]) < minValue:
                minValue = min(self.yData[i])

        self.axes.set_xlabel('Time(UTC) '+xlabel, fontsize=fontSize)
        if self.typeFlag == 0:
            self.axes.set_ylabel('Res: GR delay / ns', fontsize=fontSize)
        elif self.typeFlag == 1:
            self.axes.set_ylabel('Sigma of GR delay / ns')
        self.axes.set_title(self.title, fontsize=fontSize)
        
                
        if useDay == 1:
            self.xticksSpace(3.0/24.0)
            xlim_min = int(self.scanInfo.scanMJD[0]) + np.floor((self.scanInfo.scanMJD[0]-int(self.scanInfo.scanMJD[0]))*24)/24 - 1/24
            xlim_max = int(self.scanInfo.scanMJD[-1]) + np.ceil((self.scanInfo.scanMJD[-1]-int(self.scanInfo.scanMJD[-1]))*24)/24 + 1/24
        else:
            xlim_min = int(self.scanInfo.scanMJD[0]) + np.floor((self.scanInfo.scanMJD[0]-int(self.scanInfo.scanMJD[0]))*96)/96 - 15/1440
            xlim_max = int(self.scanInfo.scanMJD[-1]) + np.ceil((self.scanInfo.scanMJD[-1]-int(self.scanInfo.scanMJD[-1]))*96)/96 + 15/1440
            self.xticksSpace(15.0/1440.0)
            
        self.axes.set_xlim([xlim_min, xlim_max])
        
        self.axes.tick_params(axis='x',labelsize=fontSize)
        self.axes.tick_params(axis='y',labelsize=fontSize)
        
        self.draw()
        
    def onClick(self,event):
        '''
        Get the mouse click position in axes.
        
        '''
        
        self.rectSx = None
        self.rectSy = None
        if event.inaxes:
            
            if self.clkbkFlag == 1:
                self.clkbkTime = event.xdata
                self.finished_clk.emit(event.xdata)
            else:
                self.rectSx = event.xdata
                self.rectSy = event.ydata
                
            if event.dblclick:
                self.leftSelector.set_active(False)
                self.rightSelector.set_active(False)
                showPosit = []
                minValue = []
                for i in range(len(self.xData)):
                    resx = np.abs(self.xData[i]-event.xdata)
                    xminp = np.where(resx==min(resx))[0]
                    minValue.append(abs(self.yData[i][xminp[0]]-event.ydata))
                    showPosit.append(xminp[0])
                                         
                index = np.where(minValue==min(minValue))[0]
                ymin,ymax = self.axes.get_ybound()
                space = (ymax-ymin)*0.1
                if min(minValue) < space:
                    blPosit = self.xbl[index[0]]
                    self.signal_dbclick.emit(blPosit, showPosit[index[0]])

            else:
                self.leftSelector.set_active(True)
                self.rightSelector.set_active(True)

                
    def onRelease(self, event):
        '''
        Get the select region and amplify, if outlier mode, point the select.

        '''
        self.rectEx = None
        self.rectEy = None
        
        if event.inaxes:
            self.rectEx = event.xdata
            self.rectEy = event.ydata
            
            if self.rectSx != None and self.rectEx != None:
                x1 = min(self.rectSx,self.rectEx)
                x2 = max(self.rectSx,self.rectEx)
                y1 = min(self.rectSy,self.rectEy)
                y2 = max(self.rectSy,self.rectEy)
                
                if self.outlierFlag == 1:
                    selectPoint = [[],[],[]]   # first is xData index, second is baseline index, third is resposit index
                    for i in range(len(self.xData)):
                        p1 = np.where((self.xData[i] >= x1) & (self.xData[i] <= x2))[0]
                        if len(p1):
                            p2 = np.where((self.yData[i][p1] >= y1) & (self.yData[i][p1] <= y2))[0]
                        
                            if len(p2):
                                selectPoint[0].append(i)
                                selectPoint[1].append(self.xbl[i])
                                selectPoint[2].append(p1[p2].tolist())
                                
                    if event.button == 1:
                        for i in range(len(selectPoint[0])):
                            # self.axes.plot(self.xData[selectPoint[0][i]][selectPoint[2][i]], self.yData[selectPoint[0][i]][selectPoint[2][i]],\
                            #                color=self.plotColor[selectPoint[0][i]],marker='o',mfc='w',linestyle='None')
                            self.axes.errorbar(self.xData[selectPoint[0][i]][selectPoint[2][i]], self.yData[selectPoint[0][i]][selectPoint[2][i]],\
                                               yerr=self.yDataErr[selectPoint[0][i]][selectPoint[2][i]], color=self.plotColor[selectPoint[0][i]],\
                                               marker='o',mfc='w',linestyle='None')
                            self.draw()
                            
                            if selectPoint[1][i] not in self.rmMark[0]:
                                self.rmMark[0].append(selectPoint[1][i])
                                self.rmMark[1].append(selectPoint[2][i])
                                self.rmMark[2].append(self.scanInfo.blResPosit[selectPoint[1][i]][selectPoint[2][i]].tolist())
                            else:
                                index = self.rmMark[0].index(selectPoint[1][i])
                                for j in selectPoint[2][i]:
                                    if j not in self.rmMark[1][index]:
                                        self.rmMark[1][index].append(j)
                                        self.rmMark[2][index].append(self.scanInfo.blResPosit[selectPoint[1][i]][j])
                                                                    
                    elif event.button == 3:
                        for i in range(len(selectPoint[0])):
                            # self.axes.plot(self.xData[selectPoint[0][i]][selectPoint[2][i]], self.yData[selectPoint[0][i]][selectPoint[2][i]],\
                            #                color=self.plotColor[selectPoint[0][i]],marker='o',linestyle='None')
                            self.axes.errorbar(self.xData[selectPoint[0][i]][selectPoint[2][i]], self.yData[selectPoint[0][i]][selectPoint[2][i]],\
                                               yerr=self.yDataErr[selectPoint[0][i]][selectPoint[2][i]],color=self.plotColor[selectPoint[0][i]],\
                                               marker='o',linestyle='None')
                            self.draw()
                            
                            if selectPoint[1][i] in self.rmMark[0]:
                                index = self.rmMark[0].index(selectPoint[1][i])
                                for j in selectPoint[2][i]:
                                    if j in self.rmMark[1][index]:
                                        popPosit = self.rmMark[1][index].index(j)
                                        self.rmMark[1][index].pop(popPosit)
                                        self.rmMark[2][index].pop(popPosit)
                                if len(self.rmMark[1]) != 0 and len(self.rmMark[1][index]) == 0:
                                    self.rmMark[0].pop(index)
                                    self.rmMark[1].pop(index)
                                    self.rmMark[2].pop(index)
                else:
                    if x1 != x2 or x2-x1>1.0/1440.0:
                        self.axes.set_xlim([x1,x2])
                        self.axes.set_ylim([y1,y2])
                        if x2-x1 > 2.0/24.0:
                            self.xticksSpace(30.0/1440.0)
                        elif x2-x1 > 30.0/1440.0:
                            self.xticksSpace(10.0/1440.0)
                        elif x2-x1 > 10.0/1440.0:
                            self.xticksSpace(2.0/1440.0)
                        elif x2-x1 < 5.0/1440.0:
                            self.xticksSpace(1.0/1440.0)
                        
                        self.draw()

    def onLegtRelease(self, eclick, erelease):
        '''
        Get the select region and amplify, if outlier mode, point the select.

        '''

        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        if self.outlierFlag == 1:
            selectPoint = [[], [],
                           []]  # first is xData index, second is baseline index, third is resposit index
            for i in range(len(self.xData)):
                p1 = np.where((self.xData[i] >= x1) & (self.xData[i] <= x2))[0]
                if len(p1):
                    p2 = np.where((self.yData[i][p1] >= y1) & (self.yData[i][p1] <= y2))[0]

                    if len(p2):
                        selectPoint[0].append(i)
                        selectPoint[1].append(self.xbl[i])
                        selectPoint[2].append(p1[p2].tolist())


            for i in range(len(selectPoint[0])):
                # self.axes.plot(self.xData[selectPoint[0][i]][selectPoint[2][i]], self.yData[selectPoint[0][i]][selectPoint[2][i]],\
                #                color=self.plotColor[selectPoint[0][i]],marker='o',mfc='w',linestyle='None')
                self.axes.errorbar(self.xData[selectPoint[0][i]][selectPoint[2][i]],
                                   self.yData[selectPoint[0][i]][selectPoint[2][i]], \
                                   yerr=self.yDataErr[selectPoint[0][i]][selectPoint[2][i]],
                                   color=self.plotColor[selectPoint[0][i]], \
                                   marker='o', mfc='w', linestyle='None')
                self.draw()

                if selectPoint[1][i] not in self.rmMark[0]:
                    self.rmMark[0].append(selectPoint[1][i])
                    self.rmMark[1].append(selectPoint[2][i])
                    self.rmMark[2].append(
                        self.scanInfo.blResPosit[selectPoint[1][i]][selectPoint[2][i]].tolist())
                else:
                    index = self.rmMark[0].index(selectPoint[1][i])
                    for j in selectPoint[2][i]:
                        if j not in self.rmMark[1][index]:
                            self.rmMark[1][index].append(j)
                            self.rmMark[2][index].append(self.scanInfo.blResPosit[selectPoint[1][i]][j])
        else:
            if x1 != x2 or x2 - x1 > 1.0 / 1440.0:
                self.axes.set_xlim([x1, x2])
                self.axes.set_ylim([y1, y2])
                if x2 - x1 > 2.0 / 24.0:
                    self.xticksSpace(30.0 / 1440.0)
                elif x2 - x1 > 30.0 / 1440.0:
                    self.xticksSpace(10.0 / 1440.0)
                elif x2 - x1 > 10.0 / 1440.0:
                    self.xticksSpace(2.0 / 1440.0)
                elif x2 - x1 < 5.0 / 1440.0:
                    self.xticksSpace(1.0 / 1440.0)

                self.draw()

    def onRightRelease(self, eclick, erelease):
        '''
        Get the select region, unselect point.

        '''

        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        if self.outlierFlag == 1:
            selectPoint = [[], [],
                           []]  # first is xData index, second is baseline index, third is resposit index
            for i in range(len(self.xData)):
                p1 = np.where((self.xData[i] >= x1) & (self.xData[i] <= x2))[0]
                if len(p1):
                    p2 = np.where((self.yData[i][p1] >= y1) & (self.yData[i][p1] <= y2))[0]

                    if len(p2):
                        selectPoint[0].append(i)
                        selectPoint[1].append(self.xbl[i])
                        selectPoint[2].append(p1[p2].tolist())


            for i in range(len(selectPoint[0])):
                # self.axes.plot(self.xData[selectPoint[0][i]][selectPoint[2][i]], self.yData[selectPoint[0][i]][selectPoint[2][i]],\
                #                color=self.plotColor[selectPoint[0][i]],marker='o',mfc='w',linestyle='None')
                self.axes.errorbar(self.xData[selectPoint[0][i]][selectPoint[2][i]],
                                   self.yData[selectPoint[0][i]][selectPoint[2][i]], \
                                   yerr=self.yDataErr[selectPoint[0][i]][selectPoint[2][i]],
                                   color=self.plotColor[selectPoint[0][i]], \
                                   marker='o', linestyle='None')
                self.draw()

                if selectPoint[1][i] in self.rmMark[0]:
                    index = self.rmMark[0].index(selectPoint[1][i])
                    for j in selectPoint[2][i]:
                        if j in self.rmMark[1][index]:
                            popPosit = self.rmMark[1][index].index(j)
                            self.rmMark[1][index].pop(popPosit)
                            self.rmMark[2][index].pop(popPosit)
                    if len(self.rmMark[1]) != 0 and len(self.rmMark[1][index]) == 0:
                        self.rmMark[0].pop(index)
                        self.rmMark[1].pop(index)
                        self.rmMark[2].pop(index)


    def do_scrollZoom(self,event):
        ax = event.inaxes
        if ax == None:
            return
        
        xmin,xmax = ax.get_xbound()
        ymin,ymax = ax.get_ybound()

        xc = event.xdata
        yc = event.ydata
        
        xlen1 = xc - xmin
        xlen2 = xmax - xc
        ylen1 = yc - ymin
        ylen2 = ymax - yc

        xchg1 = event.step * xlen1 / 10
        xchg2 = event.step * xlen2 / 10
        xmin = xmin + xchg1
        xmax = xmax - xchg2
        ychg1 = event.step * ylen1 / 10
        ychg2 = event.step * ylen2 / 10
        ymin = ymin + ychg1
        ymax = ymax - ychg2
        ax.set_xbound(xmin,xmax)
        ax.set_ybound(ymin,ymax)
        
        # ax.set_xlim(xmin,xmax)
        # ax.set_ylim(ymin,ymax)
        # self.xticksSpace()
        event.canvas.draw()

        
    def xticksSpace(self,num):
        # xmin,xmax = self.axes.get_xlim()
        
        # self.axes.xaxis.set_major_locator(ticker.MultipleLocator((xmax-xmin)/num))
        x_major_locator=MultipleLocator(num)
        
        self.axes.xaxis.set_major_locator(x_major_locator)
        
        xnum = self.axes.get_xticks()
        
        xticks = []
        for i in range(len(xnum)):
            y,m,d,h,mi,s = mjd2ymdhms(xnum[i])
            if s > 59:
                tmi = mi + 1
            elif s < 1:
                tmi = mi
            if tmi == 60:
                tmi = 0
                th = h + 1
                if th == 24:
                    th = 0
            else:
                th = h
            xticks.append('%02d:%02d'%(th,tmi))
        
        self.axes.set_xticks(xnum, xticks)
        self.axes.grid('on')
        
    def figInit(self):
        select_style = {'fill': False,
                        'edgecolor': 'red',
                        'alpha': 0.3,
                        'linewidth': 2,
                        'linestyle': '--'}

        self.leftSelector = RectangleSelector(self.axes,
                                          self.onLegtRelease,
                                          useblit = True,
                                          button = [1],
                                          props = select_style,
                                          minspanx = 5,
                                          minspany = 5,
                                          spancoords = 'pixels',
                                          interactive = False)

        self.rightSelector = RectangleSelector(self.axes,
                                              self.onRightRelease,
                                              useblit=True,
                                              button=[3],
                                              props=select_style,
                                              minspanx=5,
                                              minspany=5,
                                              spancoords='pixels',
                                              interactive=False)


        self.axes.clear()
        self.axes.grid(color='silver',linewidth=1,alpha=0.3)
        self.draw()
        # self.axes.set_xlim([0,1])
        # self.axes.set_ylim([0,1])
        # cr = 'silver'
        # self.axes.grid(color=cr,linewidth=1,alpha=0.3)
        # self.axes.spines['left'].set_color(cr)
        # self.axes.spines['right'].set_color(cr)
        # self.axes.spines['top'].set_color(cr)
        # self.axes.spines['bottom'].set_color(cr)
        # self.axes.tick_params(axis='x',colors=cr)
        # self.axes.tick_params(axis='y',colors=cr)
        
        # self.axes.patch.set_color('whitesmoke')
        # self.axes.spines['top'].set_visible(False)

    def getColor(self):
        self.color = ['#e50000','#653700','#ff81c0','#0343df','#15b01a','#7e1e9c','#acc2d9','#56ae57','#b2996e','#a8ff04',\
                      '#69d84f','#894585','#70b23f','#d4ffff','#65ab7c','#952e8f','#fcfc81','#a5a391','#388004','#4c9085',\
                      '#5e9b8a','#efb435','#d99b82','#0a5f38','#0c06f7','#61de2a','#3778bf','#2242c7','#533cc6','#9bb53c',\
                      '#05ffa6','#1f6357','#017374','#0cb577','#ff0789','#afa88b','#08787f','#dd85d7','#a6c875','#a7ffb5',\
                      '#c2b709','#e78ea5','#966ebd','#ccad60','#ac86a8','#947e94','#983fb2','#ff63e9','#b2fba5','#63b365',\
                      '#8ee53f','#b7e1a1','#ff6f52','#bdf8a3','#d3b683','#fffcc4','#430541','#ffb2d0','#997570','#ad900d',\
                      '#c48efd','#507b9c','#7d7103','#fffd78','#da467d','#410200','#c9d179','#fffa86','#5684ae','#6b7c85',\
                      '#6f6c0a','#7e4071','#009337','#d0e429','#fff917','#1d5dec','#054907','#b5ce08','#8fb67b','#c8ffb0',\
                      '#fdde6c','#ffdf22','#a9be70','#6832e3','#fdb147','#c7ac7d','#fff39a','#850e04','#efc0fe','#40fd14',\
                      '#b6c406','#9dff00','#3c4142','#f2ab15','#ac4f06','#c4fe82','#2cfa1f','#9a6200','#ca9bf7','#875f42',\
                      '#3a2efe','#fd8d49','#8b3103','#cba560','#698339','#0cdc73','#b75203','#7f8f4e','#26538d','#63a950',\
                      '#c87f89','#b1fc99','#ff9a8a','#f6688e','#76fda8','#53fe5c','#4efd54','#a0febf','#7bf2da','#bcf5a6',\
                      '#ca6b02','#107ab0','#2138ab','#719f91','#fdb915','#fefcaf','#fcf679','#1d0200','#cb6843','#31668a',\
                      '#247afd','#ffffb6','#90fda9','#86a17d','#fddc5c','#78d1b6','#13bbaf','#fb5ffc','#20f986','#ffe36e',\
                      '#9d0759','#3a18b1','#c2ff89','#d767ad','#720058','#ffda03','#01c08d','#ac7434','#014600','#9900fa']


class PlotStation(FigureCanvas):
    
    def __init__(self, width,height):
        self.outlierFlag = 0
        self.clkbkFlag = 0
        self.typeFlag = 0
        self.getColor()
    
        self.fig = Figure(figsize=(width,height),tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.figInit()
        
        self.canvas = FigureCanvas(self.fig)
        
        
    def initParam(self, scanInfo, stationInfo):
        self.scanInfo = scanInfo
        self.stationInfo = stationInfo
        
    def plotInit(self, flag, listPosit):
        
        obsPosit = np.where(self.scanInfo.Obs2Scan!=0)
        scanNum = (np.unique(self.scanInfo.Obs2Scan[obsPosit]) - 1).tolist()
        # print(len(scanNum))
        
        if flag == 0:
            yData = self.scanInfo.T
            scale = 1
            self.ylabel = 'Temperature (C)'
        elif flag == 1:        
            yData = self.scanInfo.H
            scale = 100
            self.ylabel = 'Humidity (%)'
        elif flag == 2:
            yData = self.scanInfo.P
            scale = 1
            self.ylabel = 'Pressure (mb)'
        elif flag == 3:
            yData = self.scanInfo.cableCal
            scale = 1E12
            self.ylabel = 'Cable Cal (ps)'
        if flag == 4:
            scale = 1
            self.ylabel = 'fmout-GNSS (s)'
        
        self.xData = []
        self.yData = []
        self.plotColor = []
        
        if flag != 4:
            for i in listPosit:
                ista = self.scanInfo.staUsed[i] - 1
                self.plotColor.append(self.color[ista])
                
                scanSta = np.where(self.scanInfo.Scan2Station[:,ista] != 0)
                temp = np.where(self.scanInfo.Station2Scan[:,ista] != 0)
                staScan = (self.scanInfo.Station2Scan[temp[0],ista] - 1).tolist()  
                # if ista == 0:
                #     print([len(self.scanInfo.Scan2Station[:,ista]), len(scanSta[0]),len(staScan)])
                
                staMJD = []
                staData = []
                # xiscan = []
                # yiscan = []
                for iscan in scanSta[0]:
                    if iscan in scanNum:
                        staMJD.append(self.scanInfo.scanMJD[scanNum.index(iscan)])
                        # xiscan.append(iscan)
                    if iscan in staScan:
                        staData.append(yData[ista][staScan.index(iscan)]*scale)
                        # yiscan.append(iscan)
                self.xData.append(staMJD)
                self.yData.append(staData)
        else:
            for i in listPosit:
                ista = self.scanInfo.staUsed[i] - 1
                self.plotColor.append(self.color[ista])
                self.xData.append(self.scanInfo.Fmout_GNSS[ista][0])
                self.yData.append(self.scanInfo.Fmout_GNSS[ista][1])
        
        self.plotData()
        
    def plotData(self):
        
        useDay = np.floor(self.scanInfo.scanMJD[-1]) - np.floor(self.scanInfo.scanMJD[0])
        if useDay == 0:
            xlabel = '%02d.%02d.%4d'%(self.scanInfo.scanTime[0][2],self.scanInfo.scanTime[0][1],\
                                      self.scanInfo.scanTime[0][0])
        elif useDay == 1:
            xlabel = '%02d.%02d.%4d-%02d.%02d.%4d'%(self.scanInfo.scanTime[0][2],self.scanInfo.scanTime[0][1],self.scanInfo.scanTime[0][0],\
                                                    self.scanInfo.scanTime[-1][2],self.scanInfo.scanTime[-1][1],self.scanInfo.scanTime[-1][0])
        else:
            xlabel = ''
        for i in range(len(self.xData)):        
            self.axes.plot(self.xData[i],self.yData[i],color=self.plotColor[i],marker='o',linestyle='-')
        
        self.axes.set_xlabel('Time(UTC) '+xlabel)
        self.axes.set_ylabel(self.ylabel)
        # self.axes.set_xlim([self.scanInfo.scanMJD[0],self.scanInfo.scanMJD[-1]])
        self.axes.grid('on')
        
        
        xnum = self.axes.get_xticks()
        xticks = []
        for i in range(len(xnum)):
            y,m,d,h,mi,s = mjd2ymdhms(xnum[i])
            xticks.append('%02d:%02d'%(h,mi))
        self.axes.set_xticks(xnum, xticks) 
        self.draw()
    
    def figInit(self):
        
        # self.axes.set_xlim([0,1])
        # self.axes.set_ylim([0,1])
        cr = 'silver'
        self.axes.grid(color=cr,linewidth=1,alpha=0.3)
    
    def getColor(self):
        self.color = ['#e50000','#653700','#ff81c0','#0343df','#15b01a','#7e1e9c','#000000','#FFA500','#00FFFF','#7FF000',\
                      '#FF00FF','#7CFC00','#808000','#FFFF00','#708090','#000080','#fcfc81','#a5a391','#388004','#4c9085',\
                      '#5e9b8a','#efb435','#d99b82','#0a5f38','#0c06f7','#61de2a','#3778bf','#2242c7','#533cc6','#9bb53c',\
                      '#05ffa6','#1f6357','#017374','#0cb577','#ff0789','#afa88b','#08787f','#dd85d7','#a6c875','#a7ffb5',\
                      '#c2b709','#e78ea5','#966ebd','#ccad60','#ac86a8','#947e94','#983fb2','#ff63e9','#b2fba5','#63b365']
            
class PlotResult(FigureCanvas):
    
    def __init__(self, width,height):
        self.outlierFlag = 0
        self.clkbkFlag = 0
        self.typeFlag = 0
        self.getColor()
    
        self.fig = Figure(figsize=(width,height),tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.figInit()
        
        self.canvas = FigureCanvas(self.fig)
        
    def initParam(self, scanInfo, Param, stationInfo, result, out):
        self.scanInfo = scanInfo
        self.Param = Param
        self.result = result
        self.stationInfo = stationInfo
        self.out = out
        
        
    def plotInit(self, flag, staStr):
        
        if flag == 0:
            self.ylabel = 'Clock (cm)'
            index = self.result.clkEstInfo[0].index(staStr)
            start = sum(self.result.clkEstInfo[1][:index])
            end = start+self.result.clkEstInfo[1][index]
            self.yData = self.result.para[start:end]*100
            self.yDataErr = self.result.err[start:end]*100
            self.xData = np.floor(self.scanInfo.scanMJD[0]) + np.array(self.result.paramMJD[0])[start:end]/1440
            self.plotColor = self.color[index]
            
        if flag == 1:
            self.ylabel = 'ZWD (cm)'
            index = self.result.zwdEstInfo[0].index(staStr)
            addNum = sum(self.result.clkEstInfo[1])
            start = addNum + sum(self.result.zwdEstInfo[1][:index])
            end = start+self.result.zwdEstInfo[1][index]
            self.yData = self.result.para[start:end]*100
            self.yDataErr = self.result.err[start:end]*100
            self.xData = np.floor(self.scanInfo.scanMJD[0]) + np.array(self.result.paramMJD[1])[start-addNum:end-addNum]/1440
            self.plotColor = self.color[index]
            
        # if flag == 2:
            
        
        if flag == 4:
            index = self.out.param.index('ut1')
            indexr = self.out.param.index('lod')
            self.ylabel = r'$\delta$UT1 (ms)'
            name = 'UT1'
        elif flag == 5:
            index = self.out.param.index('pmx')
            indexr = self.out.param.index('pmxr')
            self.ylabel = r'$\delta polar_{x}$ (mas)'
            name = 'polar_{x}'
        elif flag == 6:
            index = self.out.param.index('pmy')
            indexr = self.out.param.index('pmyr')
            self.ylabel = r'$\delta polar_{y}$ (mas)'
            name = 'polar_{y}'
        
        if (flag == 4 or flag == 5 or flag == 6) and self.Param.Flags.type == 'POLY':
            paramPoly = [0,0]
            if self.out.estFlag[index] == 1:
                paramPoly[1] = self.out.estValue[index][0]
                if self.out.estFlag[indexr] == 1:
                    paramPoly[0] = self.out.estValue[indexr][0]
            self.label = r'$\delta %s=%8.4f + %8.4f*t$'%(name, paramPoly[1], paramPoly[0])
            
            polyCoef = np.poly1d(paramPoly)
            self.xData = self.scanInfo.scanMJD
            self.yData = polyCoef(self.xData - self.scanInfo.refMJD)    
            
        elif (flag == 4 or flag == 5 or flag == 6) and self.Param.Flags.type == 'SEGMENT':
            self.xData = self.out.mjd[index]
            self.yData = self.out.estValue[index]
        
        self.plotData(flag)
            
    def plotData(self, flag):
        useDay = np.floor(self.scanInfo.scanMJD[-1]) - np.floor(self.scanInfo.scanMJD[0])
        if useDay == 0:
            xlabel = '%02d.%02d.%4d'%(self.scanInfo.scanTime[0][2],self.scanInfo.scanTime[0][1],\
                                      self.scanInfo.scanTime[0][0])
        elif useDay == 1:
            xlabel = '%02d.%02d.%4d-%02d.%02d.%4d'%(self.scanInfo.scanTime[0][2],self.scanInfo.scanTime[0][1],self.scanInfo.scanTime[0][0],\
                                                    self.scanInfo.scanTime[-1][2],self.scanInfo.scanTime[-1][1],self.scanInfo.scanTime[-1][0])

        if (flag == 4 or flag == 5 or flag == 6) and self.Param.Flags.type == 'POLY':
            self.axes.plot(self.xData,self.yData,color=self.color[0], marker='o',linestyle='None')
            self.axes.text(self.scanInfo.scanMJD[0], max(self.yData), self.label)
        elif (flag == 4 or flag == 5 or flag == 6) and self.Param.Flags.type == 'SEGMENT':
            self.axes.plot(self.xData,self.yData,color=self.color[0], marker='o')
        elif flag == 0 or flag == 1:
            self.axes.errorbar(self.xData,self.yData,yerr=self.yDataErr,color=self.plotColor, marker='o')
            
        
         
        self.axes.set_xlabel('Time(UTC) '+xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.grid('on')
        
        xnum = self.axes.get_xticks()
        xticks = []
        for i in range(len(xnum)):
            y,m,d,h,mi,s = mjd2ymdhms(xnum[i])
            xticks.append('%02d:%02d'%(h,mi))
        self.axes.set_xticks(xnum, xticks)
        
        self.draw()
       
            
    def figInit(self):
        
        self.axes.set_xlim([0,1])
        self.axes.set_ylim([0,1])
        cr = 'silver'
        self.axes.grid(color=cr,linewidth=1,alpha=0.3)            

    def getColor(self):
        self.color = ['#e50000','#653700','#ff81c0','#0343df','#15b01a','#7e1e9c','#000000','#FFA500','#00FFFF','#7FF000',\
                      '#FF00FF','#7CFC00','#808000','#FFFF00','#708090','#000080','#fcfc81','#a5a391','#388004','#4c9085']
            
class PlotGlob(FigureCanvas):
    
    def __init__(self, width,height):
        self.outlierFlag = 0
        self.clkbkFlag = 0
        self.typeFlag = 0
        # self.getColor()
    
        self.fig = Figure(figsize=(width,height),tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.font = {'family' : 'Times New Roman', 
                     'size':13}
        # self.figInit()
        
        self.canvas = FigureCanvas(self.fig)

    def figInit(self):
        
        self.axes.set_xlim([0,1])
        self.axes.set_ylim([0,1])
        cr = 'silver'
        self.axes.grid(color=cr,linewidth=1,alpha=0.3)
        
        
    def plotSelect(self,typeFlag,choice,titleName,xData,yData):

        self.yData = []
        self.color = []
        self.legend = []
        self.title = titleName
        self.xData = xData

        color = ['r', 'b', 'k']
        if typeFlag == 0:
            self.ylabel = 'cm'
            legend = ['X','Y','Z']
            for i in range(3):
                if choice[i]:
                    self.yData.append(yData[:,i]-yData[0,i])
                    self.color.append(color[i])
                    self.legend.append(legend[i])
        elif typeFlag == 1:
            self.ylabel = 'mas'
            legend = ['Ra','De']
            for i in range(2):
                if choice[i]:
                    self.yData.append(yData[:,i])
                    self.color.append(color[i])
                    self.legend.append(legend[i])
        
        self.plotData()
        
    def plotData(self):
        
        for i in range(len(self.yData)):
            self.axes.plot(self.xData,self.yData[i],color=self.color[i], marker='o',linestyle='None')
        
        self.axes.legend(self.legend,fontsize=self.font['size'])
        self.axes.tick_params(axis='x',rotation=45)
        self.axes.tick_params(labelsize=self.font['size'])
        self.axes.set_xlabel('MJD',self.font)
        self.axes.set_ylabel(self.ylabel,self.font)
        self.axes.set_title(self.title,self.font)
        self.axes.grid('on')        
        self.draw()
