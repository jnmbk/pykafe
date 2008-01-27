#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under GPL v2
# Copyright 2008, Ugur Cetin
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtCore
from PyQt4 import QtGui

import mainwindow_server_ui, tcpserver

class MainWindow(QtGui.QMainWindow, mainwindow_server_ui.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.tcpServer = tcpserver.TcpServer(self)

        self.show()
        if not self.tcpServer.isListening():
            QtGui.QMessageBox.critical(self,
                QtGui.QApplication.translate("MainWindow", "Connection Error"),
                QtGui.QApplication.translate("MainWindow",
                "Unable to start server: %1").arg(self.tcpServer.errorString()))

    @QtCore.pyqtSignature("on_main_startButton_clicked()")
    def on_main_startButton_clicked(self):
        print "started"
