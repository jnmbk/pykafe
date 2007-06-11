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
from config import PykafeConfiguration, ClientInformation
from session import ClientSession
from database import Database
from settingswindow import Ui_SettingsWindow
from clientsettingswindow import Ui_ClientSettingsWindow
from currencyformat import currency
from payment import Ui_PaymentDialog
from memberreports import Ui_MemberReports
import logger
import base64, sha, os

import locale, gettext
locale.setlocale(locale.LC_MESSAGES, "C")
locale.setlocale(locale.LC_MONETARY, "")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext


def validIp(ip):
    "returns true when you give it a valid ip"
    try:
        is_ip = True
        num = ip.split('.')
        for n in num:
            if not 256 > int(n) > 0:
                is_ip = False
                break;
        return is_ip
    except ValueError:
        return False

class MessageSender(QtCore.QThread):
    def __init__(self, ip, port, message):
        QtCore.QThread.__init__(self)
        self.ip, self.port, self.message = ip, port, message
        print "sending %s to %s:%d" % (message, ip, port)
    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        tcpSocket.connectToHost(QtNetwork.QHostAddress(self.ip), self.port)
        tcpSocket.waitForConnected()
        tcpSocket.write(base64.encodestring(self.message))
        tcpSocket.waitForBytesWritten()
        tcpSocket.disconnectFromHost()


class ListenerThread(QtCore.QThread):
    def __init__(self, parent, socketDescriptor, clients, config, server):
        #TODO: We should use server only, clients and config aren't necessary
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
        self.clients = clients
        self.config = config
        self.server = server

    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.setSocketDescriptor(self.socketDescriptor)
        clientIpList = []
        for client in self.clients:
            clientIpList.append(QtNetwork.QHostAddress(client.ip))
        try:
            self.clientNumber = clientIpList.index(self.tcpSocket.peerAddress())
            print "came from a known client:", self.tcpSocket.peerAddress().toString()
        except ValueError:
            self.tcpSocket.disconnectFromHost()
        QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.readSocket)
        self.exec_()

    def readSocket(self):
        client = self.clients[self.clientNumber]
        data = base64.decodestring(self.tcpSocket.readAll())
        print "data:", data
        if data[:3] == "011":
            self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.notReady)
        elif data[:3] == "004":
            self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.ready)
        elif data[:3] == "000":
            self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.requestedOpening)
        elif data[:3] == "008":
            self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.waitingMoney)
        elif data[:3] == "002":
            if client.session.state == ClientSession.ready:
                username, password = data[3:].split("|")
                if Database().runOnce("select count() from members where username = ? and password = ?", (username, password))[0][0]:
                    wallpaper = ""
                    try:
                        wallpaper = Database().runOnce("select setting_value from member_settings where username=? and setting_name=?", (username,"wallpaper"))[0][0]
                        print wallpaper
                    except IndexError:
                        pass
                    client.sendMessage("0031%s|%s" % (username, wallpaper))
                    logger.add(logger.logTypes.information, _("Member logged in"), computer = client.name, member = username)
                    self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.loggedIn, username)
                else:
                    logger.add(logger.logTypes.warning, _("Someone entered wrong password or username"), computer = client.name, member = username)
                    client.sendMessage("0030")
        elif data[:3] == "018":
            message = ""
            for product in self.server.products:
                message += product.name +'|'+ str(product.quantity) +'|'+ str(product.price) +'||'
            print "sending:", message[:-2]
            self.tcpSocket.write(base64.encodestring(message[:-2]))
            self.tcpSocket.waitForBytesWritten()
        elif data[:3] == "019":
            for order in data[3:].split('||'):
                self.emit(QtCore.SIGNAL("orderCame"), order.split('|'), client.name)
        elif data[:3] == "022":
            self.sleep(2)
            Database().runOnce("update member_settings set setting_value=? where username=? and setting_name=?", (data[3:], client.session.user, "wallpaper"))
        elif data[:3] == "023":
            self.sleep(5)
            member, recv, trans = data[3:].split('|')
            logger.add(logger.logTypes.information, _("received, sent:") + recv + '|' + trans, client.name, member)
        self.tcpSocket.disconnectFromHost()


