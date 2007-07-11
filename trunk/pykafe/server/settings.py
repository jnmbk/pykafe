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

from PyQt4 import QtGui, QtCore
from pysqlite2 import dbapi2 as sqlite
from database import Database
from cashierreports import Ui_CashierReports
import sha, socket

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
locale.setlocale(locale.LC_MONETARY, "")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

def getSiteIP(site):
    try:
        return socket.gethostbyname(str(site))
    except socket.gaierror:
        return False

class Cashier(QtGui.QTreeWidgetItem):
    def __init__(self, parent, cashierInformation):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.userName, self.password, self.realName = cashierInformation
        self.setText(0, self.userName)
    def updateValues(self, cashierInformation, password = True):
        if password: self.userName, self.password, self.realName = cashierInformation
        else: self.userName, self.realName = cashierInformation
        self.setText(0, self.userName)

class SettingsManager:
    def __init__(self, ui, parent, config):
        self.ui = ui
        self.parent = parent
        self.config = config
        self.readFromConfig()
        self.filterItems = []
        self.filterEnable()
        self.filterRead()
        self.cashiers = []
        self.fillCashiers()
        self.localize()

    def fillCashiers(self):
        cashierList = Database().run("select username,password,name from members where is_cashier='1'")
        for cashierInformation in cashierList:
            self.cashiers.append(Cashier(self.ui.cashiers_treeWidget, cashierInformation))

    def filterAdd(self, text = None, errorDialog = True):
        if not text:
            text = self.ui.filter_address.text()
        #TODO: a QtGui.QProgressDialog() is needed here because getSiteIP takes some time to complete its job
        if errorDialog:
            if not getSiteIP(text):
                QtGui.QMessageBox.critical(self.parent, _("Error"), _("You didn't enter a valid address"))
                return
        self.filterItems.append(QtGui.QTreeWidgetItem(self.ui.filter_treeWidget))
        self.filterItems[-1].setText(0, text)

    def filterDelete(self):
        currentFilter = self.ui.filter_treeWidget.currentItem()
        if not currentFilter:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("You must select a filter first"))
            return
        self.ui.filter_treeWidget.takeTopLevelItem(self.ui.filter_treeWidget.indexOfTopLevelItem(currentFilter))
        del(self.filterItems[self.filterItems.index(currentFilter)])

    def filterUpdate(self):
        currentFilter = self.ui.filter_treeWidget.currentItem()
        if not currentFilter:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("You must select a filter first"))
            return
        currentFilter.setText(0, self.ui.filter_address.text())

    def filterChanged(self, current, previous):
        currentFilter = current
        if not currentFilter:
            currentFilter = previous
        self.ui.filter_address.setText(currentFilter.text(0))

    def filterEnable(self):
        if self.ui.filter_enable.checkState() == QtCore.Qt.Checked:
            self.ui.filter_address.setEnabled(True)
            self.ui.filter_add.setEnabled(True)
            self.ui.filter_delete.setEnabled(True)
            self.ui.filter_update.setEnabled(True)
            self.ui.filter_treeWidget.setEnabled(True)
            self.ui.filter_file.setEnabled(True)
            self.ui.filter_browse.setEnabled(True)
        else:
            self.ui.filter_address.setEnabled(False)
            self.ui.filter_add.setEnabled(False)
            self.ui.filter_delete.setEnabled(False)
            self.ui.filter_update.setEnabled(False)
            self.ui.filter_treeWidget.setEnabled(False)
            self.ui.filter_file.setEnabled(False)
            self.ui.filter_browse.setEnabled(False)

    def filterBrowse(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self.parent, _("Select Filter File"), self.config.filter_file[:self.config.filter_file.rfind('/')], "Text files (*.txt)")
        if not fileName:
            return
        self.ui.filter_file.setText(fileName)
        self.filterRead()
            
    def accept(self):
        if self.ui.filter_enable.checkState() == QtCore.Qt.Checked: self.config.set("filter_enable", 1)
        else: self.config.set("filter_enable", "")
        if self.ui.checkBox_2.checkState() == QtCore.Qt.Checked: self.config.set("startup_askpassword", 1)
        else: self.config.set("startup_askpassword", "")
        filters = []
        for i in self.filterItems:
            filters.append(unicode(i.text(0))+'\n')
        filter_file = open(self.config.filter_file, "w")
        filter_file.writelines(filters)
        filter_file.close()
        self.config.set("filter_file", unicode(self.ui.filter_file.text()))
        self.config.set("price_fixedpriceminutes", str(self.ui.pricing_minutes.value()))
        self.config.set("price_fixedprice", str(self.ui.pricing_fixed.value()))
        self.config.set("price_onehourprice", str(self.ui.pricing_onehour.value()))
        self.config.set("price_rounding", str(self.ui.pricing_rounding.value()))
        #TODO: cashier changes should be applied here, not directly to db!
        self.parent.accept()

    def readFromConfig(self):
        if self.config.filter_enable:
            self.ui.filter_enable.setCheckState(QtCore.Qt.Checked)
        self.ui.filter_file.setText(self.config.filter_file)
        if self.config.startup_askpassword:
            self.ui.checkBox_2.setCheckState(QtCore.Qt.Checked)
        self.ui.pricing_minutes.setValue(int(self.config.price_fixedpriceminutes))
        self.ui.pricing_fixed.setValue(float(self.config.price_fixedprice))
        self.ui.pricing_onehour.setValue(float(self.config.price_onehourprice))
        self.ui.pricing_rounding.setValue(float(self.config.price_rounding))

    def localize(self):
        conv = locale.localeconv()
        symbol = conv['currency_symbol']
        if conv['p_cs_precedes']:
            symbol += ' '
            self.ui.pricing_fixed.setPrefix(symbol)
            self.ui.pricing_onehour.setPrefix(symbol)
            self.ui.pricing_rounding.setPrefix(symbol)
        else:
            symbol = ' ' + symbol
            self.ui.pricing_fixed.setSuffix(symbol)
            self.ui.pricing_onehour.setSuffix(symbol)
            self.ui.pricing_rounding.setSuffix(symbol)

    def filterRead(self):
        file = open(unicode(self.ui.filter_file.text()))
        filters = file.readlines()
        file.close()
        for i in filters:
            self.filterAdd(i.rstrip(), errorDialog = False)
    def cashierAdd(self):
        cashierInformation = [unicode(self.ui.cashiers_username.text()),
                              unicode(self.ui.cashiers_password.text()),
                              unicode(self.ui.cashiers_realName.text())]
        if "" in cashierInformation:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("All cashier information must be filled"))
            return
        cashierInformation[1] = sha.new(unicode(self.ui.cashiers_password.text())).hexdigest()
        try:
            Database().runOnce("insert into members values (?,?,?,'','','','',1)", cashierInformation)
            self.cashiers.append(Cashier(self.ui.cashiers_treeWidget, cashierInformation))
        except sqlite.IntegrityError:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("Username must be unique"))

    def cashierDelete(self):
        if len(self.cashiers) == 1:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("There should be one cashier at least"))
            return
        cashier = self.ui.cashiers_treeWidget.currentItem()
        if not cashier:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("You must select a cashier first"))
            return
        answer = QtGui.QMessageBox.question(self.parent, _("Are you sure?"), _("Do you really want to delete this cashier?"), QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes).__or__(QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            Database().runOnce("delete from members where username = ?", (cashier.userName,))
            self.ui.cashiers_treeWidget.takeTopLevelItem(self.ui.cashiers_treeWidget.indexOfTopLevelItem(cashier))
            del(self.cashiers[self.cashiers.index(cashier)])

    def cashierUpdate(self):
        cashier = self.ui.cashiers_treeWidget.currentItem()
        if not cashier:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("You must select a cashier first"))
            return
        cashierInformation = [unicode(self.ui.cashiers_username.text()),
                              " ",
                              unicode(self.ui.cashiers_realName.text())]
        if "" in cashierInformation:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("All cashier information must be filled"))
            return
        cashierInformation[1] = sha.new(unicode(self.ui.cashiers_password.text())).hexdigest()
        if self.ui.cashiers_password.text():
            try:
                Database().runOnce("update members set username=?,password=?,name=? where username = ?", cashierInformation + [cashierInformation[0],])
                cashier.updateValues(cashierInformation)
            except sqlite.IntegrityError:
                QtGui.QMessageBox.critical(self.parent, _("Error"), _("Username must be unique"))
        else:
            del(cashierInformation[1])
            try:
                Database().runOnce("update members set username=?,name=? where username = ?", cashierInformation + [cashierInformation[0],])
                cashier.updateValues(cashierInformation, password = False)
            except sqlite.IntegrityError:
                QtGui.QMessageBox.critical(self.parent, _("Error"), _("Username must be unique"))
    def cashierReports(self):
        cashier = self.ui.cashiers_treeWidget.currentItem()
        if not cashier:
            QtGui.QMessageBox.critical(self.parent, _("Error"), _("You must select a cashier first"))
            return
        dialog = QtGui.QDialog(self.parent)
        reportwindow = Ui_CashierReports()
        reportwindow.setupUi(dialog, cashier.userName)
        dialog.show()

    def cashierChanged(self, current, previous):
        currentCashier = current
        if not currentCashier:
            currentCashier = previous
        self.ui.cashiers_username.setText(currentCashier.userName)
        self.ui.cashiers_password.clear()
        self.ui.cashiers_realName.setText(currentCashier.realName)
    def checkPricingOnehourValue(self):
        if self.ui.pricing_fixed.value() > self.ui.pricing_onehour.value():
            QtGui.QMessageBox.warning(self.parent, _("Warning"), _("One hour price must be bigger than or equal to fixed price.  Correct value will be set."))
            self.ui.pricing_onehour.setValue(self.ui.pricing_fixed.value())
    def checkPricingFixedValue(self):
        if self.ui.pricing_fixed.value() > self.ui.pricing_onehour.value():
            QtGui.QMessageBox.warning(self.parent, _("Warning"), _("Fixed price must be smaller than or equal to one hour price. Correct value will be set."))
            self.ui.pricing_fixed.setValue(self.ui.pricing_onehour.value())
