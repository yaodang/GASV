#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys,datetime,os,multiprocessing
from itertools import *
from COMMON import *
from GUI import mysource_rc
from GUI import *
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
# from MAKE import createFromProcess
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt

from GUI.Figure import Ui_GASV


class MyForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_GASV()
        self.ui.setupUi(self)
        
        self.name,self.dirpath = read_initdir()
        self.updatePreference()
        
        
        # the class of plot
        self.plot_mapsta = PlotMapSta(50,50)
        self.ui.horizontalLayout_prarm_mapsta.addWidget(self.plot_mapsta)

        self.plot_mapsou = PlotMapSou(50, 50)
        self.ui.horizontalLayout_prarm_mapsou.addWidget(self.plot_mapsou)

        self.plot_res = PlotRes(50,50)
        self.ui.verticalLayout_plot_res.addWidget(self.plot_res)
        self.plot_res.finished_clk.connect(self.plot_signal_showClockBreak)
        self.plot_res.signal_dbclick.connect(self.plot_signal_showBaseLine)
        
        self.plot_sta = PlotStation(50,50)
        toolbar0 = NavigationToolbar(self.plot_sta, self)
        self.ui.verticalLayout_plot_sta.addWidget(toolbar0)
        self.ui.verticalLayout_plot_sta.addWidget(self.plot_sta)
        
        self.plot_result = PlotResult(50,50)
        toolbar1 = NavigationToolbar(self.plot_result, self)
        self.ui.verticalLayout_plot_result.addWidget(toolbar1)
        self.ui.verticalLayout_plot_result.addWidget(self.plot_result)
        
        self.plot_glob = PlotGlob(50,50)
        toolbar2 = NavigationToolbar(self.plot_glob, self)
        self.ui.verticalLayout_plot_glob.addWidget(toolbar2)
        self.ui.verticalLayout_plot_glob.addWidget(self.plot_glob)

        font = QFont('Consolas', 12)
        self.ui.textEdit_glob.setFont(font)
        self.ui.textBrowser_information.setFont(font)
        #self.ui.textBrowser.setFont(font)

        self.init_gui()
        self.init_param()
        
        # the class of init, mod adn solve thread
        self.backend = runThread()
        self.backend.finished.connect(self.thread_signal_showResult)
        self.backend.error.connect(self.thread_signal_runError)
        
        # the class of output thread
        self.outthread = resultThread()
        self.outthread.finished.connect(self.thread_signal_showOutFinish)
        
        # the class of ambiguity correct thread
        self.ambCorr = ambigCorrThread()
        self.ambCorr.finished.connect(self.thread_signal_showAmbCorr)
        
        self.globthread = GLOBThread()
        self.globthread.finished.connect(self.thread_signal_showGlob)
        
        self.LocalThread = localFileThread()
        self.LocalThread.initSet()
        self.LocalThread.finished.connect(self.thread_signal_showLocalResult)
        
        
        ############### menu action ##############
        self.ui.menu_file_welcome.triggered.connect(self.menuAction_showFileWelcome)
        self.ui.menu_file_input.triggered.connect(lambda:self.signal_showLoadData('menu',''))
        self.ui.menu_file_preference.triggered.connect(self.menuAction_showFilePreference)
        self.ui.menu_file_dblist.triggered.connect(self.menuAction_showDBList)
        self.ui.menu_file_exit.triggered.connect(self.closeEvent)

        self.ui.menu_param_basic.triggered.connect(self.menuAction_showParamBasic)

        self.ui.menu_data_Station.triggered.connect(self.menuAction_showDataStation)
        self.ui.menu_data_Baseline.triggered.connect(self.menuAction_showDataBaseline)
        self.ui.menu_data_Source.triggered.connect(self.menuAction_showDataSource)
        
        self.ui.menu_est_EOP.triggered.connect(self.menuAction_showEstEOP)
        self.ui.menu_est_clktrop.triggered.connect(self.menuAction_showEstClkTrop)
        
        self.ui.menu_glob_setup.triggered.connect(self.menuAction_showGlobSetup)
        self.ui.menu_glob_station.triggered.connect(self.menuAction_showGlobStation)
        self.ui.menu_glob_source.triggered.connect(self.menuAction_showGlobSource)
        
        self.ui.menu_plot_residual.triggered.connect(self.menuAction_showPlotRes)
        self.ui.menu_plot_station.triggered.connect(self.menuAction_showPlotStation)
        self.ui.menu_plot_result.triggered.connect(self.menuAction_showPlotResult)
        self.ui.menu_plot_glob.triggered.connect(self.menuAction_showPlotGlob)
        
        ############### pushbutton action ############
        self.ui.pushButton_file_save.clicked.connect(self.onBottonClick_savePath)
        self.ui.pushButton_file_typesub.clicked.connect(self.onBottonClick_dataTypeSub)
        self.ui.pushButton_file_typeadd.clicked.connect(self.onBottonClick_dataTypeAdd)
        self.ui.listWidget_datatype.itemSelectionChanged.connect(self.signal_localFileShow)
        self.ui.pushButton_file_makearc.clicked.connect(self.onBottonClick_produceARC)
        self.ui.pushButton_file_refresh.clicked.connect(self.signal_localFileShow)
        self.ui.pushButton_param_questions.clicked.connect(self.onBottonClick_showHelp)
        self.ui.pushButton_browse_vgosdb.clicked.connect(lambda:self.onBottonClick_browsePath(0))
        self.ui.pushButton_browse_master.clicked.connect(lambda: self.onBottonClick_browsePath(1))
        self.ui.pushButton_browse_apriori.clicked.connect(lambda:self.onBottonClick_browsePath(2))
        self.ui.pushButton_browse_station.clicked.connect(lambda:self.onBottonClick_browseFile(3))
        self.ui.pushButton_browse_source.clicked.connect(lambda:self.onBottonClick_browseFile(4))
        self.ui.pushButton_browse_eop.clicked.connect(lambda:self.onBottonClick_browseFile(5))
        self.ui.pushButton_browse_ephem.clicked.connect(lambda:self.onBottonClick_browseFile(6))
        self.ui.pushButton_browse_residual.clicked.connect(lambda:self.onBottonClick_browsePath(7))
        self.ui.pushButton_browse_report.clicked.connect(lambda:self.onBottonClick_browsePath(8))
        self.ui.pushButton_browse_snx.clicked.connect(lambda:self.onBottonClick_browsePath(9))
        self.ui.pushButton_browse_eopo.clicked.connect(lambda:self.onBottonClick_browsePath(10))
        self.ui.pushButton_browse_arcpath.clicked.connect(lambda:self.onBottonClick_browsePath(11))
        self.ui.pushButton_est_clearblclk.clicked.connect(self.onBottonClick_clearBlClk)
        self.ui.pushButton_autoset_source.clicked.connect(self.onBottonClick_setSouEst)
        self.ui.pushButton_autoset_station.clicked.connect(self.onBottonClick_setStaEst)
        self.ui.pushButton_process.clicked.connect(self.onBottonClick_process)
        self.ui.pushButton_glob_edit_trf.clicked.connect(self.onBottonClick_modify_nnrt_trf)
        self.ui.pushButton_glob_edit_crf.clicked.connect(self.onBottonClick_modify_nnr_crf)
        self.ui.pushButton_glob_edit_crf.clicked.connect(self.onBottonClick_modify_nnr_crf)
        self.ui.pushButton_glob_edit_globexsta.clicked.connect(self.onBottonClick_modify_exsta)
        self.ui.pushButton_glob_edit_globexsou.clicked.connect(self.onBottonClick_modify_exsou)
        self.ui.pushButton_glob_save.clicked.connect(self.onBottonClick_modify_save)
        self.ui.pushButton_glob_run.clicked.connect(self.onBottonClick_globrun)
        self.ui.pushButton_plot_save.clicked.connect(self.onBottonClick_saveOut)
        self.ui.pushButton_plot_reload.clicked.connect(lambda:self.signal_showLoadData('plot',''))
        #self.ui.pushButton_plot_reload.clicked.connect(self.onBottonClick_reLoad)
        self.ui.pushButton_plot_home.clicked.connect(self.onBottonClick_rePlot)
        self.ui.pushButton_plot_S.clicked.connect(lambda:self.onBottonClick_bandChoice(0))
        self.ui.pushButton_plot_X.clicked.connect(lambda:self.onBottonClick_bandChoice(1))
        self.ui.pushButton_plot_outlier.clicked.connect(self.onBottonClick_outlierMode)
        self.ui.pushButton_plot_remove.clicked.connect(self.onBottonClick_removeOutlier)
        self.ui.pushButton_plot_clkbk.clicked.connect(self.onBottonClick_clkbkMode)
        self.ui.pushButton_plot_ambAdd.clicked.connect(lambda:self.onBottonClick_ambAddandSub(1))
        self.ui.pushButton_plot_ambSub.clicked.connect(lambda:self.onBottonClick_ambAddandSub(-1))
        self.ui.pushButton_plot_ambigCorr.clicked.connect(self.onBottonClick_ambCorr)
        self.ui.pushButton_plot_ambigZero.clicked.connect(self.onBottonClick_ambZero)
        self.ui.pushButton_plot_ionCorr.clicked.connect(self.onBottonClick_ionCorr)
        self.ui.pushButton_plot_ionZero.clicked.connect(self.onBottonClick_ionZero)
        self.ui.pushButton_plot_resStaAdd.clicked.connect(self.onBottonClick_resStaAdd)
        self.ui.pushButton_plot_resStaSub.clicked.connect(self.onBottonClick_resStaSub)
        self.ui.pushButton_plot_resAddBlClock.clicked.connect(self.onBottonClick_addBlClock4Est)
        self.ui.pushButton_plot_resOmitBL.clicked.connect(self.onBottonClick_omitBL)
        self.ui.pushButton_plot_resOmitSta.clicked.connect(self.onBottonClick_omitSta)
        self.ui.pushButton_plot_reweight.clicked.connect(self.onBottonClick_reWeight)
        self.ui.pushButton_plot_autoOut.clicked.connect(self.onBottonClick_autoOutlier)
        self.ui.pushButton_plot_modeUT1.clicked.connect(self.onBottonClick_SetUT1Mode)
        self.ui.pushButton_plot_modeEOP.clicked.connect(self.onBottonClick_SetEOPMode)
        self.ui.pushButton_plot_moderegular.clicked.connect(self.onBottonClick_SetRegularMode)
        self.ui.pushButton_plot_modeClear.clicked.connect(self.onBottonClick_SetClearMode)
        self.ui.pushButton_plot_sta_sub.clicked.connect(self.onBottonClick_staInfoSub)
        self.ui.pushButton_plot_sta_add.clicked.connect(self.onBottonClick_staInfoAdd)
        
        outlierShortCut = QShortcut(QKeySequence('Ctrl+space'),self)
        outlierShortCut.activated.connect(self.onBottonClick_process)
        
        ############### radioButton action ############
        self.ui.radioButton_plot_all.clicked.connect(self.signal_plotResAll)
        self.ui.radioButton_plot_station.clicked.connect(self.signal_plotResSta)
        self.ui.radioButton_plot_baseline.clicked.connect(self.signal_plotResBl)
        self.ui.radioButton_plot_source.toggled.connect(self.signal_plotResSou)
        self.ui.radioButton_est_eop_cpwl.clicked.connect(self.onRadioClick_enableShow)
        self.ui.radioButton_est_eop_poly.clicked.connect(self.onRadioClick_enableShow)
        self.ui.radioButton_glob_trf.clicked.connect(self.signal_plotGlob)
        self.ui.radioButton_glob_crf.clicked.connect(self.signal_plotGlob)

        self.ui.comboBox_plot_y.currentIndexChanged.connect(self.signal_plotChange)
        self.ui.comboBox_plot_station.currentIndexChanged.connect(self.signal_plotResSta)
        self.ui.comboBox_plot_baseline.currentIndexChanged.connect(self.signal_plotChange)
        #self.ui.comboBox_plot_source.currentIndexChanged.connect(self.signal_plotChange)
        self.ui.comboBox_plot_sta_y.currentIndexChanged.connect(self.signal_plotStationInfo)
        self.ui.comboBox_plot_result_y.currentIndexChanged.connect(self.signal_plotResult)

        self.ui.checkBox_est_clk.stateChanged.connect(self.checkBox_setClock)
        self.ui.checkBox_est_blclk.stateChanged.connect(self.checkBox_setBlClock)
        self.ui.checkBox_est_grad.stateChanged.connect(self.checkBox_setGrad)
        self.ui.checkBox_est_nutxy.stateChanged.connect(self.checkBox_setNuation)
        self.ui.checkBox_est_pmxy.stateChanged.connect(self.checkBox_setPmxy)
        self.ui.checkBox_est_nnr.stateChanged.connect(self.checkBox_setStaNNRT)
        self.ui.checkBox_est_sounnr.stateChanged.connect(self.checkBox_setSouNNR)
        self.ui.checkBox_est_source.stateChanged.connect(self.checkBox_setSouEnable)
        self.ui.checkBox_est_station.stateChanged.connect(self.checkBox_setStaEnable)
        self.ui.checkBox_est_ut1.stateChanged.connect(self.checkBox_setUT1)
        self.ui.checkBox_est_wet.stateChanged.connect(self.checkBox_setWet)
        self.ui.checkBox_plot_glob_x.stateChanged.connect(self.signal_plotGlobStation)
        self.ui.checkBox_plot_glob_y.stateChanged.connect(self.signal_plotGlobStation)
        self.ui.checkBox_plot_glob_z.stateChanged.connect(self.signal_plotGlobStation)
        
        # self.ui.checkBox_glob_station_yes.clicked.connect(self.checkBox_setGlobStationY)
        # self.ui.checkBox_glob_station_no.clicked.connect(self.checkBox_setGlobStationN)
        # self.ui.checkBox_glob_source_yes.clicked.connect(self.checkBox_setGlobSourceY)
        # self.ui.checkBox_glob_source_no.clicked.connect(self.checkBox_setGlobSourceN)
        
        self.ui.listWidget_plot_station.itemSelectionChanged.connect(self.signal_plotStationInfo)
        self.ui.listWidget_plot_resSta.itemSelectionChanged.connect(self.signal_plotChange)
        self.ui.listWidget_plot_resSou.itemSelectionChanged.connect(self.signal_plotChange)
        self.ui.listWidget_plot_result.itemSelectionChanged.connect(self.signal_plotResult)
        self.ui.listWidget_plot_glob_trf.itemSelectionChanged.connect(self.signal_plotGlobStation)
        self.ui.listWidget_plot_glob_crf.itemSelectionChanged.connect(self.signal_plotGlobSource)
        
        ############### textChange action ############
        self.ui.lineEdit_clk_constr.editingFinished.connect(self.checkBox_setClock)
        self.ui.lineEdit_clk_interval.editingFinished.connect(self.checkBox_setClock)
        self.ui.lineEdit_wet_interval.editingFinished.connect(self.checkBox_setWet)
        self.ui.lineEdit_wet_constr.editingFinished.connect(self.checkBox_setWet)
        self.ui.lineEdit_grad_interval.editingFinished.connect(self.checkBox_setGrad)
        self.ui.lineEdit_grad_absconstr.editingFinished.connect(self.checkBox_setGrad)
        self.ui.lineEdit_grad_relconstr.editingFinished.connect(self.checkBox_setGrad)
        
        self.ui.table_data_station.cellDoubleClicked.connect(self.on_table_data_station_doubleClicked)
    
    ######## Start #######
    def init_gui(self):
        
        self.ui.stackedWidget.setCurrentIndex(0)
        
        self.ui.label_iers.setOpenExternalLinks(True)
        self.ui.label_ivs.setOpenExternalLinks(True)
        self.ui.label_itrf.setOpenExternalLinks(True)
        
        currentTime = datetime.datetime.now()
        self.ui.lineEdit_file_startyear.setText('%4d'%currentTime.year)
        self.ui.lineEdit_file_stopyear.setText('%4d'%currentTime.year)
        self.oldPattern = ''
        
        self.ui.table_data_station.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table_data_station.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.ui.table_data_bl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table_data_bl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.ui.table_data_source.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table_data_source.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        
        self.ui.tableWidget_glob_station.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_glob_station.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.ui.tableWidget_glob_source.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_glob_source.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)

        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        # font = QFont("monospace")
        #font = QFont('Times New Roman')
        #self.ui.comboBox_plot_station.setFont(font)
        #self.ui.comboBox_plot_baseline.setFont(font)
        
        
    def init_param(self):
        
        self.Param = PARAMETER()
        self.Param.Setup.vgosdbPath = self.dirpath[0]
        self.Param.Map.stationFile = self.dirpath[2]+'station.txt'
        self.Param.Out.snxPath = ['NO',self.dirpath[9]]

        #self.checkBox_setDataStaRemove()

        self.handOutlierFlag = 0
        self.rmOutlier = []
        self.runFlag = 0
        self.globFlag = 0
        self.bandNum = 2
        self.globModifyFile = ''

    def updatePreference(self):
        self.ui.lineEdit_path_vgosDb.setText(self.dirpath[0])
        self.ui.lineEdit_path_master.setText(self.dirpath[1])
        self.ui.lineEdit_path_Apriori.setText(self.dirpath[2])
        self.ui.lineEdit_param_Station.setText(self.dirpath[3])
        self.ui.lineEdit_param_Source.setText(self.dirpath[4])
        self.ui.lineEdit_param_EOP.setText(self.dirpath[5])
        self.ui.lineEdit_param_EPHEM.setText(self.dirpath[6])
        self.ui.lineEdit_path_Residual.setText(self.dirpath[7])
        self.ui.lineEdit_path_Report.setText(self.dirpath[8])
        self.ui.lineEdit_path_SNX.setText(self.dirpath[9])
        self.ui.lineEdit_path_EOPO.setText(self.dirpath[10])
        self.ui.lineEdit_path_arcpath.setText(self.dirpath[11])
        self.ui.lineEdit_param_ac.setText(self.dirpath[12])
        self.ui.comboBox_dataType.setCurrentIndex(int(self.dirpath[13]))
            
    def initEstParam(self):
        self.ui.checkBox_est_pmxy.setChecked(False)
        self.ui.checkBox_est_rpmxy.setChecked(False)
        self.ui.checkBox_est_ut1.setChecked(False)
        self.ui.checkBox_est_lod.setChecked(False)
        self.ui.checkBox_est_nutxy.setChecked(False)
        self.ui.checkBox_est_clk.setChecked(False)
        self.ui.checkBox_est_blclk.setChecked(False)
        self.ui.checkBox_est_wet.setChecked(False)
        self.ui.checkBox_est_grad.setChecked(False)
        self.ui.checkBox_est_station.setChecked(False)
        self.ui.checkBox_est_source.setChecked(False)
        self.Param.Flags.sou = ['NO']
        self.Param.Flags.xyz = ['NO']
        self.ui.pushButton_plot_modeUT1.setChecked(False)
        self.ui.pushButton_plot_modeEOP.setChecked(False)
        self.ui.table_data_station.setRowCount(0)
        self.ui.table_data_bl.setRowCount(0)
        self.plot_res.axes.cla()
        # self.plot_res.figInit()

    @Slot(int,int)
    def on_table_data_station_cellClicked(self, row, column):
        #self.ui.table_data_station.setSelectionBehavior(QAbstractItemView.SelectRows)
        if column == 5:
            for i in range(self.ui.table_data_station.rowCount()):
                if self.ui.table_data_station.item(i,column) == None:
                    continue
                elif self.ui.table_data_station.item(i,column).text() == 'R':
                    item = QTableWidgetItem('')
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.table_data_station.setItem(i, column, item)
            
            temp = self.ui.table_data_station.currentIndex().data()
            if temp == 'R':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('R')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_station.setItem(row, column, item)
            self.scanInfo.refclk = self.ui.table_data_station.item(row,1).text()

        if column == 6:
            temp = self.ui.table_data_station.currentIndex().data()
            if temp == 'X':
                item = QTableWidgetItem('')
            else:
                if self.ui.table_data_station.item(row, column-1).text() == 'R':
                    QMessageBox.warning(self,'Error','%s is clock reference, Please modify!'\
                    %self.ui.table_data_station.item(row, 1).text(),QMessageBox.Ok)
                    return
                item = QTableWidgetItem('X')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_station.setItem(row, column, item)
                
        if column == 7:
            temp = self.ui.table_data_station.currentIndex().data()
            if temp == 'Y':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('Y')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_station.setItem(row, column, item)
            
        if column == 8:
            temp = self.ui.table_data_station.currentIndex().data()
            if temp == 'Y':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('Y')
            item.setTextAlignment(Qt.AlignCenter) 
            self.ui.table_data_station.setItem(row, column, item)
            
    def on_table_data_station_doubleClicked(self, row, column):
        if column == 4:
            staName = self.ui.table_data_station.item(row, 1).text()
            if self.ui.table_data_station.item(row, 4).text() != '':
                index = self.scanInfo.stationAll.index(staName)
                brkMJD = self.scanInfo.clkBrk.brkMJD[index]
                
                strTime = ''
                for mjd in brkMJD:
                    temp = mjd2ymdhms(mjd)
                    strTime += '%4d-%02d-%02d %02d:%02d:%05.2f\n\n'%(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5])
                
                QMessageBox.information(self,'%s Clock break Information'%staName,'There %s clock break:\n\n%s'%(len(brkMJD),strTime),QMessageBox.Ok)
                
    @Slot(int,int)
    def on_table_data_bl_cellClicked(self, row, column):
        if column == 5:
            temp = self.ui.table_data_bl.currentIndex().data()
            if temp == 'Y':
                item = QTableWidgetItem('')
                index = self.scanInfo.blClkList.index(self.scanInfo.blUsed[row])
                self.scanInfo.blClkList.pop(index)
            else:
                if self.ui.table_data_bl.item(row, column+1) != None:
                    if self.ui.table_data_bl.item(row, column+1).text() == 'X':
                        QMessageBox.warning(self,'Error','The baseline is omit, its clock can not be estimated!',QMessageBox.Ok)
                        return
                item = QTableWidgetItem('Y')
                self.scanInfo.blClkList.append(self.scanInfo.blUsed[row])
                
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_bl.setItem(row, column, item)
                
        if column == 6:
            temp = self.ui.table_data_bl.currentIndex().data()
            if temp == 'X':
                item = QTableWidgetItem('')
            else:
                if self.ui.table_data_bl.item(row, column-1) != None:
                    if self.ui.table_data_bl.item(row, column-1).text() == 'Y':
                        QMessageBox.warning(self,'Error','The baseline clock is estimated, can not be omit!',QMessageBox.Ok)
                        return
                item = QTableWidgetItem('X')
                
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_bl.setItem(row, column, item)
            
    @Slot(int,int)
    def on_table_data_source_cellClicked(self, row, column):
        if column == 5:
            temp = self.ui.table_data_source.currentIndex().data()
            if temp == 'X':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('X')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_source.setItem(row, column, item)
            
        elif column == 6:
            temp = self.ui.table_data_source.currentIndex().data()
            if temp == 'Y':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('Y')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_source.setItem(row, column, item)
            
        elif column == 7:
            temp = self.ui.table_data_source.currentIndex().data()
            if temp == 'Y':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('Y')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_source.setItem(row, column, item)
            
    @Slot(int,int)
    def on_tableWidget_glob_station_cellDoubleClicked(self, row, column):
        if column == 3:
            temp = self.ui.tableWidget_glob_station.currentIndex().data()
            if temp == 'X':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('X')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_glob_station.setItem(row, column, item)
            
        elif column == 4:
            temp = self.ui.tableWidget_glob_station.currentIndex().data()
            if temp == 'Y':
                item = QTableWidgetItem('')
            else:
                item = QTableWidgetItem('Y')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_glob_station.setItem(row, column, item)

    @Slot(int,int)
    def on_tableWidget_session_cellDoubleClicked(self, row, column):
        session = self.ui.tableWidget_session.item(row, 1).text()
        version = int(self.ui.tableWidget_session.item(row, 4).text())
        ac = self.ui.tableWidget_session.item(row, 5).text()
        reply = QMessageBox.question(self,'Load data','Loading %s?'%session, \
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == 16384:
            # if len(session) == 9:
            #     year = str(2000 + int(session[:2]))
            # else:
            #     year = session[:4]
                
            # if ac == 'NONE':
            #     sessionName = '%s_V%03d_kall.wrp'%(session,version)
            #     dataFile = os.path.join(self.dirpath[1],year,session,sessionName)
            # else:
            #     sessionName = '%s_V%03d_i%s_kall.wrp'%(session,version,ac)
            #     dataFile = os.path.join(self.dirpath[1],year,session,sessionName)
            #     if not os.path.exists(dataFile):
            #         sessionName = '%s_V%03d_kall_i%s.wrp'%(session,version,ac)
            #         dataFile = os.path.join(self.dirpath[1],year,session,sessionName)
            # print(dataFile)
            self.signal_showLoadData('table',[session,version,ac])

    #-------------------------------------------------------------------------#
    #----------------------------- checkBox action ---------------------------#
    def checkBox_setClock(self):
        if self.ui.checkBox_est_clk.isChecked():
            order = int(self.ui.comboBox_clk_order.currentText())
            self.Param.Flags.clk = [int(self.ui.lineEdit_clk_interval.text()), order]
            self.Param.Const.clk = float(self.ui.lineEdit_clk_constr.text())
        else:
            self.Param.Flags.clk = 'NO'

    def checkBox_setBlClock(self):
        if self.ui.checkBox_est_blclk.isChecked():
            self.Param.Flags.blClk = 'IN'
        else:
            self.Param.Flags.blClk = 'NO'

    def checkBox_setGrad(self):
        if self.ui.checkBox_est_grad.isChecked():
            interval = self.ui.lineEdit_grad_interval.text()
            self.Param.Flags.gradient = ['YES',interval]
            relConstr = float(self.ui.lineEdit_grad_relconstr.text())
            absConstr = float(self.ui.lineEdit_grad_absconstr.text())
            self.Param.Const.grad = [relConstr, absConstr]
        else:
            self.Param.Flags.gradient = ['NO']
            
    def checkBox_setNuation(self):
        if self.ui.checkBox_est_nutxy.isChecked():
            self.Param.Flags.nut = ['YES']
        else:
            self.Param.Flags.nut = ['NO']
            
    def checkBox_setPmxy(self):
        if self.ui.checkBox_est_pmxy.isChecked():
            self.Param.Flags.pm = ['YES']
        else:
            self.Param.Flags.pm = ['NO']
            
    def checkBox_setUT1(self):
        if self.ui.checkBox_est_ut1.isChecked():
            self.Param.Flags.ut1 = ['YES']
        else:
            self.Param.Flags.ut1 = ['NO']
            
    def checkBox_setStaEnable(self):
        if self.ui.checkBox_est_station.isChecked():
            self.ui.pushButton_autoset_station.setEnabled(True)
        else:
            self.ui.pushButton_autoset_station.setEnabled(False)

    def checkBox_setStaNNRT(self):
        if self.runFlag:
            rownum = self.ui.table_data_station.rowCount()
            for i in range(rownum):
                if self.ui.checkBox_est_nnr.isChecked():
                    item = QTableWidgetItem('Y')
                else:
                    item = QTableWidgetItem('')

                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_data_station.setItem(i, 8, item)
        
    def checkBox_setSouEnable(self):
        if self.ui.checkBox_est_source.isChecked():
            self.ui.pushButton_autoset_source.setEnabled(True)
            self.Param.Flags.sou[0] = 'YES'
        else:
            self.ui.pushButton_autoset_source.setEnabled(False)
            self.Param.Flags.sou = ['NO']

    def checkBox_setSouNNR(self):
        if self.ui.checkBox_est_sounnr.isChecked():
            if self.runFlag:
                sounnr = []
                for irow in self.souICRF3Flag:
                    sounnr.append(self.ui.table_data_source.item(irow,1).text())
                self.Param.Const.nnr_sou = ['NO','EXCEPT'] + sounnr
        else:
            self.Param.Const.nnr_sou = ['NO']
                        
    def checkBox_setWet(self):
        if self.ui.checkBox_est_wet.isChecked():
            self.Param.Flags.zwd = int(self.ui.lineEdit_wet_interval.text())
            self.Param.Const.atm = float(self.ui.lineEdit_wet_constr.text())
        else:
            self.Param.Flags.zwd = 'NO'


    def getParam(self):
        self.Param.Map.stationFile = self.ui.lineEdit_path_Apriori.text()+self.ui.lineEdit_param_Station.text()
        self.Param.Map.sourceFile = self.ui.lineEdit_path_Apriori.text()+self.ui.lineEdit_param_Source.text()
        self.Param.Map.eopFile = self.ui.lineEdit_path_Apriori.text()+self.ui.lineEdit_param_EOP.text()
        self.Param.Map.ephemFile = self.ui.lineEdit_path_Apriori.text()+self.ui.lineEdit_param_EPHEM.text()
        
        ######################## parameter to estimate #########################
        self.Param.Setup.qcodeLim = self.ui.spinBox_param_quality.value()
        if self.ui.radioButton_param_outlier.isChecked():
            self.Param.Data.outlier = ['YES',float(self.ui.lineEdit_param_outlier.text())]
        else:
            self.Param.Data.outlier = ['NO']
            
        #---------------------------- EOP Estimate ---------------------------#
        if self.ui.checkBox_est_rpmxy.isChecked():
            self.Param.Flags.pmr = ['YES']
        else:
            self.Param.Flags.pmr = ['NO']
            
        if self.ui.checkBox_est_lod.isChecked():
            self.Param.Flags.lod = ['YES']
        else:
            self.Param.Flags.lod = ['NO']
        
        if self.ui.radioButton_est_eop_cpwl.isChecked():
            self.Param.Flags.type = 'SEGMENT'
            self.Param.Flags.pm.append(self.ui.lineEdit_pmxy_interval.text())
            self.Param.Flags.ut1.append(self.ui.lineEdit_ut1_interval.text())
            self.Param.Flags.pmr = ['NO']
            self.Param.Flags.lod = ['NO']
            self.Param.Flags.segConstr = [float(self.ui.lineEdit_pmxy_constr.text()),float(self.ui.lineEdit_ut1_constr.text())]
        else:
            self.Param.Flags.type = 'POLY'
            self.Param.Const.erp = [float(self.ui.lineEdit_pmxy_constr_poly.text()),\
                                    float(self.ui.lineEdit_ut1_constr_poly.text()),\
                                    float(self.ui.lineEdit_rpmxy_constr_poly.text()),\
                                    float(self.ui.lineEdit_lod_constr_poly.text())]
            if self.ui.radioButton_est_reftime_MIDDEL.isChecked():
                self.Param.Flags.eopTime = 'MIDDEL'
            elif self.ui.radioButton_est_reftime_MIDNIGHT.isChecked():
                self.Param.Flags.eopTime = 'MIDNIGHT'
            else:
                self.Param.Flags.eopTime = 'NOON'
                
        if self.ui.checkBox_setup_hfeop.isChecked():
            self.Param.Map.heopm = 'Desai'
        
        if self.bandNum == 1:
            self.bandIndex = 0
        elif self.bandNum == 2:
            if self.ui.pushButton_plot_S.isChecked():
                self.bandIndex = 0
            elif self.ui.pushButton_plot_X.isChecked():
                self.bandIndex = 1
                
        ######################## source to be estimated ######################
        noEstSou = []
        self.nnrSou = []
        if self.runFlag == 1:
            if self.ui.checkBox_est_source.isChecked():
                for i in range(self.ui.table_data_source.rowCount()):
                    if self.ui.table_data_source.item(i,6) != None:
                        if self.ui.table_data_source.item(i,6).text() != 'Y':
                            noEstSou.append(self.ui.table_data_source.item(i,1).text())
                    else:
                        noEstSou.append(self.ui.table_data_source.item(i,1).text())
                    
                    if self.ui.table_data_source.item(i,7) != None:
                        if self.ui.table_data_source.item(i,7).text() == 'Y':
                            self.nnrSou.append(self.ui.table_data_source.item(i,1).text())
                            
                for i in range(len(self.scanInfo.sourceAll)):
                    sp = np.where(self.scanInfo.Obs2Source==(i+1))
                    if len(sp[0]) == 0:
                        if self.scanInfo.sourceAll[i] not in noEstSou:
                            noEstSou.append(self.scanInfo.sourceAll[i])
                            
                
                            
                if self.ui.checkBox_est_sounnr.isChecked():
                    self.Param.Const.nnr_sou = ['NO','EXCEPT'] + self.nnrSou
                else:
                    self.Param.Const.nnr_sou = ['NO']
                    
        
        ######################## station to be estimated ######################
        noEstSta = []
        self.nnrtSta = []
        if self.runFlag == 1:
            if self.ui.checkBox_est_station.isChecked():
                for i in range(self.ui.table_data_station.rowCount()):
                    temp = self.scanInfo.staUsed[i] - 1
                    if self.ui.table_data_station.item(i,7) != None:
                        if self.ui.table_data_station.item(i,7).text() != 'Y':
                            noEstSta.append(self.scanInfo.stationAll[temp])
                    else:
                        noEstSta.append(self.scanInfo.stationAll[temp])
                            
                    if self.ui.table_data_station.item(i,8) != None:
                        if self.ui.table_data_station.item(i,8).text() == 'Y':
                            self.nnrtSta.append(self.scanInfo.stationAll[temp].strip())
                            
                if len(noEstSta) < len(self.scanInfo.staUsed):
                    self.Param.Flags.xyz = ['YES','EXCEPT'] + noEstSta
                else:
                    self.Param.Flags.xyz = ['NO']
                    
                if self.ui.checkBox_est_nnr.isChecked():
                    self.Param.Const.nnr_nnt_sta[0] = ['NO','EXCEPT'] + self.nnrtSta
                    self.Param.Const.sigma_nnr_nnt_sta[0] = float(self.ui.lineEdit_sigma_stannr.text())
                else:
                    self.Param.Const.nnr_nnt_sta[0] = ['NO']
                    
                if self.ui.checkBox_est_nnt.isChecked():
                    self.Param.Const.nnr_nnt_sta[1] = ['NO','EXCEPT'] + self.nnrtSta
                    self.Param.Const.sigma_nnr_nnt_sta[1] = float(self.ui.lineEdit_sigma_stannt.text())
                else:
                    self.Param.Const.nnr_nnt_sta[1] = ['NO']
            else:
                self.Param.Flags.xyz = ['NO']
                
            if self.ui.checkBox_est_station.isChecked():
                self.Param.Const.sta = ['YES', float(self.ui.lineEdit_sigma_sta.text())]
            else:
                self.Param.Const.sta = ['NO', float(self.ui.lineEdit_sigma_sta.text())]
            
        ######################## station to be exclude ########################
        useObs = np.where(self.scanInfo.Obs2Scan != 0)
        offset = np.abs(self.scanInfo.Obs2Baseline[useObs[0],1] - self.scanInfo.Obs2Baseline[useObs[0],0])
        
        excludeSta = []
        
        for i in range(self.ui.table_data_station.rowCount()):
            if self.ui.table_data_station.item(i,6).text() == 'X':
                rmSta = self.ui.table_data_station.item(i,1).text()
                if not rmSta in self.scanInfo.rmSta:
                    self.scanInfo.rmSta.append(rmSta)
                    
                    indexSta = self.scanInfo.stationAll.index(rmSta) + 1
                    excludeSta.append(indexSta)
                                        
                    self.scanInfo.delayFlag += pickRmObs(self.scanInfo.Obs2Scan, self.scanInfo.Obs2Baseline, indexSta, 0)
        
        rmObs = []
        for i in excludeSta:
            addR = np.abs(np.sum(self.scanInfo.Obs2Baseline[useObs[0]] - i, axis=1))
            rmP = np.where((addR == offset) == True)
            rmObs.extend(rmP[0].tolist())
            
        ######################## baseline to be exclude #######################
        rmObsBl = []
        if self.runFlag == 1:
            for i in range(self.ui.table_data_bl.rowCount()):
                if self.ui.table_data_bl.item(i,6) != None:
                    if self.ui.table_data_bl.item(i,6).text() == 'X':
                        rmObsBl.extend(self.scanInfo.blResPosit[i].tolist())
                        
                        self.scanInfo.delayFlag += pickRmObs(self.scanInfo.Obs2Scan, self.scanInfo.Obs2Baseline, self.scanInfo.blResPosit[i], 1)
                        
        for ip in rmObsBl:
            if not ip in rmObs:
                rmObs.append(ip)
            
        if len(rmObs):
            self.handOutlierFlag = 1
            self.rmOutlier = rmObs

    #-------------------------------------------------------------------------#
    #------------------------------ Menu Action ------------------------------#
    def menuAction_showFileWelcome(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def menuAction_showFilePreference(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        
    def menuAction_showDBList(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        
    def menuAction_showParamBasic(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        
    def menuAction_showDataStation(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        
    def menuAction_showDataBaseline(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        
    def menuAction_showDataSource(self):
       self.ui.stackedWidget.setCurrentIndex(6)
        
    def menuAction_showEstClkTrop(self):
        self.ui.stackedWidget.setCurrentIndex(7)
        
    def menuAction_showEstEOP(self):
        self.ui.stackedWidget.setCurrentIndex(8)
        
    def menuAction_showGlobSetup(self):
        self.ui.stackedWidget.setCurrentIndex(9)
        
    def menuAction_showGlobStation(self):
        self.ui.stackedWidget.setCurrentIndex(10)
        
    def menuAction_showGlobSource(self):
        self.ui.stackedWidget.setCurrentIndex(11)
        
    def menuAction_showPlotRes(self):
        self.ui.stackedWidget.setCurrentIndex(12)
        
    def menuAction_showPlotStation(self):
        self.ui.stackedWidget.setCurrentIndex(13)
        
    def menuAction_showPlotResult(self):
        self.ui.stackedWidget.setCurrentIndex(14)
    
    def menuAction_showPlotGlob(self):
        self.ui.stackedWidget.setCurrentIndex(15)
        
        
    #-------------------------------------------------------------------------#
    #---------------------------- pushBotton action --------------------------#
    def onBottonClick_addBlClock4Est(self):
        if self.runFlag == 1:
            blPosit = self.ui.comboBox_plot_baseline.currentIndex()
            bl = self.scanInfo.blUsed[blPosit]
            
            if bl not in self.scanInfo.blClkList:
                self.scanInfo.blClkList.append(bl)
                
                item = QTableWidgetItem('Y')
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_data_bl.setItem(blPosit, 5, item)
        
    
    def onBottonClick_ambAddandSub(self, flag):
        
        if len(self.plot_res.rmMark[0]) != 0:
            ambigCorr = np.zeros(len(self.scanInfo.oc_obs[self.bandIndex]))
            ambigNum = np.zeros(len(self.scanInfo.oc_obs[self.bandIndex]))
            obsPosit = np.where(self.scanInfo.Obs2Scan != 0)
            ambigSize = self.scanInfo.baseInfo[2][self.bandIndex][obsPosit]
            
            for i in range(len(self.plot_res.rmMark[0])):
                for j in self.plot_res.rmMark[2][i]:
                    ambigCorr[j] += flag*ambigSize[j]
                    ambigNum[j] += flag
                    
            self.result.VReal[self.bandIndex] += ambigCorr*const.c
            self.scanInfo.ambigNum[self.bandIndex][obsPosit] += ambigNum
            self.scanInfo.oc_obs[self.bandIndex] += ambigCorr
            
            self.plot_res.rmMark = [[],[],[]]
            self.signal_plotChange()
            
    def onBottonClick_ambCorr(self):
        if self.runFlag == 1:
            print('\n\n-------------------------------------------------------\n    Remove the ambiguity...')
            self.ui.statusBar.showMessage('Ambiguity correcting...')
            
            self.ambCorr.setParam(self.scanInfo, self.result.VReal[self.bandIndex], self.bandIndex)
            self.ambCorr.start()
            
    def onBottonClick_ambZero(self):
        if self.runFlag == 1:
            if np.sum(np.abs(self.scanInfo.ambigNum[self.bandIndex])) != 0:
                obsPosit = np.where(self.scanInfo.Obs2Scan!=0)
                self.scanInfo.oc_obs[self.bandIndex] -= self.scanInfo.ambigNum[self.bandIndex][obsPosit] * self.scanInfo.baseInfo[2][self.bandIndex][obsPosit]
                
                self.scanInfo.ambigNum[self.bandIndex] = np.zeros(len(self.scanInfo.Obs2Scan))
                self.onBottonClick_process()
        
            
    def onBottonClick_autoOutlier(self):
        flag = 1
        try:
            self.result.wrms
        except AttributeError:
            flag = 0
        
        if flag == 1:
            self.Param.Data.outlier = ['YES',float(self.ui.lineEdit_param_outlier.text())]
            outFlag,outPosit = getOutFlag(self.staObs, self.scanInfo, self.stationInfo, self.Param, self.result, [], 0, self.bandIndex)
            if len(outPosit):
                self.scanInfo.delayFlag[outPosit] += 1
                self.onBottonClick_process()
            
    def onBottonClick_bandChoice(self,iband):
        
        if self.bandNum == 2:
            if iband == 0:
                self.ui.pushButton_plot_X.setChecked(False)
                self.ui.pushButton_plot_S.setChecked(True)
            elif iband == 1:
                self.ui.pushButton_plot_X.setChecked(True)
                self.ui.pushButton_plot_S.setChecked(False)
                    
            try:
                len(self.result.VReal[iband])
            except AttributeError:
                self.plot_res.figInit()
            else:
                if len(self.result.VReal[iband]) == 0:
                    self.plot_res.figInit()
                
            self.bandIndex = iband
        elif self.bandNum == 1:
            self.ui.pushButton_plot_X.setChecked(True)
            self.bandIndex = 0
        
        if self.runFlag == 1:
            if self.result.flag[self.bandIndex] == 1 or self.ui.comboBox_plot_y.currentIndex() == 1:
                self.signal_plotChange()
                
    def onBottonClick_browseFile(self, flag):
        dataFile, fileType = QFileDialog.getOpenFileName(self,'Apriori File Select',self.dirpath[2],'All Files(*)')
        
        if len(dataFile):
            temp = dataFile.rfind('/')
            fileName = dataFile[temp+1:]
            if flag == 3:
                self.ui.lineEdit_param_Station.setText(fileName)
            elif flag == 4:
                self.ui.lineEdit_param_Source.setText(fileName)
            elif flag == 5:
                self.ui.lineEdit_param_EOP.setText(fileName)
            elif flag == 6:
                self.ui.lineEdit_param_EPHEM.setText(fileName)
                
    def onBottonClick_browsePath(self, flag):
        if len(self.dirpath[flag]):
            path = self.dirpath[flag]
        else:
            path = '/'
        
        selectPath = QFileDialog.getExistingDirectory(self,'Path Select',path)
        
        if len(selectPath):
            if flag == 0:
                self.ui.lineEdit_path_vgosDb.setText(selectPath+'/')
            elif flag == 1:
                self.ui.lineEdit_path_master.setText(selectPath+'/')
            elif flag == 2:
                self.ui.lineEdit_path_Apriori.setText(selectPath+'/')
            elif flag == 7:
                self.ui.lineEdit_path_Residual.setText(selectPath+'/')
            elif flag == 8:
                self.ui.lineEdit_path_Report.setText(selectPath+'/')
            elif flag == 9:
                self.ui.lineEdit_path_SNX.setText(selectPath+'/')
            elif flag == 10:
                self.ui.lineEdit_path_EOPO.setText(selectPath+'/')
            elif flag == 11:
                self.ui.lineEdit_path_arcpath.setText(selectPath+'/')

    def onBottonClick_clearBlClk(self):
        if self.runFlag == 1:
            self.scanInfo.blClkList = []
            rowNum = self.ui.table_data_bl.rowCount()
            for i in range(rowNum - 1):
                item = QTableWidgetItem('')
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_data_bl.setItem(i, 5, item)

    def onBottonClick_clkbkMode(self):
        if self.ui.radioButton_plot_station.isChecked():
            self.ui.pushButton_plot_outlier.setChecked(False)
            icon1 = QIcon()
            icon1.addFile(u":/icons/icons/magnifier.png", QSize(), QIcon.Normal, QIcon.Off)
            self.ui.pushButton_plot_outlier.setIcon(icon1)
            self.plot_res.outlierFlag = 0
            self.plot_res.clkbkFlag = 1
            
            if self.ui.pushButton_plot_clkbk.isChecked():
                self.ui.statusBar.showMessage('Clock break mode selecting...')
            else:
                self.ui.statusBar.showMessage('')
                self.plot_res.clkbkFlag = 0
            
        else:
            QMessageBox.warning(self,'Waring','The station to plot should be select!',QMessageBox.Ok)
            self.ui.pushButton_plot_clkbk.setChecked(False)
            self.plot_res.clkbkFlag = 0

    def onBottonClick_dataTypeAdd(self):
        if self.LocalThread.isRunning():
            QMessageBox.information(self,'Information','The thread of Local is running! Please wait!',QMessageBox.Ok)
        else:
            self.ui.listWidget_datatype.blockSignals(True)
            self.ui.listWidget_datatype.selectAll()
            self.signal_localFileShow()
            self.ui.listWidget_datatype.blockSignals(False)

    def onBottonClick_dataTypeSub(self):
        if self.LocalThread.isRunning():
            QMessageBox.information(self,'Information','The thread of Local is running! Please wait!',QMessageBox.Ok)
        else:
            self.ui.listWidget_datatype.blockSignals(True)
            for row in range(self.ui.listWidget_datatype.count()):
                self.ui.listWidget_datatype.item(row).setSelected(False)
            self.signal_localFileShow()
            self.ui.listWidget_datatype.blockSignals(False)
            
    def onBottonClick_globrun(self):
        
        #print(self.globFlag)
        #if self.globFlag == 0:
        arcFile = self.ui.lineEdit_glob_arc.text()
        arcPath = self.ui.lineEdit_path_arcpath.text()
        self.Param.Map.stationFile = self.ui.lineEdit_path_Apriori.text()+self.ui.lineEdit_param_Station.text()
        self.Param.Map.sourceFile = self.ui.lineEdit_path_Apriori.text()+self.ui.lineEdit_param_Source.text()

        fid = open(arcPath+arcFile,'r')
        lines = fid.readlines()
        fid.close()

        for line in lines:
            if line[0] == '$':
                temp = list(filter(None,line.split(" ")))
                self.Param.Arcs.session.append(temp[0][1:])
            #self.Param.Arcs.session.append(line[1:26])
        
        # glob include set
        if self.ui.checkBox_glob_station_velocity_yes.isChecked():
            self.Param.Flags.vel = ['YES']
            
        if self.ui.checkBox_glob_station_yes.isChecked():
            self.Param.Global.station[0] = 'YES'
        else:
            self.Param.Global.station[0] = 'NO'
            self.Param.Flags.vel[0] = 'NO'
        
        if self.ui.checkBox_glob_source_yes.isChecked():
            self.Param.Global.source[0] = 'YES'
        
            
        # NNR/NNT set
        if self.ui.checkBox_glob_trf_nnrnnt.isChecked():
            self.Param.Const.nnr_nnt_sta[0][0] = 'YES'
            self.Param.Const.nnr_nnt_sta[1][0] = 'YES'
        else:
            self.Param.Const.nnr_nnt_sta[0][0] = 'NO'
            self.Param.Const.nnr_nnt_sta[1][0] = 'NO'
            
        if self.ui.checkBox_glob_crf_nnr.isChecked():
            self.Param.Const.nnr_sou[0] = 'YES'
        else:
            self.Param.Const.nnr_sou[0] = 'NO'
        
        trfConstFile = os.path.join(self.ui.lineEdit_path_Apriori.text(),self.ui.lineEdit_glob_trf_nnrnnt.text())
        crfConstFile = os.path.join(self.ui.lineEdit_path_Apriori.text(),self.ui.lineEdit_glob_crf_nnr.text())
        stationRemoveFile = os.path.join(self.ui.lineEdit_path_Apriori.text(),
                                         self.ui.lineEdit_glob_station_exclude.text())
        sourceRemoveFile = os.path.join(self.ui.lineEdit_path_Apriori.text(),
                                        self.ui.lineEdit_glob_source_exclude.text())
        velTieFile = os.path.join(self.ui.lineEdit_path_Apriori.text(),
                                        self.ui.lineEdit_glob_veltie.text())

        fid = open(trfConstFile,'r')
        trfLines = fid.readlines()
        fid.close()
        fid = open(crfConstFile,'r')
        crfLines = fid.readlines()
        fid.close()

        fid = open(stationRemoveFile, 'r')
        rmStaLines = fid.readlines()
        fid.close()
        fid = open(sourceRemoveFile, 'r')
        rmSouLines = fid.readlines()
        fid.close()
        fid = open(velTieFile, 'r')
        vlTieLine = fid.readlines()
        fid.close()

        velTie = []
        for line in vlTieLine:
            temp = list(filter(None, line.split(" ")))

            if '\\\n' in line:
                velTie.append(temp[:-1])
            else:
                velTie.append(temp)

        self.Param.Tie.velTie = velTie
        self.Param.Const.nnr_nnt_sta[0].extend(getLine(True, trfLines, -1, 0))
        self.Param.Const.nnr_nnt_sta[1].extend(getLine(True, trfLines, -1, 0))
        self.Param.Const.nnr_sou.extend(getLine(True, crfLines, -1, 0))
        self.Param.Global.station.extend(getLine(True, rmStaLines, -1, 0))
        self.Param.Global.source.extend(getLine(True, rmSouLines, -1, 0))
        
        # get the omit station    
        if self.globFlag == 1:
            rows = self.ui.tableWidget_glob_station.rowCount()
            for i in range(rows):
                name = self.ui.tableWidget_glob_station.item(i,1).text()
                omitFlag = self.ui.tableWidget_glob_station.item(i,3).text()
                
                if omitFlag == 'X':
                    self.Param.Global.station.append(name)

        
        self.globthread.setParam(self.Param)
        self.globthread.start()

    def onBottonClick_ionCorr(self):
        if self.runFlag == 1 and len(self.scanInfo.baseInfo[0]) == 2:            
            if len(self.result.VReal[0]) and len(self.result.VReal[1]):                
                self.ui.pushButton_plot_ionCorr.setEnabled(False)
                self.ui.pushButton_plot_ionZero.setEnabled(True)
                
                usedPosit = np.where(self.scanInfo.Obs2Scan != 0)
                correctIono(self.scanInfo, self.staObs)
                # print(self.scanInfo.ambigNum, self.scanInfo.iondl)
                self.scanInfo.oc_obs[1] -= self.scanInfo.iondl[usedPosit]
                
                self.ionFlag = 1
                self.onBottonClick_process()
            else:
                if len(self.result.VReal[0]):
                    flag = 1
                if len(self.result.VReal[1]):
                    flag = 0
                QMessageBox.information(self,'Information','Please select %s band, process and correct ambiguity!'\
                                        %(self.scanInfo.baseInfo[0][flag]),QMessageBox.Ok)
            
    def onBottonClick_ionZero(self):
        if self.runFlag == 1 and len(self.scanInfo.baseInfo[0]) == 2 and len(self.scanInfo.iondl):
            self.ui.pushButton_plot_ionCorr.setEnabled(True)
            self.ui.pushButton_plot_ionZero.setEnabled(False)
            
            usedPosit = np.where(self.scanInfo.Obs2Scan != 0)
            self.scanInfo.oc_obs[1] += self.scanInfo.iondl[usedPosit]
            self.ionFlag = 0
            self.onBottonClick_process()
            # self.signal_plotChange()

    def onBottonClick_modify_nnrt_trf(self):
        '''
        dialog = QDialog(self)
        dialog.setWindowTitle('TRF constrain setting')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(self.size() * 0.5)

        layout = QVBoxLayout()
        label = QLabel()
        label.setFont(QFont("Arial", 10))
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec_()
        '''
        self.globModifyFile = os.path.join(self.dirpath[2],self.ui.lineEdit_glob_trf_nnrnnt.text())
        if not os.path.exists(self.globModifyFile):
            QMessageBox.critical(self,'Error',f'{self.globModifyFile} not exists!',QMessageBox.Ok)
        self.ui.textEdit_glob.clear()

        fid = open(self.globModifyFile,'r')
        lines = fid.read()
        fid.close()

        self.ui.textEdit_glob.setPlainText(lines)

    def onBottonClick_modify_nnr_crf(self):
        self.globModifyFile = os.path.join(self.dirpath[2], self.ui.lineEdit_glob_crf_nnr.text())
        if not os.path.exists(self.globModifyFile):
            QMessageBox.critical(self, 'Error', f'{self.globModifyFile} not exists!', QMessageBox.Ok)
        self.ui.textEdit_glob.clear()

        fid = open(self.globModifyFile, 'r')
        lines = fid.read()
        fid.close()

        self.ui.textEdit_glob.setPlainText(lines)

    def onBottonClick_modify_exsta(self):
        self.globModifyFile = os.path.join(self.dirpath[2], self.ui.lineEdit_glob_station_exclude.text())
        if not os.path.exists(self.globModifyFile):
            QMessageBox.critical(self, 'Error', f'{self.globModifyFile} not exists!', QMessageBox.Ok)
        self.ui.textEdit_glob.clear()

        fid = open(self.globModifyFile, 'r')
        lines = fid.read()
        fid.close()

        self.ui.textEdit_glob.setPlainText(lines)

    def onBottonClick_modify_exsou(self):
        self.globModifyFile = os.path.join(self.dirpath[2], self.ui.lineEdit_glob_source_exclude.text())
        if not os.path.exists(self.globModifyFile):
            QMessageBox.critical(self, 'Error', f'{self.globModifyFile} not exists!', QMessageBox.Ok)
        self.ui.textEdit_glob.clear()

        fid = open(self.globModifyFile, 'r')
        lines = fid.read()
        fid.close()

        self.ui.textEdit_glob.setPlainText(lines)

    def onBottonClick_modify_save(self):
        if self.globModifyFile != '':
            reply = QMessageBox.question(self,'Inquiry', f'Rewrite {self.globModifyFile}',QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                lines = self.ui.textEdit_glob.toPlainText()
                fid = open(self.globModifyFile,'w')
                fid.writelines(lines)
                fid.close()
    
    def onBottonClick_outlierMode(self):
        self.ui.pushButton_plot_clkbk.setChecked(False)
        self.plot_res.clkbkFlag = 0
        
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/magnifier.png", QSize(), QIcon.Normal, QIcon.Off)
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/select.png", QSize(), QIcon.Normal, QIcon.Off)

        if self.ui.pushButton_plot_outlier.isChecked():
            self.ui.pushButton_plot_outlier.setIcon(icon2)
            self.ui.statusBar.showMessage('Outlier selecting mode...')
            self.plot_res.outlierFlag = 1
        else:
            self.ui.pushButton_plot_outlier.setIcon(icon1)
            self.ui.statusBar.showMessage('')
            self.plot_res.outlierFlag = 0
            
    def onBottonClick_omitBL(self):
        
        reply = QMessageBox.question(self,'Omit Baseline?','Omit the %s baseline data?'\
                                    %(self.ui.comboBox_plot_baseline.currentText()),\
                                    QMessageBox.Yes, QMessageBox.No)
        if reply == 16384:
            blRow = self.ui.comboBox_plot_baseline.currentIndex()
            item = QTableWidgetItem('X')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_bl.setItem(blRow, 6, item)
        
    def onBottonClick_omitSta(self):
        reply = QMessageBox.question(self,'Omit Station?','Omit the %s station data?'\
                                    %(self.ui.comboBox_plot_station.currentText()),\
                                    QMessageBox.Yes, QMessageBox.No)
        if reply == 16384:
            staRow = self.ui.comboBox_plot_station.currentIndex()
            item = QTableWidgetItem('X')
            item.setTextAlignment(Qt.AlignCenter)
            if self.ui.table_data_station.item(staRow,5) == None:
                self.ui.table_data_station.setItem(staRow, 6, item)
            elif self.ui.table_data_station.item(staRow,5).text() == 'R':
                QMessageBox.information(self, 'Information', 'The %s station is clock reference! Please modify and omit!'%self.ui.comboBox_plot_station.currentText())
            else:
                self.ui.table_data_station.setItem(staRow, 6, item)

    def onBottonClick_process(self):
        try:
            type(self.scanInfo)
        except AttributeError:
            QMessageBox.information(self, 'Information', 'No input data!', QMessageBox.Ok)
        else:
            icon1 = QIcon()
            icon1.addFile(u":/icons/icons/pause.png", QSize(), QIcon.Normal, QIcon.Off)
            self.ui.pushButton_process.setIcon(icon1)

            if self.backend.isRunning():
                QMessageBox.information(self, 'Information', 'The thread of solve is running! Please wait!',
                                        QMessageBox.Ok)

            if self.ambCorr.isRunning():
                QMessageBox.information(self, 'Information', 'The thread of ambiguity correct is running! Please wait!',
                                        QMessageBox.Ok)

            self.setCursor(Qt.WaitCursor)
            self.ui.statusBar.showMessage('Processing...')
            self.getParam()

            if self.runFlag == 0:
                self.backend.setParam(self.scanInfo, self.Param, self.wrpInfo, self.handOutlierFlag, self.rmOutlier,
                                      self.runFlag, self.bandIndex)
            else:
                self.backend.setParam(self.scanInfo, self.Param, self.wrpInfo, self.handOutlierFlag, self.rmOutlier,
                                      self.runFlag, self.bandIndex, \
                                      self.sourceInfo, self.stationInfo)

            self.backend.start()

    def onBottonClick_produceARC(self):
        name,flag = QInputDialog.getText(self,'Input','Enter the ARC Name(if empty, set:default.arc):') 
        if flag:
            selected_rows = self.ui.tableWidget_session.selectedItems()
            colNum = self.ui.tableWidget_session.columnCount()
            # print(selected_rows,selected_rows[0].text())
            
            arcPath = self.ui.lineEdit_path_arcpath.text()
            # if not os.path.exists(arcPath):
                # os.mkdir(arcPath)
            
            if name=='':
                arcFid = open(os.path.join(arcPath,'default.arc'),'w')
            else:
                arcFid = open(os.path.join(arcPath,name),'w')
                
            for i in range(int(len(selected_rows)/colNum)):
                session = selected_rows[colNum*i+1].text()
                version = int(selected_rows[colNum*i+4].text())
                ac = selected_rows[colNum*i+5].text()

                arcFid.writelines('$%s    %d    %s\n'%(session,version,ac))
        
            arcFid.close()       

    def onBottonClick_reLoad(self):
        self.Param.Setup.weight = 'IN'
        self.signal_showLoadData('plot','')

    def onBottonClick_removeOutlier(self):
        reply = QMessageBox.question(self,'Remove','Remove the outlier from Observe?', QMessageBox.Yes, QMessageBox.No)
        if reply == 16384:
            obsPosit = np.where(self.scanInfo.Obs2Scan != 0)
            
            self.handOutlierFlag = 1
            for i in range(len(self.plot_res.rmMark[2])):
                self.rmOutlier.extend(self.plot_res.rmMark[2][i])
                for j in range(len(self.plot_res.rmMark[2][i])):
                    self.scanInfo.delayFlag[obsPosit[0][self.plot_res.rmMark[2][i][j]]] += 1
                        
            self.ui.pushButton_plot_clkbk.setChecked(False)
            # self.plot_res.outlierFlag = 0
            self.plot_res.clkbkFlag = 0
            # self.onBottonClick_process()
            # self.plot_res.rmOutlierandPlot()
            self.onBottonClick_process()
            
    def onBottonClick_resStaAdd(self):
        self.ui.listWidget_plot_resSta.blockSignals(True)
        self.ui.listWidget_plot_resSta.selectAll()
        self.ui.listWidget_plot_resSta.blockSignals(False)
        self.signal_plotChange()
        
    def onBottonClick_resStaSub(self):
        self.ui.listWidget_plot_resSta.blockSignals(True)
        for row in range(self.ui.listWidget_plot_resSta.count()):
            self.ui.listWidget_plot_resSta.item(row).setSelected(False)
        self.ui.listWidget_plot_resSta.blockSignals(False)
        self.signal_plotChange()

    def onBottonClick_rePlot(self):
        self.ui.pushButton_plot_clkbk.setChecked(False)
        self.ui.pushButton_plot_outlier.setChecked(False)
        self.plot_res.outlierFlag = 0
        self.plot_res.clkbkFlag = 0
        if self.runFlag == 1:
            self.plot_res.axes.cla()
            self.plot_res.plotData()
        self.ui.statusBar.showMessage('')

    def onBottonClick_reWeight(self):
        if self.runFlag == 1:
            if hasattr(self.result, 'chis'):
                rowNum = self.ui.table_data_bl.rowCount()
                k = 0
                for i in range(rowNum-1):
                    num = int(self.ui.table_data_bl.item(i, 4).text())
                    if num <= 1:
                        K += 1
                if k == 0:
                    self.Param.Setup.weight = 'BL'
                    self.onBottonClick_process()
                else:
                    QMessageBox.warning(self,'Warning','Observe number of some baselines equal to 1!', QMessageBox.Yes)

    def onBottonClick_saveOut(self):
        self.outFlag = [self.ui.checkBox_plot_report.isChecked(),\
                        self.ui.checkBox_plot_eopout.isChecked(),\
                        self.ui.checkBox_plot_snx.isChecked(),\
                        self.ui.checkBox_plot_vgosDb.isChecked()]
        if self.ui.checkBox_plot_snx.isChecked():
            self.Param.Out.snxPath = ['YES',self.ui.lineEdit_path_SNX.text()]
        if self.ui.checkBox_plot_report.isChecked():
            self.Param.Out.reportPath = ['YES',self.ui.lineEdit_path_Report.text()]
        if self.ui.checkBox_plot_eopout.isChecked():
            self.Param.Out.eopPath = ['YES',self.ui.lineEdit_path_EOPO.text()]
        
        
        if self.runFlag == 1:            
            self.outthread.setParam(self.scanInfo, self.wrpInfo, self.Param, \
                                    self.result, self.stationInfo, \
                                    self.sourceInfo, \
                                    self.dirpath[0], \
                                    0, \
                                    self.out,\
                                    self.outFlag)
            self.outthread.start()
        else:
            QMessageBox.warning(self,'Waring','The session not loaded or processed,\nCan not save!',QMessageBox.Ok)
        
    def onBottonClick_savePath(self):
        dirPath = os.path.dirname(os.path.abspath(__file__))
        dirFile = os.path.join(dirPath, 'directory.ini')
        fid = open(dirFile,'w')
        fid.writelines('*input dir\n')
        fid.writelines('vgosDb %s\n'%self.ui.lineEdit_path_vgosDb.text())
        fid.writelines('Master %s\n'%self.ui.lineEdit_path_master.text())
        fid.writelines('Apriori %s\n'%self.ui.lineEdit_path_Apriori.text())
        fid.writelines('*apriori file\n')
        fid.writelines('Station %s\n'%self.ui.lineEdit_param_Station.text())
        fid.writelines('Source %s\n'%self.ui.lineEdit_param_Source.text())
        fid.writelines('EOP %s\n'%self.ui.lineEdit_param_EOP.text())
        fid.writelines('EPHEM %s\n'%self.ui.lineEdit_param_EPHEM.text())
        fid.writelines('*output dir\n')
        fid.writelines('Residual %s\n'%self.ui.lineEdit_path_Residual.text())
        fid.writelines('Report %s\n'%self.ui.lineEdit_path_Report.text())
        fid.writelines('SNX %s\n'%self.ui.lineEdit_path_SNX.text())
        fid.writelines('EOPO %s\n'%self.ui.lineEdit_path_EOPO.text())
        fid.writelines('ARC %s\n'%self.ui.lineEdit_path_arcpath.text())
        fid.writelines('*Analysis Centre\n')
        fid.writelines('AC %s\n'%self.ui.lineEdit_param_ac.text())
        fid.writelines('*Data Type\n')
        fid.writelines('DT %d\n' % self.ui.comboBox_dataType.currentIndex())
        fid.close()

        self.dirpath = [self.ui.lineEdit_path_vgosDb.text(),self.ui.lineEdit_path_master.text(),\
                        self.ui.lineEdit_path_Apriori.text(),self.ui.lineEdit_param_Station.text(),\
                        self.ui.lineEdit_param_Source.text(),self.ui.lineEdit_param_EOP.text(),\
                        self.ui.lineEdit_param_EPHEM.text(),self.ui.lineEdit_path_Residual.text(),\
                        self.ui.lineEdit_path_Report.text(),self.ui.lineEdit_path_SNX.text(),\
                        self.ui.lineEdit_path_EOPO.text(),self.ui.lineEdit_path_arcpath.text()]

        self.init_param()
        self.ui.statusBar.showMessage('The path in Preference has been saved!')

    def onBottonClick_SetClearMode(self):
        if self.ui.checkBox_est_clk.isChecked():
            self.ui.checkBox_est_clk.setChecked(False)
        if self.ui.checkBox_est_blclk.isChecked():
            self.ui.checkBox_est_blclk.setChecked(False)
        if self.ui.checkBox_est_wet.isChecked():
            self.ui.checkBox_est_wet.setChecked(False)
        if self.ui.checkBox_est_grad.isChecked():
            self.ui.checkBox_est_grad.setChecked(False)
        if self.ui.checkBox_est_pmxy.isChecked():
            self.ui.checkBox_est_pmxy.setChecked(False)
        if self.ui.checkBox_est_ut1.isChecked():
            self.ui.checkBox_est_ut1.setChecked(False)
        if self.ui.checkBox_est_rpmxy.isChecked():
            self.ui.checkBox_est_rpmxy.setChecked(False)
        if self.ui.checkBox_est_lod.isChecked():
            self.ui.checkBox_est_lod.setChecked(False)
        if self.ui.checkBox_est_nutxy.isChecked():
            self.ui.checkBox_est_nutxy.setChecked(False)
        if self.ui.checkBox_est_station.isChecked():
            self.ui.checkBox_est_station.setChecked(False)
        if self.ui.checkBox_est_source.isChecked():
            self.ui.checkBox_est_source.setChecked(False)
        if self.ui.checkBox_est_station.isChecked():
            self.ui.checkBox_est_station.setChecked(False)
        if self.ui.checkBox_est_source.isChecked():
            self.ui.checkBox_est_source.setChecked(False)
        if self.ui.checkBox_est_sounnr.isChecked():
            self.ui.checkBox_est_sounnr.setChecked(False)
            print(self.Param.Const.nnr_sou)
        if self.ui.checkBox_est_nnr.isChecked():
            self.ui.checkBox_est_nnr.setChecked(False)
        if self.ui.checkBox_est_nnt.isChecked():
            self.ui.checkBox_est_nnt.setChecked(False)

        self.ui.label_result.setText('')

    def onBottonClick_SetRegularMode(self):
        self.onBottonClick_SetClearMode()
        if self.ui.pushButton_plot_moderegular.isChecked():
            self.ui.pushButton_plot_modeUT1.setChecked(False)
            self.ui.pushButton_plot_modeEOP.setChecked(False)

            self.ui.checkBox_est_clk.setChecked(True)
            self.ui.checkBox_est_wet.setChecked(True)
            self.ui.checkBox_est_grad.setChecked(True)
            self.ui.radioButton_est_eop_poly.setChecked(True)
            self.ui.checkBox_est_ut1.setChecked(True)
            self.ui.checkBox_est_pmxy.setChecked(True)
            self.ui.checkBox_est_lod.setChecked(True)
            self.ui.checkBox_est_rpmxy.setChecked(True)
            self.ui.checkBox_est_nutxy.setChecked(True)

            self.ui.checkBox_est_station.setChecked(True)
            self.ui.checkBox_est_source.setChecked(True)
            self.ui.checkBox_est_sounnr.setChecked(True)
            self.ui.checkBox_est_nnr.setChecked(True)
            self.ui.checkBox_est_nnt.setChecked(True)

    def onBottonClick_setSouEst(self):
        if self.runFlag:
            reply = QMessageBox.question(self,'Source Estimate Set','Set the observation of source more than 4 to estimate?', \
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == 16384:
                for irow in range(self.ui.table_data_source.rowCount()):
                    obsNum = int(self.ui.table_data_source.item(irow,3).text())
                    if obsNum > 4:
                        item = QTableWidgetItem('Y')
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.table_data_source.setItem(irow, 6, item)
                    else:
                        if 'EXCEPT' not in self.Param.Flags.sou:
                            self.Param.Flags.sou.append('EXCEPT')
                        self.Param.Flags.sou.append(self.ui.table_data_source.item(irow,1).text())
                        
    def onBottonClick_setStaEst(self):
        if self.runFlag:
            reply = QMessageBox.question(self,'Station Estimate Set','Set the station to estimate, except reference station?', \
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == 16384:
                for irow in range(self.ui.table_data_station.rowCount()):
                    staName = self.ui.table_data_station.item(irow,1).text()
                    if staName != self.scanInfo.refclk:
                        item = QTableWidgetItem('Y')
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.table_data_station.setItem(irow, 7, item)
    
    def onBottonClick_SetEOPMode(self):
        self.onBottonClick_SetClearMode()
        if self.ui.pushButton_plot_modeEOP.isChecked():
            self.ui.pushButton_plot_modeUT1.setChecked(False)
            self.ui.pushButton_plot_moderegular.setChecked(False)

            self.ui.checkBox_est_clk.setChecked(True)
            self.ui.checkBox_est_blclk.setChecked(True)
            self.ui.checkBox_est_wet.setChecked(True)
            self.ui.checkBox_est_grad.setChecked(True)
            self.ui.radioButton_est_eop_poly.setChecked(True)
            self.ui.checkBox_est_ut1.setChecked(True)
            self.ui.checkBox_est_pmxy.setChecked(True)
            self.ui.checkBox_est_lod.setChecked(True)
            self.ui.checkBox_est_rpmxy.setChecked(True)
            self.ui.checkBox_est_nutxy.setChecked(True)
    
    def onBottonClick_SetUT1Mode(self):
        self.onBottonClick_SetClearMode()
        if self.ui.pushButton_plot_modeUT1.isChecked():
            self.ui.pushButton_plot_modeEOP.setChecked(False)
            self.ui.pushButton_plot_moderegular.setChecked(False)
            self.ui.checkBox_est_clk.setChecked(True)
            self.ui.checkBox_est_wet.setChecked(True)
            self.ui.radioButton_est_eop_poly.setChecked(True)
            self.ui.checkBox_est_ut1.setChecked(True)

    def onBottonClick_showHelp(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('File and Path help')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(self.size()*0.5)
        layout = QVBoxLayout()
        label = QLabel()
        label.setText("""<style>span {white-space:pre;}</style>
                         <span style='color:red;'><p>Station:</p></span>
                         <span style='color:red;'><p>%Name            X(m)                 Y(m)             Z(m)        Vx(m/yr)   Vy(m/yr)  Vz(m/yr)   startMJD   notes</p></span>
                         <span style='color:red;'><p>GRASSE 4581697.4036 556126.1061 4389351.6728 -0.01390  0.01906  0.01100    57023  ITRF2020</p></span>
                         <span style='color:blue;'><p>Source:</p></span>
                         <span style='color:blue;'><p>%IERS_name  ICRF_Designation  J2000_name IVS_name    d_o    Right Ascension          Declination</p></span>
                         <span style='color:blue;'><p>%if IVS_name is equal to IERS_name, then is X, define is defining source</p></span>
                         <span style='color:blue;'><p>0005+114  J000800.8+114400  J0008+1144            X    other  00 08 00.83826352     11 44 00.7748326</p></span>
                         <span style='color:blue;'><p>0007+106  J001031.0+105829  J0010+1058   IIIZW2  define  00 10 31.00590413     10 58 29.5042981</p></span>
                         <span style='color:green;'><p>EOP: can be usno_finals, C04, for IERS finals.daily format</p></span>
                         <span style='color:black;'><p>SNX: the path is also used for menu File->DBList</p></span>""")
        label.setFont(QFont("Arial",10))
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec_()

    def onBottonClick_staInfoAdd(self):
        self.ui.listWidget_plot_station.blockSignals(True)
        self.ui.listWidget_plot_station.selectAll()
        self.signal_plotStationInfo()
        self.ui.listWidget_plot_station.blockSignals(False)

    def onBottonClick_staInfoSub(self):
        self.ui.listWidget_plot_station.blockSignals(True)
        for row in range(self.ui.listWidget_plot_station.count()):
            self.ui.listWidget_plot_station.item(row).setSelected(False)
        self.signal_plotStationInfo()
        self.ui.listWidget_plot_station.blockSignals(False)
        
    #-------------------------------------------------------------------------#
    #------------------------- Radio buttion Action --------------------------#
    def onRadioClick_enableShow(self):
        if self.ui.radioButton_est_eop_cpwl.isChecked():
            self.ui.checkBox_est_rpmxy.setEnabled(False)
            self.ui.checkBox_est_lod.setEnabled(False)
            self.ui.groupBox_refTime.setEnabled(False)
            
            self.ui.lineEdit_pmxy_interval.setEnabled(True)
            self.ui.lineEdit_ut1_interval.setEnabled(True)
            self.ui.lineEdit_pmxy_constr.setEnabled(True)
            self.ui.lineEdit_ut1_constr.setEnabled(True)
            
            self.ui.lineEdit_pmxy_constr_poly.setEnabled(False)
            self.ui.lineEdit_rpmxy_constr_poly.setEnabled(False)
            self.ui.lineEdit_ut1_constr_poly.setEnabled(False)
            self.ui.lineEdit_lod_constr_poly.setEnabled(False)
            # self.ui.lineEdit_nut_constr_poly.setEnabled(False)
            
        if self.ui.radioButton_est_eop_poly.isChecked():
            self.ui.checkBox_est_rpmxy.setEnabled(True)
            self.ui.checkBox_est_lod.setEnabled(True)
            self.ui.groupBox_refTime.setEnabled(True)
            
            self.ui.lineEdit_pmxy_interval.setEnabled(False)
            self.ui.lineEdit_ut1_interval.setEnabled(False)
            self.ui.lineEdit_pmxy_constr.setEnabled(False)
            self.ui.lineEdit_ut1_constr.setEnabled(False)
            
            self.ui.lineEdit_pmxy_constr_poly.setEnabled(True)
            self.ui.lineEdit_rpmxy_constr_poly.setEnabled(True)
            self.ui.lineEdit_ut1_constr_poly.setEnabled(True)
            self.ui.lineEdit_lod_constr_poly.setEnabled(True)

    # ------------------------------------------------------------------------#                   
    # -------------------- matplotlib of residual signal ---------------------#
    def plot_signal_showBaseLine(self, blPosit, resPosit):
        bl = self.scanInfo.blUsed[blPosit]
        
        QMessageBox.information(self,'Baseline Information','            %s-%s           '\
                                    %(self.scanInfo.stationAll[bl[0]-1],self.scanInfo.stationAll[bl[1]-1]))
            
    def plot_signal_showClockBreak(self, xdata):
        reply = QMessageBox.question(self,'Clock break add','Add the clock break (%f) to station %s?'\
                                    %(self.plot_res.clkbkTime, self.ui.comboBox_plot_station.currentText()),\
                                    QMessageBox.Yes, QMessageBox.No)
        if reply == 16384:
            clkbkSta = self.ui.comboBox_plot_station.currentText()
            index  = self.scanInfo.clkBrk.staName.index(clkbkSta)
            self.scanInfo.clkBrk.brkFlag[index] += 1
            temp = []
            temp.extend(self.scanInfo.clkBrk.brkMJD[index])
            temp.append(xdata)
            self.scanInfo.clkBrk.brkMJD[index] = sorted(temp)
            self.ui.pushButton_plot_clkbk.setChecked(False)
            self.plot_res.clkbkFlag = 0

    #-------------------------------------------------------------------------#
    #------------------------------ Other signal -----------------------------#
    def setListWidget(self):
        self.ui.listWidget_plot_resSta.blockSignals(True)
        self.ui.listWidget_plot_resSta.clear()
        stationID = self.ui.comboBox_plot_station.currentIndex()
        blPosit = self.scanInfo.staBlList[stationID]
        for ibl in blPosit:
            blList = self.scanInfo.blUsed[ibl]
            self.ui.listWidget_plot_resSta.addItem(self.scanInfo.stationAll[blList[0]-1]+'-'+\
                                                self.scanInfo.stationAll[blList[1]-1])
                
        self.ui.listWidget_plot_resSta.selectAll()
        self.ui.listWidget_plot_resSta.blockSignals(False)

    def showPathError(self):
        QMessageBox.information(self, 'Information', 'Please modify the path in File/Preference first!',QMessageBox.Ok)

    def signal_localFileShow(self):
        listSelect = self.ui.listWidget_datatype.selectedItems()
        
        dataType = []
        for item in listSelect:
            dataType.append(item.text())
        # print(dataType)
        
        if len(dataType) == 0:
            rowNum = self.ui.tableWidget_session.rowCount()
            for i in range(rowNum):
                self.ui.tableWidget_session.removeRow(0)
        else:
            startYear = int(self.ui.lineEdit_file_startyear.text())
            stopYear = int(self.ui.lineEdit_file_stopyear.text())
            
            if len(dataType) == self.ui.listWidget_datatype.count():
                dataType = 'All'
            
            self.LocalThread.setParam(self.dirpath,startYear, stopYear, dataType)
            self.LocalThread.start()
        
    def signal_plotChange(self):
        if self.runFlag == 1:
            index  = self.ui.comboBox_plot_y.currentIndex()
            if index == 0:
                result = [self.result.VReal[self.bandIndex],self.result.SReal[self.bandIndex]]
                    
            elif index == 1:
                temp = np.sqrt(np.array(self.scanInfo.pObs[self.bandIndex])**2-(0.005/const.c)**2)
                result = np.array(temp)*1E9
                
            self.plot_res.typeFlag = index
            self.plot_res.axes.clear() 
            self.plot_res.initParam(self.scanInfo, self.stationInfo, result, self.Param.Arcs.session[0])
            
            plotSelect = [self.ui.radioButton_plot_all.isChecked(),\
                          self.ui.radioButton_plot_station.isChecked(),\
                          self.ui.radioButton_plot_baseline.isChecked(),\
                          self.ui.radioButton_plot_source.isChecked()]
            posit = plotSelect.index(True)
            if posit == 0:
                self.ui.listWidget_plot_resSta.clear()
                self.ui.listWidget_plot_resSta.setEnabled(False)
                self.ui.listWidget_plot_resSou.setEnabled(False)
                self.ui.pushButton_plot_resStaAdd.setEnabled(False)
                self.ui.pushButton_plot_resStaSub.setEnabled(False)

                self.plot_res.plotAll()
            elif posit == 1:
                stationID = self.ui.comboBox_plot_station.currentIndex()
                listSelect = self.ui.listWidget_plot_resSta.selectedIndexes()
                listSelectIndex = []
                for item in listSelect:
                    listSelectIndex.append(item.row())
                                    
                self.plot_res.plotStation(stationID, listSelectIndex)
            elif posit == 2:
                self.ui.listWidget_plot_resSta.clear()
                self.ui.listWidget_plot_resSta.setEnabled(False)
                self.ui.listWidget_plot_resSou.setEnabled(False)
                self.ui.pushButton_plot_resStaAdd.setEnabled(False)
                self.ui.pushButton_plot_resStaSub.setEnabled(False)
                baselineID = self.ui.comboBox_plot_baseline.currentIndex()
                self.plot_res.plotBaseline(baselineID)
            elif posit == 3:
                self.ui.listWidget_plot_resSta.clear()
                self.ui.listWidget_plot_resSta.setEnabled(False)
                self.ui.listWidget_plot_resSou.setEnabled(True)
                self.ui.pushButton_plot_resStaAdd.setEnabled(False)
                self.ui.pushButton_plot_resStaSub.setEnabled(False)

                sourceID = -1
                listSelect = self.ui.listWidget_plot_resSou.selectedIndexes()
                for item in listSelect:
                    sourceID = item.row()

                if sourceID >= 0:
                    print(sourceID)
                    self.plot_res.plotSource(sourceID)

    def signal_plotResAll(self):
        self.ui.pushButton_plot_resOmitBL.setEnabled(False)
        self.ui.pushButton_plot_resAddBlClock.setEnabled(False)
        self.ui.pushButton_plot_resOmitSta.setEnabled(False)
        
        self.signal_plotChange()
                
    def signal_plotResBl(self):
        self.ui.pushButton_plot_resOmitBL.setEnabled(True)
        self.ui.pushButton_plot_resAddBlClock.setEnabled(True)
        self.ui.pushButton_plot_resOmitSta.setEnabled(False)
        
        self.signal_plotChange()
                
    def signal_plotResSta(self):
        self.ui.pushButton_plot_resOmitBL.setEnabled(False)
        self.ui.pushButton_plot_resAddBlClock.setEnabled(False)
        self.ui.pushButton_plot_resOmitSta.setEnabled(True)
        
        
        if self.runFlag == 1:
            self.ui.listWidget_plot_resSta.setEnabled(True)
            self.ui.pushButton_plot_resStaAdd.setEnabled(True)
            self.ui.pushButton_plot_resStaSub.setEnabled(True)

            self.setListWidget()
            
            self.signal_plotChange()

    def signal_plotResSou(self):
        self.ui.pushButton_plot_resOmitBL.setEnabled(False)
        self.ui.pushButton_plot_resAddBlClock.setEnabled(False)
        self.ui.pushButton_plot_resOmitSta.setEnabled(False)
        if self.runFlag == 1:
            self.ui.listWidget_plot_resSou.setEnabled(True)
            self.ui.listWidget_plot_resSou

        self.signal_plotChange()
            
    def signal_plotResult(self):
        if self.runFlag == 1:
            comboxSelect = self.ui.comboBox_plot_result_y.currentIndex()
            
            if hasattr(self.result, 'err'):
                if comboxSelect == 0:
                    self.ui.listWidget_plot_result.setEnabled(True)
                    item = self.ui.listWidget_plot_result.currentItem()
                    if item.text() != self.scanInfo.refclk:
                        self.plot_result.axes.clear()
                        self.plot_result.plotInit(comboxSelect, item.text())
                    else:
                        self.plot_result.axes.clear()
                        self.plot_result.draw()
                elif comboxSelect == 1:
                    self.ui.listWidget_plot_result.setEnabled(True)
                    item = self.ui.listWidget_plot_result.currentItem()
                    self.plot_result.axes.clear()
                    self.plot_result.plotInit(comboxSelect, item.text())
                
                elif comboxSelect == 4 or comboxSelect == 5 or comboxSelect == 6:
                    self.ui.listWidget_plot_result.setEnabled(False)
                    self.plot_result.axes.clear()
                    self.plot_result.plotInit(comboxSelect, '')
            
            
            # else:
            #     self.ui.listWidget_plot_result.setEnabled(True)
            
            # self.plot_result.axes.clear()
            # self.plot_result.plotInit(comboxSelect, staSelect)
            
                
    def signal_plotStationInfo(self):
        if self.runFlag == 1:
            # items = self.ui.listWidget_plot_station.selectedItems()
            
            # listSelectIndex = []
            # for item in items:
            #     staName = item.text()
            #     listSelectIndex.append(self.scanInfo.stationAll.index(staName))
            comboxSelect = self.ui.comboBox_plot_sta_y.currentIndex()
            
            listSelect = self.ui.listWidget_plot_station.selectedIndexes()
            
            listSelectIndex = []
            for item in listSelect:
                listSelectIndex.append(item.row())
                            
            self.plot_sta.axes.clear()
            self.plot_sta.plotInit(comboxSelect, listSelectIndex)

    def signal_plotGlob(self):
        if self.ui.radioButton_glob_trf.isChecked():
            self.ui.listWidget_plot_glob_crf.blockSignals(True)
            self.ui.checkBox_plot_glob_ra.setEnabled(False)
            self.ui.checkBox_plot_glob_de.setEnabled(False)
            self.ui.checkBox_plot_glob_x.setEnabled(True)
            self.ui.checkBox_plot_glob_y.setEnabled(True)
            self.ui.checkBox_plot_glob_z.setEnabled(True)
            self.ui.listWidget_plot_glob_trf.blockSignals(False)
            self.signal_plotGlobStation()
        else:
            self.ui.listWidget_plot_glob_trf.blockSignals(True)
            self.ui.checkBox_plot_glob_x.setEnabled(False)
            self.ui.checkBox_plot_glob_y.setEnabled(False)
            self.ui.checkBox_plot_glob_z.setEnabled(False)
            self.ui.checkBox_plot_glob_ra.setEnabled(True)
            self.ui.checkBox_plot_glob_de.setEnabled(True)
            self.ui.listWidget_plot_glob_crf.blockSignals(False)
            self.signal_plotGlobSource()

    def signal_plotGlobStation(self):
        
        listSelect = self.ui.listWidget_plot_glob_trf.selectedIndexes()
        num = listSelect[0].row()
        station = self.ui.listWidget_plot_glob_trf.item(num).text()
        
        self.plot_glob.axes.clear()
        x = np.array(self.sitAll['estEpoch'][num])
        y = np.array(self.sitAll['estPosit'][num])
        
        choice = [self.ui.checkBox_plot_glob_x.isChecked(),\
                  self.ui.checkBox_plot_glob_y.isChecked(),\
                  self.ui.checkBox_plot_glob_z.isChecked()]
        
        self.plot_glob.plotSelect(0,choice,station,x,y*100)
        
    def signal_plotGlobSource(self):
        listSelect = self.ui.listWidget_plot_glob_crf.selectedIndexes()
        num = listSelect[0].row()
        source = self.ui.listWidget_plot_glob_crf.item(num).text()

        self.plot_glob.axes.clear()
        x = np.array(self.souAll['estEpoch'][num])
        y = np.array(self.souAll['estPosit'][num])

        choice = [self.ui.checkBox_plot_glob_ra.isChecked(), \
                  self.ui.checkBox_plot_glob_de.isChecked()]

        self.plot_glob.plotSelect(1,choice,source,x,y*180/np.pi*3600*1000)

    def signal_showLoadData(self, method, data):
        if method == 'menu':
            dataFile, fileType = QFileDialog.getOpenFileName(self,'Data Selection',self.dirpath[0],\
                                                            'All Files(*)')
            if len(dataFile):
                temp = dataFile.rfind('/')
                wrpFile = dataFile[temp + 1:]
                #if '.wrp' in wrpFile and self.ui.radioButton_file_wrp.isChecked():
                if '.wrp' in wrpFile and self.ui.comboBox_dataType.currentIndex() == 0:
                    # vgosDB data file
                    temp1 = wrpFile.index('_')
                    temp2 = wrpFile[temp1+1:].index('_')+temp1+1
                    temp3 = wrpFile.rfind('_')
                    self.Param.Arcs.session = [wrpFile[:temp1]]
                    self.Param.Arcs.version = [int(wrpFile[temp1+2:temp2])]
                    self.Param.Arcs.AC = [wrpFile[temp2+2:temp3]]
                #elif self.ui.radioButton_file_ngs.isChecked():
                elif self.ui.comboBox_dataType.currentIndex() == 1:
                    # NGS data file
                    self.Param.Arcs.session = [wrpFile]
                    self.Param.Arcs.version = [0]
                    self.Param.Arcs.AC = ['NONE']
                elif self.ui.comboBox_dataType.currentIndex() == 2:
                    self.Param.Arcs.session = [wrpFile]
                    self.Param.Arcs.version = [-1]
                    self.Param.Arcs.AC = ['NONE']
            else:
                QMessageBox.information(self, 'Information', 'Please input the data!')
                return
        elif method == 'table':
            self.Param.Arcs.session = [data[0]]
            self.Param.Arcs.version = [data[1]]
            self.Param.Arcs.AC = [data[2]]
        elif method == 'plot':
            if len(self.Param.Arcs.session) == 0:
                QMessageBox.information(self, 'Information', 'Please input the data!')
                return

        if len(self.Param.Arcs.session):
            #if self.ui.radioButton_file_wrp.isChecked():
            if self.ui.comboBox_dataType.currentIndex() == 0:
                self.scanInfo, self.wrpInfo = read_vgosDB(self.Param, 0)

                '''
                try:
                    self.scanInfo, self.wrpInfo = read_vgosDB(self.Param, 0)
                except:
                    QMessageBox.critical(self, 'Error', 'vgosDb type data loading wrong! Please check path!')
                    return
                '''
            #elif self.ui.radioButton_file_ngs.isChecked():
            elif self.ui.comboBox_dataType.currentIndex() == 1:
                try:
                    self.scanInfo, self.wrpInfo = ngsScanInfo(self.Param, 0)
                except:
                    QMessageBox.critical(self, 'Error', 'NGS type data loading wrong! Please check path!')
                    return
            elif self.ui.comboBox_dataType.currentIndex() == 2:
                try:
                    self.scanInfo, self.wrpInfo = createScanInfo(self.Param, 0)
                except:
                    QMessageBox.critical(self, 'Error', 'Other type data loading wrong! Please check path!')
                    return

            latAll = []
            lonAll = []
            for i in range(len(self.scanInfo.stationAll)):
                lon,lat,height = xyz2ell(self.scanInfo.staPosit[i])
                latAll.append(lat*180/np.pi)
                lonAll.append(lon*180/np.pi)
            self.plot_mapsta.clearMap()
            self.plot_mapsta.plotStation(latAll,lonAll,self.scanInfo.stationAll)
            self.plot_mapsou.clearMap()
            self.plot_mapsou.plotSource(self.scanInfo.souPosit)
            
            self.runFlag = 0
            self.useBlNum = 0
            self.useStaNum = 0
            self.ionFlag = 0
            self.ui.comboBox_plot_station.clear()
            self.ui.comboBox_plot_baseline.clear()
            
            obsNum = len(self.scanInfo.Obs2Scan)

            hour,minu,sec = hms(self.scanInfo.scanMJD[-1] - self.scanInfo.scanMJD[0])
            sMon = getMon(int(self.scanInfo.scanTime[0,1]))
            eMon = getMon(int(self.scanInfo.scanTime[-1,1]))
            self.ui.textBrowser_information.clear()
            self.ui.textBrowser_information.insertPlainText('\nSession/Code:                                  %s/%s\n'\
                                                            %(self.Param.Arcs.session[0],self.scanInfo.expName)+\
                                                            'Experiment description:                        %s\n'\
                                                            %self.scanInfo.expDescrip+\
                                                            'Epoch of the first observation:                %02d %s %4d;%02d:%02d:%7.4f\n'\
                                                            %(self.scanInfo.scanTime[0,2],sMon,self.scanInfo.scanTime[0,0],\
                                                            self.scanInfo.scanTime[0,3],self.scanInfo.scanTime[0,4],self.scanInfo.scanTime[0,5])+\
                                                            'Epoch of the last observation:                 %02d %s %4d;%02d:%02d:%7.4f\n'\
                                                            %(self.scanInfo.scanTime[-1,2],eMon,self.scanInfo.scanTime[-1,0],\
                                                            self.scanInfo.scanTime[-1,3],self.scanInfo.scanTime[-1,4],self.scanInfo.scanTime[-1,5])+\
                                                            'Interval of observation:                       %02dhr %02dmin %5.2fsec\n'\
                                                            %(hour,minu,sec)+\
                                                            'Number of scan:                                %-5d\n'\
                                                            %(len(self.scanInfo.scanMJD))+\
                                                            'Number of observe:                             %-5d\n'\
                                                            %obsNum+\
                                                            'Number of station:                             %-2d\n'\
                                                            %(len(self.scanInfo.stationAll))+\
                                                            'Number of source:                              %-2d'\
                                                            %(len(self.scanInfo.sourceAll)))

            self.initEstParam()
            if method != 'plot':
                self.menuAction_showParamBasic()
                self.plot_res.figInit()
            
            self.bandNum = len(self.scanInfo.baseInfo[0])
            if self.bandNum == 1:
                self.ui.pushButton_plot_S.setEnabled(False)
                self.ui.pushButton_plot_ionCorr.setEnabled(False)
                self.ui.pushButton_plot_ionZero.setEnabled(False)
                index = 0
            elif self.bandNum == 2:
                self.ui.pushButton_plot_S.setEnabled(True)
                try:
                    len(self.scanInfo.iondl)
                except AttributeError:
                    self.ui.pushButton_plot_ionCorr.setEnabled(True)
                    self.ui.pushButton_plot_ionZero.setEnabled(False)
                else:
                    self.ui.pushButton_plot_ionCorr.setEnabled(False)
                    self.ui.pushButton_plot_ionZero.setEnabled(True)
                index = 1
                
            qcodeLine = 'Number proportion of qcode:                   '
            for i in range(6):
                temp = np.where(self.scanInfo.qCode[index]==(i+4))[0]
                qcodeLine += ' %d(%3.1f%%)'%(i+4,len(temp)/obsNum*100)

            self.ui.textBrowser_information.insertPlainText('\n%s'%qcodeLine)
            
            if method == 'plot':
                self.onBottonClick_process()


    #-------------------------------------------------------------------------#
    #----------------------------- Thread Signal -----------------------------#       
    def thread_signal_runError(self, errorType):
        QMessageBox.information(self,'Error','The solve exists %s, please contact developer!'%errorType,QMessageBox.Ok)
                
    def thread_signal_showAmbCorr(self, ambNum):
        self.ui.statusBar.showMessage('Ambiguity correct over!')
        self.scanInfo.ambigNum[self.bandIndex] += ambNum
        obsPosit = np.where(self.scanInfo.Obs2Scan!=0)
        self.scanInfo.oc_obs[self.bandIndex] += ambNum[obsPosit] * self.scanInfo.baseInfo[2][self.bandIndex][obsPosit]
        
        self.onBottonClick_process()
        
    def thread_signal_showLocalResult(self, fileList, searchFile):
        # prohibit sort
        self.ui.tableWidget_session.setSortingEnabled(False)
        rowNum = self.ui.tableWidget_session.rowCount()
        for i in range(rowNum):
            self.ui.tableWidget_session.removeRow(0)
        
        self.local_fileList = fileList
        rowNum = len(searchFile)
        self.ui.tableWidget_session.setRowCount(rowNum)
        self.ui.tableWidget_session.verticalHeader().setVisible(False)

        # wrmsSum = 0
        # k = 0
        for i in range(rowNum):
            self.ui.tableWidget_session.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.ui.tableWidget_session.setItem(i, 1, QTableWidgetItem(searchFile[i][0]))
            self.ui.tableWidget_session.setItem(i, 2, QTableWidgetItem(searchFile[i][1]))
            self.ui.tableWidget_session.setItem(i, 3, QTableWidgetItem(searchFile[i][2]))

            item = QTableWidgetItem(str(searchFile[i][3]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget_session.setItem(i, 4, item)

            item = QTableWidgetItem(str(searchFile[i][4]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget_session.setItem(i, 5, item)

            item = QTableWidgetItem(str(searchFile[i][5]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget_session.setItem(i, 6, item)

            item = QTableWidgetItem('%.1f'%searchFile[i][6])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget_session.setItem(i, 7, item)

            item = QTableWidgetItem('%5.1f'%searchFile[i][7])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget_session.setItem(i, 8, item)

            self.ui.tableWidget_session.setItem(i, 9, QTableWidgetItem(searchFile[i][8]))
            # if searchFile[i][4]<=50:
                # wrmsSum += searchFile[i][4]**2
                # k += 1
        # print('RMS of %d wrms is: %.1f'%(k,np.sqrt(wrmsSum/k)))
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.ui.tableWidget_session.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

        # cancel the sort
        #self.ui.tableWidget_session.sortByColumn(-1)
        # allow sort
        self.ui.tableWidget_session.setSortingEnabled(True)
    def thread_signal_showOutFinish(self, checkFlag):
        if not -1 in checkFlag and sum(checkFlag) >= 0:
            QMessageBox.information(self,'Information','The result is saved!',QMessageBox.Ok)
        else:
            errStr = ['report','eop','snx']
            temp = np.where(np.array(self.outFlag)==-1)
            outStr = ''
            for i in range(len(temp[0])):
                outStr += errStr[temp[0][i]]+' '
            QMessageBox.warning(self,'Waring','The %s output is wrong!'%outStr,QMessageBox.Ok)
              
    def thread_signal_showResult(self, scanInfo, Param, sourceInfo, stationInfo, result, staObs, out, runFlag):
        self.rmOutlier = []
        self.handOutlierFlag = 0
    
        self.ui.statusBar.showMessage('Process over!')
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/run.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui.pushButton_process.setIcon(icon1)
        
        self.scanInfo = scanInfo
        self.Param = Param
        self.sourceInfo = sourceInfo
        self.stationInfo = stationInfo
        self.result = result
        self.staObs = staObs
        self.out = out

        useblNum = []
        for i in range(len(scanInfo.blUsed)):
            useblNum.append(len(scanInfo.blResPosit[i]))
            
        usebl = scanInfo.blUsed
        useSta = scanInfo.staUsed
        
        # update the comboBox of plot frame
        self.ui.comboBox_plot_baseline.blockSignals(True)
        self.ui.comboBox_plot_station.blockSignals(True)
        self.ui.listWidget_plot_resSou.blockSignals(True)

        if self.useStaNum != len(useSta):
            self.ui.comboBox_plot_station.clear()
            for i in range(len(useSta)):
                self.ui.comboBox_plot_station.addItem(self.scanInfo.stationAll[useSta[i]-1])
            self.useStaNum = len(useSta)
            
            if self.ui.radioButton_plot_station.isChecked():
                self.setListWidget()
        
        if self.useBlNum != len(usebl):
            self.ui.comboBox_plot_baseline.clear()
            for i in range(len(usebl)):
                self.ui.comboBox_plot_baseline.addItem('%8s-%8s'%(self.scanInfo.stationAll[usebl[i][0]-1],\
                                                                  self.scanInfo.stationAll[usebl[i][1]-1]))
            self.useBlNum = len(usebl)

        self.ui.listWidget_plot_resSou.clear()
        for i in self.scanInfo.souUsed:
            self.ui.listWidget_plot_resSou.addItem(self.scanInfo.sourceAll[i])
        self.ui.listWidget_plot_resSou.setCurrentRow(0)

        self.ui.comboBox_plot_baseline.blockSignals(False)
        self.ui.comboBox_plot_station.blockSignals(False)
        self.ui.listWidget_plot_resSou.blockSignals(False)

                
        self.updateStaTab(useSta)
        self.updateBlTab(useblNum, usebl)
        self.updateSouTab()
        
        self.handOutlierFlag = 0
        self.rmOutlier = []
        self.Param.Setup.weight = 'IN'
        
        self.runFlag = runFlag
        self.setCursor(Qt.ArrowCursor)
        
        self.signal_plotChange()
        self.plot_sta.initParam(scanInfo, stationInfo)
        self.plot_res.rmMark = [[],[],[]]
        self.updateStaList(useSta)


        if hasattr(result, 'wrms'):
            self.ui.label_result.setText('WRMS: %10.1fps       Chi-square: %8.2f'%(result.wrms,result.chis))
        else:
            self.ui.label_result.setText('')
        
        self.plot_result.initParam(scanInfo, Param, stationInfo, result, out)
        self.updateStaResult(useSta)
        
    def thread_signal_showGlob(self, sitAll, souAll):
        
        self.globFlag = 1
        
        self.sitAll = sitAll
        self.souAll = souAll

        # unpdate station listwidget of glob plot
        self.ui.listWidget_plot_glob_trf.blockSignals(True)
        self.ui.listWidget_plot_glob_trf.clear()
        for i in range(len(sitAll['name'])):
            self.ui.listWidget_plot_glob_trf.addItem(sitAll['name'][i])
            
        self.ui.listWidget_plot_glob_trf.setCurrentRow(0)
        self.ui.listWidget_plot_glob_trf.blockSignals(False)
        #self.signal_plotGlobStation()

        # unpdate source listwidget of glob plot
        self.ui.listWidget_plot_glob_crf.blockSignals(True)
        self.ui.listWidget_plot_glob_crf.clear()
        for i in range(len(souAll['name'])):
            self.ui.listWidget_plot_glob_crf.addItem(souAll['name'][i])

        self.ui.listWidget_plot_glob_crf.setCurrentRow(0)
        self.ui.listWidget_plot_glob_crf.blockSignals(False)
        #self.signal_plotGlobSource()

        self.updateGlobStationTab()
        self.updateGlobSourceTab()
        self.signal_plotGlob()
    #-------------------------------------------------------------------------#
    #------------------------------- GUI update ------------------------------#
    def updateBlTab(self, useblNum, usebl):

        self.ui.table_data_bl.setRowCount(0)
        self.ui.table_data_bl.setRowCount(len(usebl)+1)
        self.ui.table_data_bl.verticalHeader().setVisible(False)

        for i in range(len(usebl)):
            self.ui.table_data_bl.setItem(i, 0, QTableWidgetItem(str(i)))
            self.ui.table_data_bl.setItem(i, 1, QTableWidgetItem(self.scanInfo.stationAll[usebl[i][0]-1]+'-'+\
                                                                      self.scanInfo.stationAll[usebl[i][1]-1]))

            # compute baseline length
            sta_xyz1 = self.scanInfo.staPosit[usebl[i][0]-1]
            sta_xyz2 = self.scanInfo.staPosit[usebl[i][1]-1]
            bllength = np.sqrt((sta_xyz1[0]-sta_xyz2[0])**2 + \
                               (sta_xyz1[1]-sta_xyz2[1])**2 + \
                               (sta_xyz1[2]-sta_xyz2[2])**2)
            item = QTableWidgetItem(str('%9.3f'%(bllength*1E-3)))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_bl.setItem(i, 2, item)

            temp = np.where(np.sum(np.abs(self.scanInfo.Obs2Baseline - usebl[i]), axis=1) == 0)
            item = QTableWidgetItem(str(len(temp[0])))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_bl.setItem(i, 3, item)
            
            item = QTableWidgetItem(str(useblNum[i]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_bl.setItem(i,4,item)
            
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_bl.setItem(i,6,item)
            
            #------------------ baseline clock flag ---------------------#
            flag = 0
            # tempbl = [usebl[i][0]-1, usebl[i][1]-1]
            if usebl[i] in self.scanInfo.blClkList:
                if self.ui.table_data_bl.item(i,5)==None:
                    flag += 1
                elif self.ui.table_data_bl.item(i,5).text() != 'Y':
                    flag += 1
                if flag:
                    item = QTableWidgetItem('Y')
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.table_data_bl.setItem(i,5,item)
            else:
                item = QTableWidgetItem('')
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_data_bl.setItem(i,5,item)

        item = QTableWidgetItem(str(sum(useblNum)))
        item.setTextAlignment(Qt.AlignCenter)
        self.ui.table_data_bl.setItem(len(usebl), 4, item)
                
    def updateGlobSourceTab(self):
        
        souNum = len(self.souAll['name'])
        self.ui.tableWidget_glob_source.setRowCount(souNum)
        self.ui.tableWidget_glob_source.verticalHeader().setVisible(False)
        
        for i in range(souNum):
            self.ui.tableWidget_glob_source.setItem(i, 0, QTableWidgetItem(str(i)))
            self.ui.tableWidget_glob_source.setItem(i, 1, QTableWidgetItem(self.souAll['name'][i]))
            obsNum = len(self.souAll['estEpoch'][i])
            self.ui.tableWidget_glob_source.setItem(i, 2, QTableWidgetItem(str(obsNum)))
            
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_glob_source.setItem(i, 3, item)
            
            if self.souAll['nnr'][i] == 1:
                item = QTableWidgetItem('Y')
            else:
                item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_glob_source.setItem(i, 4, item)
                
    def updateGlobStationTab(self):
        
        sitNum = len(self.sitAll['name'])
        self.ui.tableWidget_glob_station.setRowCount(sitNum)
        self.ui.tableWidget_glob_station.verticalHeader().setVisible(False)
        
        for i in range(sitNum):
            self.ui.tableWidget_glob_station.setItem(i, 0, QTableWidgetItem(str(i)))
            self.ui.tableWidget_glob_station.setItem(i, 1, QTableWidgetItem(self.sitAll['name'][i]))
            obsNum = len(self.sitAll['estEpoch'][i])
            self.ui.tableWidget_glob_station.setItem(i, 2, QTableWidgetItem(str(obsNum)))
            
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_glob_station.setItem(i, 3, item)
            
            if self.sitAll['nnrt'][i] == 1:
                item = QTableWidgetItem('Y')
            else:
                item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_glob_station.setItem(i, 4, item)
            
                
    def updateStaList(self, useSta):
        self.ui.listWidget_plot_station.blockSignals(True) 
        self.ui.listWidget_plot_station.clear()
        for i in range(len(useSta)):
            self.ui.listWidget_plot_station.addItem(self.scanInfo.stationAll[useSta[i]-1])
        
        self.ui.listWidget_plot_station.selectAll()
        self.ui.listWidget_plot_station.blockSignals(False)
        self.signal_plotStationInfo()
        
    def updateStaResult(self, useSta):
        self.ui.listWidget_plot_result.blockSignals(True)
        self.ui.listWidget_plot_result.clear()
        for i in range(len(useSta)):
            self.ui.listWidget_plot_result.addItem(self.scanInfo.stationAll[useSta[i]-1])
        self.ui.listWidget_plot_result.setCurrentRow(0)
        self.ui.listWidget_plot_result.blockSignals(False)
        self.signal_plotResult()
        
    def updateStaTab(self, useSta):
        self.ui.table_data_station.setRowCount(len(useSta))
        self.ui.table_data_station.verticalHeader().setVisible(False)

        offset = np.abs(self.scanInfo.Obs2Baseline[:,1] - self.scanInfo.Obs2Baseline[:,0])
        for i in range(len(useSta)):
            self.ui.table_data_station.setItem(i, 0, QTableWidgetItem(str(i)))
            self.ui.table_data_station.setItem(i, 1, QTableWidgetItem(self.scanInfo.stationAll[useSta[i]-1]))
            
            if self.scanInfo.clkBrk.brkFlag[useSta[i]-1] != 0:
                item = QTableWidgetItem(str(self.scanInfo.clkBrk.brkFlag[useSta[i]-1]))
            else:
                item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_station.setItem(i, 4, item)
            
            addR = np.abs(np.sum(self.scanInfo.Obs2Baseline-useSta[i], axis=1))
            temp = np.where((addR == offset) == True)
            item = QTableWidgetItem(str(len(temp[0])))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_station.setItem(i, 2, item)
            
            item = QTableWidgetItem(str(len(self.staObs.mjd[useSta[i]-1])))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_station.setItem(i,3,item)
            
            # the estmate station set
            item = QTableWidgetItem('Y')
            item.setTextAlignment(Qt.AlignCenter)
            if not self.scanInfo.stationAll[useSta[i]-1] in self.Param.Flags.xyz and self.Param.Flags.xyz[0] == 'YES':
                self.ui.table_data_station.setItem(i,7,item)
            
            # the estmate station set
            item = QTableWidgetItem('Y')
            item.setTextAlignment(Qt.AlignCenter)
            if self.scanInfo.stationAll[useSta[i]-1].strip() in self.nnrtSta:
                self.ui.table_data_station.setItem(i,8,item)
            
            index = [5,6]
            for j in index:
                item = QTableWidgetItem('')
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_data_station.setItem(i,j,item)
        
        # the reference clock set
        index = self.scanInfo.stationAll.index(self.scanInfo.refclk) + 1
        item = QTableWidgetItem('R')
        item.setTextAlignment(Qt.AlignCenter)
        self.ui.table_data_station.setItem(useSta.tolist().index(index), 5, item)        
    
    def updateSouTab(self):
        usePosit = np.where(self.scanInfo.Obs2Scan != 0)
        useObs = self.scanInfo.Obs2Source[usePosit[0]]
        useSou = np.unique(useObs)
        
        useInfo = []
        for isou in useSou:
            allNum = np.where((self.scanInfo.Obs2Source-isou) == 0)
            useNum = np.where((useObs-isou) == 0)
            useInfo.append([len(allNum[0]), len(useNum[0])])
        
        self.souICRF3Flag = []
        self.ui.table_data_source.setRowCount(len(useSou))
        self.ui.table_data_source.verticalHeader().setVisible(False)
        for i in range(len(useSou)):
            self.ui.table_data_source.setItem(i, 0, QTableWidgetItem(str(i)))
            self.ui.table_data_source.setItem(i, 1, QTableWidgetItem(self.scanInfo.sourceAll[useSou[i]-1]))

            item = QTableWidgetItem(str(useInfo[i][0]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_source.setItem(i, 2, item)
            
            item = QTableWidgetItem(str(useInfo[i][1]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.table_data_source.setItem(i,3,item)
            
            if self.sourceInfo.flag[useSou[i]-1]:
                item = QTableWidgetItem('ICRF3 defining')
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_data_source.setItem(i,4,item)
                
                item = QTableWidgetItem('Y')
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_data_source.setItem(i,7,item)
                
                self.souICRF3Flag.append(i)

    def closeEvent(self, event):
        if self.backend.isRunning():
            self.backend.quit()
        
        self.close()
            
def pickRmObs(obsScan, obsBl, posit, flag):
    '''
    obsScan : start from 1
    obsBl : start from 1

    '''
    out = np.zeros(len(obsScan), dtype=int)
    obsPosit = np.where(obsScan != 0)
    
    if flag == 0:
        subSta = obsBl[obsPosit] - posit
        staObsPosit = np.where(subSta[:,0]*subSta[:,1] == 0)
    
        out[obsPosit[0][staObsPosit]] += 1
    elif flag == 1:
        out[obsPosit[0][posit]] += 1
        
    return out
        
def read_initdir():
    dirPath = os.path.dirname(os.path.abspath(__file__))
    dirFile = os.path.join(dirPath,'directory.ini')
    name,dirpath = np.loadtxt(dirFile,comments='*',dtype='str',usecols=[0,1],unpack=True)

    return name.tolist(), dirpath.tolist()
            
        
if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication([]) 
    screen = app.primaryScreen()
    size = screen.size()
    width = size.width()
    height = size.height()
    
    myapp = MyForm() 
    myapp.show() 
    myapp.resize(int(width*0.7), int(height*0.8))
    sys.exit(app.exec_()) 
