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
    def setupUi(self, MainWindow):
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

        self.members_addButton = QtGui.QPushButton(self.groupBox)
        self.members_addButton.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.members_addButton.setObjectName("members_addButton")
        self.hboxlayout3.addWidget(self.members_addButton)

        self.members_updateButton = QtGui.QPushButton(self.groupBox)
        self.members_updateButton.setIcon(QtGui.QIcon("../../data/icons/reload.png"))
        self.members_updateButton.setObjectName("members_updateButton")
        self.hboxlayout3.addWidget(self.members_updateButton)

        self.members_deleteButton = QtGui.QPushButton(self.groupBox)
        self.members_deleteButton.setIcon(QtGui.QIcon("../../data/icons/edit_remove.png"))
        self.members_deleteButton.setObjectName("members_deleteButton")
        self.hboxlayout3.addWidget(self.members_deleteButton)

        self.members_reportsButton = QtGui.QPushButton(self.groupBox)
        self.members_reportsButton.setIcon(QtGui.QIcon("../../data/icons/find.png"))
        self.members_reportsButton.setObjectName("members_reportsButton")
        self.hboxlayout3.addWidget(self.members_reportsButton)
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

        self.members_payingType = QtGui.QComboBox(self.groupBox)
        self.members_payingType.setObjectName("members_payingType")
        self.gridlayout7.addWidget(self.members_payingType,4,1,1,1)

        self.members_realName = QtGui.QLineEdit(self.groupBox)
        self.members_realName.setObjectName("members_realName")
        self.gridlayout7.addWidget(self.members_realName,2,1,1,1)

        self.textLabel1_3 = QtGui.QLabel(self.groupBox)
        self.textLabel1_3.setWordWrap(False)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.gridlayout7.addWidget(self.textLabel1_3,0,0,1,1)

        self.members_password = QtGui.QLineEdit(self.groupBox)
        self.members_password.setEchoMode(QtGui.QLineEdit.Password)
        self.members_password.setObjectName("members_password")
        self.gridlayout7.addWidget(self.members_password,1,1,1,1)

        self.textLabel4_2 = QtGui.QLabel(self.groupBox)
        self.textLabel4_2.setWordWrap(False)
        self.textLabel4_2.setObjectName("textLabel4_2")
        self.gridlayout7.addWidget(self.textLabel4_2,3,0,1,1)

        self.textLabel3_2 = QtGui.QLabel(self.groupBox)
        self.textLabel3_2.setWordWrap(False)
        self.textLabel3_2.setObjectName("textLabel3_2")
        self.gridlayout7.addWidget(self.textLabel3_2,2,0,1,1)

        self.members_username = QtGui.QLineEdit(self.groupBox)
        self.members_username.setObjectName("members_username")
        self.gridlayout7.addWidget(self.members_username,0,1,1,1)

        self.members_debt = QtGui.QSpinBox(self.groupBox)
        self.members_debt.setObjectName("members_debt")
        self.gridlayout7.addWidget(self.members_debt,3,1,1,1)
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
        self.menubar.setGeometry(QtCore.QRect(0,0,650,29))
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
        self.server = server.PykafeServer(MainWindow, self)
        QtCore.QObject.connect(self.main_startButton,QtCore.SIGNAL("clicked()"),self.server.startClient)
        QtCore.QObject.connect(self.main_stopButton,QtCore.SIGNAL("clicked()"),self.server.stopClient)
        QtCore.QObject.connect(self.actionExit,QtCore.SIGNAL("activated()"),MainWindow.close)
        QtCore.QObject.connect(self.main_startTimeButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_addButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_updateButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_deleteButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_cancelButton_1,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_addButton_2,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_updateButton_2,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.orders_deleteButton_2,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.members_addButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.members_updateButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.members_deleteButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.members_reportsButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.main_changeButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.main_remoteButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.main_settingsButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QObject.connect(self.main_shutDownButton,QtCore.SIGNAL("clicked()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_("PyKafe"))
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
        self.main_treeWidget.headerItem().setText(4,_("Time"))
        self.main_treeWidget.headerItem().setText(5,_("End Time"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _("Main"))
        self.groupBox_2.setTitle(_("Orders"))
        self.orders_addButton_1.setText(_("Add"))
        self.orders_updateButton_1.setText(_("Update"))
        self.orders_deleteButton_1.setText(_("Delete"))
        self.orders_cancelButton_1.setText(_("Cancel"))
        self.oders_treeWidget_1.headerItem().setText(0,_("ID"))
        self.oders_treeWidget_1.headerItem().setText(1,_("Item"))
        self.oders_treeWidget_1.headerItem().setText(2,_("Cost"))
        self.oders_treeWidget_1.headerItem().setText(3,_("Quantity"))
        self.groupBox_3.setTitle(_("Cafeteria Products"))
        self.orders_addButton_2.setText(_("Add"))
        self.orders_updateButton_2.setText(_("Update"))
        self.orders_deleteButton_2.setText(_("Delete"))
        self.orders_treeWidget_2.headerItem().setText(0,_("Item"))
        self.orders_treeWidget_2.headerItem().setText(1,_("Cost"))
        self.orders_treeWidget_2.headerItem().setText(2,_("Quantity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _("Orders"))
        self.members_treeWidget.headerItem().setText(0,_("Member List"))
        self.pushButton_7.setToolTip(_("Clear"))
        self.pushButton_7.setStatusTip(_("Clears filter"))
        self.lineEdit.setStatusTip(_("Type some letters to filter"))
        self.groupBox.setTitle(_("Member Information"))
        self.members_addButton.setText(_("Add"))
        self.members_updateButton.setText(_("Update"))
        self.members_deleteButton.setText(_("Delete"))
        self.members_reportsButton.setText(_("Reports"))
        self.textLabel5.setText(_("Paying Type:"))
        self.textLabel2_2.setText(_("Password:"))
        self.textLabel1_3.setText(_("Username:"))
        self.textLabel4_2.setText(_("Debt:"))
        self.textLabel3_2.setText(_("Real Name:"))
        self.textLabel7.setText(_("Subscribing period"))
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
        self.menuTools.setTitle(_("Tools"))
        self.menuFile.setTitle(_("File"))
        self.menuNew.setTitle(_("New"))
        self.actionContents.setText(_("Contents"))
        self.actionAbout_pyKafe.setText(_("About pyKafe"))
        self.actionAbout_Qt.setText(_("About Qt"))
        self.actionComputer.setText(_("Computer"))
        self.actionEntertainment.setText(_("Entertainment"))
        self.actionExit.setText(_("Exit"))
        self.actionOptions.setText(_("Options..."))

