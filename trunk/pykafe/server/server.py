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
from base64 import encodestring, decodestring

from gettext import translation
_ = translation('pyKafe', fallback=True).ugettext

class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor, clients):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
        self.clients = clients
        self.blockSize = 0

    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        clientIpList = []
        for client in self.clients:
            clientIpList.append(QtNetwork.QHostAddress(client.ip))
        try:
            self.clientNumber = clientIpList.index(self.tcpSocket.localAddress())
        except ValueError:
            self.tcpSocket.disconnectFromHost()
        QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readSocket)
        self.tcpSocket.waitForDisconnected()

    def readSocket(self):
        client = self.clients[self.clientNumber]
        data = decodestring(self.tcpSocket.readAll())
        if data[:2] == "00":
            #Says I'm here
            client.session.setState(1)
            client.settext(1, client.session.getCurrentState())
        elif data[:2] == "01":
            #Says that user wants to connect
            answer = QtGui.QMessageBox.information(client.parent().parent(), "Opening Request", "%s sent an opening request. Accept?" % client.name, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                self.tcpSocket.write("000")
            else:
                self.tcpSocket.write("001")
        self.tcpSocket.disconnectFromHost()

class Client(QtGui.QTreeWidgetItem):
    def __init__(self, parent, clientInformation):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.fillList(clientInformation)

    def fillList(self, clientInformation):
        self.session = clientInformation["session"]
        self.ip = clientInformation["ip"]
        self.name = clientInformation["name"]
        self.setText(0, self.name)
        self.setText(1, self.session.getCurrentState())

class PykafeServer(QtNetwork.QTcpServer):
    def __init__(self, parent, ui):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.config = PykafeConfiguration()
        if not self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any), self.config.network.port):
            #TODO: retry button
            QtGui.QMessageBox.critical(self.parent(), _("Connection Error"), _("Unable to start server: %s") % self.errorString())
            exit()
        self.clients = []
        for clientInformation in self.config.clientList:
            self.clients.append(Client(ui.main_treeWidget, clientInformation))
        ui.main_treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor, self.clients)
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
