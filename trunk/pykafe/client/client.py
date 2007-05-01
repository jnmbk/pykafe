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

"""client's server module"""

from PyQt4 import QtNetwork, QtCore
from config import PykafeConfiguration
from sys import exit
from base64 import encodestring

class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
        self.blockSize = 0

    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readSocket)
        self.tcpSocket.waitForDisconnected()

    def readSocket(self):
        data = self.tcpSocket.readAll()
        print data

class PykafeClient(QtNetwork.QTcpServer):
    def __init__(self, parent):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.config = PykafeConfiguration()
        self.listen(QtNetwork.QHostAddress(self.config.network.serverIP), self.config.network.port)
        self.informServer()

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor)
        thread.start()

    def informServer(self):
        #Say: I'm here to server
        tcpSocket = QtNetwork.QTcpSocket()
        print tcpSocket.connectToHost(QtNetwork.QHostAddress(self.config.network.serverIP), self.config.network.port)
        tcpSocket.waitForConnected()
        tcpSocket.write(encodestring("00"))
        tcpSocket.waitForBytesWritten()
