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

import base64, os, sys
from PyQt4 import QtCore, QtGui, QtNetwork
from config import PykafeConfiguration

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

class SenderThread(QtCore.QThread):
    def __init__(self, parent, data):
        QtCore.QThread.__init__(self, parent)
        self.data = data
    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        tcpSocket.connectToHost(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), PykafeConfiguration().network.port)
        print "connecting to:", QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost).toString(), PykafeConfiguration().network.port
        if not tcpSocket.waitForConnected(-1):
            print "error:", tcpSocket.errorString(), "sending exit signal"
            self.emit(QtCore.SIGNAL("exit()"))
        else:
            tcpSocket.write(base64.encodestring(self.data))
            tcpSocket.waitForBytesWritten()
            print "sent:", self.data
            tcpSocket.disconnectFromHost()

class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor, ui):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
        self.ui = ui
    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        data = base64.decodestring(self.tcpSocket.readAll())
        print "received:", data
        if data[:3] == "001":
            if data[3] == "1":
                os.system("pyKafeclient&")
                self.emit(QtCore.SIGNAL("close"))
            elif data[3] == "0":
                self.emit(QtCore.SIGNAL("message"), _("Server didn't give acknowledge"))
        elif data[:3] == "003":
            pass
        elif data[:3] == "005":
            os.system("pyKafeclient&")
            self.emit(QtCore.SIGNAL("close"))
        self.tcpSocket.disconnect()
        self.exec_()

class PykafeClient(QtNetwork.QTcpServer):
    def __init__(self, parent, ui):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.ui = ui
        self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), PykafeConfiguration().network.localPort)
        print "listening localhost on port:", PykafeConfiguration().network.localPort
        thread = SenderThread(self.parent(), "004")
        QtCore.QObject.connect(thread, QtCore.SIGNAL("exit()"), parent.close)
        thread.start()
        self.threads = [thread]
    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor, self.ui)
        QtCore.QObject.connect(thread,QtCore.SIGNAL("close"),self.ui.close)
        QtCore.QObject.connect(thread,QtCore.SIGNAL("message"),self.ui.statusbar.showMessage)
        thread.start()
        self.threads.append(thread)
        print "login has %d threads" % len(self.threads)
    def login(self):
        thread = SenderThread(self.parent(), "002" + self.ui.username.text + "|" + self.ui.password.text)
        thread.start()
        self.threads.append(thread)
    def request(self):
        thread = SenderThread(self.parent(), "000")
        thread.start()
        self.threads.append(thread)

class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("LoginWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,413,269).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,0,2,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,6,2,1,1)

        self.password = QtGui.QLineEdit(self.centralwidget)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridlayout.addWidget(self.password,3,2,1,1)

        self.textLabel = QtGui.QLabel(self.centralwidget)
        self.textLabel.setWordWrap(False)
        self.textLabel.setObjectName("textLabel")
        self.gridlayout.addWidget(self.textLabel,1,1,1,2)

        self.loginButton = QtGui.QPushButton(self.centralwidget)
        self.loginButton.setDefault(True)
        self.loginButton.setObjectName("loginButton")
        self.gridlayout.addWidget(self.loginButton,4,1,1,2)

        self.username = QtGui.QLineEdit(self.centralwidget)
        self.username.setObjectName("username")
        self.gridlayout.addWidget(self.username,2,2,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,3,3,1,1)

        self.textLabel1 = QtGui.QLabel(self.centralwidget)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.gridlayout.addWidget(self.textLabel1,2,1,1,1)

        self.requestButton = QtGui.QPushButton(self.centralwidget)
        self.requestButton.setDefault(True)
        self.requestButton.setObjectName("requestButton")
        self.gridlayout.addWidget(self.requestButton,5,1,1,2)

        self.textLabel2 = QtGui.QLabel(self.centralwidget)
        self.textLabel2.setWordWrap(False)
        self.textLabel2.setObjectName("textLabel2")
        self.gridlayout.addWidget(self.textLabel2,3,1,1,1)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3,3,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,413,29))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.client = PykafeClient(MainWindow, self)
        QtCore.QObject.connect(self.loginButton,QtCore.SIGNAL("clicked()"),self.client.login)
        QtCore.QObject.connect(self.requestButton,QtCore.SIGNAL("clicked()"),self.client.request)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.username,self.password)
        MainWindow.setTabOrder(self.password,self.loginButton)

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(_("pyKafe"))
        self.textLabel1.setText(_("Username:"))
        self.loginButton.setText(_("Login"))
        self.textLabel2.setText(_("Password:"))
        self.requestButton.setText(_("Request Opening"))
        self.textLabel.setText(_("Please contact cashier or enter your account information"))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
