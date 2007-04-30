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

import sys, server
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,668,505).size()).expandedTo(MainWindow.minimumSizeHint()))

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

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem2,2,0,1,1)

        self.orders_addButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_addButton_1.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.orders_addButton_1.setObjectName("orders_addButton_1")
        self.gridlayout3.addWidget(self.orders_addButton_1,2,1,1,1)

        self.orders_updateButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_updateButton_1.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.orders_updateButton_1.setObjectName("orders_updateButton_1")
        self.gridlayout3.addWidget(self.orders_updateButton_1,2,2,1,1)

        self.orders_deleteButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_deleteButton_1.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.orders_deleteButton_1.setObjectName("orders_deleteButton_1")
        self.gridlayout3.addWidget(self.orders_deleteButton_1,2,3,1,1)

        self.orders_cancelButton_1 = QtGui.QPushButton(self.groupBox_2)
        self.orders_cancelButton_1.setIcon(QtGui.QIcon("../../data/icons/button_cancel.png"))
        self.orders_cancelButton_1.setObjectName("orders_cancelButton_1")
        self.gridlayout3.addWidget(self.orders_cancelButton_1,2,4,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.orders_idComboBox = QtGui.QComboBox(self.groupBox_2)
        self.orders_idComboBox.setObjectName("orders_idComboBox")
        self.hboxlayout.addWidget(self.orders_idComboBox)

        self.orders_itemComboBox = QtGui.QComboBox(self.groupBox_2)
        self.orders_itemComboBox.setObjectName("orders_itemComboBox")
        self.hboxlayout.addWidget(self.orders_itemComboBox)

        self.orders_spinBox1 = QtGui.QSpinBox(self.groupBox_2)
        self.orders_spinBox1.setObjectName("orders_spinBox1")
        self.hboxlayout.addWidget(self.orders_spinBox1)
        self.gridlayout3.addLayout(self.hboxlayout,1,0,1,5)

        self.oders_treeWidget_1 = QtGui.QTreeWidget(self.groupBox_2)
        self.oders_treeWidget_1.setSortingEnabled(True)
        self.oders_treeWidget_1.setObjectName("oders_treeWidget_1")
        self.gridlayout3.addWidget(self.oders_treeWidget_1,0,0,1,5)

        self.groupBox_3 = QtGui.QGroupBox(self.splitter)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout4 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem3,2,0,1,1)

        self.orders_addButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.orders_addButton_2.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.orders_addButton_2.setObjectName("orders_addButton_2")
        self.gridlayout4.addWidget(self.orders_addButton_2,2,1,1,1)

        self.orders_updateButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.orders_updateButton_2.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.orders_updateButton_2.setObjectName("orders_updateButton_2")
        self.gridlayout4.addWidget(self.orders_updateButton_2,2,2,1,1)

        self.orders_deleteButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.orders_deleteButton_2.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.orders_deleteButton_2.setObjectName("orders_deleteButton_2")
        self.gridlayout4.addWidget(self.orders_deleteButton_2,2,3,1,1)

        self.orders_treeWidget_2 = QtGui.QTreeWidget(self.groupBox_3)
        self.orders_treeWidget_2.setSortingEnabled(True)
        self.orders_treeWidget_2.setObjectName("orders_treeWidget_2")
        self.gridlayout4.addWidget(self.orders_treeWidget_2,0,0,1,4)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.orders_itemLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.orders_itemLineEdit.setObjectName("orders_itemLineEdit")
        self.hboxlayout1.addWidget(self.orders_itemLineEdit)

        self.orders_spinBox_2 = QtGui.QSpinBox(self.groupBox_3)
        self.orders_spinBox_2.setObjectName("orders_spinBox_2")
        self.hboxlayout1.addWidget(self.orders_spinBox_2)

        self.orders_spinBox_3 = QtGui.QSpinBox(self.groupBox_3)
        self.orders_spinBox_3.setObjectName("orders_spinBox_3")
        self.hboxlayout1.addWidget(self.orders_spinBox_3)
        self.gridlayout4.addLayout(self.hboxlayout1,1,0,1,4)
        self.gridlayout2.addWidget(self.splitter,0,0,1,1)
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

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
        self.members_treeWidget.setSortingEnabled(True)
        self.members_treeWidget.setObjectName("members_treeWidget")
        self.vboxlayout.addWidget(self.members_treeWidget)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.pushButton_7 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_7.setIcon(QtGui.QIcon("../../data/icons/fileclose.png"))
        self.pushButton_7.setFlat(True)
        self.pushButton_7.setObjectName("pushButton_7")
        self.hboxlayout2.addWidget(self.pushButton_7)

        self.lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.hboxlayout2.addWidget(self.lineEdit)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.groupBox = QtGui.QGroupBox(self.splitter_2)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout6 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        spacerItem4 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout6.addItem(spacerItem4,2,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        spacerItem5 = QtGui.QSpacerItem(80,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem5)

        self.user_addButton = QtGui.QPushButton(self.groupBox)
        self.user_addButton.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.user_addButton.setObjectName("user_addButton")
        self.hboxlayout3.addWidget(self.user_addButton)

        self.user_updateButton = QtGui.QPushButton(self.groupBox)
        self.user_updateButton.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.user_updateButton.setObjectName("user_updateButton")
        self.hboxlayout3.addWidget(self.user_updateButton)

        self.user_deleteButton = QtGui.QPushButton(self.groupBox)
        self.user_deleteButton.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.user_deleteButton.setObjectName("user_deleteButton")
        self.hboxlayout3.addWidget(self.user_deleteButton)
        self.gridlayout6.addLayout(self.hboxlayout3,3,0,1,1)

        self.gridlayout7 = QtGui.QGridLayout()
        self.gridlayout7.setMargin(0)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.textLabel5 = QtGui.QLabel(self.groupBox)
        self.textLabel5.setWordWrap(False)
        self.textLabel5.setObjectName("textLabel5")
        self.gridlayout7.addWidget(self.textLabel5,4,0,1,1)

        self.textLabel2_2 = QtGui.QLabel(self.groupBox)
        self.textLabel2_2.setWordWrap(False)
        self.textLabel2_2.setObjectName("textLabel2_2")
        self.gridlayout7.addWidget(self.textLabel2_2,1,0,1,1)

        self.user_payingType = QtGui.QComboBox(self.groupBox)
        self.user_payingType.setObjectName("user_payingType")
        self.gridlayout7.addWidget(self.user_payingType,4,1,1,1)

        self.user_debt = QtGui.QLineEdit(self.groupBox)
        self.user_debt.setObjectName("user_debt")
        self.gridlayout7.addWidget(self.user_debt,3,1,1,1)

        self.user_realName = QtGui.QLineEdit(self.groupBox)
        self.user_realName.setObjectName("user_realName")
        self.gridlayout7.addWidget(self.user_realName,2,1,1,1)

        self.textLabel1_3 = QtGui.QLabel(self.groupBox)
        self.textLabel1_3.setWordWrap(False)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.gridlayout7.addWidget(self.textLabel1_3,0,0,1,1)

        self.user_password = QtGui.QLineEdit(self.groupBox)
        self.user_password.setEchoMode(QtGui.QLineEdit.Password)
        self.user_password.setObjectName("user_password")
        self.gridlayout7.addWidget(self.user_password,1,1,1,1)

        self.textLabel4_2 = QtGui.QLabel(self.groupBox)
        self.textLabel4_2.setWordWrap(False)
        self.textLabel4_2.setObjectName("textLabel4_2")
        self.gridlayout7.addWidget(self.textLabel4_2,3,0,1,1)

        self.textLabel3_2 = QtGui.QLabel(self.groupBox)
        self.textLabel3_2.setWordWrap(False)
        self.textLabel3_2.setObjectName("textLabel3_2")
        self.gridlayout7.addWidget(self.textLabel3_2,2,0,1,1)

        self.user_username = QtGui.QLineEdit(self.groupBox)
        self.user_username.setObjectName("user_username")
        self.gridlayout7.addWidget(self.user_username,0,1,1,1)
        self.gridlayout6.addLayout(self.gridlayout7,0,0,1,1)

        self.gridlayout8 = QtGui.QGridLayout()
        self.gridlayout8.setMargin(0)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        self.members_dateEdit_2 = QtGui.QDateEdit(self.groupBox)
        self.members_dateEdit_2.setObjectName("members_dateEdit_2")
        self.gridlayout8.addWidget(self.members_dateEdit_2,1,1,1,1)

        self.textLabel7 = QtGui.QLabel(self.groupBox)
        self.textLabel7.setWordWrap(False)
        self.textLabel7.setObjectName("textLabel7")
        self.gridlayout8.addWidget(self.textLabel7,0,0,1,2)

        self.members_dateEdit = QtGui.QDateEdit(self.groupBox)
        self.members_dateEdit.setObjectName("members_dateEdit")
        self.gridlayout8.addWidget(self.members_dateEdit,1,0,1,1)
        self.gridlayout6.addLayout(self.gridlayout8,1,0,1,1)
        self.gridlayout5.addWidget(self.splitter_2,0,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout9 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout9.setMargin(9)
        self.gridlayout9.setSpacing(6)
        self.gridlayout9.setObjectName("gridlayout9")

        spacerItem6 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout9.addItem(spacerItem6,0,2,1,1)

        spacerItem7 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout9.addItem(spacerItem7,0,0,1,1)

        self.gridlayout10 = QtGui.QGridLayout()
        self.gridlayout10.setMargin(0)
        self.gridlayout10.setSpacing(6)
        self.gridlayout10.setObjectName("gridlayout10")

        self.logs_dateTimeEdit_1 = QtGui.QDateTimeEdit(self.tab_3)
        self.logs_dateTimeEdit_1.setObjectName("logs_dateTimeEdit_1")
        self.gridlayout10.addWidget(self.logs_dateTimeEdit_1,0,0,1,1)

        self.logs_searchButton = QtGui.QPushButton(self.tab_3)
        self.logs_searchButton.setIcon(QtGui.QIcon("../../data/icons/find.png"))
        self.logs_searchButton.setIconSize(QtCore.QSize(64,64))
        self.logs_searchButton.setObjectName("logs_searchButton")
        self.gridlayout10.addWidget(self.logs_searchButton,0,1,2,1)

        self.logs_dateTimeEdit_2 = QtGui.QDateTimeEdit(self.tab_3)
        self.logs_dateTimeEdit_2.setObjectName("logs_dateTimeEdit_2")
        self.gridlayout10.addWidget(self.logs_dateTimeEdit_2,1,0,1,1)
        self.gridlayout9.addLayout(self.gridlayout10,0,1,1,1)

        self.logs_treeWidget = QtGui.QTreeWidget(self.tab_3)
        self.logs_treeWidget.setObjectName("logs_treeWidget")
        self.gridlayout9.addWidget(self.logs_treeWidget,1,0,1,3)
        self.tabWidget.addTab(self.tab_3,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,668,29))
        self.menubar.setObjectName("menubar")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuNew = QtGui.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")
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

        self.actionOptions = QtGui.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.menuHelp.addAction(self.actionContents)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_pyKafe)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuTools.addAction(self.actionOptions)
        self.menuNew.addAction(self.actionComputer)
        self.menuNew.addAction(self.actionEntertainment)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.server = server.PykafeServer(MainWindow)
        QtCore.QObject.connect(self.main_startButton,QtCore.SIGNAL("clicked()"),self.server.startClient)
        QtCore.QObject.connect(self.main_stopButton,QtCore.SIGNAL("clicked()"),self.server.stopClient)
        QtCore.QObject.connect(self.actionExit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QObject.connect(self.main_startTimeButton,QtCore.SIGNAL("clicked()"),self.server.startTimed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.main_startTimeButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Starts selected computer for usage (timed)", None, QtGui.QApplication.UnicodeUTF8))
        self.main_startTimeButton.setText(QtGui.QApplication.translate("MainWindow", "Timed", None, QtGui.QApplication.UnicodeUTF8))
        self.main_stopButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Switches to login state", None, QtGui.QApplication.UnicodeUTF8))
        self.main_stopButton.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.main_startButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Starts selected computer for usage", None, QtGui.QApplication.UnicodeUTF8))
        self.main_startButton.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.main_settingsButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Opens settings for this computer", None, QtGui.QApplication.UnicodeUTF8))
        self.main_settingsButton.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.main_remoteButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Opens remote desktop connection", None, QtGui.QApplication.UnicodeUTF8))
        self.main_remoteButton.setText(QtGui.QApplication.translate("MainWindow", "Remote", None, QtGui.QApplication.UnicodeUTF8))
        self.main_changeButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Moves user to another computer", None, QtGui.QApplication.UnicodeUTF8))
        self.main_changeButton.setText(QtGui.QApplication.translate("MainWindow", "Change", None, QtGui.QApplication.UnicodeUTF8))
        self.main_shutDownButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Shuts down selected computer", None, QtGui.QApplication.UnicodeUTF8))
        self.main_shutDownButton.setText(QtGui.QApplication.translate("MainWindow", "Shutdown", None, QtGui.QApplication.UnicodeUTF8))
        self.main_treeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.main_treeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.main_treeWidget.headerItem().setText(2,QtGui.QApplication.translate("MainWindow", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.main_treeWidget.headerItem().setText(3,QtGui.QApplication.translate("MainWindow", "Money", None, QtGui.QApplication.UnicodeUTF8))
        self.main_treeWidget.headerItem().setText(4,QtGui.QApplication.translate("MainWindow", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.main_treeWidget.headerItem().setText(5,QtGui.QApplication.translate("MainWindow", "End Time", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Main", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Orders", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_addButton_1.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_updateButton_1.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_deleteButton_1.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_cancelButton_1.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.oders_treeWidget_1.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.oders_treeWidget_1.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Item", None, QtGui.QApplication.UnicodeUTF8))
        self.oders_treeWidget_1.headerItem().setText(2,QtGui.QApplication.translate("MainWindow", "Cost", None, QtGui.QApplication.UnicodeUTF8))
        self.oders_treeWidget_1.headerItem().setText(3,QtGui.QApplication.translate("MainWindow", "Quantity", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Cafeteria", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_addButton_2.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_updateButton_2.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_deleteButton_2.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_treeWidget_2.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Item", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_treeWidget_2.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Cost", None, QtGui.QApplication.UnicodeUTF8))
        self.orders_treeWidget_2.headerItem().setText(2,QtGui.QApplication.translate("MainWindow", "Quantity", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Orders", None, QtGui.QApplication.UnicodeUTF8))
        self.members_treeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Member List", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setStatusTip(QtGui.QApplication.translate("MainWindow", "Clears filter", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Type some letters to filter", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Member Information", None, QtGui.QApplication.UnicodeUTF8))
        self.user_addButton.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.user_updateButton.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.user_deleteButton.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel5.setText(QtGui.QApplication.translate("MainWindow", "Paying Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2_2.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3.setText(QtGui.QApplication.translate("MainWindow", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel4_2.setText(QtGui.QApplication.translate("MainWindow", "Debt:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3_2.setText(QtGui.QApplication.translate("MainWindow", "Real Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel7.setText(QtGui.QApplication.translate("MainWindow", "Subscribing period", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Members", None, QtGui.QApplication.UnicodeUTF8))
        self.logs_treeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.logs_treeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.logs_treeWidget.headerItem().setText(2,QtGui.QApplication.translate("MainWindow", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.logs_treeWidget.headerItem().setText(3,QtGui.QApplication.translate("MainWindow", "Cashier", None, QtGui.QApplication.UnicodeUTF8))
        self.logs_treeWidget.headerItem().setText(4,QtGui.QApplication.translate("MainWindow", "Computer", None, QtGui.QApplication.UnicodeUTF8))
        self.logs_treeWidget.headerItem().setText(5,QtGui.QApplication.translate("MainWindow", "Member", None, QtGui.QApplication.UnicodeUTF8))
        self.logs_treeWidget.headerItem().setText(6,QtGui.QApplication.translate("MainWindow", "Income", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Logs", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuNew.setTitle(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionContents.setText(QtGui.QApplication.translate("MainWindow", "Contents", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_pyKafe.setText(QtGui.QApplication.translate("MainWindow", "About pyKafe", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Qt.setText(QtGui.QApplication.translate("MainWindow", "About Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComputer.setText(QtGui.QApplication.translate("MainWindow", "Computer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEntertainment.setText(QtGui.QApplication.translate("MainWindow", "Entertainment", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOptions.setText(QtGui.QApplication.translate("MainWindow", "Options...", None, QtGui.QApplication.UnicodeUTF8))

