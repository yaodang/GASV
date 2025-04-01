# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Figure.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_GASV(object):
    def setupUi(self, GASV):
        if not GASV.objectName():
            GASV.setObjectName(u"GASV")
        GASV.setEnabled(True)
        GASV.resize(1447, 992)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GASV.sizePolicy().hasHeightForWidth())
        GASV.setSizePolicy(sizePolicy)
        GASV.setMinimumSize(QSize(1400, 900))
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        GASV.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/icons/swallow.png", QSize(), QIcon.Normal, QIcon.Off)
        GASV.setWindowIcon(icon)
        GASV.setWindowOpacity(1.000000000000000)
        GASV.setLayoutDirection(Qt.LeftToRight)
        GASV.setIconSize(QSize(24, 24))
        self.menu_file_welcome = QAction(GASV)
        self.menu_file_welcome.setObjectName(u"menu_file_welcome")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/software.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_file_welcome.setIcon(icon1)
        font1 = QFont()
        font1.setFamily(u"Times New Roman")
        font1.setPointSize(12)
        self.menu_file_welcome.setFont(font1)
        self.menu_plot_residual = QAction(GASV)
        self.menu_plot_residual.setObjectName(u"menu_plot_residual")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/residual.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_plot_residual.setIcon(icon2)
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        self.menu_plot_residual.setFont(font2)
        self.menu_plot_station = QAction(GASV)
        self.menu_plot_station.setObjectName(u"menu_plot_station")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/antenna.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_plot_station.setIcon(icon3)
        self.menu_plot_station.setFont(font2)
        self.menu_plot_result = QAction(GASV)
        self.menu_plot_result.setObjectName(u"menu_plot_result")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/result.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_plot_result.setIcon(icon4)
        self.menu_plot_result.setFont(font2)
        self.menu_est_clktrop = QAction(GASV)
        self.menu_est_clktrop.setObjectName(u"menu_est_clktrop")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/clock.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_est_clktrop.setIcon(icon5)
        self.menu_est_clktrop.setFont(font2)
        self.menu_est_EOP = QAction(GASV)
        self.menu_est_EOP.setObjectName(u"menu_est_EOP")
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/earth.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_est_EOP.setIcon(icon6)
        self.menu_est_EOP.setFont(font2)
        self.menu_data_Station = QAction(GASV)
        self.menu_data_Station.setObjectName(u"menu_data_Station")
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/station.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_data_Station.setIcon(icon7)
        self.menu_data_Station.setFont(font2)
        self.menu_data_Baseline = QAction(GASV)
        self.menu_data_Baseline.setObjectName(u"menu_data_Baseline")
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/baseline.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_data_Baseline.setIcon(icon8)
        self.menu_data_Baseline.setFont(font2)
        self.menu_data_Source = QAction(GASV)
        self.menu_data_Source.setObjectName(u"menu_data_Source")
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/source.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_data_Source.setIcon(icon9)
        self.menu_data_Source.setFont(font2)
        self.menu_file_preference = QAction(GASV)
        self.menu_file_preference.setObjectName(u"menu_file_preference")
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/FileImport.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_file_preference.setIcon(icon10)
        self.menu_file_preference.setFont(font2)
        self.menu_file_input = QAction(GASV)
        self.menu_file_input.setObjectName(u"menu_file_input")
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/FileOpen.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_file_input.setIcon(icon11)
        self.menu_file_input.setFont(font1)
        self.menu_file_exit = QAction(GASV)
        self.menu_file_exit.setObjectName(u"menu_file_exit")
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/exit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_file_exit.setIcon(icon12)
        self.menu_file_exit.setFont(font2)
        self.menu_param_basic = QAction(GASV)
        self.menu_param_basic.setObjectName(u"menu_param_basic")
        icon13 = QIcon()
        icon13.addFile(u":/icons/icons/setting.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_param_basic.setIcon(icon13)
        self.menu_param_basic.setFont(font1)
        self.menu_file_datadownload = QAction(GASV)
        self.menu_file_datadownload.setObjectName(u"menu_file_datadownload")
        icon14 = QIcon()
        icon14.addFile(u":/icons/icons/database.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_file_datadownload.setIcon(icon14)
        self.menu_glob_setup = QAction(GASV)
        self.menu_glob_setup.setObjectName(u"menu_glob_setup")
        self.menu_glob_setup.setIcon(icon13)
        self.menu_glob_setup.setFont(font1)
        self.menu_glob_station = QAction(GASV)
        self.menu_glob_station.setObjectName(u"menu_glob_station")
        self.menu_glob_station.setIcon(icon7)
        self.menu_glob_station.setFont(font1)
        self.menu_glob_source = QAction(GASV)
        self.menu_glob_source.setObjectName(u"menu_glob_source")
        self.menu_glob_source.setIcon(icon9)
        self.menu_glob_source.setFont(font1)
        self.actionLocation = QAction(GASV)
        self.actionLocation.setObjectName(u"actionLocation")
        self.actionStation = QAction(GASV)
        self.actionStation.setObjectName(u"actionStation")
        self.actionSource = QAction(GASV)
        self.actionSource.setObjectName(u"actionSource")
        self.menu_plot_glob = QAction(GASV)
        self.menu_plot_glob.setObjectName(u"menu_plot_glob")
        icon15 = QIcon()
        icon15.addFile(u":/icons/icons/glob.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menu_plot_glob.setIcon(icon15)
        self.menu_plot_glob.setFont(font2)
        self.menu_file_dblist = QAction(GASV)
        self.menu_file_dblist.setObjectName(u"menu_file_dblist")
        self.menu_file_dblist.setIcon(icon14)
        self.menu_file_dblist.setFont(font1)
        self.menu_param_exclude = QAction(GASV)
        self.menu_param_exclude.setObjectName(u"menu_param_exclude")
        self.centralwidget = QWidget(GASV)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QSize(0, 400))
        self.stackedWidget.setFont(font)
        self.stackedWidget.setAcceptDrops(False)
        self.stackedWidget.setFrameShadow(QFrame.Plain)
        self.page_file_welcome = QWidget()
        self.page_file_welcome.setObjectName(u"page_file_welcome")
        self.verticalLayout_5 = QVBoxLayout(self.page_file_welcome)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.page_file_welcome)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setFamily(u"Times New Roman")
        font3.setPointSize(20)
        font3.setBold(True)
        font3.setItalic(True)
        font3.setWeight(75)
        self.label.setFont(font3)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_15)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_37 = QLabel(self.page_file_welcome)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMaximumSize(QSize(100, 16777215))
        font4 = QFont()
        font4.setFamily(u"Times New Roman")
        font4.setPointSize(13)
        font4.setBold(True)
        font4.setWeight(75)
        self.label_37.setFont(font4)

        self.verticalLayout_4.addWidget(self.label_37)

        self.label_iers = QLabel(self.page_file_welcome)
        self.label_iers.setObjectName(u"label_iers")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_iers.sizePolicy().hasHeightForWidth())
        self.label_iers.setSizePolicy(sizePolicy1)
        self.label_iers.setMinimumSize(QSize(60, 0))
        self.label_iers.setMaximumSize(QSize(50, 16777215))
        self.label_iers.setFont(font4)

        self.verticalLayout_4.addWidget(self.label_iers)

        self.label_ivs = QLabel(self.page_file_welcome)
        self.label_ivs.setObjectName(u"label_ivs")
        sizePolicy1.setHeightForWidth(self.label_ivs.sizePolicy().hasHeightForWidth())
        self.label_ivs.setSizePolicy(sizePolicy1)
        self.label_ivs.setMaximumSize(QSize(60, 16777215))
        self.label_ivs.setFont(font4)

        self.verticalLayout_4.addWidget(self.label_ivs)

        self.label_itrf = QLabel(self.page_file_welcome)
        self.label_itrf.setObjectName(u"label_itrf")
        sizePolicy1.setHeightForWidth(self.label_itrf.sizePolicy().hasHeightForWidth())
        self.label_itrf.setSizePolicy(sizePolicy1)
        self.label_itrf.setMaximumSize(QSize(60, 16777215))
        self.label_itrf.setFont(font4)

        self.verticalLayout_4.addWidget(self.label_itrf)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.textBrowser = QTextBrowser(self.page_file_welcome)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_5.addWidget(self.textBrowser)

        self.stackedWidget.addWidget(self.page_file_welcome)
        self.page_file_preference = QWidget()
        self.page_file_preference.setObjectName(u"page_file_preference")
        self.verticalLayout_10 = QVBoxLayout(self.page_file_preference)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox_3 = QGroupBox(self.page_file_preference)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setFont(font)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_18 = QLabel(self.groupBox_3)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_9.addWidget(self.label_18)

        self.lineEdit_path_vgosDb = QLineEdit(self.groupBox_3)
        self.lineEdit_path_vgosDb.setObjectName(u"lineEdit_path_vgosDb")

        self.horizontalLayout_9.addWidget(self.lineEdit_path_vgosDb)

        self.comboBox_dataType = QComboBox(self.groupBox_3)
        self.comboBox_dataType.addItem("")
        self.comboBox_dataType.addItem("")
        self.comboBox_dataType.addItem("")
        self.comboBox_dataType.setObjectName(u"comboBox_dataType")

        self.horizontalLayout_9.addWidget(self.comboBox_dataType)

        self.pushButton_browse_vgosdb = QPushButton(self.groupBox_3)
        self.pushButton_browse_vgosdb.setObjectName(u"pushButton_browse_vgosdb")
        icon16 = QIcon()
        icon16.addFile(u":/icons/icons/browse.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_browse_vgosdb.setIcon(icon16)
        self.pushButton_browse_vgosdb.setIconSize(QSize(20, 20))

        self.horizontalLayout_9.addWidget(self.pushButton_browse_vgosdb)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_17 = QLabel(self.groupBox_3)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_8.addWidget(self.label_17)

        self.lineEdit_path_master = QLineEdit(self.groupBox_3)
        self.lineEdit_path_master.setObjectName(u"lineEdit_path_master")

        self.horizontalLayout_8.addWidget(self.lineEdit_path_master)

        self.pushButton_browse_master = QPushButton(self.groupBox_3)
        self.pushButton_browse_master.setObjectName(u"pushButton_browse_master")
        self.pushButton_browse_master.setIcon(icon16)
        self.pushButton_browse_master.setIconSize(QSize(20, 20))

        self.horizontalLayout_8.addWidget(self.pushButton_browse_master)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_19 = QLabel(self.groupBox_3)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_10.addWidget(self.label_19)

        self.lineEdit_path_Apriori = QLineEdit(self.groupBox_3)
        self.lineEdit_path_Apriori.setObjectName(u"lineEdit_path_Apriori")

        self.horizontalLayout_10.addWidget(self.lineEdit_path_Apriori)

        self.pushButton_browse_apriori = QPushButton(self.groupBox_3)
        self.pushButton_browse_apriori.setObjectName(u"pushButton_browse_apriori")
        self.pushButton_browse_apriori.setIcon(icon16)
        self.pushButton_browse_apriori.setIconSize(QSize(20, 20))

        self.horizontalLayout_10.addWidget(self.pushButton_browse_apriori)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_3.setContentsMargins(100, -1, 0, -1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_39 = QLabel(self.groupBox_3)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_11.addWidget(self.label_39)

        self.lineEdit_param_Station = QLineEdit(self.groupBox_3)
        self.lineEdit_param_Station.setObjectName(u"lineEdit_param_Station")

        self.horizontalLayout_11.addWidget(self.lineEdit_param_Station)

        self.pushButton_browse_station = QPushButton(self.groupBox_3)
        self.pushButton_browse_station.setObjectName(u"pushButton_browse_station")
        self.pushButton_browse_station.setIcon(icon16)
        self.pushButton_browse_station.setIconSize(QSize(20, 20))

        self.horizontalLayout_11.addWidget(self.pushButton_browse_station)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_40 = QLabel(self.groupBox_3)
        self.label_40.setObjectName(u"label_40")

        self.horizontalLayout_12.addWidget(self.label_40)

        self.lineEdit_param_Source = QLineEdit(self.groupBox_3)
        self.lineEdit_param_Source.setObjectName(u"lineEdit_param_Source")

        self.horizontalLayout_12.addWidget(self.lineEdit_param_Source)

        self.pushButton_browse_source = QPushButton(self.groupBox_3)
        self.pushButton_browse_source.setObjectName(u"pushButton_browse_source")
        self.pushButton_browse_source.setIcon(icon16)
        self.pushButton_browse_source.setIconSize(QSize(20, 20))

        self.horizontalLayout_12.addWidget(self.pushButton_browse_source)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_41 = QLabel(self.groupBox_3)
        self.label_41.setObjectName(u"label_41")

        self.horizontalLayout_13.addWidget(self.label_41)

        self.lineEdit_param_EOP = QLineEdit(self.groupBox_3)
        self.lineEdit_param_EOP.setObjectName(u"lineEdit_param_EOP")

        self.horizontalLayout_13.addWidget(self.lineEdit_param_EOP)

        self.pushButton_browse_eop = QPushButton(self.groupBox_3)
        self.pushButton_browse_eop.setObjectName(u"pushButton_browse_eop")
        self.pushButton_browse_eop.setIcon(icon16)
        self.pushButton_browse_eop.setIconSize(QSize(20, 20))

        self.horizontalLayout_13.addWidget(self.pushButton_browse_eop)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_42 = QLabel(self.groupBox_3)
        self.label_42.setObjectName(u"label_42")

        self.horizontalLayout_14.addWidget(self.label_42)

        self.lineEdit_param_EPHEM = QLineEdit(self.groupBox_3)
        self.lineEdit_param_EPHEM.setObjectName(u"lineEdit_param_EPHEM")

        self.horizontalLayout_14.addWidget(self.lineEdit_param_EPHEM)

        self.pushButton_browse_ephem = QPushButton(self.groupBox_3)
        self.pushButton_browse_ephem.setObjectName(u"pushButton_browse_ephem")
        self.pushButton_browse_ephem.setIcon(icon16)
        self.pushButton_browse_ephem.setIconSize(QSize(20, 20))

        self.horizontalLayout_14.addWidget(self.pushButton_browse_ephem)


        self.verticalLayout_3.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_15.addLayout(self.verticalLayout_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_15)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)

        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.horizontalSpacer_13 = QSpacerItem(98, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_56.addItem(self.horizontalSpacer_13)

        self.pushButton_param_questions = QPushButton(self.groupBox_3)
        self.pushButton_param_questions.setObjectName(u"pushButton_param_questions")
        icon17 = QIcon()
        icon17.addFile(u":/icons/icons/question.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_param_questions.setIcon(icon17)
        self.pushButton_param_questions.setIconSize(QSize(20, 20))

        self.horizontalLayout_56.addWidget(self.pushButton_param_questions)


        self.verticalLayout_9.addLayout(self.horizontalLayout_56)


        self.verticalLayout_10.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.page_file_preference)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setCheckable(False)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.label_22 = QLabel(self.groupBox_4)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_4.addWidget(self.label_22)

        self.lineEdit_path_Residual = QLineEdit(self.groupBox_4)
        self.lineEdit_path_Residual.setObjectName(u"lineEdit_path_Residual")

        self.horizontalLayout_4.addWidget(self.lineEdit_path_Residual)

        self.pushButton_browse_residual = QPushButton(self.groupBox_4)
        self.pushButton_browse_residual.setObjectName(u"pushButton_browse_residual")
        self.pushButton_browse_residual.setIcon(icon16)
        self.pushButton_browse_residual.setIconSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.pushButton_browse_residual)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.label_23 = QLabel(self.groupBox_4)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_5.addWidget(self.label_23)

        self.lineEdit_path_Report = QLineEdit(self.groupBox_4)
        self.lineEdit_path_Report.setObjectName(u"lineEdit_path_Report")

        self.horizontalLayout_5.addWidget(self.lineEdit_path_Report)

        self.pushButton_browse_report = QPushButton(self.groupBox_4)
        self.pushButton_browse_report.setObjectName(u"pushButton_browse_report")
        self.pushButton_browse_report.setIcon(icon16)
        self.pushButton_browse_report.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.pushButton_browse_report)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.label_24 = QLabel(self.groupBox_4)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_6.addWidget(self.label_24)

        self.lineEdit_path_SNX = QLineEdit(self.groupBox_4)
        self.lineEdit_path_SNX.setObjectName(u"lineEdit_path_SNX")

        self.horizontalLayout_6.addWidget(self.lineEdit_path_SNX)

        self.pushButton_browse_snx = QPushButton(self.groupBox_4)
        self.pushButton_browse_snx.setObjectName(u"pushButton_browse_snx")
        self.pushButton_browse_snx.setIcon(icon16)
        self.pushButton_browse_snx.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.pushButton_browse_snx)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, 0, -1)
        self.label_25 = QLabel(self.groupBox_4)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_7.addWidget(self.label_25)

        self.lineEdit_path_EOPO = QLineEdit(self.groupBox_4)
        self.lineEdit_path_EOPO.setObjectName(u"lineEdit_path_EOPO")

        self.horizontalLayout_7.addWidget(self.lineEdit_path_EOPO)

        self.pushButton_browse_eopo = QPushButton(self.groupBox_4)
        self.pushButton_browse_eopo.setObjectName(u"pushButton_browse_eopo")
        self.pushButton_browse_eopo.setIcon(icon16)
        self.pushButton_browse_eopo.setIconSize(QSize(20, 20))

        self.horizontalLayout_7.addWidget(self.pushButton_browse_eopo)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_64 = QHBoxLayout()
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_64.addWidget(self.label_6)

        self.lineEdit_path_arcpath = QLineEdit(self.groupBox_4)
        self.lineEdit_path_arcpath.setObjectName(u"lineEdit_path_arcpath")

        self.horizontalLayout_64.addWidget(self.lineEdit_path_arcpath)

        self.pushButton_browse_arcpath = QPushButton(self.groupBox_4)
        self.pushButton_browse_arcpath.setObjectName(u"pushButton_browse_arcpath")
        self.pushButton_browse_arcpath.setIcon(icon16)
        self.pushButton_browse_arcpath.setIconSize(QSize(20, 20))

        self.horizontalLayout_64.addWidget(self.pushButton_browse_arcpath)


        self.verticalLayout_6.addLayout(self.horizontalLayout_64)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_61 = QLabel(self.groupBox_4)
        self.label_61.setObjectName(u"label_61")

        self.horizontalLayout_3.addWidget(self.label_61)

        self.lineEdit_param_ac = QLineEdit(self.groupBox_4)
        self.lineEdit_param_ac.setObjectName(u"lineEdit_param_ac")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_param_ac.sizePolicy().hasHeightForWidth())
        self.lineEdit_param_ac.setSizePolicy(sizePolicy2)
        self.lineEdit_param_ac.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_param_ac)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pushButton_file_save = QPushButton(self.groupBox_4)
        self.pushButton_file_save.setObjectName(u"pushButton_file_save")
        sizePolicy2.setHeightForWidth(self.pushButton_file_save.sizePolicy().hasHeightForWidth())
        self.pushButton_file_save.setSizePolicy(sizePolicy2)
        self.pushButton_file_save.setStyleSheet(u"")
        icon18 = QIcon()
        icon18.addFile(u":/icons/icons/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_file_save.setIcon(icon18)
        self.pushButton_file_save.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.pushButton_file_save)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)


        self.verticalLayout_10.addWidget(self.groupBox_4)

        self.verticalSpacer = QSpacerItem(20, 115, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page_file_preference)
        self.page_file_download = QWidget()
        self.page_file_download.setObjectName(u"page_file_download")
        self.horizontalLayout_19 = QHBoxLayout(self.page_file_download)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.groupBox_10 = QGroupBox(self.page_file_download)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.horizontalLayout_63 = QHBoxLayout(self.groupBox_10)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.verticalLayout_56 = QVBoxLayout()
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_2 = QLabel(self.groupBox_10)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_17.addWidget(self.label_2)

        self.lineEdit_file_startyear = QLineEdit(self.groupBox_10)
        self.lineEdit_file_startyear.setObjectName(u"lineEdit_file_startyear")
        sizePolicy.setHeightForWidth(self.lineEdit_file_startyear.sizePolicy().hasHeightForWidth())
        self.lineEdit_file_startyear.setSizePolicy(sizePolicy)
        self.lineEdit_file_startyear.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.lineEdit_file_startyear)


        self.horizontalLayout_61.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_5 = QLabel(self.groupBox_10)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_18.addWidget(self.label_5)

        self.lineEdit_file_stopyear = QLineEdit(self.groupBox_10)
        self.lineEdit_file_stopyear.setObjectName(u"lineEdit_file_stopyear")
        sizePolicy.setHeightForWidth(self.lineEdit_file_stopyear.sizePolicy().hasHeightForWidth())
        self.lineEdit_file_stopyear.setSizePolicy(sizePolicy)
        self.lineEdit_file_stopyear.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_18.addWidget(self.lineEdit_file_stopyear)


        self.horizontalLayout_61.addLayout(self.horizontalLayout_18)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_61.addItem(self.horizontalSpacer_14)

        self.pushButton_file_refresh = QPushButton(self.groupBox_10)
        self.pushButton_file_refresh.setObjectName(u"pushButton_file_refresh")
        icon19 = QIcon()
        icon19.addFile(u":/icons/icons/refresh.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_file_refresh.setIcon(icon19)
        self.pushButton_file_refresh.setIconSize(QSize(25, 25))

        self.horizontalLayout_61.addWidget(self.pushButton_file_refresh)

        self.pushButton_file_makearc = QPushButton(self.groupBox_10)
        self.pushButton_file_makearc.setObjectName(u"pushButton_file_makearc")
        sizePolicy1.setHeightForWidth(self.pushButton_file_makearc.sizePolicy().hasHeightForWidth())
        self.pushButton_file_makearc.setSizePolicy(sizePolicy1)
        icon20 = QIcon()
        icon20.addFile(u":/icons/icons/list.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_file_makearc.setIcon(icon20)
        self.pushButton_file_makearc.setIconSize(QSize(25, 25))

        self.horizontalLayout_61.addWidget(self.pushButton_file_makearc)


        self.verticalLayout_56.addLayout(self.horizontalLayout_61)

        self.tableWidget_session = QTableWidget(self.groupBox_10)
        if (self.tableWidget_session.columnCount() < 9):
            self.tableWidget_session.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem1.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        font5 = QFont()
        font5.setFamily(u"Abyssinica SIL")
        font5.setPointSize(12)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem2.setFont(font5);
        self.tableWidget_session.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem3.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font1);
        self.tableWidget_session.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.tableWidget_session.setObjectName(u"tableWidget_session")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tableWidget_session.sizePolicy().hasHeightForWidth())
        self.tableWidget_session.setSizePolicy(sizePolicy3)
        self.tableWidget_session.setMinimumSize(QSize(500, 0))
        self.tableWidget_session.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_session.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget_session.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_session.setTextElideMode(Qt.ElideRight)
        self.tableWidget_session.setSortingEnabled(True)
        self.tableWidget_session.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_session.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget_session.horizontalHeader().setProperty("showSortIndicator", True)

        self.verticalLayout_56.addWidget(self.tableWidget_session)


        self.horizontalLayout_63.addLayout(self.verticalLayout_56)

        self.verticalLayout_57 = QVBoxLayout()
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.verticalLayout_59 = QVBoxLayout()
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.horizontalLayout_58 = QHBoxLayout()
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.pushButton_file_typesub = QPushButton(self.groupBox_10)
        self.pushButton_file_typesub.setObjectName(u"pushButton_file_typesub")
        sizePolicy.setHeightForWidth(self.pushButton_file_typesub.sizePolicy().hasHeightForWidth())
        self.pushButton_file_typesub.setSizePolicy(sizePolicy)

        self.horizontalLayout_58.addWidget(self.pushButton_file_typesub)

        self.horizontalSpacer_31 = QSpacerItem(80, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_58.addItem(self.horizontalSpacer_31)

        self.pushButton_file_typeadd = QPushButton(self.groupBox_10)
        self.pushButton_file_typeadd.setObjectName(u"pushButton_file_typeadd")
        sizePolicy.setHeightForWidth(self.pushButton_file_typeadd.sizePolicy().hasHeightForWidth())
        self.pushButton_file_typeadd.setSizePolicy(sizePolicy)

        self.horizontalLayout_58.addWidget(self.pushButton_file_typeadd)


        self.verticalLayout_59.addLayout(self.horizontalLayout_58)

        self.listWidget_datatype = QListWidget(self.groupBox_10)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        QListWidgetItem(self.listWidget_datatype)
        self.listWidget_datatype.setObjectName(u"listWidget_datatype")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.listWidget_datatype.sizePolicy().hasHeightForWidth())
        self.listWidget_datatype.setSizePolicy(sizePolicy4)
        self.listWidget_datatype.setMinimumSize(QSize(0, 0))
        self.listWidget_datatype.setMaximumSize(QSize(16777215, 16777215))
        self.listWidget_datatype.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout_59.addWidget(self.listWidget_datatype)

        self.textBrowser_file_obs = QTextBrowser(self.groupBox_10)
        self.textBrowser_file_obs.setObjectName(u"textBrowser_file_obs")
        sizePolicy4.setHeightForWidth(self.textBrowser_file_obs.sizePolicy().hasHeightForWidth())
        self.textBrowser_file_obs.setSizePolicy(sizePolicy4)
        self.textBrowser_file_obs.setMinimumSize(QSize(0, 0))
        self.textBrowser_file_obs.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_59.addWidget(self.textBrowser_file_obs)


        self.verticalLayout_57.addLayout(self.verticalLayout_59)


        self.horizontalLayout_63.addLayout(self.verticalLayout_57)


        self.horizontalLayout_19.addWidget(self.groupBox_10)

        self.stackedWidget.addWidget(self.page_file_download)
        self.page_param_basic = QWidget()
        self.page_param_basic.setObjectName(u"page_param_basic")
        self.verticalLayout_12 = QVBoxLayout(self.page_param_basic)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.textBrowser_information = QTextBrowser(self.page_param_basic)
        self.textBrowser_information.setObjectName(u"textBrowser_information")
        sizePolicy4.setHeightForWidth(self.textBrowser_information.sizePolicy().hasHeightForWidth())
        self.textBrowser_information.setSizePolicy(sizePolicy4)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        brush2 = QBrush(QColor(127, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        brush3 = QBrush(QColor(170, 170, 170, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        brush4 = QBrush(QColor(255, 255, 220, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush5)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        brush6 = QBrush(QColor(0, 0, 0, 128))
        brush6.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush6)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        brush7 = QBrush(QColor(0, 0, 0, 128))
        brush7.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush7)
#endif
        self.textBrowser_information.setPalette(palette)
        self.textBrowser_information.setFont(font)
        self.textBrowser_information.setReadOnly(True)
        self.textBrowser_information.setAcceptRichText(True)
        self.textBrowser_information.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout_12.addWidget(self.textBrowser_information)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.groupBox_staCorrect = QGroupBox(self.page_param_basic)
        self.groupBox_staCorrect.setObjectName(u"groupBox_staCorrect")
        self.groupBox_staCorrect.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_staCorrect)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBox_staCor_solid = QCheckBox(self.groupBox_staCorrect)
        self.checkBox_staCor_solid.setObjectName(u"checkBox_staCor_solid")
        self.checkBox_staCor_solid.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_staCor_solid)

        self.checkBox_staCor_ocean = QCheckBox(self.groupBox_staCorrect)
        self.checkBox_staCor_ocean.setObjectName(u"checkBox_staCor_ocean")
        self.checkBox_staCor_ocean.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_staCor_ocean)

        self.checkBox_staCor_pole = QCheckBox(self.groupBox_staCorrect)
        self.checkBox_staCor_pole.setObjectName(u"checkBox_staCor_pole")
        self.checkBox_staCor_pole.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_staCor_pole)

        self.checkBox_staCor_oceanpole = QCheckBox(self.groupBox_staCorrect)
        self.checkBox_staCor_oceanpole.setObjectName(u"checkBox_staCor_oceanpole")
        self.checkBox_staCor_oceanpole.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_staCor_oceanpole)

        self.checkBox = QCheckBox(self.groupBox_staCorrect)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox)


        self.horizontalLayout_16.addWidget(self.groupBox_staCorrect)

        self.groupBox_eophf = QGroupBox(self.page_param_basic)
        self.groupBox_eophf.setObjectName(u"groupBox_eophf")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_eophf.sizePolicy().hasHeightForWidth())
        self.groupBox_eophf.setSizePolicy(sizePolicy5)
        self.groupBox_eophf.setMinimumSize(QSize(150, 0))
        self.groupBox_eophf.setFont(font)
        self.checkBox_setup_hfeop = QCheckBox(self.groupBox_eophf)
        self.checkBox_setup_hfeop.setObjectName(u"checkBox_setup_hfeop")
        self.checkBox_setup_hfeop.setGeometry(QRect(12, 41, 70, 22))
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.checkBox_setup_hfeop.sizePolicy().hasHeightForWidth())
        self.checkBox_setup_hfeop.setSizePolicy(sizePolicy6)
        self.checkBox_setup_hfeop.setMinimumSize(QSize(70, 0))
        self.checkBox_setup_hfeop.setChecked(True)
        self.layoutWidget = QWidget(self.groupBox_eophf)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(50, 80, 91, 81))
        self.verticalLayout_13 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.radioButton_eophf_desai = QRadioButton(self.layoutWidget)
        self.radioButton_eophf_desai.setObjectName(u"radioButton_eophf_desai")
        sizePolicy.setHeightForWidth(self.radioButton_eophf_desai.sizePolicy().hasHeightForWidth())
        self.radioButton_eophf_desai.setSizePolicy(sizePolicy)
        self.radioButton_eophf_desai.setMinimumSize(QSize(70, 0))
        self.radioButton_eophf_desai.setChecked(True)

        self.verticalLayout_13.addWidget(self.radioButton_eophf_desai)

        self.radioButton_eophf_iers = QRadioButton(self.layoutWidget)
        self.radioButton_eophf_iers.setObjectName(u"radioButton_eophf_iers")
        sizePolicy6.setHeightForWidth(self.radioButton_eophf_iers.sizePolicy().hasHeightForWidth())
        self.radioButton_eophf_iers.setSizePolicy(sizePolicy6)
        self.radioButton_eophf_iers.setMinimumSize(QSize(70, 0))

        self.verticalLayout_13.addWidget(self.radioButton_eophf_iers)


        self.horizontalLayout_16.addWidget(self.groupBox_eophf)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_28 = QLabel(self.page_param_basic)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_28)

        self.spinBox_param_quality = QSpinBox(self.page_param_basic)
        self.spinBox_param_quality.setObjectName(u"spinBox_param_quality")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.spinBox_param_quality.sizePolicy().hasHeightForWidth())
        self.spinBox_param_quality.setSizePolicy(sizePolicy7)
        self.spinBox_param_quality.setMinimumSize(QSize(60, 0))
        self.spinBox_param_quality.setFont(font)
        self.spinBox_param_quality.setAlignment(Qt.AlignCenter)
        self.spinBox_param_quality.setMaximum(9)
        self.spinBox_param_quality.setValue(5)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spinBox_param_quality)

        self.radioButton_param_outlier = QRadioButton(self.page_param_basic)
        self.radioButton_param_outlier.setObjectName(u"radioButton_param_outlier")
        self.radioButton_param_outlier.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.radioButton_param_outlier)

        self.lineEdit_param_outlier = QLineEdit(self.page_param_basic)
        self.lineEdit_param_outlier.setObjectName(u"lineEdit_param_outlier")
        sizePolicy2.setHeightForWidth(self.lineEdit_param_outlier.sizePolicy().hasHeightForWidth())
        self.lineEdit_param_outlier.setSizePolicy(sizePolicy2)
        self.lineEdit_param_outlier.setMinimumSize(QSize(60, 0))
        self.lineEdit_param_outlier.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_param_outlier.setFont(font)
        self.lineEdit_param_outlier.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_param_outlier)

        self.label_3 = QLabel(self.page_param_basic)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.comboBox_setup_mpf = QComboBox(self.page_param_basic)
        self.comboBox_setup_mpf.addItem("")
        self.comboBox_setup_mpf.addItem("")
        self.comboBox_setup_mpf.setObjectName(u"comboBox_setup_mpf")
        sizePolicy7.setHeightForWidth(self.comboBox_setup_mpf.sizePolicy().hasHeightForWidth())
        self.comboBox_setup_mpf.setSizePolicy(sizePolicy7)
        self.comboBox_setup_mpf.setMinimumSize(QSize(60, 0))
        self.comboBox_setup_mpf.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_setup_mpf)


        self.horizontalLayout_16.addLayout(self.formLayout)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_6)


        self.verticalLayout_12.addLayout(self.horizontalLayout_16)

        self.stackedWidget.addWidget(self.page_param_basic)
        self.page_data_station = QWidget()
        self.page_data_station.setObjectName(u"page_data_station")
        self.verticalLayout_16 = QVBoxLayout(self.page_data_station)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.table_data_station = QTableWidget(self.page_data_station)
        if (self.table_data_station.columnCount() < 9):
            self.table_data_station.setColumnCount(9)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.table_data_station.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(6, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(7, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.table_data_station.setHorizontalHeaderItem(8, __qtablewidgetitem17)
        self.table_data_station.setObjectName(u"table_data_station")
        self.table_data_station.setFont(font)
        self.table_data_station.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.table_data_station.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_data_station.setShowGrid(True)
        self.table_data_station.verticalHeader().setVisible(False)

        self.verticalLayout_16.addWidget(self.table_data_station)

        self.stackedWidget.addWidget(self.page_data_station)
        self.page_data_baseline = QWidget()
        self.page_data_baseline.setObjectName(u"page_data_baseline")
        self.verticalLayout_17 = QVBoxLayout(self.page_data_baseline)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.table_data_bl = QTableWidget(self.page_data_baseline)
        if (self.table_data_bl.columnCount() < 6):
            self.table_data_bl.setColumnCount(6)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.table_data_bl.setHorizontalHeaderItem(0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.table_data_bl.setHorizontalHeaderItem(1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.table_data_bl.setHorizontalHeaderItem(2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.table_data_bl.setHorizontalHeaderItem(3, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.table_data_bl.setHorizontalHeaderItem(4, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.table_data_bl.setHorizontalHeaderItem(5, __qtablewidgetitem23)
        self.table_data_bl.setObjectName(u"table_data_bl")
        font6 = QFont()
        font6.setFamily(u"Times New Roman")
        font6.setPointSize(12)
        font6.setBold(False)
        font6.setUnderline(False)
        font6.setWeight(50)
        self.table_data_bl.setFont(font6)
        self.table_data_bl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_data_bl.setShowGrid(True)
        self.table_data_bl.setColumnCount(6)

        self.verticalLayout_17.addWidget(self.table_data_bl)

        self.stackedWidget.addWidget(self.page_data_baseline)
        self.page_data_source = QWidget()
        self.page_data_source.setObjectName(u"page_data_source")
        self.verticalLayout_18 = QVBoxLayout(self.page_data_source)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.table_data_source = QTableWidget(self.page_data_source)
        if (self.table_data_source.columnCount() < 8):
            self.table_data_source.setColumnCount(8)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(2, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(3, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(4, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(5, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(6, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.table_data_source.setHorizontalHeaderItem(7, __qtablewidgetitem31)
        self.table_data_source.setObjectName(u"table_data_source")
        self.table_data_source.setFont(font)
        self.table_data_source.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_data_source.setShowGrid(True)

        self.verticalLayout_18.addWidget(self.table_data_source)

        self.stackedWidget.addWidget(self.page_data_source)
        self.page_est_clktrp = QWidget()
        self.page_est_clktrp.setObjectName(u"page_est_clktrp")
        self.verticalLayout_21 = QVBoxLayout(self.page_est_clktrp)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.groupBox_6 = QGroupBox(self.page_est_clktrp)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy5.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy5)
        self.groupBox_6.setFont(font)
        self.layoutWidget1 = QWidget(self.groupBox_6)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 40, 1071, 51))
        self.horizontalLayout_35 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.checkBox_est_clk = QCheckBox(self.layoutWidget1)
        self.checkBox_est_clk.setObjectName(u"checkBox_est_clk")

        self.horizontalLayout_35.addWidget(self.checkBox_est_clk)

        self.horizontalSpacer_38 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_38)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.lineEdit_clk_interval = QLineEdit(self.layoutWidget1)
        self.lineEdit_clk_interval.setObjectName(u"lineEdit_clk_interval")
        self.lineEdit_clk_interval.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_22.addWidget(self.lineEdit_clk_interval)

        self.label_20 = QLabel(self.layoutWidget1)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_22.addWidget(self.label_20)


        self.horizontalLayout_35.addLayout(self.horizontalLayout_22)

        self.horizontalSpacer_39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_39)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.lineEdit_clk_constr = QLineEdit(self.layoutWidget1)
        self.lineEdit_clk_constr.setObjectName(u"lineEdit_clk_constr")
        self.lineEdit_clk_constr.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_21.addWidget(self.lineEdit_clk_constr)

        self.label_21 = QLabel(self.layoutWidget1)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_21.addWidget(self.label_21)


        self.horizontalLayout_35.addLayout(self.horizontalLayout_21)

        self.horizontalSpacer_37 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_37)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_26 = QLabel(self.layoutWidget1)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_20.addWidget(self.label_26)

        self.comboBox_clk_order = QComboBox(self.layoutWidget1)
        self.comboBox_clk_order.addItem("")
        self.comboBox_clk_order.addItem("")
        self.comboBox_clk_order.addItem("")
        self.comboBox_clk_order.addItem("")
        self.comboBox_clk_order.addItem("")
        self.comboBox_clk_order.addItem("")
        self.comboBox_clk_order.setObjectName(u"comboBox_clk_order")

        self.horizontalLayout_20.addWidget(self.comboBox_clk_order)


        self.horizontalLayout_35.addLayout(self.horizontalLayout_20)


        self.verticalLayout_21.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.page_est_clktrp)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy5.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy5)
        self.groupBox_7.setFont(font)
        self.horizontalLayout_23 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.checkBox_est_wet = QCheckBox(self.groupBox_7)
        self.checkBox_est_wet.setObjectName(u"checkBox_est_wet")

        self.gridLayout_4.addWidget(self.checkBox_est_wet, 0, 0, 1, 1)

        self.lineEdit_wet_interval = QLineEdit(self.groupBox_7)
        self.lineEdit_wet_interval.setObjectName(u"lineEdit_wet_interval")
        self.lineEdit_wet_interval.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_wet_interval, 0, 1, 1, 1)

        self.label_27 = QLabel(self.groupBox_7)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_4.addWidget(self.label_27, 0, 2, 1, 1)

        self.lineEdit_wet_constr = QLineEdit(self.groupBox_7)
        self.lineEdit_wet_constr.setObjectName(u"lineEdit_wet_constr")
        self.lineEdit_wet_constr.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_wet_constr, 0, 4, 1, 1)

        self.label_31 = QLabel(self.groupBox_7)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_4.addWidget(self.label_31, 0, 5, 1, 1)

        self.checkBox_est_grad = QCheckBox(self.groupBox_7)
        self.checkBox_est_grad.setObjectName(u"checkBox_est_grad")

        self.gridLayout_4.addWidget(self.checkBox_est_grad, 1, 0, 1, 1)

        self.lineEdit_grad_interval = QLineEdit(self.groupBox_7)
        self.lineEdit_grad_interval.setObjectName(u"lineEdit_grad_interval")
        self.lineEdit_grad_interval.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_grad_interval, 1, 1, 1, 1)

        self.label_32 = QLabel(self.groupBox_7)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_4.addWidget(self.label_32, 1, 2, 1, 1)

        self.label_10 = QLabel(self.groupBox_7)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 1, 3, 1, 1)

        self.lineEdit_grad_relconstr = QLineEdit(self.groupBox_7)
        self.lineEdit_grad_relconstr.setObjectName(u"lineEdit_grad_relconstr")
        self.lineEdit_grad_relconstr.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_grad_relconstr, 1, 4, 1, 1)

        self.label_33 = QLabel(self.groupBox_7)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_4.addWidget(self.label_33, 1, 5, 1, 1)

        self.label_16 = QLabel(self.groupBox_7)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_4.addWidget(self.label_16, 2, 3, 1, 1)

        self.lineEdit_grad_absconstr = QLineEdit(self.groupBox_7)
        self.lineEdit_grad_absconstr.setObjectName(u"lineEdit_grad_absconstr")
        self.lineEdit_grad_absconstr.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_grad_absconstr, 2, 4, 1, 1)

        self.label_34 = QLabel(self.groupBox_7)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_4.addWidget(self.label_34, 2, 5, 1, 1)


        self.horizontalLayout_23.addLayout(self.gridLayout_4)

        self.horizontalSpacer_10 = QSpacerItem(300, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_10)


        self.verticalLayout_21.addWidget(self.groupBox_7)

        self.stackedWidget.addWidget(self.page_est_clktrp)
        self.page_est_eoprf = QWidget()
        self.page_est_eoprf.setObjectName(u"page_est_eoprf")
        self.verticalLayout_49 = QVBoxLayout(self.page_est_eoprf)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.groupBox_15 = QGroupBox(self.page_est_eoprf)
        self.groupBox_15.setObjectName(u"groupBox_15")
        sizePolicy5.setHeightForWidth(self.groupBox_15.sizePolicy().hasHeightForWidth())
        self.groupBox_15.setSizePolicy(sizePolicy5)
        self.horizontalLayout_54 = QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.groupBox_mode = QGroupBox(self.groupBox_15)
        self.groupBox_mode.setObjectName(u"groupBox_mode")
        self.verticalLayout_38 = QVBoxLayout(self.groupBox_mode)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.radioButton_est_eop_poly = QRadioButton(self.groupBox_mode)
        self.radioButton_est_eop_poly.setObjectName(u"radioButton_est_eop_poly")
        self.radioButton_est_eop_poly.setChecked(True)

        self.horizontalLayout_28.addWidget(self.radioButton_est_eop_poly)

        self.radioButton_est_eop_cpwl = QRadioButton(self.groupBox_mode)
        self.radioButton_est_eop_cpwl.setObjectName(u"radioButton_est_eop_cpwl")
        self.radioButton_est_eop_cpwl.setChecked(False)

        self.horizontalLayout_28.addWidget(self.radioButton_est_eop_cpwl)


        self.verticalLayout_38.addLayout(self.horizontalLayout_28)


        self.horizontalLayout_42.addWidget(self.groupBox_mode)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_42.addItem(self.horizontalSpacer_12)

        self.groupBox_refTime = QGroupBox(self.groupBox_15)
        self.groupBox_refTime.setObjectName(u"groupBox_refTime")
        self.groupBox_refTime.setEnabled(True)
        self.verticalLayout_37 = QVBoxLayout(self.groupBox_refTime)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.radioButton_est_reftime_MIDDEL = QRadioButton(self.groupBox_refTime)
        self.radioButton_est_reftime_MIDDEL.setObjectName(u"radioButton_est_reftime_MIDDEL")
        self.radioButton_est_reftime_MIDDEL.setChecked(True)

        self.horizontalLayout_29.addWidget(self.radioButton_est_reftime_MIDDEL)

        self.radioButton_est_reftime_MIDNIGHT = QRadioButton(self.groupBox_refTime)
        self.radioButton_est_reftime_MIDNIGHT.setObjectName(u"radioButton_est_reftime_MIDNIGHT")

        self.horizontalLayout_29.addWidget(self.radioButton_est_reftime_MIDNIGHT)

        self.radioButton_est_reftime_NOON = QRadioButton(self.groupBox_refTime)
        self.radioButton_est_reftime_NOON.setObjectName(u"radioButton_est_reftime_NOON")

        self.horizontalLayout_29.addWidget(self.radioButton_est_reftime_NOON)


        self.verticalLayout_37.addLayout(self.horizontalLayout_29)


        self.horizontalLayout_42.addWidget(self.groupBox_refTime)


        self.horizontalLayout_54.addLayout(self.horizontalLayout_42)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_54.addItem(self.horizontalSpacer_9)


        self.verticalLayout_49.addWidget(self.groupBox_15)

        self.groupBox_13 = QGroupBox(self.page_est_eoprf)
        self.groupBox_13.setObjectName(u"groupBox_13")
        sizePolicy4.setHeightForWidth(self.groupBox_13.sizePolicy().hasHeightForWidth())
        self.groupBox_13.setSizePolicy(sizePolicy4)
        self.horizontalLayout_51 = QHBoxLayout(self.groupBox_13)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_est_pmxy = QCheckBox(self.groupBox_13)
        self.checkBox_est_pmxy.setObjectName(u"checkBox_est_pmxy")

        self.gridLayout.addWidget(self.checkBox_est_pmxy, 0, 0, 1, 1)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.lineEdit_pmxy_interval = QLineEdit(self.groupBox_13)
        self.lineEdit_pmxy_interval.setObjectName(u"lineEdit_pmxy_interval")
        self.lineEdit_pmxy_interval.setEnabled(False)
        self.lineEdit_pmxy_interval.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_49.addWidget(self.lineEdit_pmxy_interval)

        self.label_9 = QLabel(self.groupBox_13)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_49.addWidget(self.label_9)


        self.gridLayout.addLayout(self.horizontalLayout_49, 0, 1, 1, 1)

        self.lineEdit_pmxy_constr = QLineEdit(self.groupBox_13)
        self.lineEdit_pmxy_constr.setObjectName(u"lineEdit_pmxy_constr")
        self.lineEdit_pmxy_constr.setEnabled(False)
        self.lineEdit_pmxy_constr.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_pmxy_constr, 0, 2, 1, 1)

        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.lineEdit_pmxy_constr_poly = QLineEdit(self.groupBox_13)
        self.lineEdit_pmxy_constr_poly.setObjectName(u"lineEdit_pmxy_constr_poly")
        self.lineEdit_pmxy_constr_poly.setEnabled(True)
        self.lineEdit_pmxy_constr_poly.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_41.addWidget(self.lineEdit_pmxy_constr_poly)

        self.label_11 = QLabel(self.groupBox_13)
        self.label_11.setObjectName(u"label_11")
        sizePolicy5.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy5)
        self.label_11.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_41.addWidget(self.label_11)


        self.gridLayout.addLayout(self.horizontalLayout_41, 0, 3, 1, 1)

        self.checkBox_est_ut1 = QCheckBox(self.groupBox_13)
        self.checkBox_est_ut1.setObjectName(u"checkBox_est_ut1")
        self.checkBox_est_ut1.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_est_ut1, 1, 0, 1, 1)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.lineEdit_ut1_interval = QLineEdit(self.groupBox_13)
        self.lineEdit_ut1_interval.setObjectName(u"lineEdit_ut1_interval")
        self.lineEdit_ut1_interval.setEnabled(False)
        self.lineEdit_ut1_interval.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_50.addWidget(self.lineEdit_ut1_interval)

        self.label_8 = QLabel(self.groupBox_13)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_50.addWidget(self.label_8)


        self.gridLayout.addLayout(self.horizontalLayout_50, 1, 1, 1, 1)

        self.lineEdit_ut1_constr = QLineEdit(self.groupBox_13)
        self.lineEdit_ut1_constr.setObjectName(u"lineEdit_ut1_constr")
        self.lineEdit_ut1_constr.setEnabled(False)
        self.lineEdit_ut1_constr.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_ut1_constr, 1, 2, 1, 1)

        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.lineEdit_ut1_constr_poly = QLineEdit(self.groupBox_13)
        self.lineEdit_ut1_constr_poly.setObjectName(u"lineEdit_ut1_constr_poly")
        self.lineEdit_ut1_constr_poly.setEnabled(True)
        self.lineEdit_ut1_constr_poly.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_44.addWidget(self.lineEdit_ut1_constr_poly)

        self.label_13 = QLabel(self.groupBox_13)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_44.addWidget(self.label_13)


        self.gridLayout.addLayout(self.horizontalLayout_44, 1, 3, 1, 1)

        self.checkBox_est_rpmxy = QCheckBox(self.groupBox_13)
        self.checkBox_est_rpmxy.setObjectName(u"checkBox_est_rpmxy")
        self.checkBox_est_rpmxy.setEnabled(True)
        self.checkBox_est_rpmxy.setCheckable(True)

        self.gridLayout.addWidget(self.checkBox_est_rpmxy, 2, 0, 1, 1)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.lineEdit_rpmxy_constr_poly = QLineEdit(self.groupBox_13)
        self.lineEdit_rpmxy_constr_poly.setObjectName(u"lineEdit_rpmxy_constr_poly")
        self.lineEdit_rpmxy_constr_poly.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.lineEdit_rpmxy_constr_poly.sizePolicy().hasHeightForWidth())
        self.lineEdit_rpmxy_constr_poly.setSizePolicy(sizePolicy6)
        self.lineEdit_rpmxy_constr_poly.setMinimumSize(QSize(100, 0))
        self.lineEdit_rpmxy_constr_poly.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_45.addWidget(self.lineEdit_rpmxy_constr_poly)

        self.label_12 = QLabel(self.groupBox_13)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_45.addWidget(self.label_12)


        self.gridLayout.addLayout(self.horizontalLayout_45, 2, 3, 1, 1)

        self.checkBox_est_lod = QCheckBox(self.groupBox_13)
        self.checkBox_est_lod.setObjectName(u"checkBox_est_lod")
        self.checkBox_est_lod.setEnabled(True)

        self.gridLayout.addWidget(self.checkBox_est_lod, 3, 0, 1, 1)

        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.lineEdit_lod_constr_poly = QLineEdit(self.groupBox_13)
        self.lineEdit_lod_constr_poly.setObjectName(u"lineEdit_lod_constr_poly")
        self.lineEdit_lod_constr_poly.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.lineEdit_lod_constr_poly.sizePolicy().hasHeightForWidth())
        self.lineEdit_lod_constr_poly.setSizePolicy(sizePolicy6)
        self.lineEdit_lod_constr_poly.setMinimumSize(QSize(100, 0))
        self.lineEdit_lod_constr_poly.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_46.addWidget(self.lineEdit_lod_constr_poly)

        self.label_15 = QLabel(self.groupBox_13)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_46.addWidget(self.label_15)


        self.gridLayout.addLayout(self.horizontalLayout_46, 3, 3, 1, 1)

        self.checkBox_est_nutxy = QCheckBox(self.groupBox_13)
        self.checkBox_est_nutxy.setObjectName(u"checkBox_est_nutxy")

        self.gridLayout.addWidget(self.checkBox_est_nutxy, 4, 0, 1, 1)

        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.lineEdit_nut_constr_poly = QLineEdit(self.groupBox_13)
        self.lineEdit_nut_constr_poly.setObjectName(u"lineEdit_nut_constr_poly")
        self.lineEdit_nut_constr_poly.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.lineEdit_nut_constr_poly.sizePolicy().hasHeightForWidth())
        self.lineEdit_nut_constr_poly.setSizePolicy(sizePolicy6)
        self.lineEdit_nut_constr_poly.setMinimumSize(QSize(100, 0))
        self.lineEdit_nut_constr_poly.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_47.addWidget(self.lineEdit_nut_constr_poly)

        self.label_14 = QLabel(self.groupBox_13)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_47.addWidget(self.label_14)


        self.gridLayout.addLayout(self.horizontalLayout_47, 4, 3, 1, 1)


        self.horizontalLayout_51.addLayout(self.gridLayout)

        self.horizontalSpacer_8 = QSpacerItem(400, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_8)


        self.verticalLayout_49.addWidget(self.groupBox_13)

        self.groupBox_14 = QGroupBox(self.page_est_eoprf)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.horizontalLayout_53 = QHBoxLayout(self.groupBox_14)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.horizontalLayout_48.setSizeConstraint(QLayout.SetNoConstraint)
        self.groupBox_est_trf = QGroupBox(self.groupBox_14)
        self.groupBox_est_trf.setObjectName(u"groupBox_est_trf")
        sizePolicy3.setHeightForWidth(self.groupBox_est_trf.sizePolicy().hasHeightForWidth())
        self.groupBox_est_trf.setSizePolicy(sizePolicy3)
        self.groupBox_est_trf.setMinimumSize(QSize(0, 0))
        self.checkBox_est_station = QCheckBox(self.groupBox_est_trf)
        self.checkBox_est_station.setObjectName(u"checkBox_est_station")
        self.checkBox_est_station.setGeometry(QRect(10, 29, 186, 23))
        self.layoutWidget2 = QWidget(self.groupBox_est_trf)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(50, 70, 461, 191))
        self.gridLayout_3 = QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_autoset_station = QPushButton(self.layoutWidget2)
        self.pushButton_autoset_station.setObjectName(u"pushButton_autoset_station")
        self.pushButton_autoset_station.setEnabled(False)

        self.gridLayout_3.addWidget(self.pushButton_autoset_station, 0, 0, 1, 1)

        self.horizontalSpacer_34 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_34, 0, 1, 1, 1)

        self.label_68 = QLabel(self.layoutWidget2)
        self.label_68.setObjectName(u"label_68")

        self.gridLayout_3.addWidget(self.label_68, 0, 2, 1, 1)

        self.lineEdit_sigma_sta = QLineEdit(self.layoutWidget2)
        self.lineEdit_sigma_sta.setObjectName(u"lineEdit_sigma_sta")
        self.lineEdit_sigma_sta.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_sigma_sta, 0, 3, 1, 1)

        self.label_69 = QLabel(self.layoutWidget2)
        self.label_69.setObjectName(u"label_69")

        self.gridLayout_3.addWidget(self.label_69, 0, 4, 1, 1)

        self.checkBox_est_nnr = QCheckBox(self.layoutWidget2)
        self.checkBox_est_nnr.setObjectName(u"checkBox_est_nnr")
        self.checkBox_est_nnr.setChecked(False)

        self.gridLayout_3.addWidget(self.checkBox_est_nnr, 1, 0, 1, 1)

        self.horizontalSpacer_35 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_35, 1, 1, 1, 1)

        self.label_63 = QLabel(self.layoutWidget2)
        self.label_63.setObjectName(u"label_63")

        self.gridLayout_3.addWidget(self.label_63, 1, 2, 1, 1)

        self.lineEdit_sigma_stannr = QLineEdit(self.layoutWidget2)
        self.lineEdit_sigma_stannr.setObjectName(u"lineEdit_sigma_stannr")
        self.lineEdit_sigma_stannr.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_sigma_stannr, 1, 3, 1, 1)

        self.label_62 = QLabel(self.layoutWidget2)
        self.label_62.setObjectName(u"label_62")

        self.gridLayout_3.addWidget(self.label_62, 1, 4, 1, 1)

        self.checkBox_est_nnt = QCheckBox(self.layoutWidget2)
        self.checkBox_est_nnt.setObjectName(u"checkBox_est_nnt")
        self.checkBox_est_nnt.setChecked(False)

        self.gridLayout_3.addWidget(self.checkBox_est_nnt, 2, 0, 1, 1)

        self.horizontalSpacer_36 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_36, 2, 1, 1, 1)

        self.label_64 = QLabel(self.layoutWidget2)
        self.label_64.setObjectName(u"label_64")

        self.gridLayout_3.addWidget(self.label_64, 2, 2, 1, 1)

        self.lineEdit_sigma_stannt = QLineEdit(self.layoutWidget2)
        self.lineEdit_sigma_stannt.setObjectName(u"lineEdit_sigma_stannt")
        self.lineEdit_sigma_stannt.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_sigma_stannt, 2, 3, 1, 1)

        self.label_65 = QLabel(self.layoutWidget2)
        self.label_65.setObjectName(u"label_65")

        self.gridLayout_3.addWidget(self.label_65, 2, 4, 1, 1)

        self.checkBox_nns = QCheckBox(self.layoutWidget2)
        self.checkBox_nns.setObjectName(u"checkBox_nns")
        self.checkBox_nns.setEnabled(False)
        self.checkBox_nns.setCheckable(True)

        self.gridLayout_3.addWidget(self.checkBox_nns, 3, 0, 1, 1)


        self.horizontalLayout_48.addWidget(self.groupBox_est_trf)

        self.groupBox_est_crf = QGroupBox(self.groupBox_14)
        self.groupBox_est_crf.setObjectName(u"groupBox_est_crf")
        sizePolicy3.setHeightForWidth(self.groupBox_est_crf.sizePolicy().hasHeightForWidth())
        self.groupBox_est_crf.setSizePolicy(sizePolicy3)
        self.groupBox_est_crf.setMinimumSize(QSize(0, 0))
        self.checkBox_est_source = QCheckBox(self.groupBox_est_crf)
        self.checkBox_est_source.setObjectName(u"checkBox_est_source")
        self.checkBox_est_source.setGeometry(QRect(10, 29, 187, 23))
        self.layoutWidget3 = QWidget(self.groupBox_est_crf)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(60, 70, 411, 121))
        self.gridLayout_2 = QGridLayout(self.layoutWidget3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_autoset_source = QPushButton(self.layoutWidget3)
        self.pushButton_autoset_source.setObjectName(u"pushButton_autoset_source")
        self.pushButton_autoset_source.setEnabled(False)

        self.gridLayout_2.addWidget(self.pushButton_autoset_source, 0, 0, 1, 1)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_32, 0, 1, 1, 1)

        self.label_70 = QLabel(self.layoutWidget3)
        self.label_70.setObjectName(u"label_70")

        self.gridLayout_2.addWidget(self.label_70, 0, 2, 1, 1)

        self.lineEdit_sigma_sou = QLineEdit(self.layoutWidget3)
        self.lineEdit_sigma_sou.setObjectName(u"lineEdit_sigma_sou")
        self.lineEdit_sigma_sou.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_sigma_sou, 0, 3, 1, 1)

        self.label_71 = QLabel(self.layoutWidget3)
        self.label_71.setObjectName(u"label_71")

        self.gridLayout_2.addWidget(self.label_71, 0, 4, 1, 1)

        self.checkBox_est_sounnr = QCheckBox(self.layoutWidget3)
        self.checkBox_est_sounnr.setObjectName(u"checkBox_est_sounnr")

        self.gridLayout_2.addWidget(self.checkBox_est_sounnr, 1, 0, 1, 1)

        self.horizontalSpacer_33 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_33, 1, 1, 1, 1)

        self.label_66 = QLabel(self.layoutWidget3)
        self.label_66.setObjectName(u"label_66")

        self.gridLayout_2.addWidget(self.label_66, 1, 2, 1, 1)

        self.lineEdit_sigma_sounnr = QLineEdit(self.layoutWidget3)
        self.lineEdit_sigma_sounnr.setObjectName(u"lineEdit_sigma_sounnr")
        self.lineEdit_sigma_sounnr.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_sigma_sounnr, 1, 3, 1, 1)

        self.label_67 = QLabel(self.layoutWidget3)
        self.label_67.setObjectName(u"label_67")

        self.gridLayout_2.addWidget(self.label_67, 1, 4, 1, 1)


        self.horizontalLayout_48.addWidget(self.groupBox_est_crf)


        self.horizontalLayout_53.addLayout(self.horizontalLayout_48)


        self.verticalLayout_49.addWidget(self.groupBox_14)

        self.stackedWidget.addWidget(self.page_est_eoprf)
        self.page_glob_setup = QWidget()
        self.page_glob_setup.setObjectName(u"page_glob_setup")
        self.horizontalLayout_65 = QHBoxLayout(self.page_glob_setup)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.groupBox_12 = QGroupBox(self.page_glob_setup)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_19 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_72 = QHBoxLayout()
        self.horizontalLayout_72.setObjectName(u"horizontalLayout_72")
        self.label_57 = QLabel(self.groupBox_12)
        self.label_57.setObjectName(u"label_57")

        self.horizontalLayout_72.addWidget(self.label_57)

        self.lineEdit_glob_arc = QLineEdit(self.groupBox_12)
        self.lineEdit_glob_arc.setObjectName(u"lineEdit_glob_arc")

        self.horizontalLayout_72.addWidget(self.lineEdit_glob_arc)


        self.horizontalLayout_24.addLayout(self.horizontalLayout_72)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_28)


        self.verticalLayout_19.addLayout(self.horizontalLayout_24)

        self.verticalSpacer_6 = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_19.addItem(self.verticalSpacer_6)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_55 = QLabel(self.groupBox_12)
        self.label_55.setObjectName(u"label_55")
        sizePolicy5.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy5)

        self.gridLayout_5.addWidget(self.label_55, 0, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_12)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_5.addWidget(self.label_7, 1, 0, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_19, 1, 1, 1, 1)

        self.checkBox_glob_station_yes = QCheckBox(self.groupBox_12)
        self.checkBox_glob_station_yes.setObjectName(u"checkBox_glob_station_yes")
        sizePolicy5.setHeightForWidth(self.checkBox_glob_station_yes.sizePolicy().hasHeightForWidth())
        self.checkBox_glob_station_yes.setSizePolicy(sizePolicy5)
        self.checkBox_glob_station_yes.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_glob_station_yes, 1, 2, 1, 1)

        self.label_36 = QLabel(self.groupBox_12)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_5.addWidget(self.label_36, 2, 0, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_20, 2, 1, 1, 1)

        self.checkBox_glob_station_velocity_yes = QCheckBox(self.groupBox_12)
        self.checkBox_glob_station_velocity_yes.setObjectName(u"checkBox_glob_station_velocity_yes")
        sizePolicy5.setHeightForWidth(self.checkBox_glob_station_velocity_yes.sizePolicy().hasHeightForWidth())
        self.checkBox_glob_station_velocity_yes.setSizePolicy(sizePolicy5)

        self.gridLayout_5.addWidget(self.checkBox_glob_station_velocity_yes, 2, 2, 1, 1)

        self.label_48 = QLabel(self.groupBox_12)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_5.addWidget(self.label_48, 3, 0, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_21, 3, 1, 1, 1)

        self.checkBox_glob_source_yes = QCheckBox(self.groupBox_12)
        self.checkBox_glob_source_yes.setObjectName(u"checkBox_glob_source_yes")
        sizePolicy5.setHeightForWidth(self.checkBox_glob_source_yes.sizePolicy().hasHeightForWidth())
        self.checkBox_glob_source_yes.setSizePolicy(sizePolicy5)

        self.gridLayout_5.addWidget(self.checkBox_glob_source_yes, 3, 2, 1, 1)

        self.label_54 = QLabel(self.groupBox_12)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_5.addWidget(self.label_54, 4, 0, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_22, 4, 1, 1, 1)

        self.checkBox_glob_eop_yes = QCheckBox(self.groupBox_12)
        self.checkBox_glob_eop_yes.setObjectName(u"checkBox_glob_eop_yes")
        sizePolicy5.setHeightForWidth(self.checkBox_glob_eop_yes.sizePolicy().hasHeightForWidth())
        self.checkBox_glob_eop_yes.setSizePolicy(sizePolicy5)

        self.gridLayout_5.addWidget(self.checkBox_glob_eop_yes, 4, 2, 1, 1)


        self.horizontalLayout_25.addLayout(self.gridLayout_5)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_29)


        self.verticalLayout_19.addLayout(self.horizontalLayout_25)

        self.verticalSpacer_4 = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_19.addItem(self.verticalSpacer_4)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_56 = QLabel(self.groupBox_12)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_6.addWidget(self.label_56, 0, 0, 1, 1)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_23, 0, 1, 1, 1)

        self.checkBox_glob_trf_nnrnnt = QCheckBox(self.groupBox_12)
        self.checkBox_glob_trf_nnrnnt.setObjectName(u"checkBox_glob_trf_nnrnnt")

        self.gridLayout_6.addWidget(self.checkBox_glob_trf_nnrnnt, 0, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_12)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_6.addWidget(self.label_4, 0, 3, 1, 1)

        self.lineEdit_glob_trf_nnrnnt = QLineEdit(self.groupBox_12)
        self.lineEdit_glob_trf_nnrnnt.setObjectName(u"lineEdit_glob_trf_nnrnnt")
        self.lineEdit_glob_trf_nnrnnt.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_glob_trf_nnrnnt, 0, 4, 1, 1)

        self.pushButton_glob_edit_trf = QPushButton(self.groupBox_12)
        self.pushButton_glob_edit_trf.setObjectName(u"pushButton_glob_edit_trf")
        sizePolicy2.setHeightForWidth(self.pushButton_glob_edit_trf.sizePolicy().hasHeightForWidth())
        self.pushButton_glob_edit_trf.setSizePolicy(sizePolicy2)
        self.pushButton_glob_edit_trf.setMinimumSize(QSize(25, 35))
        icon21 = QIcon()
        icon21.addFile(u":/icons/icons/edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_glob_edit_trf.setIcon(icon21)
        self.pushButton_glob_edit_trf.setIconSize(QSize(25, 25))

        self.gridLayout_6.addWidget(self.pushButton_glob_edit_trf, 0, 5, 1, 1)

        self.label_58 = QLabel(self.groupBox_12)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_6.addWidget(self.label_58, 1, 0, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_24, 1, 1, 1, 1)

        self.checkBox_glob_crf_nnr = QCheckBox(self.groupBox_12)
        self.checkBox_glob_crf_nnr.setObjectName(u"checkBox_glob_crf_nnr")

        self.gridLayout_6.addWidget(self.checkBox_glob_crf_nnr, 1, 2, 1, 1)

        self.label_59 = QLabel(self.groupBox_12)
        self.label_59.setObjectName(u"label_59")

        self.gridLayout_6.addWidget(self.label_59, 1, 3, 1, 1)

        self.lineEdit_glob_crf_nnr = QLineEdit(self.groupBox_12)
        self.lineEdit_glob_crf_nnr.setObjectName(u"lineEdit_glob_crf_nnr")
        self.lineEdit_glob_crf_nnr.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_glob_crf_nnr, 1, 4, 1, 1)

        self.pushButton_glob_edit_crf = QPushButton(self.groupBox_12)
        self.pushButton_glob_edit_crf.setObjectName(u"pushButton_glob_edit_crf")
        sizePolicy2.setHeightForWidth(self.pushButton_glob_edit_crf.sizePolicy().hasHeightForWidth())
        self.pushButton_glob_edit_crf.setSizePolicy(sizePolicy2)
        self.pushButton_glob_edit_crf.setMinimumSize(QSize(25, 35))
        self.pushButton_glob_edit_crf.setIcon(icon21)
        self.pushButton_glob_edit_crf.setIconSize(QSize(25, 25))

        self.gridLayout_6.addWidget(self.pushButton_glob_edit_crf, 1, 5, 1, 1)

        self.label_60 = QLabel(self.groupBox_12)
        self.label_60.setObjectName(u"label_60")

        self.gridLayout_6.addWidget(self.label_60, 2, 0, 1, 1)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_26, 2, 1, 1, 1)

        self.lineEdit_glob_station_exclude = QLineEdit(self.groupBox_12)
        self.lineEdit_glob_station_exclude.setObjectName(u"lineEdit_glob_station_exclude")
        self.lineEdit_glob_station_exclude.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_glob_station_exclude, 2, 4, 1, 1)

        self.pushButton_glob_edit_globex = QPushButton(self.groupBox_12)
        self.pushButton_glob_edit_globex.setObjectName(u"pushButton_glob_edit_globex")
        sizePolicy2.setHeightForWidth(self.pushButton_glob_edit_globex.sizePolicy().hasHeightForWidth())
        self.pushButton_glob_edit_globex.setSizePolicy(sizePolicy2)
        self.pushButton_glob_edit_globex.setMinimumSize(QSize(25, 35))
        self.pushButton_glob_edit_globex.setIcon(icon21)
        self.pushButton_glob_edit_globex.setIconSize(QSize(25, 25))

        self.gridLayout_6.addWidget(self.pushButton_glob_edit_globex, 2, 5, 1, 1)


        self.horizontalLayout_26.addLayout(self.gridLayout_6)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_30)


        self.verticalLayout_19.addLayout(self.horizontalLayout_26)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_3)


        self.horizontalLayout_65.addWidget(self.groupBox_12)

        self.stackedWidget.addWidget(self.page_glob_setup)
        self.page_glob_station = QWidget()
        self.page_glob_station.setObjectName(u"page_glob_station")
        self.verticalLayout_62 = QVBoxLayout(self.page_glob_station)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.tableWidget_glob_station = QTableWidget(self.page_glob_station)
        if (self.tableWidget_glob_station.columnCount() < 5):
            self.tableWidget_glob_station.setColumnCount(5)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget_glob_station.setHorizontalHeaderItem(0, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget_glob_station.setHorizontalHeaderItem(1, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget_glob_station.setHorizontalHeaderItem(2, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget_glob_station.setHorizontalHeaderItem(3, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableWidget_glob_station.setHorizontalHeaderItem(4, __qtablewidgetitem36)
        self.tableWidget_glob_station.setObjectName(u"tableWidget_glob_station")

        self.verticalLayout_62.addWidget(self.tableWidget_glob_station)

        self.stackedWidget.addWidget(self.page_glob_station)
        self.page_glob_source = QWidget()
        self.page_glob_source.setObjectName(u"page_glob_source")
        self.verticalLayout_65 = QVBoxLayout(self.page_glob_source)
        self.verticalLayout_65.setObjectName(u"verticalLayout_65")
        self.tableWidget_glob_source = QTableWidget(self.page_glob_source)
        if (self.tableWidget_glob_source.columnCount() < 5):
            self.tableWidget_glob_source.setColumnCount(5)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableWidget_glob_source.setHorizontalHeaderItem(0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableWidget_glob_source.setHorizontalHeaderItem(1, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableWidget_glob_source.setHorizontalHeaderItem(2, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableWidget_glob_source.setHorizontalHeaderItem(3, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableWidget_glob_source.setHorizontalHeaderItem(4, __qtablewidgetitem41)
        self.tableWidget_glob_source.setObjectName(u"tableWidget_glob_source")

        self.verticalLayout_65.addWidget(self.tableWidget_glob_source)

        self.stackedWidget.addWidget(self.page_glob_source)
        self.page_plot_residual = QWidget()
        self.page_plot_residual.setObjectName(u"page_plot_residual")
        self.verticalLayout_28 = QVBoxLayout(self.page_plot_residual)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.pushButton_plot_S = QPushButton(self.page_plot_residual)
        self.pushButton_plot_S.setObjectName(u"pushButton_plot_S")
        self.pushButton_plot_S.setCheckable(True)

        self.horizontalLayout_37.addWidget(self.pushButton_plot_S)

        self.pushButton_plot_X = QPushButton(self.page_plot_residual)
        self.pushButton_plot_X.setObjectName(u"pushButton_plot_X")
        self.pushButton_plot_X.setCheckable(True)
        self.pushButton_plot_X.setChecked(True)

        self.horizontalLayout_37.addWidget(self.pushButton_plot_X)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_3)

        self.label_result = QLabel(self.page_plot_residual)
        self.label_result.setObjectName(u"label_result")
        sizePolicy1.setHeightForWidth(self.label_result.sizePolicy().hasHeightForWidth())
        self.label_result.setSizePolicy(sizePolicy1)
        self.label_result.setMinimumSize(QSize(400, 0))
        self.label_result.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_37.addWidget(self.label_result)


        self.verticalLayout_28.addLayout(self.horizontalLayout_37)

        self.groupBox_plot_res = QGroupBox(self.page_plot_residual)
        self.groupBox_plot_res.setObjectName(u"groupBox_plot_res")
        sizePolicy.setHeightForWidth(self.groupBox_plot_res.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_res.setSizePolicy(sizePolicy)
        self.groupBox_plot_res.setMinimumSize(QSize(1050, 400))
        self.verticalLayout_51 = QVBoxLayout(self.groupBox_plot_res)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_plot_res = QVBoxLayout()
        self.verticalLayout_plot_res.setObjectName(u"verticalLayout_plot_res")

        self.verticalLayout_51.addLayout(self.verticalLayout_plot_res)


        self.verticalLayout_28.addWidget(self.groupBox_plot_res)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.pushButton_plot_reload = QPushButton(self.page_plot_residual)
        self.pushButton_plot_reload.setObjectName(u"pushButton_plot_reload")
        icon22 = QIcon()
        icon22.addFile(u":/icons/icons/reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_reload.setIcon(icon22)
        self.pushButton_plot_reload.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_reload)

        self.pushButton_plot_home = QPushButton(self.page_plot_residual)
        self.pushButton_plot_home.setObjectName(u"pushButton_plot_home")
        icon23 = QIcon()
        icon23.addFile(u":/icons/icons/home.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_home.setIcon(icon23)
        self.pushButton_plot_home.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_home)

        self.pushButton_plot_outlier = QPushButton(self.page_plot_residual)
        self.pushButton_plot_outlier.setObjectName(u"pushButton_plot_outlier")
        icon24 = QIcon()
        icon24.addFile(u":/icons/icons/magnifier.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_outlier.setIcon(icon24)
        self.pushButton_plot_outlier.setIconSize(QSize(27, 27))
        self.pushButton_plot_outlier.setCheckable(True)
        self.pushButton_plot_outlier.setChecked(False)

        self.horizontalLayout_30.addWidget(self.pushButton_plot_outlier)

        self.pushButton_plot_ambigCorr = QPushButton(self.page_plot_residual)
        self.pushButton_plot_ambigCorr.setObjectName(u"pushButton_plot_ambigCorr")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.pushButton_plot_ambigCorr.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_ambigCorr.setSizePolicy(sizePolicy8)
        self.pushButton_plot_ambigCorr.setMinimumSize(QSize(0, 27))
        self.pushButton_plot_ambigCorr.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_ambigCorr)

        self.pushButton_plot_ambAdd = QPushButton(self.page_plot_residual)
        self.pushButton_plot_ambAdd.setObjectName(u"pushButton_plot_ambAdd")
        icon25 = QIcon()
        icon25.addFile(u":/icons/icons/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_ambAdd.setIcon(icon25)
        self.pushButton_plot_ambAdd.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_ambAdd)

        self.pushButton_plot_ambSub = QPushButton(self.page_plot_residual)
        self.pushButton_plot_ambSub.setObjectName(u"pushButton_plot_ambSub")
        icon26 = QIcon()
        icon26.addFile(u":/icons/icons/substraction.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_ambSub.setIcon(icon26)
        self.pushButton_plot_ambSub.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_ambSub)

        self.pushButton_plot_ambigZero = QPushButton(self.page_plot_residual)
        self.pushButton_plot_ambigZero.setObjectName(u"pushButton_plot_ambigZero")
        sizePolicy8.setHeightForWidth(self.pushButton_plot_ambigZero.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_ambigZero.setSizePolicy(sizePolicy8)

        self.horizontalLayout_30.addWidget(self.pushButton_plot_ambigZero)

        self.pushButton_plot_clkbk = QPushButton(self.page_plot_residual)
        self.pushButton_plot_clkbk.setObjectName(u"pushButton_plot_clkbk")
        sizePolicy8.setHeightForWidth(self.pushButton_plot_clkbk.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_clkbk.setSizePolicy(sizePolicy8)
        self.pushButton_plot_clkbk.setIconSize(QSize(30, 30))
        self.pushButton_plot_clkbk.setCheckable(True)
        self.pushButton_plot_clkbk.setChecked(False)

        self.horizontalLayout_30.addWidget(self.pushButton_plot_clkbk)

        self.pushButton_plot_ionCorr = QPushButton(self.page_plot_residual)
        self.pushButton_plot_ionCorr.setObjectName(u"pushButton_plot_ionCorr")
        sizePolicy8.setHeightForWidth(self.pushButton_plot_ionCorr.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_ionCorr.setSizePolicy(sizePolicy8)
        self.pushButton_plot_ionCorr.setCheckable(False)

        self.horizontalLayout_30.addWidget(self.pushButton_plot_ionCorr)

        self.pushButton_plot_ionZero = QPushButton(self.page_plot_residual)
        self.pushButton_plot_ionZero.setObjectName(u"pushButton_plot_ionZero")
        sizePolicy8.setHeightForWidth(self.pushButton_plot_ionZero.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_ionZero.setSizePolicy(sizePolicy8)

        self.horizontalLayout_30.addWidget(self.pushButton_plot_ionZero)

        self.horizontalSpacer_40 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_40)

        self.pushButton_plot_remove = QPushButton(self.page_plot_residual)
        self.pushButton_plot_remove.setObjectName(u"pushButton_plot_remove")
        icon27 = QIcon()
        icon27.addFile(u":/icons/icons/deleteData.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_remove.setIcon(icon27)
        self.pushButton_plot_remove.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_remove)

        self.pushButton_plot_autoOut = QPushButton(self.page_plot_residual)
        self.pushButton_plot_autoOut.setObjectName(u"pushButton_plot_autoOut")
        icon28 = QIcon()
        icon28.addFile(u":/icons/icons/updateData.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_autoOut.setIcon(icon28)
        self.pushButton_plot_autoOut.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_autoOut)

        self.pushButton_plot_reweight = QPushButton(self.page_plot_residual)
        self.pushButton_plot_reweight.setObjectName(u"pushButton_plot_reweight")
        icon29 = QIcon()
        icon29.addFile(u":/icons/icons/weight.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_reweight.setIcon(icon29)
        self.pushButton_plot_reweight.setIconSize(QSize(27, 27))

        self.horizontalLayout_30.addWidget(self.pushButton_plot_reweight)


        self.verticalLayout_28.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(-1, -1, 0, -1)
        self.groupBox_2 = QGroupBox(self.page_plot_residual)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.verticalLayout_60 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_29 = QLabel(self.groupBox_2)
        self.label_29.setObjectName(u"label_29")

        self.verticalLayout_11.addWidget(self.label_29)

        self.label_30 = QLabel(self.groupBox_2)
        self.label_30.setObjectName(u"label_30")

        self.verticalLayout_11.addWidget(self.label_30)


        self.horizontalLayout_33.addLayout(self.verticalLayout_11)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.comboBox_plot_x = QComboBox(self.groupBox_2)
        self.comboBox_plot_x.addItem("")
        self.comboBox_plot_x.setObjectName(u"comboBox_plot_x")
        sizePolicy7.setHeightForWidth(self.comboBox_plot_x.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_x.setSizePolicy(sizePolicy7)
        self.comboBox_plot_x.setMinimumSize(QSize(0, 0))

        self.verticalLayout_26.addWidget(self.comboBox_plot_x)

        self.comboBox_plot_y = QComboBox(self.groupBox_2)
        self.comboBox_plot_y.addItem("")
        self.comboBox_plot_y.addItem("")
        self.comboBox_plot_y.addItem("")
        self.comboBox_plot_y.addItem("")
        self.comboBox_plot_y.setObjectName(u"comboBox_plot_y")
        sizePolicy7.setHeightForWidth(self.comboBox_plot_y.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_y.setSizePolicy(sizePolicy7)

        self.verticalLayout_26.addWidget(self.comboBox_plot_y)


        self.horizontalLayout_33.addLayout(self.verticalLayout_26)


        self.verticalLayout_60.addLayout(self.horizontalLayout_33)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_60.addItem(self.verticalSpacer_2)


        self.horizontalLayout_36.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.page_plot_residual)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy3.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy3)
        self.groupBox.setMinimumSize(QSize(0, 0))
        self.groupBox.setFont(font)
        self.horizontalLayout_27 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.radioButton_plot_all = QRadioButton(self.groupBox)
        self.radioButton_plot_all.setObjectName(u"radioButton_plot_all")
        sizePolicy2.setHeightForWidth(self.radioButton_plot_all.sizePolicy().hasHeightForWidth())
        self.radioButton_plot_all.setSizePolicy(sizePolicy2)
        self.radioButton_plot_all.setChecked(True)

        self.gridLayout_7.addWidget(self.radioButton_plot_all, 0, 0, 1, 1)

        self.radioButton_plot_station = QRadioButton(self.groupBox)
        self.radioButton_plot_station.setObjectName(u"radioButton_plot_station")
        self.radioButton_plot_station.setChecked(False)

        self.gridLayout_7.addWidget(self.radioButton_plot_station, 1, 0, 1, 1)

        self.comboBox_plot_station = QComboBox(self.groupBox)
        self.comboBox_plot_station.setObjectName(u"comboBox_plot_station")
        sizePolicy2.setHeightForWidth(self.comboBox_plot_station.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_station.setSizePolicy(sizePolicy2)
        self.comboBox_plot_station.setMinimumSize(QSize(200, 0))

        self.gridLayout_7.addWidget(self.comboBox_plot_station, 1, 1, 1, 1)

        self.pushButton_plot_resOmitSta = QPushButton(self.groupBox)
        self.pushButton_plot_resOmitSta.setObjectName(u"pushButton_plot_resOmitSta")
        self.pushButton_plot_resOmitSta.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.pushButton_plot_resOmitSta.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_resOmitSta.setSizePolicy(sizePolicy2)
        icon30 = QIcon()
        icon30.addFile(u":/icons/icons/remove.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_resOmitSta.setIcon(icon30)
        self.pushButton_plot_resOmitSta.setIconSize(QSize(20, 20))

        self.gridLayout_7.addWidget(self.pushButton_plot_resOmitSta, 1, 2, 1, 1)

        self.radioButton_plot_baseline = QRadioButton(self.groupBox)
        self.radioButton_plot_baseline.setObjectName(u"radioButton_plot_baseline")

        self.gridLayout_7.addWidget(self.radioButton_plot_baseline, 2, 0, 1, 1)

        self.comboBox_plot_baseline = QComboBox(self.groupBox)
        self.comboBox_plot_baseline.setObjectName(u"comboBox_plot_baseline")

        self.gridLayout_7.addWidget(self.comboBox_plot_baseline, 2, 1, 1, 1)

        self.pushButton_plot_resOmitBL = QPushButton(self.groupBox)
        self.pushButton_plot_resOmitBL.setObjectName(u"pushButton_plot_resOmitBL")
        self.pushButton_plot_resOmitBL.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.pushButton_plot_resOmitBL.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_resOmitBL.setSizePolicy(sizePolicy2)
        self.pushButton_plot_resOmitBL.setIcon(icon30)
        self.pushButton_plot_resOmitBL.setIconSize(QSize(20, 20))

        self.gridLayout_7.addWidget(self.pushButton_plot_resOmitBL, 2, 2, 1, 1)

        self.pushButton_plot_resAddBlClock = QPushButton(self.groupBox)
        self.pushButton_plot_resAddBlClock.setObjectName(u"pushButton_plot_resAddBlClock")
        self.pushButton_plot_resAddBlClock.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.pushButton_plot_resAddBlClock.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_resAddBlClock.setSizePolicy(sizePolicy2)
        font7 = QFont()
        font7.setFamily(u"Times New Roman")
        font7.setPointSize(13)
        font7.setBold(False)
        font7.setWeight(50)
        self.pushButton_plot_resAddBlClock.setFont(font7)
        icon31 = QIcon()
        icon31.addFile(u":/icons/icons/estimate.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_plot_resAddBlClock.setIcon(icon31)
        self.pushButton_plot_resAddBlClock.setIconSize(QSize(20, 20))

        self.gridLayout_7.addWidget(self.pushButton_plot_resAddBlClock, 2, 3, 1, 1)

        self.radioButton_plot_source = QRadioButton(self.groupBox)
        self.radioButton_plot_source.setObjectName(u"radioButton_plot_source")

        self.gridLayout_7.addWidget(self.radioButton_plot_source, 3, 0, 1, 1)


        self.horizontalLayout_27.addLayout(self.gridLayout_7)


        self.horizontalLayout_36.addWidget(self.groupBox)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.pushButton_plot_resStaSub = QPushButton(self.page_plot_residual)
        self.pushButton_plot_resStaSub.setObjectName(u"pushButton_plot_resStaSub")
        self.pushButton_plot_resStaSub.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.pushButton_plot_resStaSub.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_resStaSub.setSizePolicy(sizePolicy2)

        self.horizontalLayout_32.addWidget(self.pushButton_plot_resStaSub)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer)

        self.pushButton_plot_resStaAdd = QPushButton(self.page_plot_residual)
        self.pushButton_plot_resStaAdd.setObjectName(u"pushButton_plot_resStaAdd")
        self.pushButton_plot_resStaAdd.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.pushButton_plot_resStaAdd.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_resStaAdd.setSizePolicy(sizePolicy2)

        self.horizontalLayout_32.addWidget(self.pushButton_plot_resStaAdd)


        self.verticalLayout_25.addLayout(self.horizontalLayout_32)

        self.listWidget_plot_resSta = QListWidget(self.page_plot_residual)
        self.listWidget_plot_resSta.setObjectName(u"listWidget_plot_resSta")
        self.listWidget_plot_resSta.setEnabled(False)
        self.listWidget_plot_resSta.setStyleSheet(u"")
        self.listWidget_plot_resSta.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget_plot_resSta.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout_25.addWidget(self.listWidget_plot_resSta)


        self.horizontalLayout_36.addLayout(self.verticalLayout_25)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")

        self.horizontalLayout_36.addLayout(self.verticalLayout_20)

        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.horizontalSpacer_42 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_52.addItem(self.horizontalSpacer_42)

        self.pushButton_plot_resOmitSou = QPushButton(self.page_plot_residual)
        self.pushButton_plot_resOmitSou.setObjectName(u"pushButton_plot_resOmitSou")
        self.pushButton_plot_resOmitSou.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.pushButton_plot_resOmitSou.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_resOmitSou.setSizePolicy(sizePolicy2)
        self.pushButton_plot_resOmitSou.setIcon(icon30)
        self.pushButton_plot_resOmitSou.setIconSize(QSize(20, 20))

        self.horizontalLayout_52.addWidget(self.pushButton_plot_resOmitSou)


        self.verticalLayout_27.addLayout(self.horizontalLayout_52)

        self.listWidget_plot_resSou = QListWidget(self.page_plot_residual)
        self.listWidget_plot_resSou.setObjectName(u"listWidget_plot_resSou")

        self.verticalLayout_27.addWidget(self.listWidget_plot_resSou)


        self.horizontalLayout_36.addLayout(self.verticalLayout_27)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer_17)

        self.groupBox_11 = QGroupBox(self.page_plot_residual)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_39 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.pushButton_plot_modeUT1 = QPushButton(self.groupBox_11)
        self.pushButton_plot_modeUT1.setObjectName(u"pushButton_plot_modeUT1")
        self.pushButton_plot_modeUT1.setCheckable(True)
        self.pushButton_plot_modeUT1.setChecked(False)

        self.verticalLayout_39.addWidget(self.pushButton_plot_modeUT1)

        self.pushButton_plot_modeEOP = QPushButton(self.groupBox_11)
        self.pushButton_plot_modeEOP.setObjectName(u"pushButton_plot_modeEOP")
        self.pushButton_plot_modeEOP.setCheckable(True)

        self.verticalLayout_39.addWidget(self.pushButton_plot_modeEOP)

        self.pushButton_plot_moderegular = QPushButton(self.groupBox_11)
        self.pushButton_plot_moderegular.setObjectName(u"pushButton_plot_moderegular")
        self.pushButton_plot_moderegular.setCheckable(True)

        self.verticalLayout_39.addWidget(self.pushButton_plot_moderegular)

        self.pushButton_plot_modeClear = QPushButton(self.groupBox_11)
        self.pushButton_plot_modeClear.setObjectName(u"pushButton_plot_modeClear")

        self.verticalLayout_39.addWidget(self.pushButton_plot_modeClear)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_39.addItem(self.verticalSpacer_5)


        self.horizontalLayout_36.addWidget(self.groupBox_11)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer_16)

        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, -1, -1, -1)
        self.groupBox_5 = QGroupBox(self.page_plot_residual)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.checkBox_plot_report = QCheckBox(self.groupBox_5)
        self.checkBox_plot_report.setObjectName(u"checkBox_plot_report")

        self.verticalLayout_23.addWidget(self.checkBox_plot_report)

        self.checkBox_plot_eopout = QCheckBox(self.groupBox_5)
        self.checkBox_plot_eopout.setObjectName(u"checkBox_plot_eopout")
        self.checkBox_plot_eopout.setChecked(False)

        self.verticalLayout_23.addWidget(self.checkBox_plot_eopout)

        self.checkBox_plot_snx = QCheckBox(self.groupBox_5)
        self.checkBox_plot_snx.setObjectName(u"checkBox_plot_snx")

        self.verticalLayout_23.addWidget(self.checkBox_plot_snx)

        self.checkBox_plot_vgosDb = QCheckBox(self.groupBox_5)
        self.checkBox_plot_vgosDb.setObjectName(u"checkBox_plot_vgosDb")

        self.verticalLayout_23.addWidget(self.checkBox_plot_vgosDb)


        self.verticalLayout_24.addWidget(self.groupBox_5)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_35 = QLabel(self.page_plot_residual)
        self.label_35.setObjectName(u"label_35")
        sizePolicy2.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy2)

        self.horizontalLayout_31.addWidget(self.label_35)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_4)

        self.pushButton_plot_save = QPushButton(self.page_plot_residual)
        self.pushButton_plot_save.setObjectName(u"pushButton_plot_save")
        sizePolicy2.setHeightForWidth(self.pushButton_plot_save.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_save.setSizePolicy(sizePolicy2)
        self.pushButton_plot_save.setIcon(icon18)
        self.pushButton_plot_save.setIconSize(QSize(20, 20))

        self.horizontalLayout_31.addWidget(self.pushButton_plot_save)


        self.verticalLayout_24.addLayout(self.horizontalLayout_31)


        self.horizontalLayout_36.addLayout(self.verticalLayout_24)


        self.verticalLayout_28.addLayout(self.horizontalLayout_36)

        self.stackedWidget.addWidget(self.page_plot_residual)
        self.page_plot_station = QWidget()
        self.page_plot_station.setObjectName(u"page_plot_station")
        self.verticalLayout_35 = QVBoxLayout(self.page_plot_station)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.groupBox_plot_station = QGroupBox(self.page_plot_station)
        self.groupBox_plot_station.setObjectName(u"groupBox_plot_station")
        sizePolicy.setHeightForWidth(self.groupBox_plot_station.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_station.setSizePolicy(sizePolicy)
        self.groupBox_plot_station.setMinimumSize(QSize(0, 400))
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_plot_station)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_plot_sta = QVBoxLayout()
        self.verticalLayout_plot_sta.setObjectName(u"verticalLayout_plot_sta")

        self.verticalLayout_22.addLayout(self.verticalLayout_plot_sta)


        self.verticalLayout_35.addWidget(self.groupBox_plot_station)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.groupBox_plot_sta_axis = QGroupBox(self.page_plot_station)
        self.groupBox_plot_sta_axis.setObjectName(u"groupBox_plot_sta_axis")
        self.groupBox_plot_sta_axis.setFont(font)
        self.horizontalLayout_38 = QHBoxLayout(self.groupBox_plot_sta_axis)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(-1, -1, 9, 150)
        self.verticalLayout_32 = QVBoxLayout()
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.label_51 = QLabel(self.groupBox_plot_sta_axis)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font)

        self.verticalLayout_32.addWidget(self.label_51)

        self.label_52 = QLabel(self.groupBox_plot_sta_axis)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font)

        self.verticalLayout_32.addWidget(self.label_52)


        self.horizontalLayout_38.addLayout(self.verticalLayout_32)

        self.verticalLayout_33 = QVBoxLayout()
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.comboBox_plot_sta_x = QComboBox(self.groupBox_plot_sta_axis)
        self.comboBox_plot_sta_x.addItem("")
        self.comboBox_plot_sta_x.setObjectName(u"comboBox_plot_sta_x")

        self.verticalLayout_33.addWidget(self.comboBox_plot_sta_x)

        self.comboBox_plot_sta_y = QComboBox(self.groupBox_plot_sta_axis)
        self.comboBox_plot_sta_y.addItem("")
        self.comboBox_plot_sta_y.addItem("")
        self.comboBox_plot_sta_y.addItem("")
        self.comboBox_plot_sta_y.addItem("")
        self.comboBox_plot_sta_y.addItem("")
        self.comboBox_plot_sta_y.setObjectName(u"comboBox_plot_sta_y")

        self.verticalLayout_33.addWidget(self.comboBox_plot_sta_y)


        self.horizontalLayout_38.addLayout(self.verticalLayout_33)


        self.horizontalLayout_40.addWidget(self.groupBox_plot_sta_axis)

        self.verticalLayout_34 = QVBoxLayout()
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(50, -1, -1, -1)
        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.pushButton_plot_sta_sub = QPushButton(self.page_plot_station)
        self.pushButton_plot_sta_sub.setObjectName(u"pushButton_plot_sta_sub")

        self.horizontalLayout_39.addWidget(self.pushButton_plot_sta_sub)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_39.addItem(self.horizontalSpacer_27)

        self.label_53 = QLabel(self.page_plot_station)
        self.label_53.setObjectName(u"label_53")

        self.horizontalLayout_39.addWidget(self.label_53)

        self.pushButton_plot_sta_add = QPushButton(self.page_plot_station)
        self.pushButton_plot_sta_add.setObjectName(u"pushButton_plot_sta_add")

        self.horizontalLayout_39.addWidget(self.pushButton_plot_sta_add)


        self.verticalLayout_34.addLayout(self.horizontalLayout_39)

        self.listWidget_plot_station = QListWidget(self.page_plot_station)
        self.listWidget_plot_station.setObjectName(u"listWidget_plot_station")
        self.listWidget_plot_station.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget_plot_station.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout_34.addWidget(self.listWidget_plot_station)


        self.horizontalLayout_40.addLayout(self.verticalLayout_34)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_40.addItem(self.horizontalSpacer_11)


        self.verticalLayout_35.addLayout(self.horizontalLayout_40)

        self.stackedWidget.addWidget(self.page_plot_station)
        self.page_plot_result = QWidget()
        self.page_plot_result.setObjectName(u"page_plot_result")
        self.verticalLayout_52 = QVBoxLayout(self.page_plot_result)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.groupBox_plot_result = QGroupBox(self.page_plot_result)
        self.groupBox_plot_result.setObjectName(u"groupBox_plot_result")
        sizePolicy.setHeightForWidth(self.groupBox_plot_result.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_result.setSizePolicy(sizePolicy)
        self.groupBox_plot_result.setMinimumSize(QSize(0, 400))
        self.verticalLayout_36 = QVBoxLayout(self.groupBox_plot_result)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_plot_result = QVBoxLayout()
        self.verticalLayout_plot_result.setObjectName(u"verticalLayout_plot_result")

        self.verticalLayout_36.addLayout(self.verticalLayout_plot_result)


        self.verticalLayout_52.addWidget(self.groupBox_plot_result)

        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.groupBox_plot_result_axis = QGroupBox(self.page_plot_result)
        self.groupBox_plot_result_axis.setObjectName(u"groupBox_plot_result_axis")
        self.groupBox_plot_result_axis.setFont(font)
        self.horizontalLayout_43 = QHBoxLayout(self.groupBox_plot_result_axis)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(-1, -1, -1, 130)
        self.verticalLayout_40 = QVBoxLayout()
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.label_49 = QLabel(self.groupBox_plot_result_axis)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font)

        self.verticalLayout_40.addWidget(self.label_49)

        self.label_50 = QLabel(self.groupBox_plot_result_axis)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font)

        self.verticalLayout_40.addWidget(self.label_50)


        self.horizontalLayout_43.addLayout(self.verticalLayout_40)

        self.verticalLayout_50 = QVBoxLayout()
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.comboBox_plot_result_x = QComboBox(self.groupBox_plot_result_axis)
        self.comboBox_plot_result_x.addItem("")
        self.comboBox_plot_result_x.setObjectName(u"comboBox_plot_result_x")

        self.verticalLayout_50.addWidget(self.comboBox_plot_result_x)

        self.comboBox_plot_result_y = QComboBox(self.groupBox_plot_result_axis)
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.addItem("")
        self.comboBox_plot_result_y.setObjectName(u"comboBox_plot_result_y")

        self.verticalLayout_50.addWidget(self.comboBox_plot_result_y)


        self.horizontalLayout_43.addLayout(self.verticalLayout_50)


        self.horizontalLayout_55.addWidget(self.groupBox_plot_result_axis)

        self.listWidget_plot_result = QListWidget(self.page_plot_result)
        self.listWidget_plot_result.setObjectName(u"listWidget_plot_result")
        self.listWidget_plot_result.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget_plot_result.setSelectionMode(QAbstractItemView.SingleSelection)

        self.horizontalLayout_55.addWidget(self.listWidget_plot_result)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_55.addItem(self.horizontalSpacer_7)


        self.verticalLayout_52.addLayout(self.horizontalLayout_55)

        self.stackedWidget.addWidget(self.page_plot_result)
        self.page_plot_glob_station = QWidget()
        self.page_plot_glob_station.setObjectName(u"page_plot_glob_station")
        self.verticalLayout_64 = QVBoxLayout(self.page_plot_glob_station)
        self.verticalLayout_64.setObjectName(u"verticalLayout_64")
        self.groupBox_plot_glob = QGroupBox(self.page_plot_glob_station)
        self.groupBox_plot_glob.setObjectName(u"groupBox_plot_glob")
        sizePolicy4.setHeightForWidth(self.groupBox_plot_glob.sizePolicy().hasHeightForWidth())
        self.groupBox_plot_glob.setSizePolicy(sizePolicy4)
        self.groupBox_plot_glob.setMinimumSize(QSize(0, 300))
        self.verticalLayout_63 = QVBoxLayout(self.groupBox_plot_glob)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.verticalLayout_plot_glob = QVBoxLayout()
        self.verticalLayout_plot_glob.setObjectName(u"verticalLayout_plot_glob")

        self.verticalLayout_63.addLayout(self.verticalLayout_plot_glob)


        self.verticalLayout_64.addWidget(self.groupBox_plot_glob)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.groupBox_8 = QGroupBox(self.page_plot_glob_station)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(150, 0))
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.radioButton_glob_trf = QRadioButton(self.groupBox_8)
        self.radioButton_glob_trf.setObjectName(u"radioButton_glob_trf")
        self.radioButton_glob_trf.setChecked(True)

        self.verticalLayout_14.addWidget(self.radioButton_glob_trf)

        self.radioButton_glob_crf = QRadioButton(self.groupBox_8)
        self.radioButton_glob_crf.setObjectName(u"radioButton_glob_crf")

        self.verticalLayout_14.addWidget(self.radioButton_glob_crf)


        self.horizontalLayout_34.addWidget(self.groupBox_8)

        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_5)

        self.groupBox_16 = QGroupBox(self.page_plot_glob_station)
        self.groupBox_16.setObjectName(u"groupBox_16")
        sizePolicy1.setHeightForWidth(self.groupBox_16.sizePolicy().hasHeightForWidth())
        self.groupBox_16.setSizePolicy(sizePolicy1)
        self.groupBox_16.setMinimumSize(QSize(150, 0))
        self.verticalLayout_69 = QVBoxLayout(self.groupBox_16)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.checkBox_plot_glob_x = QCheckBox(self.groupBox_16)
        self.checkBox_plot_glob_x.setObjectName(u"checkBox_plot_glob_x")
        self.checkBox_plot_glob_x.setChecked(True)

        self.verticalLayout_69.addWidget(self.checkBox_plot_glob_x)

        self.checkBox_plot_glob_y = QCheckBox(self.groupBox_16)
        self.checkBox_plot_glob_y.setObjectName(u"checkBox_plot_glob_y")
        self.checkBox_plot_glob_y.setChecked(True)

        self.verticalLayout_69.addWidget(self.checkBox_plot_glob_y)

        self.checkBox_plot_glob_z = QCheckBox(self.groupBox_16)
        self.checkBox_plot_glob_z.setObjectName(u"checkBox_plot_glob_z")
        self.checkBox_plot_glob_z.setChecked(True)

        self.verticalLayout_69.addWidget(self.checkBox_plot_glob_z)


        self.horizontalLayout_34.addWidget(self.groupBox_16)

        self.listWidget_plot_glob_trf = QListWidget(self.page_plot_glob_station)
        self.listWidget_plot_glob_trf.setObjectName(u"listWidget_plot_glob_trf")
        sizePolicy2.setHeightForWidth(self.listWidget_plot_glob_trf.sizePolicy().hasHeightForWidth())
        self.listWidget_plot_glob_trf.setSizePolicy(sizePolicy2)
        self.listWidget_plot_glob_trf.setMinimumSize(QSize(0, 200))

        self.horizontalLayout_34.addWidget(self.listWidget_plot_glob_trf)

        self.horizontalSpacer_41 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_41)

        self.groupBox_17 = QGroupBox(self.page_plot_glob_station)
        self.groupBox_17.setObjectName(u"groupBox_17")
        sizePolicy1.setHeightForWidth(self.groupBox_17.sizePolicy().hasHeightForWidth())
        self.groupBox_17.setSizePolicy(sizePolicy1)
        self.groupBox_17.setMinimumSize(QSize(150, 0))
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_17)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.checkBox_plot_glob_ra = QCheckBox(self.groupBox_17)
        self.checkBox_plot_glob_ra.setObjectName(u"checkBox_plot_glob_ra")
        self.checkBox_plot_glob_ra.setChecked(True)

        self.verticalLayout_15.addWidget(self.checkBox_plot_glob_ra)

        self.checkBox_plot_glob_de = QCheckBox(self.groupBox_17)
        self.checkBox_plot_glob_de.setObjectName(u"checkBox_plot_glob_de")
        self.checkBox_plot_glob_de.setChecked(True)

        self.verticalLayout_15.addWidget(self.checkBox_plot_glob_de)


        self.horizontalLayout_34.addWidget(self.groupBox_17)

        self.listWidget_plot_glob_crf = QListWidget(self.page_plot_glob_station)
        self.listWidget_plot_glob_crf.setObjectName(u"listWidget_plot_glob_crf")
        sizePolicy2.setHeightForWidth(self.listWidget_plot_glob_crf.sizePolicy().hasHeightForWidth())
        self.listWidget_plot_glob_crf.setSizePolicy(sizePolicy2)

        self.horizontalLayout_34.addWidget(self.listWidget_plot_glob_crf)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_18)


        self.verticalLayout_64.addLayout(self.horizontalLayout_34)

        self.stackedWidget.addWidget(self.page_plot_glob_station)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_25)

        self.pushButton_glob_run = QPushButton(self.centralwidget)
        self.pushButton_glob_run.setObjectName(u"pushButton_glob_run")

        self.horizontalLayout.addWidget(self.pushButton_glob_run)

        self.pushButton_process = QPushButton(self.centralwidget)
        self.pushButton_process.setObjectName(u"pushButton_process")
        self.pushButton_process.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.pushButton_process.sizePolicy().hasHeightForWidth())
        self.pushButton_process.setSizePolicy(sizePolicy6)
        self.pushButton_process.setMaximumSize(QSize(50, 16777215))
        icon32 = QIcon()
        icon32.addFile(u":/icons/icons/run.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_process.setIcon(icon32)
        self.pushButton_process.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButton_process)


        self.verticalLayout.addLayout(self.horizontalLayout)

        GASV.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(GASV)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1447, 24))
        self.menubar.setFont(font)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        self.menuParam = QMenu(self.menubar)
        self.menuParam.setObjectName(u"menuParam")
        self.menuParam.setFont(font)
        self.menuData = QMenu(self.menubar)
        self.menuData.setObjectName(u"menuData")
        self.menuData.setFont(font)
        self.menuEst = QMenu(self.menubar)
        self.menuEst.setObjectName(u"menuEst")
        self.menuEst.setFont(font)
        self.menuPlot = QMenu(self.menubar)
        self.menuPlot.setObjectName(u"menuPlot")
        self.menuPlot.setFont(font)
        self.menuGlob = QMenu(self.menubar)
        self.menuGlob.setObjectName(u"menuGlob")
        self.menuGlob.setFont(font)
        GASV.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(GASV)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setFont(font)
        GASV.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuParam.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuEst.menuAction())
        self.menubar.addAction(self.menuGlob.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.menuFile.addAction(self.menu_file_welcome)
        self.menuFile.addAction(self.menu_file_preference)
        self.menuFile.addAction(self.menu_file_input)
        self.menuFile.addAction(self.menu_file_dblist)
        self.menuFile.addAction(self.menu_file_exit)
        self.menuParam.addAction(self.menu_param_basic)
        self.menuData.addAction(self.menu_data_Baseline)
        self.menuData.addAction(self.menu_data_Station)
        self.menuData.addAction(self.menu_data_Source)
        self.menuEst.addAction(self.menu_est_clktrop)
        self.menuEst.addAction(self.menu_est_EOP)
        self.menuPlot.addAction(self.menu_plot_residual)
        self.menuPlot.addAction(self.menu_plot_station)
        self.menuPlot.addAction(self.menu_plot_result)
        self.menuPlot.addAction(self.menu_plot_glob)
        self.menuGlob.addAction(self.menu_glob_setup)
        self.menuGlob.addAction(self.menu_glob_station)
        self.menuGlob.addAction(self.menu_glob_source)

        self.retranslateUi(GASV)

        self.stackedWidget.setCurrentIndex(12)


        QMetaObject.connectSlotsByName(GASV)
    # setupUi

    def retranslateUi(self, GASV):
        GASV.setWindowTitle(QCoreApplication.translate("GASV", u"GASV", None))
        self.menu_file_welcome.setText(QCoreApplication.translate("GASV", u"Welcome", None))
#if QT_CONFIG(shortcut)
        self.menu_file_welcome.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.menu_plot_residual.setText(QCoreApplication.translate("GASV", u"Residual", None))
#if QT_CONFIG(shortcut)
        self.menu_plot_residual.setShortcut(QCoreApplication.translate("GASV", u"Alt+R", None))
#endif // QT_CONFIG(shortcut)
        self.menu_plot_station.setText(QCoreApplication.translate("GASV", u"Station", None))
#if QT_CONFIG(shortcut)
        self.menu_plot_station.setShortcut(QCoreApplication.translate("GASV", u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.menu_plot_result.setText(QCoreApplication.translate("GASV", u"Result", None))
#if QT_CONFIG(shortcut)
        self.menu_plot_result.setShortcut(QCoreApplication.translate("GASV", u"Alt+O", None))
#endif // QT_CONFIG(shortcut)
        self.menu_est_clktrop.setText(QCoreApplication.translate("GASV", u"Clock_TRP", None))
#if QT_CONFIG(shortcut)
        self.menu_est_clktrop.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+T", None))
#endif // QT_CONFIG(shortcut)
        self.menu_est_EOP.setText(QCoreApplication.translate("GASV", u"EOP_TRF_CRF", None))
#if QT_CONFIG(shortcut)
        self.menu_est_EOP.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.menu_data_Station.setText(QCoreApplication.translate("GASV", u"Station", None))
#if QT_CONFIG(shortcut)
        self.menu_data_Station.setShortcut(QCoreApplication.translate("GASV", u"Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.menu_data_Baseline.setText(QCoreApplication.translate("GASV", u"Baseline", None))
#if QT_CONFIG(shortcut)
        self.menu_data_Baseline.setShortcut(QCoreApplication.translate("GASV", u"Shift+B", None))
#endif // QT_CONFIG(shortcut)
        self.menu_data_Source.setText(QCoreApplication.translate("GASV", u"Source", None))
#if QT_CONFIG(shortcut)
        self.menu_data_Source.setShortcut(QCoreApplication.translate("GASV", u"Shift+Q", None))
#endif // QT_CONFIG(shortcut)
        self.menu_file_preference.setText(QCoreApplication.translate("GASV", u"Preference", None))
#if QT_CONFIG(shortcut)
        self.menu_file_preference.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.menu_file_input.setText(QCoreApplication.translate("GASV", u"vgosDB input", None))
#if QT_CONFIG(shortcut)
        self.menu_file_input.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.menu_file_exit.setText(QCoreApplication.translate("GASV", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.menu_file_exit.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.menu_param_basic.setText(QCoreApplication.translate("GASV", u"Setup", None))
#if QT_CONFIG(shortcut)
        self.menu_param_basic.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.menu_file_datadownload.setText(QCoreApplication.translate("GASV", u"Database", None))
        self.menu_glob_setup.setText(QCoreApplication.translate("GASV", u"Setup", None))
        self.menu_glob_station.setText(QCoreApplication.translate("GASV", u"Station", None))
        self.menu_glob_source.setText(QCoreApplication.translate("GASV", u"Source", None))
        self.actionLocation.setText(QCoreApplication.translate("GASV", u"Location", None))
        self.actionStation.setText(QCoreApplication.translate("GASV", u"Station", None))
        self.actionSource.setText(QCoreApplication.translate("GASV", u"Source", None))
        self.menu_plot_glob.setText(QCoreApplication.translate("GASV", u"Glob", None))
#if QT_CONFIG(shortcut)
        self.menu_plot_glob.setShortcut(QCoreApplication.translate("GASV", u"Alt+G", None))
#endif // QT_CONFIG(shortcut)
        self.menu_file_dblist.setText(QCoreApplication.translate("GASV", u"DBList", None))
#if QT_CONFIG(shortcut)
        self.menu_file_dblist.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.menu_param_exclude.setText(QCoreApplication.translate("GASV", u"Exclude", None))
        self.label.setText(QCoreApplication.translate("GASV", u"Welcome to VLBI analysis software for Geodesy and Astrometry (GASV)", None))
        self.label_37.setText(QCoreApplication.translate("GASV", u"links:", None))
        self.label_iers.setText(QCoreApplication.translate("GASV", u"<html><head/><body><p><a href=\"https://www.iers.org/IERS/EN/Home/home_node.html\"><span style=\" font-size:12pt; text-decoration: underline; color:#0000ff;\">IERS</span></a></p></body></html>", None))
        self.label_ivs.setText(QCoreApplication.translate("GASV", u"<html><head/><body><p><a href=\"https://ivscc.gsfc.nasa.gov/\"><span style=\" text-decoration: underline; color:#0000ff;\">IVS</span></a></p></body></html>", None))
        self.label_itrf.setText(QCoreApplication.translate("GASV", u"<html><head/><body><p><a href=\"https://itrf.ign.fr/en/homepage\"><span style=\" font-size:12pt; text-decoration: underline; color:#0000ff;\">ITRF</span></a></p></body></html>", None))
        self.textBrowser.setHtml(QCoreApplication.translate("GASV", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Times New Roman','Times New Roman'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-weight:600;\">Manual:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-weight:600;\">  </span><span style=\" font-family:'Sans Serif'; font-style:italic;\">File"
                        " menu     :</span><span style=\" font-family:'Sans Serif'; font-weight:600;\"> </span><span style=\" font-family:'Sans Serif';\">apriori</span><span style=\" font-family:'Sans Serif'; font-weight:600;\"> </span><span style=\" font-family:'Sans Serif';\">path setup and vgosDB data load.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">  </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">  </span><span style=\" font-family:'Sans Serif'; font-style:italic;\">Param menu    :</span><span style=\" font-family:'Sans Serif';\"> mode setup and certain observatin category select.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><b"
                        "r /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">  </span><span style=\" font-family:'Sans Serif'; font-style:italic;\">Observe menu  :</span><span style=\" font-family:'Sans Serif';\"> list the obsere station, baseline and source.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">  </span><span style=\" font-family:'Sans Serif'; font-style:italic;\">Estimate menu :</span><span style=\" font-family:'Sans Serif';\"> the clock, troposphere, TRF and CRF parameter set.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-"
                        "right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">  </span><span style=\" font-family:'Sans Serif'; font-style:italic;\">Glob menu     :</span><span style=\" font-family:'Sans Serif';\"> golbal solution set.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">  </span><span style=\" font-family:'Sans Serif'; font-style:italic;\">Plot menu     :</span><span style=\" font-family:'Sans Serif';\"> plot the residual and result.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bott"
                        "om:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">  </span><span style=\" font-family:'Sans Serif'; font-style:italic;\">Shutcut:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-style:italic;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-style:italic;\">	Ctrl+space : process</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-style:italic;\"><br /></p>\n"
"<p style=\""
                        " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-weight:600;\">Tips:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-style:italic;\">First, check the path in File/Preference and save;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-style:italic;\">Then, load data and process.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\""
                        "><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-weight:600;\">Version:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">This software is still in under development! Currently can analysis VLBI data, future will analysis SLR data.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><sp"
                        "an style=\" font-family:'Ubuntu';\">If you find any bugs or if you have great ideas what could be improved, </span><span style=\" font-family:'Ubuntu'; font-weight:600;\">raise an issue</span><span style=\" font-family:'Ubuntu';\"> to yaodang@ntsc.ac.cn, thank you!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Ubuntu';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-weight:600;\">Reference:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-f"
                        "amily:'MS Shell Dlg 2';\">If you use our software and write a paper, it would be nice if you would cite us. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2';\">Current reference:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-weight:600;\">License:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-b"
                        "lock-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2';\">VLBI analysis software for Geodesy and Astrometry (GASV)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2';\">Copyright (C) 2023  Dang Yao</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2';\">This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public Lice"
                        "nse as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2';\">You should have received a copy of the GNU General Public License along with this program.</span></p></body></html>", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("GASV", u"Input Path", None))
        self.label_18.setText(QCoreApplication.translate("GASV", u"DataPath", None))
        self.comboBox_dataType.setItemText(0, QCoreApplication.translate("GASV", u"vgosDB", None))
        self.comboBox_dataType.setItemText(1, QCoreApplication.translate("GASV", u"NGS", None))
        self.comboBox_dataType.setItemText(2, QCoreApplication.translate("GASV", u"other", None))

        self.pushButton_browse_vgosdb.setText("")
        self.label_17.setText(QCoreApplication.translate("GASV", u"Master    ", None))
        self.pushButton_browse_master.setText("")
        self.label_19.setText(QCoreApplication.translate("GASV", u"Apriori   ", None))
        self.pushButton_browse_apriori.setText("")
        self.label_39.setText(QCoreApplication.translate("GASV", u"Station:   ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_param_Station.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Contain the sit position and velocity</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit_param_Station.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.lineEdit_param_Station.setText("")
        self.pushButton_browse_station.setText("")
        self.label_40.setText(QCoreApplication.translate("GASV", u"Source:   ", None))
        self.lineEdit_param_Source.setText("")
        self.pushButton_browse_source.setText("")
        self.label_41.setText(QCoreApplication.translate("GASV", u"EOP:      ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_param_EOP.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Can be C04 or USNO finals</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_param_EOP.setText("")
        self.pushButton_browse_eop.setText("")
        self.label_42.setText(QCoreApplication.translate("GASV", u"EPHEM:", None))
        self.lineEdit_param_EPHEM.setText("")
        self.pushButton_browse_ephem.setText("")
        self.pushButton_param_questions.setText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("GASV", u"Output Path", None))
        self.label_22.setText(QCoreApplication.translate("GASV", u"Residual  ", None))
        self.pushButton_browse_residual.setText("")
        self.label_23.setText(QCoreApplication.translate("GASV", u"Report     ", None))
        self.pushButton_browse_report.setText("")
        self.label_24.setText(QCoreApplication.translate("GASV", u"SNX        ", None))
        self.pushButton_browse_snx.setText("")
        self.label_25.setText(QCoreApplication.translate("GASV", u"EOPO     ", None))
        self.pushButton_browse_eopo.setText("")
        self.label_6.setText(QCoreApplication.translate("GASV", u"ARC        ", None))
        self.pushButton_browse_arcpath.setText("")
        self.label_61.setText(QCoreApplication.translate("GASV", u"Analysis Centre", None))
#if QT_CONFIG(tooltip)
        self.pushButton_file_save.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>(ctrl+s)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_file_save.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_file_save.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox_10.setTitle("")
        self.label_2.setText(QCoreApplication.translate("GASV", u"Start year:", None))
        self.label_5.setText(QCoreApplication.translate("GASV", u"Stop year:", None))
        self.pushButton_file_refresh.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_file_makearc.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p><span style=\" font-size:12pt;\">create process list</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_file_makearc.setText("")
        ___qtablewidgetitem = self.tableWidget_session.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("GASV", u"Num.", None));
        ___qtablewidgetitem1 = self.tableWidget_session.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("GASV", u"DName", None));
        ___qtablewidgetitem2 = self.tableWidget_session.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("GASV", u"SName", None));
        ___qtablewidgetitem3 = self.tableWidget_session.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("GASV", u"STime", None));
        ___qtablewidgetitem4 = self.tableWidget_session.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("GASV", u"Version", None));
        ___qtablewidgetitem5 = self.tableWidget_session.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("GASV", u"AC", None));
        ___qtablewidgetitem6 = self.tableWidget_session.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("GASV", u"Used Obs.", None));
        ___qtablewidgetitem7 = self.tableWidget_session.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("GASV", u"WRMS(ps)", None));
        ___qtablewidgetitem8 = self.tableWidget_session.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("GASV", u"Station", None));
        self.pushButton_file_typesub.setText(QCoreApplication.translate("GASV", u"-", None))
        self.pushButton_file_typeadd.setText(QCoreApplication.translate("GASV", u"+", None))

        __sortingEnabled = self.listWidget_datatype.isSortingEnabled()
        self.listWidget_datatype.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget_datatype.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("GASV", u"IVS_R", None));
        ___qlistwidgetitem1 = self.listWidget_datatype.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("GASV", u"AOV", None));
        ___qlistwidgetitem2 = self.listWidget_datatype.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("GASV", u"APSG", None));
        ___qlistwidgetitem3 = self.listWidget_datatype.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("GASV", u"AUA", None));
        ___qlistwidgetitem4 = self.listWidget_datatype.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("GASV", u"AUM", None));
        ___qlistwidgetitem5 = self.listWidget_datatype.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("GASV", u"VGOS_24h", None));
        ___qlistwidgetitem6 = self.listWidget_datatype.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("GASV", u"TRF", None));
        ___qlistwidgetitem7 = self.listWidget_datatype.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("GASV", u"CRF", None));
        ___qlistwidgetitem8 = self.listWidget_datatype.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("GASV", u"CONT", None));
        ___qlistwidgetitem9 = self.listWidget_datatype.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("GASV", u"24h_other", None));
        ___qlistwidgetitem10 = self.listWidget_datatype.item(10)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("GASV", u"INT0", None));
        ___qlistwidgetitem11 = self.listWidget_datatype.item(11)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("GASV", u"INT1", None));
        ___qlistwidgetitem12 = self.listWidget_datatype.item(12)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("GASV", u"INT2", None));
        ___qlistwidgetitem13 = self.listWidget_datatype.item(13)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("GASV", u"INT3", None));
        ___qlistwidgetitem14 = self.listWidget_datatype.item(14)
        ___qlistwidgetitem14.setText(QCoreApplication.translate("GASV", u"VGOS_1h", None));
        ___qlistwidgetitem15 = self.listWidget_datatype.item(15)
        ___qlistwidgetitem15.setText(QCoreApplication.translate("GASV", u"1h_other", None));
        ___qlistwidgetitem16 = self.listWidget_datatype.item(16)
        ___qlistwidgetitem16.setText(QCoreApplication.translate("GASV", u"other", None));
        self.listWidget_datatype.setSortingEnabled(__sortingEnabled)

        self.textBrowser_file_obs.setHtml(QCoreApplication.translate("GASV", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Times New Roman','Times New Roman'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Times New Roman','Times New Roman','Times New Roman','Times New Roman','Times New Roman','Times New Roman','Times New Roman','Times New Roman'; font-size:16pt; font-weight:600; font-style:italic;\">Note:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic; color:#000000;\">IVS_R</span><span style=\" font-style:italic;\">: IVS R1/R4/RD</span></"
                        "p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic; color:#000000;\">AOV</span><span style=\" font-style:italic;\">: Asia-Oceania  Obs.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">APSG</span><span style=\" font-style:italic;\">: Asia-Pacific Obs.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; marg"
                        "in-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">AUA</span><span style=\" font-style:italic;\">: Southern Obs.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">AUM</span><span style=\" font-style:italic;\">: Southern mix Obs.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; t"
                        "ext-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">VGOS_24h</span><span style=\" font-style:italic;\">: VGOS 24h Obs.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">TRF:</span><span style=\" font-style:italic;\"> 24h Obs to monitor TRF</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" styl"
                        "e=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">CRF</span><span style=\" font-style:italic;\">: 24h Obs to monitor TRF</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">CONT:</span><span style=\" font-style:italic;\"> 15 days continue Obs.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px"
                        "; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">24h_other</span><span style=\" font-style:italic;\">: Other 24h Obs.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">INT0-3</span><span style=\" font-style:italic;\">: IVS 1h UT1</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:"
                        "italic;\">VGOS_1h</span><span style=\" font-style:italic;\">: VGOS 1h UT1</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">1h_other:</span><span style=\" font-style:italic;\"> Other 1h UT1</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">other:</span><span style=\" font-style:italic;\"> not show in master</span>"
                        "</p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:italic;\"><br /></p></body></html>", None))
        self.groupBox_staCorrect.setTitle(QCoreApplication.translate("GASV", u"Station Correct:", None))
        self.checkBox_staCor_solid.setText(QCoreApplication.translate("GASV", u"Solid Earth tides", None))
        self.checkBox_staCor_ocean.setText(QCoreApplication.translate("GASV", u"Ocean tides loading", None))
        self.checkBox_staCor_pole.setText(QCoreApplication.translate("GASV", u"Pole tide", None))
        self.checkBox_staCor_oceanpole.setText(QCoreApplication.translate("GASV", u"Ocean pole tide", None))
        self.checkBox.setText(QCoreApplication.translate("GASV", u"Atm. S1-S2 loading", None))
        self.groupBox_eophf.setTitle(QCoreApplication.translate("GASV", u"ERP HF", None))
        self.checkBox_setup_hfeop.setText(QCoreApplication.translate("GASV", u"Used", None))
        self.radioButton_eophf_desai.setText(QCoreApplication.translate("GASV", u"Desai", None))
        self.radioButton_eophf_iers.setText(QCoreApplication.translate("GASV", u"IERS", None))
        self.label_28.setText(QCoreApplication.translate("GASV", u"use observations with quality code", None))
        self.radioButton_param_outlier.setText(QCoreApplication.translate("GASV", u"Threshold for outliers(in sigmas)", None))
        self.lineEdit_param_outlier.setText(QCoreApplication.translate("GASV", u"3.0", None))
        self.label_3.setText(QCoreApplication.translate("GASV", u"Troposphere Mapping Function", None))
        self.comboBox_setup_mpf.setItemText(0, QCoreApplication.translate("GASV", u"GPT3", None))
        self.comboBox_setup_mpf.setItemText(1, QCoreApplication.translate("GASV", u"VMF1", None))

        ___qtablewidgetitem9 = self.table_data_station.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("GASV", u"Idx", None));
        ___qtablewidgetitem10 = self.table_data_station.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("GASV", u"Name", None));
        ___qtablewidgetitem11 = self.table_data_station.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("GASV", u"Tot. Obs", None));
        ___qtablewidgetitem12 = self.table_data_station.horizontalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("GASV", u"Use Obs", None));
        ___qtablewidgetitem13 = self.table_data_station.horizontalHeaderItem(4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("GASV", u"Clk Brk", None));
        ___qtablewidgetitem14 = self.table_data_station.horizontalHeaderItem(5)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("GASV", u"Clk Ref", None));
        ___qtablewidgetitem15 = self.table_data_station.horizontalHeaderItem(6)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("GASV", u"Omit", None));
        ___qtablewidgetitem16 = self.table_data_station.horizontalHeaderItem(7)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("GASV", u"Est", None));
        ___qtablewidgetitem17 = self.table_data_station.horizontalHeaderItem(8)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("GASV", u"NNRT", None));
        ___qtablewidgetitem18 = self.table_data_bl.horizontalHeaderItem(0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("GASV", u"Idx", None));
        ___qtablewidgetitem19 = self.table_data_bl.horizontalHeaderItem(1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("GASV", u"Name", None));
        ___qtablewidgetitem20 = self.table_data_bl.horizontalHeaderItem(2)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("GASV", u"Tot.Obs", None));
        ___qtablewidgetitem21 = self.table_data_bl.horizontalHeaderItem(3)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("GASV", u"Use Obs", None));
        ___qtablewidgetitem22 = self.table_data_bl.horizontalHeaderItem(4)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("GASV", u"Est Clk", None));
        ___qtablewidgetitem23 = self.table_data_bl.horizontalHeaderItem(5)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("GASV", u"Omit", None));
        ___qtablewidgetitem24 = self.table_data_source.horizontalHeaderItem(0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("GASV", u"IDx", None));
        ___qtablewidgetitem25 = self.table_data_source.horizontalHeaderItem(1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("GASV", u"Name", None));
        ___qtablewidgetitem26 = self.table_data_source.horizontalHeaderItem(2)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("GASV", u"Tot. Obs", None));
        ___qtablewidgetitem27 = self.table_data_source.horizontalHeaderItem(3)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("GASV", u"Use Obs", None));
        ___qtablewidgetitem28 = self.table_data_source.horizontalHeaderItem(4)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("GASV", u"Status", None));
        ___qtablewidgetitem29 = self.table_data_source.horizontalHeaderItem(5)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("GASV", u"Omit", None));
        ___qtablewidgetitem30 = self.table_data_source.horizontalHeaderItem(6)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("GASV", u"Est", None));
        ___qtablewidgetitem31 = self.table_data_source.horizontalHeaderItem(7)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("GASV", u"NNR", None));
        self.groupBox_6.setTitle(QCoreApplication.translate("GASV", u"Clock estimate", None))
        self.checkBox_est_clk.setText(QCoreApplication.translate("GASV", u"Estimate Clock", None))
        self.lineEdit_clk_interval.setText(QCoreApplication.translate("GASV", u"60", None))
        self.label_20.setText(QCoreApplication.translate("GASV", u"minutes", None))
        self.lineEdit_clk_constr.setText(QCoreApplication.translate("GASV", u"1.3", None))
        self.label_21.setText(QCoreApplication.translate("GASV", u"cm/minutes", None))
        self.label_26.setText(QCoreApplication.translate("GASV", u"Polynomial Num:", None))
        self.comboBox_clk_order.setItemText(0, QCoreApplication.translate("GASV", u"0", None))
        self.comboBox_clk_order.setItemText(1, QCoreApplication.translate("GASV", u"1", None))
        self.comboBox_clk_order.setItemText(2, QCoreApplication.translate("GASV", u"2", None))
        self.comboBox_clk_order.setItemText(3, QCoreApplication.translate("GASV", u"3", None))
        self.comboBox_clk_order.setItemText(4, QCoreApplication.translate("GASV", u"4", None))
        self.comboBox_clk_order.setItemText(5, QCoreApplication.translate("GASV", u"5", None))

        self.groupBox_7.setTitle(QCoreApplication.translate("GASV", u"Troposphere estimate", None))
        self.checkBox_est_wet.setText(QCoreApplication.translate("GASV", u"Estimate zenith wet delay", None))
        self.lineEdit_wet_interval.setText(QCoreApplication.translate("GASV", u"60", None))
        self.label_27.setText(QCoreApplication.translate("GASV", u"minutes", None))
        self.lineEdit_wet_constr.setText(QCoreApplication.translate("GASV", u"1.5", None))
        self.label_31.setText(QCoreApplication.translate("GASV", u"cm/minutes", None))
        self.checkBox_est_grad.setText(QCoreApplication.translate("GASV", u"Estimate north gradients", None))
        self.lineEdit_grad_interval.setText(QCoreApplication.translate("GASV", u"6", None))
        self.label_32.setText(QCoreApplication.translate("GASV", u"hours", None))
        self.label_10.setText(QCoreApplication.translate("GASV", u"Rel constraint:", None))
        self.lineEdit_grad_relconstr.setText(QCoreApplication.translate("GASV", u"0.05", None))
        self.label_33.setText(QCoreApplication.translate("GASV", u"cm/hours", None))
        self.label_16.setText(QCoreApplication.translate("GASV", u"Abs constraint:", None))
        self.lineEdit_grad_absconstr.setText(QCoreApplication.translate("GASV", u"0.2", None))
        self.label_34.setText(QCoreApplication.translate("GASV", u"cm/hours", None))
        self.groupBox_15.setTitle("")
        self.groupBox_mode.setTitle(QCoreApplication.translate("GASV", u"MODE", None))
        self.radioButton_est_eop_poly.setText(QCoreApplication.translate("GASV", u"POLY", None))
        self.radioButton_est_eop_cpwl.setText(QCoreApplication.translate("GASV", u"CPWL", None))
        self.groupBox_refTime.setTitle(QCoreApplication.translate("GASV", u"Referece Time", None))
        self.radioButton_est_reftime_MIDDEL.setText(QCoreApplication.translate("GASV", u"MIDDEL", None))
        self.radioButton_est_reftime_MIDNIGHT.setText(QCoreApplication.translate("GASV", u"MIDNIGHT", None))
        self.radioButton_est_reftime_NOON.setText(QCoreApplication.translate("GASV", u"NOON", None))
        self.groupBox_13.setTitle("")
        self.checkBox_est_pmxy.setText(QCoreApplication.translate("GASV", u"PM", None))
        self.lineEdit_pmxy_interval.setInputMask("")
        self.lineEdit_pmxy_interval.setText(QCoreApplication.translate("GASV", u"1440", None))
        self.label_9.setText(QCoreApplication.translate("GASV", u"minutes", None))
        self.lineEdit_pmxy_constr.setText(QCoreApplication.translate("GASV", u"0.0001", None))
        self.lineEdit_pmxy_constr_poly.setText(QCoreApplication.translate("GASV", u"45", None))
        self.label_11.setText(QCoreApplication.translate("GASV", u"mas      ", None))
        self.checkBox_est_ut1.setText(QCoreApplication.translate("GASV", u"UT1", None))
        self.lineEdit_ut1_interval.setText(QCoreApplication.translate("GASV", u"1440", None))
        self.label_8.setText(QCoreApplication.translate("GASV", u"minutes", None))
        self.lineEdit_ut1_constr.setText(QCoreApplication.translate("GASV", u"0.0001", None))
        self.lineEdit_ut1_constr_poly.setText(QCoreApplication.translate("GASV", u"3", None))
        self.label_13.setText(QCoreApplication.translate("GASV", u"ms        ", None))
        self.checkBox_est_rpmxy.setText(QCoreApplication.translate("GASV", u"PM rate", None))
        self.lineEdit_rpmxy_constr_poly.setText(QCoreApplication.translate("GASV", u"45", None))
        self.label_12.setText(QCoreApplication.translate("GASV", u"mas/day", None))
        self.checkBox_est_lod.setText(QCoreApplication.translate("GASV", u"LOD    ", None))
        self.lineEdit_lod_constr_poly.setText(QCoreApplication.translate("GASV", u"3", None))
        self.label_15.setText(QCoreApplication.translate("GASV", u"ms/day  ", None))
        self.checkBox_est_nutxy.setText(QCoreApplication.translate("GASV", u"Nutation", None))
        self.lineEdit_nut_constr_poly.setText(QCoreApplication.translate("GASV", u"3", None))
        self.label_14.setText(QCoreApplication.translate("GASV", u"mas       ", None))
        self.groupBox_14.setTitle("")
        self.groupBox_est_trf.setTitle(QCoreApplication.translate("GASV", u"TRF", None))
        self.checkBox_est_station.setText(QCoreApplication.translate("GASV", u"Estimate station coordinate", None))
        self.pushButton_autoset_station.setText(QCoreApplication.translate("GASV", u"Auto Set", None))
        self.label_68.setText(QCoreApplication.translate("GASV", u"Sigma:", None))
        self.lineEdit_sigma_sta.setText(QCoreApplication.translate("GASV", u"1", None))
        self.label_69.setText(QCoreApplication.translate("GASV", u"m", None))
        self.checkBox_est_nnr.setText(QCoreApplication.translate("GASV", u"NNR", None))
        self.label_63.setText(QCoreApplication.translate("GASV", u"Sigma:", None))
        self.lineEdit_sigma_stannr.setText(QCoreApplication.translate("GASV", u"1E-4", None))
        self.label_62.setText(QCoreApplication.translate("GASV", u"m", None))
        self.checkBox_est_nnt.setText(QCoreApplication.translate("GASV", u"NNT", None))
        self.label_64.setText(QCoreApplication.translate("GASV", u"Sigma:", None))
        self.lineEdit_sigma_stannt.setText(QCoreApplication.translate("GASV", u"1E-4", None))
        self.label_65.setText(QCoreApplication.translate("GASV", u"m", None))
        self.checkBox_nns.setText(QCoreApplication.translate("GASV", u"NNS", None))
        self.groupBox_est_crf.setTitle(QCoreApplication.translate("GASV", u"CRF", None))
        self.checkBox_est_source.setText(QCoreApplication.translate("GASV", u"Estimate source coordinate", None))
        self.pushButton_autoset_source.setText(QCoreApplication.translate("GASV", u"Auto Set", None))
        self.label_70.setText(QCoreApplication.translate("GASV", u"Sigma:", None))
        self.lineEdit_sigma_sou.setText(QCoreApplication.translate("GASV", u"1E-6", None))
        self.label_71.setText(QCoreApplication.translate("GASV", u"rad", None))
        self.checkBox_est_sounnr.setText(QCoreApplication.translate("GASV", u"NNR", None))
        self.label_66.setText(QCoreApplication.translate("GASV", u"Sigma:", None))
        self.lineEdit_sigma_sounnr.setText(QCoreApplication.translate("GASV", u"1E-10", None))
        self.label_67.setText(QCoreApplication.translate("GASV", u"rad", None))
        self.groupBox_12.setTitle("")
        self.label_57.setText(QCoreApplication.translate("GASV", u"SNXList", None))
        self.label_55.setText(QCoreApplication.translate("GASV", u"Include", None))
        self.label_7.setText(QCoreApplication.translate("GASV", u"Station", None))
        self.checkBox_glob_station_yes.setText("")
        self.label_36.setText(QCoreApplication.translate("GASV", u"Station velocity", None))
        self.checkBox_glob_station_velocity_yes.setText("")
        self.label_48.setText(QCoreApplication.translate("GASV", u"Source", None))
        self.checkBox_glob_source_yes.setText("")
        self.label_54.setText(QCoreApplication.translate("GASV", u"EOP", None))
        self.checkBox_glob_eop_yes.setText("")
        self.label_56.setText(QCoreApplication.translate("GASV", u"TRF NNR/NNT:", None))
        self.checkBox_glob_trf_nnrnnt.setText("")
        self.label_4.setText(QCoreApplication.translate("GASV", u"EXCEPT", None))
        self.lineEdit_glob_trf_nnrnnt.setText(QCoreApplication.translate("GASV", u"ITRF_NNRT.txt", None))
        self.pushButton_glob_edit_trf.setText("")
        self.label_58.setText(QCoreApplication.translate("GASV", u"CRF NNR:          ", None))
        self.checkBox_glob_crf_nnr.setText("")
        self.label_59.setText(QCoreApplication.translate("GASV", u"EXCEPT", None))
        self.lineEdit_glob_crf_nnr.setText(QCoreApplication.translate("GASV", u"ICRF3_NNR.txt", None))
        self.pushButton_glob_edit_crf.setText("")
        self.label_60.setText(QCoreApplication.translate("GASV", u"GLOB EXCLUDE", None))
        self.lineEdit_glob_station_exclude.setText(QCoreApplication.translate("GASV", u"GLOB_rm.txt", None))
        self.pushButton_glob_edit_globex.setText("")
        ___qtablewidgetitem32 = self.tableWidget_glob_station.horizontalHeaderItem(0)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("GASV", u"ID", None));
        ___qtablewidgetitem33 = self.tableWidget_glob_station.horizontalHeaderItem(1)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("GASV", u"Name", None));
        ___qtablewidgetitem34 = self.tableWidget_glob_station.horizontalHeaderItem(2)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("GASV", u"Tol. Obs.", None));
        ___qtablewidgetitem35 = self.tableWidget_glob_station.horizontalHeaderItem(3)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("GASV", u"Omit", None));
        ___qtablewidgetitem36 = self.tableWidget_glob_station.horizontalHeaderItem(4)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("GASV", u"NNRT", None));
        ___qtablewidgetitem37 = self.tableWidget_glob_source.horizontalHeaderItem(0)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("GASV", u"ID", None));
        ___qtablewidgetitem38 = self.tableWidget_glob_source.horizontalHeaderItem(1)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("GASV", u"Name", None));
        ___qtablewidgetitem39 = self.tableWidget_glob_source.horizontalHeaderItem(2)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("GASV", u"Tol. Obs.", None));
        ___qtablewidgetitem40 = self.tableWidget_glob_source.horizontalHeaderItem(3)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("GASV", u"Omit", None));
        ___qtablewidgetitem41 = self.tableWidget_glob_source.horizontalHeaderItem(4)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("GASV", u"NNR", None));
        self.pushButton_plot_S.setText(QCoreApplication.translate("GASV", u"S", None))
        self.pushButton_plot_X.setText(QCoreApplication.translate("GASV", u"X", None))
        self.label_result.setText("")
        self.groupBox_plot_res.setTitle("")
