#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

import mainwindow_server_ui, tcpserver

class MainWindow(QtGui.QMainWindow, mainwindow_server_ui.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.tcpServer = tcpserver.TcpServer(self)

    @QtCore.pyqtSignature("on_main_startButton_clicked()")
    def on_main_startButton_clicked(self):
        print "started"
