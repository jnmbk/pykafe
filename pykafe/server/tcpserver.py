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

"""Server module"""

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork

from defaultsettings import defaultsettings

class TcpServer(QtNetwork.QTcpServer):
    def __init__(self, parent = None):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.mainWindow = parent

        settings = QtCore.QSettings()

        if not self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any),
        settings.value("server/port", defaultsettings["server/port"]).toInt()[0]):
            QtGui.QMessageBox.critical(self.parent(),
                    QtGui.QApplication.translate("TcpServer", "Connection Error"),
                    QtGui.QApplication.translate("TcpServer", "Unable to start server: %1").arg(self.errorString()))

    def incomingConnection(self, socketDescriptor):
        # this is called when someone tries to connect
        pass
