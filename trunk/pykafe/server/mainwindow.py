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

import server
from PyQt4 import QtCore, QtGui

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, cashier = None):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,650,500).size()).expandedTo(MainWindow.minimumSizeHint()))
        icon = QtGui.QIcon("../../data/icons/pyKafe.png")
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,8,1,1)

        self.main_startTimeButton = QtGui.QToolButton(self.tab)
        self.main_startTimeButton.setIcon(QtGui.QIcon("../../data/icons/kalarm.png"))
        self.main_startTimeButton.setIconSize(QtCore.QSize(64,64))
        self.main_startTimeButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.main_startTimeButton.setAutoRaise(True)
        self.main_startTimeButton.setObjectName("main_startTimeButton")
        self.gridlayout1.addWidget(self.main_startTimeButton,0,2,1,1)

        self.main_stopButton = QtGui.QToolButton(self.tab)
        self.main_stopButton.setIcon(QtGui.QIcon("../../data/icons/stop.png"))
        self.main_stopButton.setIconSize(QtCore.QSize(64,64))
        self.main_stopButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.main_stopButton.setAutoRaise(True)
        self.main_stopButton.setObjectName("main_stopButton")
        self.gridlayout1.addWidget(self.main_stopButton,0,3,1,1)

        self.main_startButton = QtGui.QToolButton(self.tab)
        self.main_startButton.setIcon(QtGui.QIcon("../../data/icons/player_play.png"))
        self.main_startButton.setIconSize(QtCore.QSize(64,64))
        self.main_startButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.main_startButton.setAutoRaise(True)
        self.main_startButton.setObjectName("main_startButton")
        self.gridlayout1.addWidget(self.main_startButton,0,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem1,0,0,1,1)

        self.main_settingsButton = QtGui.QToolButton(self.tab)
        self.main_settingsButton.setIcon(QtGui.QIcon("../../data/icons/kcontrol.png"))
        self.main_settingsButton.setIconSize(QtCore.QSize(64,64))
        self.main_settingsButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.main_settingsButton.setAutoRaise(True)
        self.main_settingsButton.setObjectName("main_settingsButton")
        self.gridlayout1.addWidget(self.main_settingsButton,0,6,1,1)

        self.main_remoteButton = QtGui.QToolButton(self.tab)
        self.main_remoteButton.setIcon(QtGui.QIcon("../../data/icons/remote.png"))
        self.main_remoteButton.setIconSize(QtCore.QSize(64,64))
        self.main_remoteButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.main_remoteButton.setAutoRaise(True)
        self.main_remoteButton.setObjectName("main_remoteButton")
        self.gridlayout1.addWidget(self.main_remoteButton,0,5,1,1)

        self.main_changeButton = QtGui.QToolButton(self.tab)
        self.main_changeButton.setIcon(QtGui.QIcon("../../data/icons/kontact_contacts.png"))
        self.main_changeButton.setIconSize(QtCore.QSize(64,64))
        self.main_changeButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.main_changeButton.setAutoRaise(True)
        self.main_changeButton.setObjectName("main_changeButton")
        self.gridlayout1.addWidget(self.main_changeButton,0,4,1,1)

        self.main_shutDownButton = QtGui.QToolButton(self.tab)
        self.main_shutDownButton.setIcon(QtGui.QIcon("../../data/icons/exit.png"))
        self.main_shutDownButton.setIconSize(QtCore.QSize(64,64))
        self.main_shutDownButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.main_shutDownButton.setAutoRaise(True)
        self.main_shutDownButton.setObjectName("main_shutDownButton")
        self.gridlayout1.addWidget(self.main_shutDownButton,0,7,1,1)

        self.main_treeWidget = QtGui.QTreeWidget(self.tab)
        self.main_treeWidget.setRootIsDecorated(False)
        self.main_treeWidget.setSortingEnabled(True)
        self.main_treeWidget.setAllColumnsShowFocus(True)
        self.main_treeWidget.setObjectName("main_treeWidget")
        self.gridlayout1.addWidget(self.main_treeWidget,1,0,1,9)
        self.tabWidget.addTab(self.tab,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.splitter = QtGui.QSplitter(self.tab_4)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.groupBox_2 = QtGui.QGroupBox(self.splitter)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setMargin(0)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridlayout4.addWidget(self.label_8,0,1,1,1)

        self.orders_idComboBox = QtGui.QComboBox(self.groupBox_2)
        self.orders_idComboBox.setObjectName("orders_idComboBox")
        self.gridlayout4.addWidget(self.orders_idComboBox,1,0,1,1)

        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridlayout4.addWidget(self.label_7,0,0,1,1)

        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridlayout4.addWidget(self.label_9,0,2,1,1)

        self.orders_itemComboBox = QtGui.QComboBox(self.groupBox_2)
        self.orders_itemComboBox.setObjectName("orders_itemComboBox")
        self.gridlayout4.addWidget(self.orders_itemComboBox,1,1,1,1)

        self.orders_spinBox_1 = QtGui.QSpinBox(self.groupBox_2)
        self.orders_spinBox_1.setMinimum(1)
        self.orders_spinBox_1.setObjectName("orders_spinBox_1")
        self.gridlayout4.addWidget(self.orders_spinBox_1,1,2,1,1)
        self.gridlayout3.addLayout(self.gridlayout4,1,0,1,5)

        self.orders_treeWidget_1 = QtGui.QTreeWidget(self.groupBox_2)
        self.orders_treeWidget_1.setRootIsDecorated(False)
        self.orders_treeWidget_1.setSortingEnabled(True)
        self.orders_treeWidget_1.setObjectName("orders_treeWidget_1")
        self.gridlayout3.addWidget(self.orders_treeWidget_1,0,0,1,5)

        self.orders_cancelButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_cancelButton_1.setIcon(QtGui.QIcon("../../data/icons/button_cancel.png"))
        self.orders_cancelButton_1.setObjectName("orders_cancelButton_1")
        self.gridlayout3.addWidget(self.orders_cancelButton_1,2,4,1,1)

        self.orders_deleteButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_deleteButton_1.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.orders_deleteButton_1.setObjectName("orders_deleteButton_1")
        self.gridlayout3.addWidget(self.orders_deleteButton_1,2,3,1,1)

        self.orders_updateButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_updateButton_1.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.orders_updateButton_1.setObjectName("orders_updateButton_1")
        self.gridlayout3.addWidget(self.orders_updateButton_1,2,2,1,1)

        self.orders_addButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_addButton_1.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.orders_addButton_1.setObjectName("orders_addButton_1")
        self.gridlayout3.addWidget(self.orders_addButton_1,2,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem2,2,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.splitter)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout5 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.orders_treeWidget_2 = QtGui.QTreeWidget(self.groupBox_3)
        self.orders_treeWidget_2.setRootIsDecorated(False)
        self.orders_treeWidget_2.setSortingEnabled(True)
        self.orders_treeWidget_2.setObjectName("orders_treeWidget_2")
        self.gridlayout5.addWidget(self.orders_treeWidget_2,0,0,1,4)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setMargin(0)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.orders_itemLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.orders_itemLineEdit.setObjectName("orders_itemLineEdit")
        self.gridlayout6.addWidget(self.orders_itemLineEdit,1,0,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridlayout6.addWidget(self.label_6,0,2,1,1)

        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.gridlayout6.addWidget(self.label_5,0,1,1,1)

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout6.addWidget(self.label_4,0,0,1,1)

        self.orders_spinBox_3 = QtGui.QSpinBox(self.groupBox_3)
        self.orders_spinBox_3.setMaximum(5000)
        self.orders_spinBox_3.setObjectName("orders_spinBox_3")
        self.gridlayout6.addWidget(self.orders_spinBox_3,1,2,1,1)

        self.orders_spinBox_2 = QtGui.QDoubleSpinBox(self.groupBox_3)
        self.orders_spinBox_2.setMaximum(1000000000.0)
        self.orders_spinBox_2.setObjectName("orders_spinBox_2")
        self.gridlayout6.addWidget(self.orders_spinBox_2,1,1,1,1)
        self.gridlayout5.addLayout(self.gridlayout6,1,0,1,4)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem3,2,0,1,1)

        self.orders_addButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.orders_addButton_2.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.orders_addButton_2.setObjectName("orders_addButton_2")
        self.gridlayout5.addWidget(self.orders_addButton_2,2,1,1,1)

        self.orders_updateButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.orders_updateButton_2.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.orders_updateButton_2.setObjectName("orders_updateButton_2")
        self.gridlayout5.addWidget(self.orders_updateButton_2,2,2,1,1)

        self.orders_deleteButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.orders_deleteButton_2.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.orders_deleteButton_2.setObjectName("orders_deleteButton_2")
        self.gridlayout5.addWidget(self.orders_deleteButton_2,2,3,1,1)
        self.gridlayout2.addWidget(self.splitter,0,0,1,1)
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout7 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.splitter_2 = QtGui.QSplitter(self.tab_2)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.members_treeWidget = QtGui.QTreeWidget(self.layoutWidget)
        self.members_treeWidget.setAlternatingRowColors(True)
        self.members_treeWidget.setRootIsDecorated(False)
        self.members_treeWidget.setSortingEnabled(True)
        self.members_treeWidget.setObjectName("members_treeWidget")
        self.vboxlayout.addWidget(self.members_treeWidget)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.members_clearButton = QtGui.QPushButton(self.layoutWidget)
        self.members_clearButton.setIcon(QtGui.QIcon("../../data/icons/locationbar_erase.png"))
        self.members_clearButton.setFlat(True)
        self.members_clearButton.setObjectName("members_clearButton")
        self.hboxlayout.addWidget(self.members_clearButton)

        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.members_filter = QtGui.QLineEdit(self.layoutWidget)
        self.members_filter.setObjectName("members_filter")
        self.hboxlayout.addWidget(self.members_filter)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.groupBox = QtGui.QGroupBox(self.splitter_2)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout8.setMargin(9)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        spacerItem4 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout8.addItem(spacerItem4,2,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem5 = QtGui.QSpacerItem(80,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem5)

        self.members_addButton = QtGui.QPushButton(self.groupBox)
        self.members_addButton.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.members_addButton.setObjectName("members_addButton")
        self.hboxlayout1.addWidget(self.members_addButton)

        self.members_updateButton = QtGui.QPushButton(self.groupBox)
        self.members_updateButton.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.members_updateButton.setObjectName("members_updateButton")
        self.hboxlayout1.addWidget(self.members_updateButton)

        self.members_deleteButton = QtGui.QPushButton(self.groupBox)
        self.members_deleteButton.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.members_deleteButton.setObjectName("members_deleteButton")
        self.hboxlayout1.addWidget(self.members_deleteButton)

        self.members_reportsButton = QtGui.QPushButton(self.groupBox)
        self.members_reportsButton.setIcon(QtGui.QIcon("../../data/icons/find.png"))
        self.members_reportsButton.setObjectName("members_reportsButton")
        self.hboxlayout1.addWidget(self.members_reportsButton)
        self.gridlayout8.addLayout(self.hboxlayout1,3,0,1,1)

        self.gridlayout9 = QtGui.QGridLayout()
        self.gridlayout9.setMargin(0)
        self.gridlayout9.setSpacing(6)
        self.gridlayout9.setObjectName("gridlayout9")

        self.textLabel5 = QtGui.QLabel(self.groupBox)
        self.textLabel5.setWordWrap(False)
        self.textLabel5.setObjectName("textLabel5")
        self.gridlayout9.addWidget(self.textLabel5,4,0,1,1)

        self.textLabel2_2 = QtGui.QLabel(self.groupBox)
        self.textLabel2_2.setWordWrap(False)
        self.textLabel2_2.setObjectName("textLabel2_2")
        self.gridlayout9.addWidget(self.textLabel2_2,1,0,1,1)

        self.members_payingType = QtGui.QComboBox(self.groupBox)
        self.members_payingType.setObjectName("members_payingType")
        self.gridlayout9.addWidget(self.members_payingType,4,1,1,1)

        self.members_realName = QtGui.QLineEdit(self.groupBox)
        self.members_realName.setObjectName("members_realName")
        self.gridlayout9.addWidget(self.members_realName,2,1,1,1)

        self.textLabel1_3 = QtGui.QLabel(self.groupBox)
        self.textLabel1_3.setWordWrap(False)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.gridlayout9.addWidget(self.textLabel1_3,0,0,1,1)

        self.members_password = QtGui.QLineEdit(self.groupBox)
        self.members_password.setEchoMode(QtGui.QLineEdit.Password)
        self.members_password.setObjectName("members_password")
        self.gridlayout9.addWidget(self.members_password,1,1,1,1)

        self.textLabel4_2 = QtGui.QLabel(self.groupBox)
        self.textLabel4_2.setWordWrap(False)
        self.textLabel4_2.setObjectName("textLabel4_2")
        self.gridlayout9.addWidget(self.textLabel4_2,3,0,1,1)

        self.textLabel3_2 = QtGui.QLabel(self.groupBox)
        self.textLabel3_2.setWordWrap(False)
        self.textLabel3_2.setObjectName("textLabel3_2")
        self.gridlayout9.addWidget(self.textLabel3_2,2,0,1,1)

        self.members_username = QtGui.QLineEdit(self.groupBox)
        self.members_username.setObjectName("members_username")
        self.gridlayout9.addWidget(self.members_username,0,1,1,1)

        self.members_debt = QtGui.QDoubleSpinBox(self.groupBox)
        self.members_debt.setAlignment(QtCore.Qt.AlignRight)
        self.members_debt.setMaximum(1000000000.0)
        self.members_debt.setMinimum(0)
        self.members_debt.setObjectName("members_debt")
        self.gridlayout9.addWidget(self.members_debt,3,1,1,1)
        self.gridlayout8.addLayout(self.gridlayout9,0,0,1,1)

        self.gridlayout10 = QtGui.QGridLayout()
        self.gridlayout10.setMargin(0)
        self.gridlayout10.setSpacing(6)
        self.gridlayout10.setObjectName("gridlayout10")

        self.members_dateEdit = QtGui.QDateEdit(self.groupBox)
        self.members_dateEdit.setAlignment(QtCore.Qt.AlignHCenter)
        self.members_dateEdit.setObjectName("members_dateEdit")
        self.gridlayout10.addWidget(self.members_dateEdit,2,0,1,1)

        self.textLabel7 = QtGui.QLabel(self.groupBox)
        self.textLabel7.setWordWrap(False)
        self.textLabel7.setObjectName("textLabel7")
        self.gridlayout10.addWidget(self.textLabel7,0,0,1,2)

        self.members_dateEdit_2 = QtGui.QDateEdit(self.groupBox)
        self.members_dateEdit_2.setAlignment(QtCore.Qt.AlignHCenter)
        self.members_dateEdit_2.setObjectName("members_dateEdit_2")
        self.gridlayout10.addWidget(self.members_dateEdit_2,2,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridlayout10.addWidget(self.label_2,1,0,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout10.addWidget(self.label_3,1,1,1,1)
        self.gridlayout8.addLayout(self.gridlayout10,1,0,1,1)
        self.gridlayout7.addWidget(self.splitter_2,0,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout11 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout11.setMargin(9)
        self.gridlayout11.setSpacing(6)
        self.gridlayout11.setObjectName("gridlayout11")

        spacerItem6 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout11.addItem(spacerItem6,0,2,1,1)

        spacerItem7 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout11.addItem(spacerItem7,0,0,1,1)

        self.gridlayout12 = QtGui.QGridLayout()
        self.gridlayout12.setMargin(0)
        self.gridlayout12.setSpacing(6)
        self.gridlayout12.setObjectName("gridlayout12")

        self.logs_dateTimeEdit_1 = QtGui.QDateTimeEdit(self.tab_3)
        self.logs_dateTimeEdit_1.setObjectName("logs_dateTimeEdit_1")
        self.gridlayout12.addWidget(self.logs_dateTimeEdit_1,0,0,1,1)

        self.logs_searchButton = QtGui.QPushButton(self.tab_3)
        self.logs_searchButton.setIcon(QtGui.QIcon("../../data/icons/find.png"))
        self.logs_searchButton.setIconSize(QtCore.QSize(64,64))
        self.logs_searchButton.setObjectName("logs_searchButton")
        self.gridlayout12.addWidget(self.logs_searchButton,0,1,2,1)

        self.logs_dateTimeEdit_2 = QtGui.QDateTimeEdit(self.tab_3)
        self.logs_dateTimeEdit_2.setObjectName("logs_dateTimeEdit_2")
        self.gridlayout12.addWidget(self.logs_dateTimeEdit_2,1,0,1,1)
        self.gridlayout11.addLayout(self.gridlayout12,0,1,1,1)

        self.logs_treeWidget = QtGui.QTreeWidget(self.tab_3)
        self.logs_treeWidget.setObjectName("logs_treeWidget")
        self.gridlayout11.addWidget(self.logs_treeWidget,1,0,1,3)
        self.tabWidget.addTab(self.tab_3,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,650,29))
        self.menubar.setObjectName("menubar")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuNew = QtGui.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")

        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionContents = QtGui.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")

        self.actionAbout_pyKafe = QtGui.QAction(MainWindow)
        self.actionAbout_pyKafe.setObjectName("actionAbout_pyKafe")

        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")

        self.actionComputer = QtGui.QAction(MainWindow)
        self.actionComputer.setObjectName("actionComputer")

        self.actionEntertainment = QtGui.QAction(MainWindow)
        self.actionEntertainment.setObjectName("actionEntertainment")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuHelp.addAction(self.actionContents)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_pyKafe)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuNew.addAction(self.actionComputer)
        self.menuNew.addAction(self.actionEntertainment)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.server = server.PykafeServer(MainWindow, self, cashier)
        QtCore.QObject.connect(self.main_startButton,QtCore.SIGNAL("clicked()"),self.server.startClient)
        QtCore.QObject.connect(self.main_stopButton,QtCore.SIGNAL("clicked()"),self.server.stopClient)
        QtCore.QObject.connect(self.actionExit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QObject.connect(self.main_startTimeButton,QtCore.SIGNAL("clicked()"),self.server.startTimed)
        QtCore.QObject.connect(self.orders_addButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_updateButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_deleteButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_cancelButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_addButton_2,QtCore.SIGNAL("clicked()"),self.server.addProduct)
        QtCore.QObject.connect(self.orders_updateButton_2,QtCore.SIGNAL("clicked()"),self.server.updateProduct)
        QtCore.QObject.connect(self.orders_deleteButton_2,QtCore.SIGNAL("clicked()"),self.server.deleteProduct)
        QtCore.QObject.connect(self.members_addButton,QtCore.SIGNAL("clicked()"),self.server.addMember)
        QtCore.QObject.connect(self.members_updateButton,QtCore.SIGNAL("clicked()"),self.server.updateMember)
        QtCore.QObject.connect(self.members_deleteButton,QtCore.SIGNAL("clicked()"),self.server.deleteMember)
        QtCore.QObject.connect(self.members_reportsButton,QtCore.SIGNAL("clicked()"),self.server.memberReports)
        QtCore.QObject.connect(self.main_changeButton,QtCore.SIGNAL("clicked()"),self.server.changeButton)
        QtCore.QObject.connect(self.main_remoteButton,QtCore.SIGNAL("clicked()"),self.server.remoteButton)
        QtCore.QObject.connect(self.main_settingsButton,QtCore.SIGNAL("clicked()"),self.server.settingsButton)
        QtCore.QObject.connect(self.main_shutDownButton,QtCore.SIGNAL("clicked()"),self.server.shutdownButton)
        QtCore.QObject.connect(self.members_treeWidget,QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem *,QTreeWidgetItem *)"),self.server.memberChanged)
        QtCore.QObject.connect(self.members_clearButton,QtCore.SIGNAL("clicked()"),self.members_filter.clear)
        QtCore.QObject.connect(self.members_filter,QtCore.SIGNAL("textChanged(QString)"),self.server.filterMembers)
        QtCore.QObject.connect(self.actionAbout_pyKafe,QtCore.SIGNAL("activated()"),self.server.about)
        QtCore.QObject.connect(self.actionAbout_Qt,QtCore.SIGNAL("activated()"),self.server.aboutQt)
        QtCore.QObject.connect(self.orders_treeWidget_1,QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"),MainWindow.close)
        QtCore.QObject.connect(self.orders_treeWidget_2,QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"),self.server.productChanged)
        QtCore.QObject.connect(self.actionSettings,QtCore.SIGNAL("activated()"),self.server.settings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget,self.main_startButton)
        MainWindow.setTabOrder(self.main_startButton,self.main_startTimeButton)
        MainWindow.setTabOrder(self.main_startTimeButton,self.main_stopButton)
        MainWindow.setTabOrder(self.main_stopButton,self.main_changeButton)
        MainWindow.setTabOrder(self.main_changeButton,self.main_remoteButton)
        MainWindow.setTabOrder(self.main_remoteButton,self.main_settingsButton)
        MainWindow.setTabOrder(self.main_settingsButton,self.main_shutDownButton)
        MainWindow.setTabOrder(self.main_shutDownButton,self.main_treeWidget)
        MainWindow.setTabOrder(self.main_treeWidget,self.orders_treeWidget_1)
        MainWindow.setTabOrder(self.orders_treeWidget_1,self.orders_idComboBox)
        MainWindow.setTabOrder(self.orders_idComboBox,self.orders_itemComboBox)
        MainWindow.setTabOrder(self.orders_itemComboBox,self.orders_addButton_1)
        MainWindow.setTabOrder(self.orders_addButton_1,self.orders_updateButton_1)
        MainWindow.setTabOrder(self.orders_updateButton_1,self.orders_deleteButton_1)
        MainWindow.setTabOrder(self.orders_deleteButton_1,self.orders_cancelButton_1)
        MainWindow.setTabOrder(self.orders_cancelButton_1,self.orders_treeWidget_2)
        MainWindow.setTabOrder(self.orders_treeWidget_2,self.orders_itemLineEdit)
        MainWindow.setTabOrder(self.orders_itemLineEdit,self.orders_spinBox_3)
        MainWindow.setTabOrder(self.orders_spinBox_3,self.orders_addButton_2)
        MainWindow.setTabOrder(self.orders_addButton_2,self.orders_updateButton_2)
        MainWindow.setTabOrder(self.orders_updateButton_2,self.orders_deleteButton_2)
        MainWindow.setTabOrder(self.orders_deleteButton_2,self.members_treeWidget)
        MainWindow.setTabOrder(self.members_treeWidget,self.members_clearButton)
        MainWindow.setTabOrder(self.members_clearButton,self.members_filter)
        MainWindow.setTabOrder(self.members_filter,self.members_username)
        MainWindow.setTabOrder(self.members_username,self.members_password)
        MainWindow.setTabOrder(self.members_password,self.members_realName)
        MainWindow.setTabOrder(self.members_realName,self.members_debt)
        MainWindow.setTabOrder(self.members_debt,self.members_payingType)
        MainWindow.setTabOrder(self.members_payingType,self.members_dateEdit)
        MainWindow.setTabOrder(self.members_dateEdit,self.members_dateEdit_2)
        MainWindow.setTabOrder(self.members_dateEdit_2,self.members_addButton)
        MainWindow.setTabOrder(self.members_addButton,self.members_updateButton)
        MainWindow.setTabOrder(self.members_updateButton,self.members_deleteButton)
        MainWindow.setTabOrder(self.members_deleteButton,self.members_reportsButton)
        MainWindow.setTabOrder(self.members_reportsButton,self.logs_dateTimeEdit_1)
        MainWindow.setTabOrder(self.logs_dateTimeEdit_1,self.logs_searchButton)
        MainWindow.setTabOrder(self.logs_searchButton,self.logs_dateTimeEdit_2)
        MainWindow.setTabOrder(self.logs_dateTimeEdit_2,self.logs_treeWidget)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("PyKafe")
        self.main_startTimeButton.setStatusTip(_("Starts selected computer for usage (timed)"))
        self.main_startTimeButton.setText(_("Timed"))
        self.main_stopButton.setStatusTip(_("Switches to login state"))
        self.main_stopButton.setText(_("Stop"))
        self.main_startButton.setStatusTip(_("Starts selected computer for usage"))
        self.main_startButton.setText(_("Start"))
        self.main_settingsButton.setStatusTip(_("Opens settings for this computer"))
        self.main_settingsButton.setText(_("Settings"))
        self.main_remoteButton.setStatusTip(_("Opens remote desktop connection"))
        self.main_remoteButton.setText(_("Remote"))
        self.main_changeButton.setStatusTip(_("Moves user to another computer"))
        self.main_changeButton.setText(_("Change"))
        self.main_shutDownButton.setStatusTip(_("Shuts down selected computer"))
        self.main_shutDownButton.setText(_("Shutdown"))
        self.main_treeWidget.headerItem().setText(0,_("ID"))
        self.main_treeWidget.headerItem().setText(1,_("Status"))
        self.main_treeWidget.headerItem().setText(2,_("User"))
        self.main_treeWidget.headerItem().setText(3,_("Money"))
        self.main_treeWidget.headerItem().setText(4,_("Usage Time"))
        self.main_treeWidget.headerItem().setText(5,_("End Time"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _("Main"))
        self.groupBox_2.setTitle(_("Orders"))
        self.label_8.setText(_("Item"))
        self.label_7.setText(_("Computer ID"))
        self.label_9.setText(_("Quantity"))
        self.orders_treeWidget_1.headerItem().setText(0,_("ID"))
        self.orders_treeWidget_1.headerItem().setText(1,_("Item"))
        self.orders_treeWidget_1.headerItem().setText(2,_("Cost"))
        self.orders_treeWidget_1.headerItem().setText(3,_("Quantity"))
        self.orders_cancelButton_1.setText(_("Cancel"))
        self.orders_deleteButton_1.setText(_("Delete"))
        self.orders_updateButton_1.setText(_("Update"))
        self.orders_addButton_1.setText(_("Add"))
        self.groupBox_3.setTitle(_("Cafeteria Stocks"))
        self.orders_treeWidget_2.headerItem().setText(0,_("Item"))
        self.orders_treeWidget_2.headerItem().setText(1,_("Cost"))
        self.orders_treeWidget_2.headerItem().setText(2,_("Quantity"))
        self.label_6.setText(_("Quantity"))
        self.label_5.setText(_("Price"))
        self.label_4.setText(_("Item"))
        self.orders_addButton_2.setText(_("Add"))
        self.orders_updateButton_2.setText(_("Update"))
        self.orders_deleteButton_2.setText(_("Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _("Orders"))
        self.members_treeWidget.headerItem().setText(0,_("Member List"))
        self.members_clearButton.setToolTip(_("Clear"))
        self.members_clearButton.setStatusTip(_("Clears filter"))
        self.label.setText(_("Find:"))
        self.members_filter.setStatusTip(_("Type some letters to filter"))
        self.groupBox.setTitle(_("Member Information"))
        self.members_addButton.setText(_("Add"))
        self.members_updateButton.setText(_("Update"))
        self.members_deleteButton.setText(_("Delete"))
        self.members_reportsButton.setText(_("Reports"))
        self.textLabel5.setText(_("Paying Type:"))
        self.textLabel2_2.setText(_("Password:"))
        self.members_payingType.addItem(_("Pre Paid"))
        self.members_payingType.addItem(_("Normal"))
        self.textLabel1_3.setText(_("Username:"))
        self.textLabel4_2.setText(_("Credit:"))
        self.textLabel3_2.setText(_("Real Name:"))
        self.textLabel7.setText(_("Subscribing period:"))
        self.label_2.setText(_("Starts"))
        self.label_3.setText(_("Ends"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _("Members"))
        self.logs_treeWidget.headerItem().setText(0,_("Date"))
        self.logs_treeWidget.headerItem().setText(1,_("Type"))
        self.logs_treeWidget.headerItem().setText(2,_("Description"))
        self.logs_treeWidget.headerItem().setText(3,_("Cashier"))
        self.logs_treeWidget.headerItem().setText(4,_("Computer"))
        self.logs_treeWidget.headerItem().setText(5,_("Member"))
        self.logs_treeWidget.headerItem().setText(6,_("Income"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _("Logs"))
        self.menuHelp.setTitle(_("Help"))
        self.menuFile.setTitle(_("File"))
        self.menuNew.setTitle(_("New"))
        self.menuTools.setTitle(_("Tools"))
        self.actionContents.setText(_("Contents"))
        self.actionAbout_pyKafe.setText(_("About pyKafe"))
        self.actionAbout_Qt.setText(_("About Qt"))
        self.actionComputer.setText(_("Computer"))
        self.actionEntertainment.setText(_("Entertainment"))
        self.actionExit.setText(_("Exit"))
        self.actionSettings.setText(_("Settings..."))
