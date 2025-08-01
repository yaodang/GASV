# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_note.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(783, 566)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.label)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font)
        self.groupBox_4.setStyleSheet(u"color: rgb(0, 0, 255);")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet(u"color: rgb(0, 255, 127);")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"color: rgb(0, 255, 127);")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.label_3)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet(u"color: rgb(255, 170, 127);")

        self.verticalLayout_3.addWidget(self.groupBox_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Apriori file help", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Station file:", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Name X(m) Y(m) Z(m) Vx(m/yr) Vy(m/yr) Vz(m/yr) startMJD notes</p><p>for example:</p><p>GRASSE 4581697.4036 556126.1061 4389351.6728 -0.01390 0.01906 0.01100 57023 ITRF2020</p></body></html>", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Source file:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>#ICRF Designation        IERS Des. Inf.  Right Ascension       Declination</p><p>#                                       J2000.0               J2000.0 </p><p>#                                       h  m  s               o  '  &quot;</p><p>ICRF J000020.3-322101    2357-326       00 00 20.39997606    -32 21 01.2337415</p><p>ICRF J000027.0+030715    2357+028       00 00 27.02251377     03 07 15.6463606</p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"EOP file:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt;\">EOP file can be:</span></p><p><span style=\" font-size:12pt;\">IERS C04 14</span></p><p><span style=\" font-size:12pt;\">IERS C04 20</span></p><p><span style=\" font-size:12pt;\">USNO format</span></p></body></html>", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"EPHEM file:", None))
    # retranslateUi

