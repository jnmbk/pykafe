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

import sha

from PyQt4 import QtCore
from PyQt4 import QtGui

import passwordwindow_ui

class PasswordWindow(QtGui.QDialog, passwordwindow_ui.Ui_Dialog):
    def __init__(self, mainWindow):
        QtGui.QDialog.__init__(self, mainWindow)
        self.setupUi(self)
        self.mainWindow = mainWindow

    def accept(self):
        parameters = (unicode(self.username.text()),
            sha.new(unicode(self.password.text())).hexdigest())
        #TODO: this shoud use database
        #found = Database().runOnce("select count(*) from members where username=? and password=? and is_cashier='1'", parameters)
        found = True
        if found:
            self.hide()
            self.mainWindow.show()
        else:
            QtGui.QMessageBox.critical(None, QtGui.QApplication.translate("MainWindow",
            "Error"), QtGui.QApplication.translate("MainWindow",
                "Wrong username or password!"))
            QtGui.QApplication.quit()
    def reject(self):
        QtGui.QApplication.quit()
