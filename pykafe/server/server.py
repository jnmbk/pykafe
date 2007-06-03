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
from settingswindow import Ui_SettingsWindow
from currencyformat import currency
import logger
import base64, sha, os

import locale, gettext
locale.setlocale(locale.LC_MESSAGES, "C")
locale.setlocale(locale.LC_MONETARY, "")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext


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
    def __init__(self, parent, socketDescriptor, clients, config):
        QtCore.QThread.__init__(self, parent)
        self.socketDescriptor = socketDescriptor
        self.clients = clients
        self.config = config

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
                db = Database()
                db.cur.execute("select count() from members where username = ? and password = ?", (username, password))
                if db.cur.fetchall()[0][0]:
                    client.sendMessage("0031")
                    logger.add(logger.logTypes.information, _("Member logged in"), computer = client.name, member = username)
                    self.emit(QtCore.SIGNAL("stateChange"), self.clientNumber, ClientSession.loggedIn, user = username)
                else:
                    logger.add(logger.logTypes.warning, _("Someone entered wrong password or username"), computer = client.name, member = username)
                    client.sendMessage("0030")
        self.tcpSocket.disconnectFromHost()


class ClientThread(QtCore.QThread):
    def __init__(self, parent, config):
        QtCore.QThread.__init__(self)
        self.client = parent
        self.config = config
    def run(self):
        while(True):
            if self.client.session.state == ClientSession.loggedIn:
                self.emit(QtCore.SIGNAL("changetext"),3,currency(self.client.session.calculatePrice(self.config)))
                usedTime = QtCore.QDateTime()
                usedTime.setTime_t(self.client.session.startTime.secsTo(QtCore.QDateTime.currentDateTime()))
                self.emit(QtCore.SIGNAL("changetext"),4,usedTime.toUTC().time().toString("hh.mm"))
            self.sleep(int(self.config.ui_refreshdelay))

class Client(QtGui.QTreeWidgetItem):
    def __init__(self, parent, clientInformation, config):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.config = config
        self.fillList(clientInformation)
        watcherThread = ClientThread(self, config)
        QtCore.QObject.connect(watcherThread, QtCore.SIGNAL("changetext"), self.setText)
        watcherThread.start()
        self.threads = [watcherThread]

    def fillList(self, clientInformation):
        self.session = clientInformation.session
        self.ip = clientInformation.ip
        self.name = clientInformation.name
        self.setText(0, self.name)
        self.setState(ClientSession.notConnected)

    def changeColor(self, colorName):
        for i in range(self.columnCount()):
            self.setBackground(i, QtGui.QBrush(QtGui.QColor(colorName)))

    def sendMessage(self, message):
        thread = MessageSender(self.ip, int(self.config.network_port), message)
        thread.start()
        self.threads.append(thread)
        print "This client has %d threads" % len(self.threads)

    def setState(self, state, user = "guest", endTime = ""):
        if state == ClientSession.loggedIn:
            self.session.user = user
            self.session.startTime = QtCore.QDateTime.currentDateTime()
            self.setTexts((2,3,4), (user,currency(0.0), self.session.startTime.time().toString("00.00")))
            if endTime:
                self.session.endTime = endTime
                self.setText(5, self.session.endTime.time().toString("hh.mm"))
            self.changeColor("green")
        elif state == ClientSession.notReady:
            #if self.session.state in (ClientSession.notConnected, ClientSession.notReady):
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
        logger.add(logger.logTypes.information, _("State changed to %s") % self.session.toString(), member = self.name)
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
        self.setText(1,currency(float(self.price)))
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
            self.clients.append(Client(ui.main_treeWidget, clientInformation, self.config))
        ui.main_treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        self.initMembers(first = True)
        self.initProducts()
        self.localize()
        self.threads = []

    def initMembers(self, first = False):
        #TODO: Call this function after adding and deleting
        if first:
            self.members = []
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

    def incomingConnection(self, socketDescriptor):
        thread = ListenerThread(self.parent(), socketDescriptor, self.clients, self.config)
        self.threads.append(thread)
        QtCore.QObject.connect(thread, QtCore.SIGNAL("stateChange"), self.setClientState)
        thread.start()
        print "We have %d thread(s)" % len(self.threads)

    def setClientState(self, client, state):
        self.clients[client].setState(state)

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
            client.setState(ClientSession.ready)
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
            client.setState(ClientSession.ready)
            client.sendMessage("015")
        elif state == ClientSession.notReady:
            QtGui.QMessageBox.critical(self.parent(), _("Error"), _("Client isn't ready"))
        elif state == ClientSession.ready:
            answer = QtGui.QInputDialog.getInteger(self.parent(), _("Enter time"), _("Enter time in minutes"),
                                                   int(self.config.price_fixedpriceminutes),
                                                   int(self.config.price_fixedpriceminutes),
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
            client.setState(ClientSession.ready)
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

    def settingsButton(self):
        pass

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
            self.ui.members_treeWidget.takeTopLevelItem(self.ui.members_treeWidget.indexOfTopLevelItem(member))
            del(self.members[self.members.index(member)])
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
