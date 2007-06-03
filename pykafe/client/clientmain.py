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

import sys, base64
from PyQt4 import QtCore, QtGui, QtNetwork
from config import PykafeConfiguration

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

config = PykafeConfiguration()

class SenderThread(QtCore.QThread):
    def __init__(self, parent, data):
        QtCore.QThread.__init__(self, parent)
        self.data = data
    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        tcpSocket.connectToHost(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), config.network_port)
        print "connecting to:", QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost).toString(), config.network_port
        tcpSocket.waitForConnected(-1)
        tcpSocket.write(base64.encodestring(self.data))
        tcpSocket.waitForBytesWritten()
        print "sent:", self.data
        tcpSocket.disconnectFromHost()

class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        self.tcpSocket.waitForReadyRead()
        data = base64.decodestring(self.tcpSocket.readAll())
        print "received:", data
        self.tcpSocket.disconnectFromHost()
        self.exec_()

class PykafeClientMain(QtNetwork.QTcpServer):
    def __init__(self, parent, ui):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.ui = ui
        self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), config.network_localPort)
        self.threads = []
    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor)
        QtCore.QObject.connect(thread,QtCore.SIGNAL("close"),self.parent().close)
        QtCore.QObject.connect(thread,QtCore.SIGNAL("message"),self.ui.statusbar.showMessage)
        thread.start()
        self.threads.append(thread)
    def sendMessage(self, data):
        thread = SenderThread(self.parent(), data)
        thread.start()
        self.threads.append(thread)
    def cafeteria(self):
        pass
    def logout(self):
        answer = QtGui.QMessageBox.question(self.parent(), _("Are you sure?"), _("Do you really want to logout?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            self.sendMessage("008")

class TimerThread(QtCore.QThread):
    def run(self):
        while True:
            tcpSocket = QtNetwork.QTcpSocket()
            tcpSocket.connectToHost(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), config.network_port)
            tcpSocket.waitForConnected()
            tcpSocket.write(base64.encodestring("017"))
            tcpSocket.waitForReadyRead()
            text = base64.decodestring(tcpSocket.readAll())
            text1, text2 = text.rsplit('|', 1)
            #there's a big problem here, somehow time returns "1" and money returns ""
            #TODO: fix it
            self.emit(QtCore.SIGNAL("changeTimeLabel"), text1)
            self.emit(QtCore.SIGNAL("changeMoneyLabel"), text2)
            self.sleep(60)

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
        self.server = PykafeClientMain(MainWindow, self)
        QtCore.QObject.connect(self.cafeteriaButton,QtCore.SIGNAL("clicked()"),self.server.cafeteria)
        QtCore.QObject.connect(self.logoutButton,QtCore.SIGNAL("clicked()"),self.server.logout)
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
        thread = TimerThread()
        QtCore.QObject.connect(thread,QtCore.SIGNAL("changeTimeLabel"),self.timeLabel.setText)
        QtCore.QObject.connect(thread,QtCore.SIGNAL("changeMoneyLabel"),self.moneyLabel.setText)
        thread.start()
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
        self.label.setText(_("Starting Time:") + "\n" + _("Remaining Time:") + "\n" + _("Used Time:"))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
