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

from PyQt4 import QtCore, QtGui
from settings import SettingsManager

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow, config):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(QtCore.QSize(QtCore.QRect(0,0,468,300).size()).expandedTo(SettingsWindow.minimumSizeHint()))
        SettingsWindow.setWindowIcon(QtGui.QIcon("../../data/icons/pyKafe.png"))

        self.gridlayout = QtGui.QGridLayout(SettingsWindow)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(SettingsWindow)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.checkBox_2 = QtGui.QCheckBox(self.tab)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridlayout1.addWidget(self.checkBox_2,1,0,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,2,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,2,1,1,1)

        self.checkBox = QtGui.QCheckBox(self.tab)
        self.checkBox.setObjectName("checkBox")
        self.gridlayout1.addWidget(self.checkBox,0,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem2 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem2,2,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem3,4,1,1,1)

        self.lineEdit_4 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridlayout2.addWidget(self.lineEdit_4,3,1,1,1)

        self.lineEdit_3 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridlayout2.addWidget(self.lineEdit_3,2,1,1,1)

        self.lineEdit_2 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridlayout2.addWidget(self.lineEdit_2,1,1,1,1)

        self.lineEdit = QtGui.QLineEdit(self.tab_2)
        self.lineEdit.setObjectName("lineEdit")
        self.gridlayout2.addWidget(self.lineEdit,0,1,1,1)

        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridlayout2.addWidget(self.label_4,3,0,1,1)

        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3,2,0,1,1)

        self.label = QtGui.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridlayout2.addWidget(self.label,0,0,1,1)

        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,1,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setObjectName("label_5")
        self.gridlayout3.addWidget(self.label_5,0,0,1,1)

        self.label_6 = QtGui.QLabel(self.tab_3)
        self.label_6.setObjectName("label_6")
        self.gridlayout3.addWidget(self.label_6,1,0,1,1)

        self.spinBox_2 = QtGui.QSpinBox(self.tab_3)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridlayout3.addWidget(self.spinBox_2,1,1,1,1)

        self.spinBox = QtGui.QSpinBox(self.tab_3)
        self.spinBox.setObjectName("spinBox")
        self.gridlayout3.addWidget(self.spinBox,0,1,1,1)

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem4,1,2,1,1)

        spacerItem5 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem5,2,0,1,1)
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout4 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_8 = QtGui.QLabel(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.hboxlayout.addWidget(self.label_8)

        self.filter_file = QtGui.QLineEdit(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_file.sizePolicy().hasHeightForWidth())
        self.filter_file.setSizePolicy(sizePolicy)
        self.filter_file.setReadOnly(True)
        self.filter_file.setObjectName("filter_file")
        self.hboxlayout.addWidget(self.filter_file)

        self.filter_browse = QtGui.QPushButton(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_browse.sizePolicy().hasHeightForWidth())
        self.filter_browse.setSizePolicy(sizePolicy)
        self.filter_browse.setIcon(QtGui.QIcon("../../data/icons/fileopen.png"))
        self.filter_browse.setObjectName("filter_browse")
        self.hboxlayout.addWidget(self.filter_browse)
        self.gridlayout4.addLayout(self.hboxlayout,1,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_7 = QtGui.QLabel(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.hboxlayout1.addWidget(self.label_7)

        self.filter_address = QtGui.QLineEdit(self.tab_4)
        self.filter_address.setObjectName("filter_address")
        self.hboxlayout1.addWidget(self.filter_address)

        self.filter_add = QtGui.QPushButton(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_add.sizePolicy().hasHeightForWidth())
        self.filter_add.setSizePolicy(sizePolicy)
        self.filter_add.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.filter_add.setObjectName("filter_add")
        self.hboxlayout1.addWidget(self.filter_add)

        self.filter_delete = QtGui.QPushButton(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_delete.sizePolicy().hasHeightForWidth())
        self.filter_delete.setSizePolicy(sizePolicy)
        self.filter_delete.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.filter_delete.setObjectName("filter_delete")
        self.hboxlayout1.addWidget(self.filter_delete)

        self.filter_update = QtGui.QPushButton(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_update.sizePolicy().hasHeightForWidth())
        self.filter_update.setSizePolicy(sizePolicy)
        self.filter_update.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.filter_update.setObjectName("filter_update")
        self.hboxlayout1.addWidget(self.filter_update)
        self.gridlayout4.addLayout(self.hboxlayout1,2,0,1,1)

        self.filter_treeWidget = QtGui.QTreeWidget(self.tab_4)
        self.filter_treeWidget.setRootIsDecorated(False)
        self.filter_treeWidget.setItemsExpandable(False)
        self.filter_treeWidget.setSortingEnabled(True)
        self.filter_treeWidget.setObjectName("filter_treeWidget")
        self.gridlayout4.addWidget(self.filter_treeWidget,3,0,1,1)

        self.filter_enable = QtGui.QCheckBox(self.tab_4)
        self.filter_enable.setObjectName("filter_enable")
        self.gridlayout4.addWidget(self.filter_enable,0,0,1,1)
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_5)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        spacerItem6 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout5.addItem(spacerItem6,1,1,1,1)

        self.cashiers_treeWidget = QtGui.QTreeWidget(self.tab_5)
        self.cashiers_treeWidget.setRootIsDecorated(False)
        self.cashiers_treeWidget.setSortingEnabled(True)
        self.cashiers_treeWidget.setObjectName("cashiers_treeWidget")
        self.gridlayout5.addWidget(self.cashiers_treeWidget,0,0,3,1)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setMargin(0)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.cashiers_password = QtGui.QLineEdit(self.tab_5)
        self.cashiers_password.setEchoMode(QtGui.QLineEdit.Password)
        self.cashiers_password.setObjectName("cashiers_password")
        self.gridlayout6.addWidget(self.cashiers_password,1,1,1,1)

        self.cashiers_username = QtGui.QLineEdit(self.tab_5)
        self.cashiers_username.setObjectName("cashiers_username")
        self.gridlayout6.addWidget(self.cashiers_username,0,1,1,1)

        self.textLabel3_2 = QtGui.QLabel(self.tab_5)
        self.textLabel3_2.setWordWrap(False)
        self.textLabel3_2.setObjectName("textLabel3_2")
        self.gridlayout6.addWidget(self.textLabel3_2,2,0,1,1)

        self.textLabel1_3 = QtGui.QLabel(self.tab_5)
        self.textLabel1_3.setWordWrap(False)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.gridlayout6.addWidget(self.textLabel1_3,0,0,1,1)

        self.textLabel2_2 = QtGui.QLabel(self.tab_5)
        self.textLabel2_2.setWordWrap(False)
        self.textLabel2_2.setObjectName("textLabel2_2")
        self.gridlayout6.addWidget(self.textLabel2_2,1,0,1,1)

        self.cashiers_realName = QtGui.QLineEdit(self.tab_5)
        self.cashiers_realName.setObjectName("cashiers_realName")
        self.gridlayout6.addWidget(self.cashiers_realName,2,1,1,1)
        self.gridlayout5.addLayout(self.gridlayout6,0,1,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem7 = QtGui.QSpacerItem(80,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem7)

        self.cashiers_addButton = QtGui.QPushButton(self.tab_5)
        self.cashiers_addButton.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.cashiers_addButton.setObjectName("cashiers_addButton")
        self.hboxlayout2.addWidget(self.cashiers_addButton)

        self.cashiers_updateButton = QtGui.QPushButton(self.tab_5)
        self.cashiers_updateButton.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.cashiers_updateButton.setObjectName("cashiers_updateButton")
        self.hboxlayout2.addWidget(self.cashiers_updateButton)

        self.cashiers_deleteButton = QtGui.QPushButton(self.tab_5)
        self.cashiers_deleteButton.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.cashiers_deleteButton.setObjectName("cashiers_deleteButton")
        self.hboxlayout2.addWidget(self.cashiers_deleteButton)

        self.cashiers_reportsButton = QtGui.QPushButton(self.tab_5)
        self.cashiers_reportsButton.setIcon(QtGui.QIcon("../../data/icons/find.png"))
        self.cashiers_reportsButton.setObjectName("cashiers_reportsButton")
        self.hboxlayout2.addWidget(self.cashiers_reportsButton)
        self.gridlayout5.addLayout(self.hboxlayout2,2,1,1,1)
        self.tabWidget.addTab(self.tab_5,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(SettingsWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,1,0,1,1)

        self.retranslateUi(SettingsWindow)
        self.tabWidget.setCurrentIndex(4)
        self.manager = SettingsManager(self, SettingsWindow, config)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),self.manager.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),SettingsWindow.close)
        QtCore.QObject.connect(self.filter_add,QtCore.SIGNAL("clicked()"),self.manager.filterAdd)
        QtCore.QObject.connect(self.filter_delete,QtCore.SIGNAL("clicked()"),self.manager.filterDelete)
        QtCore.QObject.connect(self.filter_update,QtCore.SIGNAL("clicked()"),self.manager.filterUpdate)
        QtCore.QObject.connect(self.filter_treeWidget,QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"),self.manager.filterChanged)
        QtCore.QObject.connect(self.filter_enable,QtCore.SIGNAL("stateChanged(int)"),self.manager.filterEnable)
        QtCore.QObject.connect(self.filter_browse,QtCore.SIGNAL("clicked()"),self.manager.filterBrowse)
        QtCore.QObject.connect(self.cashiers_treeWidget,QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"),self.manager.cashierChanged)
        QtCore.QObject.connect(self.cashiers_addButton,QtCore.SIGNAL("clicked()"),self.manager.cashierAdd)
        QtCore.QObject.connect(self.cashiers_deleteButton,QtCore.SIGNAL("clicked()"),self.manager.cashierDelete)
        QtCore.QObject.connect(self.cashiers_updateButton,QtCore.SIGNAL("clicked()"),self.manager.cashierUpdate)
        QtCore.QObject.connect(self.cashiers_reportsButton,QtCore.SIGNAL("clicked()"),self.manager.cashierReports)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(_("PyKafe Settings"))
        self.checkBox_2.setText(_("Ask password when opening"))
        self.checkBox.setText(_("Tray Icon"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _("General"))
        self.label_4.setText(_("Decimals Seperator:"))
        self.label_3.setText(_("Thousands seperator:"))
        self.label.setText(_("Currency prefix:"))
        self.label_2.setText(_("Currency suffix:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _("Regional"))
        self.label_5.setText(_("Fixed price for first 30 minutes:"))
        self.label_6.setText(_("Price for one hour:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _("Pricing"))
        self.label_8.setText(_("Filter File:"))
        self.filter_browse.setToolTip(_("Browse"))
        self.label_7.setText(_("Addres:"))
        self.filter_add.setToolTip(_("Add"))
        self.filter_delete.setToolTip(_("Delete"))
        self.filter_treeWidget.headerItem().setText(0,_("Filtered Addresses"))
        self.filter_enable.setText(_("Enable Internet Filter"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _("Internet Filter"))
        self.cashiers_treeWidget.headerItem().setText(0,_("Cashier List"))
        self.textLabel3_2.setText(_("Real Name:"))
        self.textLabel1_3.setText(_("Username:"))
        self.textLabel2_2.setText(_("Password:"))
        self.cashiers_addButton.setText(_("Add"))
        self.cashiers_updateButton.setText(_("Update"))
        self.cashiers_deleteButton.setText(_("Delete"))
        self.cashiers_reportsButton.setText(_("Reports"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _("Cashiers"))
