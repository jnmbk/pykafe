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

"""Listens connections"""

from PyQt4 import QtNetwork, QtCore, QtGui
from config import PykafeConfiguration
from sys import exit

from gettext import translation
_ = translation('pyKafe', fallback=True).ugettext

class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor

    def run(self):
        socket = QtNetwork.QTcpSocket()
        socket.setSocketDescriptor(self.socketDescriptor)
        socket.write("jghvyv")
        print "yazdım"
        socket.disconnectFromHost()
        socket.waitForDisconnected()

class PykafeServer(QtNetwork.QTcpServer):
    def __init__(self, parent):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.config = PykafeConfiguration()
        if not self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), self.config.network.port):
            #TODO: retry button
            QtGui.QMessageBox.critical(self.parent(), _("Connection Error"), _("Unable to start server: %s") % self.errorString())
            exit()
        #QtCore.QObject.connect(self.server, QtCore.SIGNAL("incomingConnection()"), self.handleConnection)

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor)
        thread.start()

    def startClient(self):
        print 1
        pass
    def startTimed(self):
        print 2
        pass
    def stopClient(self):
        print 3
        pass
