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
from session import ClientSession
from database import Database
import base64

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class MessageSender(QtCore.QThread):
    def __init__(self, parent, ip, port, message):
        QtCore.QThread.__init__(self, parent)
        self.ip, self.port, self.message = ip, port, message
    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        tcpSocket.connectToHost(QtNetWork.QHostAddress(self.ip), self.port)
        tcpSocket.waitForConnected()
        tcpSocket.write(base64.encodestring(self.message))
        tcpSocket.waitForBytesWritten()
        tcpSocket.disconnectFromHost()
        tcpSocket.waitForDisconnected()

class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor, clients):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
        self.clients = clients

    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        clientIpList = []
        for client in self.clients:
            clientIpList.append(QtNetwork.QHostAddress(client.ip))
        try:
            self.clientNumber = clientIpList.index(self.tcpSocket.peerAddress())
        except ValueError:
            self.tcpSocket.disconnectFromHost()
        QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readSocket)
        self.tcpSocket.waitForDisconnected()

    def readSocket(self):
        client = self.clients[self.clientNumber]
        data = base64.decodestring(self.tcpSocket.readAll())
        if data[:3] == "004":
            #Says I'm here
            if client.session.state == ClientSession.notAvailable:
                self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.working)
            else:
                #TODO: illegal activity
                pass
        elif data[:3] == "000":
            #User wants to open
            if client.session.state == ClientSession.working:
                self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.requestedOpening)
            else:
                #TODO: illegal activity
                pass
        elif data[:3] == "002":
            if client.session.state == ClientSession.working:
                username, password = data[3:].split("|")
                db = Database()
                db.cur.execute("select count() from members where username = ? and password = ?", username, password)
                if db.cur.fetchall()[0][0]:
                    self.secureSend("0031")
                    client.setState(ClientSession.loggedIn)
                else:
                    #TODO: log: wrong password or username entered
                    self.secureSend("0030")
        self.tcpSocket.disconnectFromHost()
    def secureSend(self, data):
        self.tcpSocket.write(base64.encodestring("data"))

class Client(QtGui.QTreeWidgetItem):
    def __init__(self, parent, clientInformation, config):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.fillList(clientInformation)
        self.config = config 

    def fillList(self, clientInformation):
        self.session = clientInformation.session
        self.ip = clientInformation.ip
        self.name = clientInformation.name
        self.setText(0, self.name)
        self.setState(ClientSession.notAvailable)
    def changeColor(self, colorName):
        for i in range(self.columnCount()):
            self.setBackground(i, QtGui.QBrush(QtGui.QColor(colorName)))
    def sendMessage(self, message):
        thread = MessageSender(self.ip, self.config.network.port, message)
    def setState(self, state, user = None, endTime = None):
        self.session.state = state
        self.setText(1, self.session.getCurrentState())
        if state == ClientSession.loggedIn:
            self.session.user = user
            self.setText(2, user)
            self.setText(3, self.config.currency.prefix + "0" + self.config.currency.suffix)
            self.session.startTime = QtCore.QDateTime.currentDateTime()
            self.setText(4, self.session.startTime.time().toString())
            if endTime:
                self.setText(5, self.session.endTime.time().toString())

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
            self.clients.append(Client(ui.main_treeWidget, clientInformation, self.config))
        ui.main_treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.ui = ui

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor, self.clients)
        QtCore.QObject.connect(thread, QtCore.SIGNAL("stateChange"), self.setClientState)
        thread.start()

    def setClientState(self, client, state):
        self.clients[client].setState(state)

    def startClient(self):
        current = self.ui.main_treeWidget.currentColumn()
        if current != -1:
            client = self.clients[current]
            state = client.session.state
            if state == ClientSession.notAvailable:
                QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Can't connect to client"))
            if state == ClientSession.working:
                #TODO
                pass
            if state == ClientSession.loggedIn:
                QtGui.QMessageBox.information(self.parent(), _("Information"), _("Client is already logged in"))
            if state == ClientSession.requestedOpening:
                client.sendMessage("0011")
                client.setState(ClientSession.loggedIn)
        else:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose a client first"))
    def startTimed(self):
        print 2
        pass
    def stopClient(self):
        print 3
        pass