class ClientThread(QtCore.QThread):
    def __init__(self, parent, config):
        QtCore.QThread.__init__(self)
        self.client = parent
        self.config = config
    def run(self):
        while(True):
            if self.client.session.state == ClientSession.loggedIn:
                self.emit(QtCore.SIGNAL("changetext"),3,currency(self.client.session.calculateTotal(self.config)))
                usedTime = QtCore.QDateTime()
                usedTime.setTime_t(self.client.session.startTime.secsTo(QtCore.QDateTime.currentDateTime()))
                self.emit(QtCore.SIGNAL("changetext"),4,usedTime.toUTC().time().toString("hh.mm"))
                if self.client.session.endTime and QtCore.QDateTime.currentDateTime().__gt__(self.client.session.endTime):
                    self.emit(QtCore.SIGNAL("timepassed"))
            self.sleep(int(self.config.ui_refreshdelay))

class Log(QtGui.QTreeWidgetItem):
    def __init__(self, parent, textTuple):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.updateTexts(textTuple)
    def updateTexts(self, textTuple):
        for column, text in map(lambda x,y:(x,y), xrange(7), textTuple):
            self.setText(column, unicode(str(text)))
            if column == 1:
                if text == _("emergency"): color = "purple"
                elif text == _("warning"): color = "orange"
                elif text == _("error"): color = "red"
                elif text == _("information"): color = "lightblue"
        self.changeColor(color)
    def changeColor(self, colorName):
        for i in range(self.columnCount()):
            self.setBackground(i, QtGui.QBrush(QtGui.QColor(colorName)))

class Order(QtGui.QTreeWidgetItem):
    def __init__(self, parent, order, clientName, toDatabase = True):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.productName = str(order[0])
        self.quantity = int(order[1])
        self.clientName = str(clientName)
        self.updateTexts()
        if toDatabase:
            Database().run("insert into orders values(?,?,?)", (self.productName, self.quantity, self.clientName))

    def updateTexts(self):
        for column, text in map(lambda x,y:(x,y), xrange(4), (self.clientName, self.productName, currency(self.price()), str(self.quantity))):
            self.setText(column, text)

    def price(self):
        "Calculates and returns price of order"
        products = Database().runOnce("select product_name, unit_price from products")
        for product in products:
            if self.productName == product[0]:
                return float(product[1]) * self.quantity
        return 0.0

    def update(self, clientName, productName, quantity):
        Database().run("update orders set product_name=?,quantity=?,computer_name=? where product_name=? and quantity=? and computer_name=?", (str(productName), int(quantity), str(clientName), self.productName, self.quantity, self.clientName))
        self.clientName = str(clientName)
        self.productName = str(productName)
        self.quantity = int(quantity)
        self.updateTexts()