#if QT_CONFIG(tooltip)
        self.pushButton_plot_reload.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Reload the database</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_reload.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_plot_home.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Reset original view</p><p>(Shift+S)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_home.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_plot_home.setShortcut(QCoreApplication.translate("GASV", u"Shift+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_outlier.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Residual point select mode:</p><p>left mouse--selected</p><p>right mouse--unselected</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_outlier.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_plot_ambigCorr.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Ambiguity correct run</p><p>(Shift+A)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_ambigCorr.setText(QCoreApplication.translate("GASV", u"Ambig_C", None))
#if QT_CONFIG(shortcut)
        self.pushButton_plot_ambigCorr.setShortcut(QCoreApplication.translate("GASV", u"Shift+A", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_ambAdd.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>ambiguity space add</p><p>short cut: =</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_ambAdd.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_plot_ambAdd.setShortcut(QCoreApplication.translate("GASV", u"=", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_ambSub.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>ambiguity space subtraction</p><p>short cut: -</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_ambSub.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_plot_ambSub.setShortcut(QCoreApplication.translate("GASV", u"-", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_ambigZero.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Set the ambiguity correct to zeros</p><p>(Shift+Z)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_ambigZero.setText(QCoreApplication.translate("GASV", u"Ambig_0", None))
#if QT_CONFIG(shortcut)
        self.pushButton_plot_ambigZero.setShortcut(QCoreApplication.translate("GASV", u"Shift+Z", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_clkbk.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Clock break select mode</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_clkbk.setText(QCoreApplication.translate("GASV", u"Clk_break", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_ionCorr.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Correct ionosphere influence by doble frequency</p><p>the VGOS mode has remove the ionosphere! </p><p>(Shift+C)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_ionCorr.setText(QCoreApplication.translate("GASV", u"Ion_C", None))
#if QT_CONFIG(shortcut)
        self.pushButton_plot_ionCorr.setShortcut(QCoreApplication.translate("GASV", u"Shift+C", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_ionZero.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Set the ionosphere influence to zeros</p><p>(Shift+blank)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_ionZero.setText(QCoreApplication.translate("GASV", u"Ion_0", None))
#if QT_CONFIG(shortcut)
        self.pushButton_plot_ionZero.setShortcut(QCoreApplication.translate("GASV", u"Shift+Space", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_remove.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Remove the select point as outlier</p><p>(Shift+X)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_remove.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_plot_remove.setShortcut(QCoreApplication.translate("GASV", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_autoOut.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Auto remove the outlier by 3 wrms</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_autoOut.setText("")
#if QT_CONFIG(shortcut)
        self.pushButton_plot_autoOut.setShortcut(QCoreApplication.translate("GASV", u"Shift+F", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButton_plot_reweight.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>reweight the data based on baseline</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_reweight.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("GASV", u"Axis to plot", None))
        self.label_29.setText(QCoreApplication.translate("GASV", u"X:", None))
        self.label_30.setText(QCoreApplication.translate("GASV", u"Y:", None))
        self.comboBox_plot_x.setItemText(0, QCoreApplication.translate("GASV", u"Time (UTC)", None))

        self.comboBox_plot_y.setItemText(0, QCoreApplication.translate("GASV", u"Res: GR delay", None))
        self.comboBox_plot_y.setItemText(1, QCoreApplication.translate("GASV", u"Sigma of GR delay", None))
        self.comboBox_plot_y.setItemText(2, QCoreApplication.translate("GASV", u"Res: PH delay", None))
        self.comboBox_plot_y.setItemText(3, QCoreApplication.translate("GASV", u"SNR", None))

        self.groupBox.setTitle(QCoreApplication.translate("GASV", u"Data to plot", None))
        self.radioButton_plot_all.setText(QCoreApplication.translate("GASV", u"All", None))
        self.radioButton_plot_station.setText(QCoreApplication.translate("GASV", u"Station", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_resOmitSta.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>Remove the station data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_resOmitSta.setText("")
        self.radioButton_plot_baseline.setText(QCoreApplication.translate("GASV", u"Baseline", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_resOmitBL.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>remove the baseline data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_resOmitBL.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_plot_resAddBlClock.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>estimate the baseline clock</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_resAddBlClock.setText("")
        self.radioButton_plot_source.setText(QCoreApplication.translate("GASV", u"Source", None))
        self.pushButton_plot_resStaSub.setText(QCoreApplication.translate("GASV", u"-*", None))
        self.pushButton_plot_resStaAdd.setText(QCoreApplication.translate("GASV", u"*+", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_resOmitSou.setToolTip(QCoreApplication.translate("GASV", u"<html><head/><body><p>remove the baseline data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_resOmitSou.setText("")
        self.groupBox_11.setTitle(QCoreApplication.translate("GASV", u"Quick Mode", None))
        self.pushButton_plot_modeUT1.setText(QCoreApplication.translate("GASV", u"1h UT1", None))
        self.pushButton_plot_modeEOP.setText(QCoreApplication.translate("GASV", u"24h EOP", None))
        self.pushButton_plot_moderegular.setText(QCoreApplication.translate("GASV", u"Regular", None))
        self.pushButton_plot_modeClear.setText(QCoreApplication.translate("GASV", u"Clear", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("GASV", u"Out Select", None))
        self.checkBox_plot_report.setText(QCoreApplication.translate("GASV", u"Spool", None))
        self.checkBox_plot_eopout.setText(QCoreApplication.translate("GASV", u"EOP", None))
        self.checkBox_plot_snx.setText(QCoreApplication.translate("GASV", u"Sinex", None))
        self.checkBox_plot_vgosDb.setText(QCoreApplication.translate("GASV", u"vgosDb", None))
        self.label_35.setText("")
        self.pushButton_plot_save.setText("")
        self.groupBox_plot_station.setTitle("")
        self.groupBox_plot_sta_axis.setTitle(QCoreApplication.translate("GASV", u"Axis", None))
        self.label_51.setText(QCoreApplication.translate("GASV", u"X:", None))
        self.label_52.setText(QCoreApplication.translate("GASV", u"Y:", None))
        self.comboBox_plot_sta_x.setItemText(0, QCoreApplication.translate("GASV", u"Time (UTC)", None))

        self.comboBox_plot_sta_y.setItemText(0, QCoreApplication.translate("GASV", u"Temperature (C)", None))
        self.comboBox_plot_sta_y.setItemText(1, QCoreApplication.translate("GASV", u"Humidity (%)", None))
        self.comboBox_plot_sta_y.setItemText(2, QCoreApplication.translate("GASV", u"Pressure (mb)", None))
        self.comboBox_plot_sta_y.setItemText(3, QCoreApplication.translate("GASV", u"Cable Cal (ps)", None))
        self.comboBox_plot_sta_y.setItemText(4, QCoreApplication.translate("GASV", u"fmout-GPS (s)", None))

        self.pushButton_plot_sta_sub.setText(QCoreApplication.translate("GASV", u"-*", None))
        self.label_53.setText("")
        self.pushButton_plot_sta_add.setText(QCoreApplication.translate("GASV", u"*+", None))
        self.groupBox_plot_result.setTitle("")
        self.groupBox_plot_result_axis.setTitle(QCoreApplication.translate("GASV", u"Axis", None))
        self.label_49.setText(QCoreApplication.translate("GASV", u"X:", None))
        self.label_50.setText(QCoreApplication.translate("GASV", u"Y:", None))
        self.comboBox_plot_result_x.setItemText(0, QCoreApplication.translate("GASV", u"Time (UTC)", None))

        self.comboBox_plot_result_y.setItemText(0, QCoreApplication.translate("GASV", u"Station Clk (us)", None))
        self.comboBox_plot_result_y.setItemText(1, QCoreApplication.translate("GASV", u"Station ZWD (us)", None))
        self.comboBox_plot_result_y.setItemText(2, QCoreApplication.translate("GASV", u"Station Posit(m)", None))
        self.comboBox_plot_result_y.setItemText(3, QCoreApplication.translate("GASV", u"Baseline Clk (us)", None))
        self.comboBox_plot_result_y.setItemText(4, QCoreApplication.translate("GASV", u"UT1 (ms)", None))
        self.comboBox_plot_result_y.setItemText(5, QCoreApplication.translate("GASV", u"Polar_X (mas)", None))
        self.comboBox_plot_result_y.setItemText(6, QCoreApplication.translate("GASV", u"Polar_Y (mas)", None))
        self.comboBox_plot_result_y.setItemText(7, QCoreApplication.translate("GASV", u"Nutation (uas)", None))

        self.groupBox_plot_glob.setTitle("")
        self.groupBox_8.setTitle(QCoreApplication.translate("GASV", u"Choice", None))
        self.radioButton_glob_trf.setText(QCoreApplication.translate("GASV", u"TRF", None))
        self.radioButton_glob_crf.setText(QCoreApplication.translate("GASV", u"CRF", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("GASV", u"TRF", None))
        self.checkBox_plot_glob_x.setText(QCoreApplication.translate("GASV", u"axis-X", None))
        self.checkBox_plot_glob_y.setText(QCoreApplication.translate("GASV", u"axis-Y", None))
        self.checkBox_plot_glob_z.setText(QCoreApplication.translate("GASV", u"axis-Z", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("GASV", u"CRF", None))
        self.checkBox_plot_glob_ra.setText(QCoreApplication.translate("GASV", u"Ra", None))
        self.checkBox_plot_glob_de.setText(QCoreApplication.translate("GASV", u"De", None))
        self.pushButton_glob_run.setText(QCoreApplication.translate("GASV", u"Grun", None))
        self.pushButton_process.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("GASV", u"File", None))
        self.menuParam.setTitle(QCoreApplication.translate("GASV", u"Param", None))
        self.menuData.setTitle(QCoreApplication.translate("GASV", u"Observe", None))
        self.menuEst.setTitle(QCoreApplication.translate("GASV", u"Estimate", None))
        self.menuPlot.setTitle(QCoreApplication.translate("GASV", u"Plot", None))
        self.menuGlob.setTitle(QCoreApplication.translate("GASV", u"Glob", None))
    # retranslateUi

