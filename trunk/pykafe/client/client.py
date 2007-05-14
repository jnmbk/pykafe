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
from session import ClientSession
import base64, sys

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

def sendData(ip, port, data):
    tcpSocket = QtNetwork.QTcpSocket()
    tcpSocket.connectToHost(QtNetwork.QHostAddress(ip), port)
    tcpSocket.waitForConnected(-1)
    tcpSocket.write(base64.encodestring(data))
    tcpSocket.waitForBytesWritten()
    tcpSocket.disconnectFromHost()

class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor, client):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
        self.client = client

    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        if self.tcpSocket.peerAddress() == QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost):
            QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readUi)
        elif self.tcpSocket.peerAddress() == QtNetwork.QHostAddress(self.client.config.network.serverIP):
            QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readServer)
        else:
            sys.stderr.write(_("Unauthorized server tried to connect, aborting: %s") % self.tcpSocket.peerAddress())
            self.tcpSocket.disconnectFromHost()
        self.tcpSocket.waitForDisconnected()

    def readServer(self):
        data = base64.decodestring(self.tcpSocket.readAll())
        if data[:3] == "001":
            pass
    def readUi(self):
        data = base64.decodestring(self.tcpSocket.readAll())
        if data[:3] == "000":
            if self.client.state == ClientSession.working:
                sendData(self.client.config.network.serverIP, self.client.config.network.port, "000")
            else:
                sys.stderr.write(_("Client tried to send opening request, state was: %s") % self.client.session.getCurrentState())

class PykafeClient(QtNetwork.QTcpServer):
    def __init__(self, parent):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.config = PykafeConfiguration()
        self.session = ClientSession()
        self.listen(QtNetwork.QHostAddress(self.config.network.serverIP), self.config.network.port)
        #Say: I'm here to server
        sendData(self.config.network.serverIP, self.config.network.port, "004")
        self.session.state = ClientSession.working

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor, self)
        thread.start()
