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

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class SettingsManager:
    def __init__(self, ui, parent, config):
        self.ui = ui
        self.parent = parent
        self.config = config
        self.readFromConfig()
        self.filterItems = []
        self.filterEnable()
        self.filterRead()

    def filterAdd(self, text = None):
        if not text:
            text = self.ui.filter_address.text()
        if not text:
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
        del(self.filterItems)

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
        if self.ui.filter_enable.checkState() == QtCore.Qt.Checked:
            self.config.set("filter_enable", 1)
        else:
            self.config.set("filter_enable", "")
        filters = []
        for i in self.filterItems:
            filters.append(unicode(i.text(0))+'\n')
        filter_file = open(self.config.filter_file, "w")
        filter_file.writelines(filters)
        filter_file.close()
        self.config.set("filter_file", unicode(self.ui.filter_file.text()))
        self.parent.close()

    def readFromConfig(self):
        if self.config.filter_enable:
            self.ui.filter_enable.setCheckState(QtCore.Qt.Checked)
        self.ui.filter_file.setText(self.config.filter_file)

    def filterRead(self):
        file = open(unicode(self.ui.filter_file.text()))
        filters = file.readlines()
        file.close()
        for i in filters:
            self.filterAdd(i.rstrip())
