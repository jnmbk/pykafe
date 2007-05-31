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
import base64, sys, os

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

def sendDataToServer(data):
    tcpSocket = QtNetwork.QTcpSocket()
    tcpSocket.connectToHost(QtNetwork.QHostAddress(PykafeConfiguration().network.serverIP), PykafeConfiguration().network.port)
    tcpSocket.waitForConnected(-1)
    tcpSocket.write(base64.encodestring(data))
    tcpSocket.waitForBytesWritten()
    print "sent to server:", data

def sendDataToUi(data):
    tcpSocket = QtNetwork.QTcpSocket()
    tcpSocket.connectToHost(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), PykafeConfiguration().network.localPort)
    tcpSocket.waitForConnected(-1)
    tcpSocket.write(base64.encodestring(data))
    tcpSocket.waitForBytesWritten()
    print "sent to ui:", data

def siteValidate(site):
    #TODO: Look if that is an ip adress
    return True

class ListenerThread(QtCore.QThread):
    def __init__(self, socketDescriptor, client):
        QtCore.QThread.__init__(self)
        self.socketDescriptor = socketDescriptor
        self.client = client

    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        print "connection request from:", self.tcpSocket.peerAddress().toString()
        if self.tcpSocket.peerAddress() == QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost):
            QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readUi)
        elif self.tcpSocket.peerAddress() == QtNetwork.QHostAddress(self.client.config.network.serverIP):
            QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readServer)
        else:
            sys.stderr.write(_("Unauthorized server tried to connect, aborting: %s") % self.tcpSocket.peerAddress())
            self.exit()
        self.tcpSocket.waitForDisconnected()
        self.exec_()

    def readServer(self):
        data = base64.decodestring(self.tcpSocket.readAll())
        print "received from server:", data
        if data[:3] == "001":
            if self.client.session.state == ClientSession.working:
                sendDataToUi(data)
            else:
                sys.stderr.write(_("Received ack from server, state was: %s") % self.client.session.getCurrentState())
        elif data[:3] == "003":
            if self.client.session.state == ClientSession.working:
                sendDataToUi(data)
                if data[3] == "1":
                    self.client.session.state = ClientSession.loggedIn
            else:
                sys.stderr.write(_("Received %s from server, state was: %s") % (data, self.client.session.getCurrentState()))
        elif data[:3] == "005":
            if self.client.session.state == ClientSession.working:
                self.client.session.user = "guest"
                self.client.session.state = ClientSession.loggedIn
                sendDataToUi("005")
        elif data[:3] == "007":
            self.emit(QtCore.SIGNAL("filter"), data[4:])
            """iptablesFile = "*filter\n:INPUT ACCEPT [94:7144]\n:FORWARD ACCEPT [0:0]\n:OUTPUT ACCEPT [177:10428]\n"
            for site in data[3:].split('\n'):
                if siteValidate(site):
                    iptablesFile += "-A INPUT -s %s -j DROP\n" % site
            iptablesFile += "COMMIT\n"
            file = open("/etc/pyKafe/iptables.conf", "w")
            file.write(iptablesFile)
            file.close()
            os.system("iptables-restore < /etc/pyKafe/iptables.conf")"""
            for site in data[3:].split('\n'):
                os.system("iptables -A INPUT -s %s -j DROP&" % site)
        elif data[:3] == "010":
            os.system("init 0")
        self.exit()

    def readUi(self):
        data = base64.decodestring(self.tcpSocket.readAll())
        print "received from user:", data
        if data[:3] == "000":
            if self.client.session.state == ClientSession.working:
                sendDataToServer("000")
                self.client.session.setState(ClientSession.requestedOpening)
            else:
                sys.stderr.write(_("Client tried to send opening request, state was: %s") % self.client.session.getCurrentState())
        elif data[:3] == "002":
            if self.client.session.state == ClientSession.working:
                sendDataToServer(data)
        elif data[:3] == "004":
            if self.client.session.state == ClientSession.notAvailable:
                sendDataToServer("004")
                self.client.session.state = ClientSession.working
            else:
                sys.stderr.write(_("Client tried to say I'm here, state was: %s") % self.client.session.getCurrentState())
        elif data[:3] == "008":
            print 8
            if self.client.session.state == ClientSession.loggedIn:
                print "gdg"
                sendDataToServer(data)
                os.system("service kdebase stop && sleep 3 && service kdebase start")
        self.exit()

class PykafeClient(QtNetwork.QTcpServer):
    def __init__(self):
        QtNetwork.QTcpServer.__init__(self)
        self.config = PykafeConfiguration()
        self.session = ClientSession()
        self.threads = []
        self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any), self.config.network.port)
        print "listening?", self.isListening()
        print "listening to:", QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any).toString() ,self.config.network.port
    def incomingConnection(self, socketDescriptor):
        print "called incomingConnection"
        thread = ListenerThread(socketDescriptor, self)
        thread.start()
        QtCore.QObject.connect(thread,QtCore.SIGNAL("filter"),self.filterCame)
        self.threads.append(thread)
        print "We have " + str(len(self.threads)) + " thread(s)"
    def filterCame(self, text):
        print "filtering:", text
