# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, pyKafe Development Team
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys, time
from PyQt4 import QtCore, QtGui

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

class CurrencyConfig:
    prefix = ""
    suffix = " YTL"
    fixedPrice = 0.50
    tenMinutePrice = 10

class TimerThread(QtCore.QThread):
    def __init__(self, parent, ui, startTime, endTime, currencyConfig):
        QtCore.QThread.__init__(self, parent)
        self.startTime = startTime
        self.endTime = endTime
        self.currencyConfig = currencyConfig
        self.ui = ui
    def run(self):
        while True:
            time.sleep(1)
            self.do()
    def do(self):
        currentTime = QtCore.QDateTime.currentDateTime()
        usedTime = self.startTime.secsTo(currentTime)
        price = usedTime/6*self.currencyConfig.tenMinutePrice
        remainingTime = QtCore.QDateTime()
        if self.endTime.isValid():
            remainingTime.setTime_t(currentTime.secsTo(self.endTime))
        else:
            remainingTime.setTime_t(0)
        temp = usedTime
        usedTime = QtCore.QDateTime()
        usedTime.setTime_t(temp)
        print 1
        self.ui.timeLabel.setText(currentTime.time().toString("hh.mm") + "\n" +\
                               remainingTime.toUTC().time().toString("hh.mm") + "\n" +\
                               usedTime.toUTC().time().toString("hh.mm"))
        print 2

        if self.currencyConfig.fixedPrice < temp/6*self.currencyConfig.tenMinutePrice:
            self.ui.moneyLabel.setText(self.currencyConfig.prefix + str(price) + self.currencyConfig.suffix)
        else:
            self.ui.moneyLabel.setText(self.currencyConfig.prefix + str(self.currencyConfig.fixedPrice) + self.currencyConfig.suffix)
        print 3
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,216,465).size()).expandedTo(MainWindow.minimumSizeHint()))
        icon = QtGui.QIcon("../../data/icons/pyKafe.png")
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.logoutButton = QtGui.QPushButton(self.centralwidget)
        self.logoutButton.setObjectName("logoutButton")
        self.gridlayout.addWidget(self.logoutButton,1,0,1,1)

        self.cafeteriaButton = QtGui.QPushButton(self.centralwidget)
        self.cafeteriaButton.setObjectName("cafeteriaButton")
        self.gridlayout.addWidget(self.cafeteriaButton,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(20,81,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridlayout1 = QtGui.QGridLayout(self.frame)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.line = QtGui.QFrame(self.frame)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,2)

        self.moneyLabel = QtGui.QLabel(self.frame)
        self.moneyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.moneyLabel.setObjectName("moneyLabel")
        self.gridlayout1.addWidget(self.moneyLabel,2,0,1,2)

        self.timeLabel = QtGui.QLabel(self.frame)
        self.timeLabel.setObjectName("timeLabel")
        self.gridlayout1.addWidget(self.timeLabel,0,1,1,1)

        self.label = QtGui.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)
        self.gridlayout.addWidget(self.frame,3,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,216,29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.cafeteriaButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.logoutButton,QtCore.SIGNAL("clicked()"),sys.exit)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #tray things
        trayMenu = QtGui.QMenu("pyKafe", MainWindow)
        action = trayMenu.addAction(_("Exit"))
        QtCore.QObject.connect(action,QtCore.SIGNAL("triggered()"),sys.exit)
        self.trayIcon = QtGui.QSystemTrayIcon(icon, MainWindow)
        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.show()
        self.ui = MainWindow
        QtCore.QObject.connect(self.trayIcon, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.iconActivated)
        #TODO:
        #thread = TimerThread(MainWindow, self, QtCore.QDateTime.currentDateTime(), QtCore.QDateTime(), CurrencyConfig())
        #thread.start()
    def iconActivated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self.ui.isVisible():
                self.ui.hide()
            else:
                self.ui.show()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_("pyKafe"))
        self.logoutButton.setText(_("Logout"))
        self.cafeteriaButton.setText(_("Cafeteria"))
        self.moneyLabel.setText("0")
        self.timeLabel.setText("00.00\n00.00\n00.00")
        self.label.setText(_("Starting Time:\n") + _("Remaining Time:\n") + _("Used Time:"))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