class Client(QtGui.QTreeWidgetItem):
    def __init__(self, parent, clientInformation, config, server):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.config = config
        self.server = server
        self.fillList(clientInformation)
        watcherThread = ClientThread(self, config)
        QtCore.QObject.connect(watcherThread, QtCore.SIGNAL("changetext"), self.setText)
        QtCore.QObject.connect(watcherThread, QtCore.SIGNAL("timepassed"), self.timeWarning)
        watcherThread.start()
        self.threads = [watcherThread]

    def fillList(self, clientInformation):
        self.id = id
        self.session = clientInformation.session
        self.ip = clientInformation.ip
        self.name = clientInformation.name
        self.setText(0, self.name)
        self.setState(ClientSession.notConnected)

    def updateInformation(self, parent, name, ip):
        try:
            Database().runOnce("update computers set name=?,ip=? where name=?", (str(name), str(ip), self.name))
            self.name = name
            self.ip = ip
            self.setText(0, self.name)
        except sqlite.IntegrityError:
            QtGui.QMessageBox.critical(parent, _("Error"), _("Client ip and name must be unique.") + " " + _("Client information won't be changed"))

    def changeColor(self, colorName):
        for i in range(self.columnCount()):
            self.setBackground(i, QtGui.QBrush(QtGui.QColor(colorName)))
    def timeWarning(self):
        self.setBackground(5, QtGui.QBrush(QtGui.QColor("red")))

    def sendMessage(self, message):
        thread = MessageSender(self.ip, int(self.config.network_port), message)
        thread.start()
        self.threads.append(thread)
        print "This client has %d threads" % len(self.threads)

    def setState(self, state, user = "guest", endTime = ""):
        if state == ClientSession.loggedIn:
            self.session.user = user
            self.session.startTime = QtCore.QDateTime.currentDateTime()
            self.setTexts((2,3,4), (user,currency(float(self.config.price_fixedprice)), self.session.startTime.time().toString("00.00")))
            if endTime:
                self.session.endTime = endTime
                self.setText(5, self.session.endTime.time().toString("hh.mm"))
            self.changeColor("green")
        elif state == ClientSession.notReady:
            if self.session.state == ClientSession.waitingMoney:
                self.server.payment(self)
                #total = self.session.calculateTotal(self.config)
                #dialog = Ui_PaymentDialog()
                #self.parent()
                """
                self.paymentDialog = QtGui.QDialog(self.parent())
                QtCore.QObject.connect(self.paymentDialog, QtCore.SIGNAL("accepted()"), self.sendOptions)
                settingsUi = Ui_SettingsWindow()
                settingsUi.setupUi(self.settingsDialog, self.config)
                self.settingsDialog.show()
                print "will pay", total
                payingType, credit = Database().runOnce("select paying_type, debt from members where username=?",(self.session.user,))[0]
                print payingType, credit
                if payingType == _("Pre Paid"):
                    print "user is pre_paid and has %s credit" % currency(credit)
                    for member in self.server.members:
                        print member.userName, self.session.user
                        if member.userName == self.session.user:
                            if member.debt < total:
                                QtGui.QMessageBox.warning(self.server.parent(), _("Low credit"), _("%s's credit has finished! Has %s debt.") % (member.userName, currency(total - member.debt)))
                                logger.add(logger.logTypes.warning, _("Member has low credit"), self.name, member.userName, member.debt - total)
                            member.debt -= total
                            Database().runOnce("update members set debt=? where username=?", (member.debt, member.userName))
                else:
                    #logger.add(logger.logTypes.information, _("Money paid"), self.name, member.userName, total)
                    #Database().runOnce("insert into safe values(?,?,?)", (QtCore.QDateTime.currentDateTime().toTime_t(), self.config.last_cashier, total))
                    #logger.add(logger.logTypes.information, _("money paid"), self.name, self.session.user, self.session.calculateTotal()
                """
                pass
            if self.session.state == ClientSession.loggedIn:
                self.server.payment(self)
                """total = self.session.calculateTotal(self.config)
                payingType, credit = Database().runOnce("select paying_type, debt from members where username=?",(self.session.user,))[0]
                if payingType == _("Pre Paid"):
                    print "user is pre_paid and has %s credit" % currency(credit)
                    for member in self.server.members:
                        if member.userName == self.session.user:
                            if member.debt < total:
                                QtGui.QMessageBox.warning(self.server.parent(), _("Low credit"), _("%s's credit has finished! Has %s debt.") % (member.userName, currency(total - member.debt)))
                                logger.add(logger.logTypes.warning, _("Member has low credit"), self.name, member.userName, member.debt - total)
                            member.debt -= total
                            Database().runOnce("update members set debt=? where username=?", (member.debt, member.userName))
                else:
                    #logger.add(logger.logTypes.information, _("Money paid"), self.name, member.userName, total)
                    #Database().runOnce("insert into safe values(?,?,?)", (QtCore.QDateTime.currentDateTime().toTime_t(), self.config.last_cashier, total))
                    pass"""
                pass
            if self.config.filter_enable:
                message = "007"
                filterFile = open(self.config.filter_file)
                filters = filterFile.readlines()
                filterFile.close()
                for i in filters:
                    message += i
                self.sendMessage(message.strip())
            message = "016"
            message += "%s|%s|%s|%s" % (self.config.price_fixedprice,
                                        self.config.price_fixedpriceminutes,
                                        self.config.price_onehourprice,
                                        self.config.price_rounding)
            self.sendMessage(message)
            self.setTexts((2,3,4,5), ("","","",""))
            self.changeColor("orange")
            self.session.initialize()
        elif state == ClientSession.requestedOpening:
            self.changeColor("red")
        elif state == ClientSession.waitingMoney:
            self.changeColor("red")
        elif state == ClientSession.notConnected:
            if self.session.state == ClientSession.loggedIn:
                logger.add(logger.logTypes.information, "client shutted down while logged in", computer = self.name, member = self.session.user, income = self.session.calculatePrice(self.config))
            self.setTexts((2,3,4,5), ("","","",""))
            self.changeColor("orange")
        elif state == ClientSession.ready:
            self.setTexts((2,3,4,5), ("","","",""))
            self.changeColor("lightblue")
        self.session.state = state
        self.setText(1, self.session.toString())
        logger.add(logger.logTypes.information, _("State changed to %s") % self.session.toString(), computer = self.name, member = self.session.user)
        self.setSelected(False)

    def sendSession(self):
        "sends latest session to the client, this is for eliminating client side problems like rebooting"
        message = "012"+\
            str(self.session.state)+'|'+\
            self.session.user+'|'+\
            str(self.session.startTime.toTime_t())+'|'+\
            str(self.session.endTime.toTime_t())
        self.sendMessage(message)

    def setTexts(self, columns, texts):
        "Sets multiple texts at once"
        #there may be a better way to do this
        for column, text in map(lambda x,y:(x,y), columns, texts):
            self.setText(column, text)


