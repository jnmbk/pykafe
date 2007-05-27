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

"""Controls most of the server routines"""

from PyQt4 import QtNetwork, QtCore, QtGui
from pysqlite2 import dbapi2 as sqlite
from config import PykafeConfiguration
from session import ClientSession
from database import Database
import base64, sha

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class MessageSender(QtCore.QThread):
    def __init__(self, parent, ip, port, message):
        QtCore.QThread.__init__(self, parent)
        self.ip, self.port, self.message = ip, port, message
    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        tcpSocket.connectToHost(QtNetwork.QHostAddress(self.ip), self.port)
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
        self.tcpSocket.write(base64.encodestring(data))

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
        thread.run()

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

class Member(QtGui.QTreeWidgetItem):
    def __init__(self, parent, memberInformation):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.updateValues(memberInformation)

    def updateValues(self, memberInformation):
        self.userName, self.password, self.realName, self.startDate, self.endDate, self.debt, self.payingType = memberInformation
        self.setText(0, self.userName)

    def updateValuesWithoutPassword(self, memberInformation):
        self.userName, self.realName, self.startDate, self.endDate, self.debt, self.payingType = memberInformation
        self.setText(0, self.userName)        

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
        #TODO: Initialize ui
        self.ui = ui
        self.initMembers()
        self.localize()

    def initMembers(self):
        self.members = []
        memberList = Database().run("select * from members")
        for memberInformation in memberList:
            self.members.append(Member(self.ui.members_treeWidget, memberInformation[:7]))
        self.ui.members_dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.members_dateEdit_2.setDate(QtCore.QDate.currentDate().addMonths(1))
        self.ui.members_username.clear()
        self.ui.members_password.clear()
        self.ui.members_realName.clear()
        self.ui.members_debt.setValue(0.0)
        self.ui.members_payingType.setCurrentIndex(0)

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
    def addMember(self, toDatabase = True, memberInformation = None):
        "Adds a new member"
        #check if startdate is smaller than enddate
        if self.ui.members_dateEdit.date().__gt__(self.ui.members_dateEdit_2.date()):
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Start date must be smaller than end date"))
            return
        if not memberInformation:
            memberInformation = [unicode(self.ui.members_username.text()),
                                 unicode(self.ui.members_password.text()),
                                 unicode(self.ui.members_realName.text()),
                                 str(self.ui.members_dateEdit.date().toString("yyyy-MM-dd")),
                                 str(self.ui.members_dateEdit_2.date().toString("yyyy-MM-dd")),
                                 self.ui.members_debt.value(),
                                 str(self.ui.members_payingType.currentText()),
                                 False]
        if "" in memberInformation:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("All member information must be filled"))
        else:
            memberInformation[1] = sha.new(unicode(self.ui.members_password.text())).hexdigest()
            if toDatabase:
                try:
                    Database().runOnce("insert into members values (?,?,?,?,?,?,?,?)", memberInformation)
                    self.members.append(Member(self.ui.members_treeWidget, memberInformation[:7]))
                    self.filterMembers(self.ui.members_filter.text())
                    self.ui.statusbar.showMessage(_("Added member"))
                except sqlite.IntegrityError:
                    QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Username must be unique"))

    def updateMember(self):
        "Updates selected member information"
        if self.ui.members_dateEdit.date().__gt__(self.ui.members_dateEdit_2.date()):
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Start date must be smaller than end date"))
            return
        member = self.ui.members_treeWidget.currentItem()
        if not member:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("You must select a member first"))
            return
        memberInformation = [unicode(self.ui.members_username.text()),
                             " ",
                             unicode(self.ui.members_realName.text()),
                             str(self.ui.members_dateEdit.date().toString("yyyy-MM-dd")),
                             str(self.ui.members_dateEdit_2.date().toString("yyyy-MM-dd")),
                             self.ui.members_debt.value(),
                             str(self.ui.members_payingType.currentText()),
                             member.userName]
        if "" in memberInformation:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("All member information must be filled"))
        memberInformation[1] = sha.new(unicode(self.ui.members_password.text())).hexdigest()
        if self.ui.members_password.text():
            try:
                Database().runOnce("update members set username=?,password=?,name=?,starting_date=?,finish_date=?,debt=?,paying_type=? where username = ?", memberInformation)
                member.updateValues(memberInformation[:7])
                self.filterMembers(self.ui.members_filter.text())
                self.ui.statusbar.showMessage(_("Updated member information"))
            except sqlite.IntegrityError:
                QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Username must be unique"))
        else:
            del(memberInformation[1])
            try:
                Database().runOnce("update members set username=?,name=?,starting_date=?,finish_date=?,debt=?,paying_type=? where username=?", memberInformation)
                member.updateValuesWithoutPassword(memberInformation[:6])
                self.filterMembers(self.ui.members_filter.text())
                self.ui.statusbar.showMessage(_("Updated member information"))
            except sqlite.IntegrityError:
                QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Username must be unique"))

    def deleteMember(self):
        "Deletes selected member"
        member = self.ui.members_treeWidget.currentItem()
        if not member:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("You must select a member first"))
            return
        answer = QtGui.QMessageBox.question(self.parent(), _("Are you sure?"), _("Do you really want to delete this member?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            Database().runOnce("delete from members where username = ?", (member.userName,))
            #TODO: There may be a better way of this
            self.ui.members_treeWidget.clear()
            self.initMembers()
            self.filterMembers(self.ui.members_filter.text())
            self.ui.statusbar.showMessage(_("Deleted member"))

    def memberReports(self):
        "Shows statistics about selected member"
        pass

    def memberChanged(self, current, previous):
        member = current
        if not member:
            member = previous
        self.ui.members_username.setText(member.userName)
        self.ui.members_password.clear()
        self.ui.members_realName.setText(member.realName)
        self.ui.members_dateEdit.setDate(QtCore.QDate.fromString(member.startDate, "yyyy-MM-dd"))
        self.ui.members_dateEdit_2.setDate(QtCore.QDate.fromString(member.endDate, "yyyy-MM-dd"))
        self.ui.members_debt.setValue(float(member.debt))
        self.ui.members_payingType.setEditText(member.payingType)

    def filterMembers(self, text):
        for member in self.members:
            member.setHidden(False)
            if unicode(text) not in member.userName:
                member.setHidden(True)

    def localize(self):
        self.ui.members_debt.setPrefix(self.config.currency.prefix)
        self.ui.members_debt.setSuffix(self.config.currency.suffix)
