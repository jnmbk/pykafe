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
        stream = QtCore.QDataStream(self.tcpSocket)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        if self.blockSize == 0 and self.tcpSocket.bytesAvailable() > 2:
            self.blockSize = stream.readInt16()
        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return
        data = stream.readString()
        print data

class PykafeClient(QtNetwork.QTcpServer):
    def __init__(self, parent):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.config = PykafeConfiguration()
        self.listen(QtNetwork.QHostAddress(self.config.network.serverIP), self.config.network.port)
        if not self.informServer():
            print "olmadı"

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor)
        thread.start()

    def informServer(self):
        tcpSocket = QtNetwork.QTcpSocket()
        print tcpSocket.connectToHost(QtNetwork.QHostAddress(self.config.network.serverIP), self.config.network.port)
        tcpSocket.waitForConnected()
        data = "sşçüelam"
        print "data:", data
        print tcpSocket.write(encodestring(data))
        tcpSocket.waitForBytesWritten()
        return True
