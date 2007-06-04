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
from currencyformat import currency
import base64, sys, os, socket, time

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

config = PykafeConfiguration()

class SenderThread(QtCore.QThread):
    def __init__(self, data):
        QtCore.QThread.__init__(self)
        self.data = data
    def run(self):
        while not sendDataToServer(self.data):
            self.emit(QtCore.SIGNAL("connectionError"))
            print "connection error retrying"
            time.sleep(10)
        self.emit(QtCore.SIGNAL("messageSent"))

def sendDataToServer(data):
    tcpSocket = QtNetwork.QTcpSocket()
    tcpSocket.connectToHost(QtNetwork.QHostAddress(config.network_serverIP), config.network_port)
    tcpSocket.waitForConnected(-1)
    print "trying to send:", data
    if tcpSocket.write(base64.encodestring(data)) == -1:
        print "failed"
        return False
    else:
        print "success"
        tcpSocket.waitForBytesWritten()
        return True

def sendDataToUi(data):
    tcpSocket = QtNetwork.QTcpSocket()
    tcpSocket.connectToHost(QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost), config.network_localPort)
    tcpSocket.waitForConnected(-1)
    tcpSocket.write(base64.encodestring(data))
    tcpSocket.waitForBytesWritten()
    print "sent to ui:", data

def getSiteIP(site):
    try:
        return socket.gethostbyname(site)
    except socket.gaierror:
        return False

def getNetworkBytes():
    "returns a tuple of received bytes and transferred bytes"
    receivedBytes = 0
    transferredBytes = 0
    interfaces = os.listdir("/sys/class/net")
    for interface in interfaces:
        if file("/sys/class/net/%s/operstate" % interface).read() == "up\n":
            receivedBytes += int(file("/sys/class/net/%s/statistics/rx_bytes" % interface).read())
            transferredBytes += int(file("/sys/class/net/%s/statistics/tx_bytes" % interface).read())
    return receivedBytes, transferredBytes

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
        elif self.tcpSocket.peerAddress() == QtNetwork.QHostAddress(config.network_serverIP):
            QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readServer)
        else:
            sys.stderr.write(_("Unauthorized server tried to connect, aborting connection: %s") % self.tcpSocket.peerAddress())
        self.tcpSocket.waitForDisconnected()
        self.exec_()

    def readServer(self):
        data = base64.decodestring(self.tcpSocket.readAll())
        print "received from server:", data
        if data[:3] == "001":
            sendDataToUi(data)
        elif data[:3] == "003":
            sendDataToUi(data)
            if data[3] == "1":
                self.client.setState(ClientSession.loggedIn)
        elif data[:3] == "005":
            self.client.setState(ClientSession.loggedIn)
            sendDataToUi(data)
        elif data[:3] == "006":
            sendDataToUi("005")
            self.client.setState(ClientSession.loggedIn, endTime = QtCore.QDateTime.fromTime_t(int(data[3:])))
        elif data[:3] == "007":
            iptablesFile = "*filter\n:INPUT ACCEPT [94:7144]\n:FORWARD ACCEPT [0:0]\n:OUTPUT ACCEPT [177:10428]\n"
            for site in data[3:].split('\n'):
                ip = getSiteIP(site)
                if ip:
                    iptablesFile += "-A INPUT -s %s -j DROP\n" % ip
            iptablesFile += "COMMIT\n"
            file = open("/etc/pyKafe/iptables.conf", "w")
            file.write(iptablesFile)
            file.close()
            print iptablesFile
            os.system("iptables-restore < /etc/pyKafe/iptables.conf")
        elif data[:3] == "009":
            os.system("restartkde&")
        elif data[:3] == "010":
            os.system("init 0")
        elif data[:3] == "015":
            if self.client.state == ClientSession.ready:
                sendDataToServer("004")
        elif data[:3] == "016":
            for c, value in map(lambda x,y:(x,y), ("price_fixedprice", "price_fixedpriceminutes", "price_onehourprice", "price_rounding"), data[3:].split("|")):
                config.set(c, value)

    def readUi(self):
        data = base64.decodestring(self.tcpSocket.readAll())
        print "received from user:", data
        if self.client.session.state == ClientSession.notConnected:
            sendDataToUi("014")
            return
        if data[:3] == "000":
            sendDataToServer("000")
            self.client.setState(ClientSession.requestedOpening)
        elif data[:3] == "002":
            sendDataToServer(data)
        elif data[:3] == "004":
            sendDataToServer("004")
            self.client.setState(ClientSession.ready)
        elif data[:3] == "008":
            sendDataToServer(data)
            os.system("restartkde&")
        elif data[:3] == "017":
            currentTime = QtCore.QDateTime.currentDateTime()
            usedTime = self.client.session.startTime.secsTo(currentTime)
            remainingTime = QtCore.QDateTime()
            if self.client.session.endTime:
                remainingTime.setTime_t(currentTime.secsTo(self.client.session.endTime))
            else:
                remainingTime.setTime_t(0)
            temp = usedTime
            usedTime = QtCore.QDateTime()
            usedTime.setTime_t(temp)
            text = self.client.session.startTime.time().toString("hh.mm") + "\n" +\
                   remainingTime.toUTC().time().toString("hh.mm") + "\n" +\
                   usedTime.toUTC().time().toString("hh.mm") + "|"
            text += currency(self.client.session.calculatePrice(config))
            print "sending:", text
            self.tcpSocket.write(base64.encodestring(text))
            self.tcpSocket.waitForBytesWritten()
        elif data[:3] == "018":
            tcpSocket = QtNetwork.QTcpSocket()
            tcpSocket.connectToHost(QtNetwork.QHostAddress(config.network_serverIP), config.network_port)
            tcpSocket.waitForConnected()
            tcpSocket.write(base64.encodestring(data))
            tcpSocket.waitForBytesWritten()
            tcpSocket.waitForReadyRead()
            data = tcpSocket.readAll()
            self.tcpSocket.write(data)
            self.tcpSocket.waitForBytesWritten()

class PykafeClient(QtNetwork.QTcpServer):
    def __init__(self):
        QtNetwork.QTcpServer.__init__(self)
        self.session = ClientSession()
        if not self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any), config.network_port):
            print "cant bind, exitting"
            sys.exit()
        thread = SenderThread("011")
        QtCore.QObject.connect(thread, QtCore.SIGNAL("messageSent"), self.initialConnection)
        thread.start()
        self.threads = [thread]
        print "trying to connect to server"

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(socketDescriptor, self)
        thread.start()
        self.threads.append(thread)
        print "We have " + str(len(self.threads)) + " thread(s)"

    def initialConnection(self):
        print "connected to server"
        self.session.setState(ClientSession.notReady)

    def setState(self, state, user = "guest", endTime = ""):
        if state == ClientSession.loggedIn:
            self.session.user = user
            self.session.startTime = QtCore.QDateTime.currentDateTime()
            if endTime:
                self.session.endTime = endTime
        self.session.setState(state)