class Product(QtGui.QTreeWidgetItem):
    def __init__(self, parent, productInformation):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.updateValues(productInformation)

    def updateValues(self, productInformation):
        self.name, self.price, self.quantity = productInformation
        self.setText(0,self.name)
        self.setText(1,str(self.price))
        self.setText(2,str(self.quantity))

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
    def __init__(self, parent, ui, cashier = None):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.config = PykafeConfiguration()
        self.ui = ui
        if self.config.startup_askpassword:
            self.config.set("last_cashier", cashier)
        logger.add(logger.logTypes.information, _("cashier login to server"))
        if not self.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any), int(self.config.network_port)):
            logger.add(logger.logTypes.error, _("Unable to start server: %s") % self.errorString())
            QtGui.QMessageBox.critical(self.parent(), _("Connection Error"), _("Unable to start server: %s") % self.errorString())
            self.parent().close()
        self.clients = []
        for clientInformation in self.config.clientList:
            client = Client(ui.main_treeWidget, clientInformation, self.config, self)
            self.clients.append(client)
            self.ui.orders_idComboBox.addItem(clientInformation.name, QtCore.QVariant(clientInformation.ip))
        ui.main_treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.initMembers(first = True)
        self.initProducts()
        self.initOrders()
        self.ui.logs_dateTimeEdit_1.setDateTime(QtCore.QDateTime.currentDateTime().addDays(-1))
        self.ui.logs_dateTimeEdit_2.setDateTime(QtCore.QDateTime.currentDateTime().addDays(1))
        self.refreshLogs()
        self.localize()
        self.threads = []

    def initMembers(self, first = False):
        #TODO: Call this function after adding and deleting
        if first:
            self.members = []
            self.ui.members_treeWidget.clear()
            memberList = Database().run("select * from members where is_cashier='0'")
            for memberInformation in memberList:
                self.members.append(Member(self.ui.members_treeWidget, memberInformation[:7]))
        self.ui.members_dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.members_dateEdit_2.setDate(QtCore.QDate.currentDate().addMonths(1))
        self.ui.members_username.clear()
        self.ui.members_password.clear()
        self.ui.members_realName.clear()
        self.ui.members_debt.setValue(0.0)
        self.ui.members_payingType.setCurrentIndex(0)

    def initProducts(self):
        self.products = []
        productList = Database().run("select * from products")
        for product in productList:
            self.products.append(Product(self.ui.orders_treeWidget_2, product))
            self.ui.orders_itemComboBox.addItem(product[0])

    def initOrders(self):
        self.orders = []
        orderList = Database().run("select * from orders")
        for order in orderList:
            self.orderAdd(order[:2], order[2], toDatabase = False)

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor, self.clients, self.config, self)
        self.threads.append(thread)
        QtCore.QObject.connect(thread, QtCore.SIGNAL("stateChange"), self.setClientState)
        QtCore.QObject.connect(thread, QtCore.SIGNAL("orderCame"), self.orderAdd)
        thread.start()
        print "We have %d thread(s)" % len(self.threads)

    def setClientState(self, client, state, user = "guest"):
        self.clients[client].setState(state, user)

    def startClient(self):
        client = self.ui.main_treeWidget.currentItem()
        if not client:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose a client first"))
            return
        state = client.session.state
        if state == ClientSession.notConnected:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Can't connect to client"))
        elif state == ClientSession.ready:
            client.sendMessage("005")
            client.setState(ClientSession.loggedIn, user = "guest")
        elif state == ClientSession.loggedIn:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Client is already logged in"))
        elif state == ClientSession.requestedOpening:
            client.sendMessage("0011")
            client.setState(ClientSession.loggedIn)
        elif state == ClientSession.waitingMoney:
            client.setState(ClientSession.notReady)
            client.sendMessage("015")
        elif state == ClientSession.notReady:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Client isn't ready"))

    def startTimed(self):
        client = self.ui.main_treeWidget.currentItem()
        if not client:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose a client first"))
            return
        state = client.session.state
        if state == ClientSession.notConnected:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Can't connect to client"))
        elif state == ClientSession.loggedIn:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Client is already logged in"))
        elif state == ClientSession.requestedOpening:
            client.sendMessage("0011")
            client.setState(ClientSession.loggedIn)
        elif state == ClientSession.waitingMoney:
            client.setState(ClientSession.notReady)
            client.sendMessage("015")
        elif state == ClientSession.notReady:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Client isn't ready"))
        elif state == ClientSession.ready:
            answer = QtGui.QInputDialog.getInteger(self.parent(), _("Enter time"), _("Enter time in minutes"),
                                                   int(self.config.price_fixedpriceminutes),
                                                   2,
                                                   1440, 15)
            if answer[1] != False:
                myTime = QtCore.QDateTime.currentDateTime().addSecs(answer[0]*60)
                client.sendMessage("006" + str(myTime.toTime_t()))
                client.setState(ClientSession.loggedIn, user = "guest", endTime = myTime)

    def stopClient(self):
        client = self.ui.main_treeWidget.currentItem()
        if not client:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose a client first"))
            return
        state = client.session.state
        if state == ClientSession.notConnected:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Can't connect to client"))
        elif state in (ClientSession.ready, ClientSession.notReady):
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Client is already stopped"))
        elif state == ClientSession.loggedIn:
            answer = QtGui.QMessageBox.question(self.parent(), _("Are you sure?"), _("Do you really want to stop this client?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                client.sendMessage("009")
                client.setState(ClientSession.notReady)
        elif state == ClientSession.requestedOpening:
            client.sendMessage("0010")
            client.setState(ClientSession.ready)
        elif state == ClientSession.waitingMoney:
            client.setState(ClientSession.notReady)
            client.sendMessage("015")

    def changeButton(self):
        pass

    def remoteButton(self):
        client = self.ui.main_treeWidget.currentItem()
        if not client:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose a client first"))
            return
        if client.session.state == ClientSession.notConnected:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Can't connect to client"))
            return
        os.system("krdc -s -f -l -c %s&" % client.ip)

    def shutdownButton(self):
        client = self.ui.main_treeWidget.currentItem()
        if not client:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose a client first"))
            return
        state = client.session.state
        if state == ClientSession.notConnected:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Can't connect to client"))
            return
        answer = QtGui.QMessageBox.question(self.parent(), _("Are you sure?"), _("Do you really want to shutdown this client?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            client.sendMessage("010")
            client.setState(ClientSession.notConnected)

    def addMember(self, toDatabase = True, memberInformation = None):
        "Adds a new member"
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
                                 str(self.ui.members_payingType.currentText()), 0]
        if "" in memberInformation:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("All member information must be filled"))
        else:
            memberInformation[1] = sha.new(unicode(self.ui.members_password.text())).hexdigest()
            if toDatabase:
                try:
                    Database().runOnce("insert into members values (?,?,?,?,?,?,?,?)", memberInformation)
                    Database().runOnce("insert into member_settings values (?,?,?)", (memberInformation[0], "wallpaper", ""))
                    self.members.append(Member(self.ui.members_treeWidget, memberInformation[:7]))
                    self.filterMembers(self.ui.members_filter.text())
                    self.ui.statusbar.showMessage(_("Added member"))
                    logger.add(logger.logTypes.information, _("Added member"), member = memberInformation[0])
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
        if member.userName == "guest":
            QtGui.QMessageBox.information(self.parent(), _("Error"), _("You can't change guest"))
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
                Database().runOnce("update member_settings set username=? where username = ?", (memberInformation[0], member.userName))
                member.updateValues(memberInformation[:7])
                self.filterMembers(self.ui.members_filter.text())
                logger.add(logger.logTypes.warning, _("Updated member"), member = member.userName)
                self.ui.statusbar.showMessage(_("Updated member information"))
            except sqlite.IntegrityError:
                QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Username must be unique"))
        else:
            del(memberInformation[1])
            try:
                Database().runOnce("update members set username=?,name=?,starting_date=?,finish_date=?,debt=?,paying_type=? where username=?", memberInformation)
                Database().runOnce("update member_settings set username=? where username = ?", (memberInformation[0], member.userName))
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
        if member.userName == "guest":
            QtGui.QMessageBox.information(self.parent(), _("Error"), _("You can't delete guest"))
            return
        answer = QtGui.QMessageBox.question(self.parent(), _("Are you sure?"), _("Do you really want to delete this member?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            Database().runOnce("delete from members where username = ?", (member.userName,))
            Database().runOnce("delete from member_settings where username = ?", (member.userName,))
            self.ui.members_treeWidget.takeTopLevelItem(self.ui.members_treeWidget.indexOfTopLevelItem(member))
            del(self.members[self.members.index(member)])
            self.filterMembers(self.ui.members_filter.text())
            logger.add(logger.logTypes.warning, _("Deleted member"), member = member.userName)
            self.ui.statusbar.showMessage(_("Deleted member"))

    def memberReports(self):
        "Shows statistics about selected member"
        member = self.ui.members_treeWidget.currentItem()
        if not member:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("You must select a member first"))
            return
        dialog = QtGui.QDialog(self.parent())
        reportwindow = Ui_MemberReports()
        reportwindow.setupUi(dialog, member.userName)
        dialog.show()

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

    def productChanged(self, current, previous):
        product = current
        if not product:
            product = previous
        self.ui.orders_itemLineEdit.setText(product.name)
        self.ui.orders_spinBox_2.setValue(product.price)
        self.ui.orders_spinBox_3.setValue(product.quantity)

    def filterMembers(self, text):
        for member in self.members:
            member.setHidden(False)
            if unicode(text) not in member.userName:
                member.setHidden(True)

    def localize(self):
        conv = locale.localeconv()
        symbol = conv['currency_symbol']
        if conv['p_cs_precedes']:
            symbol += ' '
            self.ui.members_debt.setPrefix(symbol)
            self.ui.orders_spinBox_2.setPrefix(symbol)
        else:
            symbol = ' ' + symbol
            self.ui.members_debt.setSuffix(symbol)
            self.ui.orders_spinBox_2.setSuffix(symbol)

    def addProduct(self):
        productName = unicode(self.ui.orders_itemLineEdit.text())
        price = self.ui.orders_spinBox_2.value()
        quantity = self.ui.orders_spinBox_3.value()
        if not productName:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("You must enter a product name"))
            return
        if price <= 0:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Price must be bigger than 0"))
            return
        try:
            Database().runOnce("insert into products values (?,?,?)", (productName, price, quantity))
            self.products.append(Product(self.ui.orders_treeWidget_2, (productName, price, quantity)))
            self.ui.statusbar.showMessage(_("Added product"))
        except sqlite.IntegrityError:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Product name must be unique"))

    def updateProduct(self):
        product = self.ui.orders_treeWidget_2.currentItem()
        if not product:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("You must select a product first"))
            return
        productName = unicode(self.ui.orders_itemLineEdit.text())
        price = self.ui.orders_spinBox_2.value()
        quantity = self.ui.orders_spinBox_3.value()
        if not productName:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("You must enter a product name"))
            return
        if price <= 0:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Price must be bigger than 0"))
            return
        try:
            Database().runOnce("update products set product_name=?, unit_price=?, stock=? where product_name=?", (productName, price, quantity, product.name))
            product.updateValues((productName, price, quantity))
            self.ui.statusbar.showMessage(_("Updated product"))
        except sqlite.IntegrityError:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Product name must be unique"))

    def deleteProduct(self):
        product = self.ui.orders_treeWidget_2.currentItem()
        if not product:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("You must select a product first"))
            return
        answer = QtGui.QMessageBox.question(self.parent(), _("Are you sure?"), _("Do you really want to delete this product?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            Database().runOnce("delete from products where product_name = ?", (product.name,))
            self.ui.orders_treeWidget_2.takeTopLevelItem(self.ui.orders_treeWidget_2.indexOfTopLevelItem(product))
            del(self.products[self.products.index(product)])
            self.ui.statusbar.showMessage(_("Deleted product"))

    def about(self):
        QtGui.QMessageBox.about(self.parent(), _("About pyKafe"), "pyKafe v0.1_alpha1\n\n" + _("Authors:") + u"\nUğur Çetin\nMustafa Sarı\n\n" + _("Mentor:") + u"\nA. Tevfik İnan")

    def aboutQt(self):
        QtGui.QMessageBox.aboutQt(self.parent())

    def settings(self):
        self.settingsDialog = QtGui.QDialog(self.parent())
        QtCore.QObject.connect(self.settingsDialog, QtCore.SIGNAL("accepted()"), self.sendOptions)
        settingsUi = Ui_SettingsWindow()
        settingsUi.setupUi(self.settingsDialog, self.config)
        self.settingsDialog.show()

    def settingsButton(self, add = False):
        client = self.ui.main_treeWidget.currentItem()
        if not client and not add:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose a client first"))
            return
        clientSettingsDialog = QtGui.QDialog(self.parent())
        self.clientSettingsUi = Ui_ClientSettingsWindow()
        self.clientSettingsUi.setupUi(clientSettingsDialog, client)
        if add:
            clientSettingsDialog.setWindowTitle(_("Add Computer"))
            clientSettingsDialog.setWindowIcon(self.ui.pyKafeIcon)
            QtCore.QObject.connect(clientSettingsDialog, QtCore.SIGNAL("accepted()"), self.clientAdder)
        else:
            QtCore.QObject.connect(clientSettingsDialog, QtCore.SIGNAL("accepted()"), self.changeClient)
        clientSettingsDialog.show()

    def changeClient(self):
        client = self.ui.main_treeWidget.currentItem()
        if not validIp(unicode(self.clientSettingsUi.clientIP.text())):
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Invalid ip address"))
            return
        client.updateInformation(self.parent(), unicode(self.clientSettingsUi.clientID.text()), self.clientSettingsUi.clientIP.text())

    def addClient(self):
        self.settingsButton(add = True)

    def clientAdder(self):
        name = unicode(self.clientSettingsUi.clientID.text())
        ip = unicode(self.clientSettingsUi.clientIP.text())
        if not validIp(ip):
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Invalid ip address"))
            return
        try:
            Database().runOnce("insert into computers(ip,name) values(?,?)", (ip, name))
            info = ClientInformation(ip, name)
            self.clients.append(Client(self.ui.main_treeWidget, info, self.config, self))
        except sqlite.IntegrityError:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Client ip and name must be unique"))

    def sendOptions(self):
        "Sends internet filtering and pricing settings to all clients"
        if self.config.filter_enable:
            filterMessage = "007"
            filterFile = open(self.config.filter_file)
            filters = filterFile.readlines()
            filterFile.close()
            for i in filters:
                filterMessage += i
            filterMessage = filterMessage.strip()
        priceMessage = "016"
        priceMessage += "%s|%s|%s|%s" % (self.config.price_fixedprice,
                                         self.config.price_fixedpriceminutes,
                                         self.config.price_onehourprice,
                                         self.config.price_rounding)
        for client in self.clients:
            if client.session.state != ClientSession.notConnected:
                client.sendMessage(priceMessage)
                if self.config.filter_enable:
                    client.sendMessage(filterMessage)

    def orderAdd(self, order = None, clientName = None, toDatabase = True):
        if not order:
            clientName = self.ui.orders_idComboBox.currentText()
            order = (self.ui.orders_itemComboBox.currentText(), self.ui.orders_spinBox_1.value())
        self.orders.append(Order(self.ui.orders_treeWidget_1, order, clientName, toDatabase))

    def orderChanged(self, current, previous):
        order = current
        if not order:
            order = previous
            if not order: return
        self.ui.orders_idComboBox.setCurrentIndex(self.ui.orders_idComboBox.findText(order.clientName))
        self.ui.orders_itemComboBox.setCurrentIndex(self.ui.orders_itemComboBox.findText(order.productName))
        self.ui.orders_spinBox_1.setValue(order.quantity)

    def orderUpdate(self):
        order = self.ui.orders_treeWidget_1.currentItem()
        if not order:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose an order first"))
            return
        order.update(self.ui.orders_idComboBox.currentText() ,self.ui.orders_itemComboBox.currentText(), self.ui.orders_spinBox_1.value())

    def orderCancel(self, question = True):
        order = self.ui.orders_treeWidget_1.currentItem()
        if not order:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose an order first"))
            return
        if question:
            answer = QtGui.QMessageBox.question(self.parent(), _("Are you sure?"), _("Do you really want to cancel this order?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        else:
            answer = QtGui.QMessageBox.Yes
        if answer == QtGui.QMessageBox.Yes:
            Database().runOnce("delete from orders where product_name=? and quantity=? and computer_name=?", (order.productName, order.quantity, order.clientName))
            self.ui.orders_treeWidget_1.takeTopLevelItem(self.ui.orders_treeWidget_1.indexOfTopLevelItem(order))
            del(self.orders[self.orders.index(order)])
            self.ui.statusbar.showMessage(_("Cancelled order"))

    def orderDelete(self):
        order = self.ui.orders_treeWidget_1.currentItem()
        if not order:
            QtGui.QMessageBox.information(self.parent(), _("Information"), _("Choose an order first"))
            return
        stocks = Database().runOnce("select stock from products where product_name=?", (order.productName,))[0][0]
        if order.quantity>stocks:
            QtGui.QMessageBox.warning(self.parent(), _("Warning"), _("Order quantity exceeds stocks. Stocks will be set to 0"))
            Database().runOnce("update products set stock=? where product_name=?", (0, order.productName))
            for product in self.products:
                if product.name == order.productName:
                    product.setText(2, "0")
        else:
            Database().runOnce("update products set stock=? where product_name=?", (stocks - order.quantity, order.productName))
            for product in self.products:
                if product.name == order.productName:
                    product.quantity = stocks - order.quantity
                    product.setText(2, str(product.quantity))
        for client in self.clients:
            if client.name == order.clientName:
                logger.add(logger.logTypes.information, _("cafeteria item sold"), order.clientName, client.session.user, order.price())
                Database().runOnce("insert into safe values(?,?,?)", (QtCore.QDateTime.currentDateTime().toTime_t(), self.config.last_cashier, order.price()))
                client.session.addOrder(order.productName, order.price())
        self.orderCancel(question = False)

    def refreshLogs(self):
        startDate = self.ui.logs_dateTimeEdit_1.dateTime().toTime_t()
        endDate = self.ui.logs_dateTimeEdit_2.dateTime().toTime_t()
        if startDate>endDate:
            QtGui.QMessageBox.warning(self.parent(), _("Warning"), _("Starting time must be smaller than ending time. They will be set to equal"))
            self.ui.logs_dateTimeEdit_1.setDateTime(self.ui.logs_dateTimeEdit_2.dateTime())
            return
        self.logs = []
        logs = Database().runOnce("select date,log_type,log_value,cashier,computer,member,income from logs where date between ? and ?", (startDate, endDate))
        for log in logs:
            time = QtCore.QDateTime.fromTime_t(log[0]).toString("dd.MM.yyyy hh.mm")
            type = log[1]
            if type == logger.logTypes.emergency: type = _("emergency")
            elif type == logger.logTypes.warning: type = _("warning")
            elif type == logger.logTypes.error: type = _("error")
            elif type == logger.logTypes.information: type = _("information")
            self.logs.append(Log(self.ui.logs_treeWidget, (time, type) + log[2:]))

    def payment(self, client):
        paymentDialog = QtGui.QDialog(self.parent())
        paymentUi = Ui_PaymentDialog()
        paymentUi.setupUi(paymentDialog)
        totalCost = client.session.calculateTotal(self.config)
        cost = client.session.calculatePrice(self.config)
        paymentUi.totalCost.setValue(totalCost)
        paymentUi.label_3.setText("%s: %s" % (client.name, client.session.user))
        time = client.session.startTime.secsTo(QtCore.QDateTime.currentDateTime())
        paymentUi.usedTime.setTime(QtCore.QTime().addSecs(time))
        for order in client.session.orders:
            print order
            QtGui.QTreeWidgetItem(paymentUi.cafeteriaWidget, [order[0], currency(order[1])])
        paymentDialog.show()
        payingType, credit = Database().runOnce("select paying_type, debt from members where username=?",(client.session.user,))[0]
        if payingType == _("Pre Paid"):
            credit = Database().runOnce("select debt from members where username = ?", (client.session.user,))[0][0]
            if totalCost > credit:
                QtGui.QMessageBox.warning(self.parent(), _("Low credit"), _("%s's credit has finished! Has %s debt.") % (client.session.user, currency(totalCost - credit)))
                logger.add(logger.logTypes.warning, _("Member has low credit"), client.name, client.session.user, totalCost - credit)
            else:
                logger.add(logger.logTypes.information, _("Money paid"), client.name, client.session.user, totalCost)
                Database().runOnce("insert into safe values(?,?,?)", (QtCore.QDateTime.currentDateTime().toTime_t(), self.config.last_cashier, cost))
            self.initMembers()
            Database().runOnce("update members set debt=? where username=?", (totalCost - credit, client.session.user))
        else:
            Database().runOnce("insert into safe values(?,?,?)", (QtCore.QDateTime.currentDateTime().toTime_t(), self.config.last_cashier, cost))
            logger.add(logger.logTypes.information, _("Money paid"), client.name, client.session.user, totalCost)
        for order in self.orders:
            if order.clientName == client.name:
                Database().runOnce("delete from orders where product_name=? and quantity=? and computer_name=?", (order.productName, order.quantity, order.clientName))
                self.ui.orders_treeWidget_1.takeTopLevelItem(self.ui.orders_treeWidget_1.indexOfTopLevelItem(order))
                del(self.orders[self.orders.index(order)])
