#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

import mainwindow_server_ui

class MainWindow(QtGui.QMainWindow, mainwindow_server_ui.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
