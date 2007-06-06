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
from database import Database

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class Handler:
    def __init__(self, ui, cashier):
        self.ui = ui
        self.cashierName = cashier
    def search(self):
        startDate = self.ui.dateTimeEdit.dateTime().toTime_t()
        endDate = self.ui.dateTimeEdit_2.dateTime().toTime_t()
        income = Database().runOnce("select sum(income) from safe where cashier=? and date between ? and ?", (self.cashierName, startDate, endDate))[0][0]
        self.ui.doubleSpinBox.setValue(income)
        added = Database().runOnce("select count() from logs where log_value=? and cashier=? and date between ? and ?", (_("Added member"), self.cashierName, startDate, endDate))[0][0]
        deleted = Database().runOnce("select count() from logs where log_value=? and cashier=? and date between ? and ?", (_("Deleted member"), self.cashierName, startDate, endDate))[0][0]
        self.ui.spinBox.setValue(added)
        self.ui.spinBox_2.setValue(deleted)

class Ui_CashierReports(object):
    def setupUi(self, CashierReports, cashier):
        CashierReports.setObjectName("CashierReports")
        CashierReports.resize(QtCore.QSize(QtCore.QRect(0,0,266,239).size()).expandedTo(CashierReports.minimumSizeHint()))
        CashierReports.setWindowIcon(QtGui.QIcon("../../data/icons/pyKafe.png"))

        self.gridlayout = QtGui.QGridLayout(CashierReports)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.doubleSpinBox = QtGui.QDoubleSpinBox(CashierReports)
        self.doubleSpinBox.setEnabled(False)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridlayout.addWidget(self.doubleSpinBox,1,1,1,2)

        self.label = QtGui.QLabel(CashierReports)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.dateTimeEdit_2 = QtGui.QDateTimeEdit(CashierReports)
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.gridlayout1.addWidget(self.dateTimeEdit_2,1,0,1,1)

        self.toolButton = QtGui.QToolButton(CashierReports)
        self.toolButton.setIcon(QtGui.QIcon("../../data/icons/find.png"))
        self.toolButton.setIconSize(QtCore.QSize(64,64))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton.setObjectName("toolButton")
        self.gridlayout1.addWidget(self.toolButton,0,1,2,1)

        self.dateTimeEdit = QtGui.QDateTimeEdit(CashierReports)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.gridlayout1.addWidget(self.dateTimeEdit,0,0,1,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,3)

        self.spinBox = QtGui.QSpinBox(CashierReports)
        self.spinBox.setEnabled(False)
        self.spinBox.setObjectName("spinBox")
        self.gridlayout.addWidget(self.spinBox,2,2,1,1)

        self.spinBox_2 = QtGui.QSpinBox(CashierReports)
        self.spinBox_2.setEnabled(False)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridlayout.addWidget(self.spinBox_2,3,2,1,1)

        self.label_3 = QtGui.QLabel(CashierReports)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,3,0,1,2)

        self.label_2 = QtGui.QLabel(CashierReports)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(CashierReports)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,4,0,1,3)

        self.retranslateUi(CashierReports)
        self.handler = Handler(self, cashier)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),CashierReports.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),CashierReports.reject)
        QtCore.QObject.connect(self.toolButton,QtCore.SIGNAL("clicked()"),self.handler.search)
        QtCore.QMetaObject.connectSlotsByName(CashierReports)

    def retranslateUi(self, CashierReports):
        CashierReports.setWindowTitle(QtGui.QApplication.translate("CashierReports", "Cashier Reports", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CashierReports", "Income:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("CashierReports", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CashierReports", "Members deleted:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CashierReports", "Members added:", None, QtGui.QApplication.UnicodeUTF8))

