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
from currencyformat import currency

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class Handler:
    def __init__(self, ui, member):
        self.ui = ui
        self.memberName = member
        self.ui.start.setDateTime(QtCore.QDateTime.currentDateTime().addDays(-7))
        self.ui.end.setDateTime(QtCore.QDateTime.currentDateTime().addDays(1))
        self.search()
    def search(self):
        self.ui.paymentTree.clear()
        self.payments = []
        startDate = self.ui.start.dateTime().toTime_t()
        endDate = self.ui.end.dateTime().toTime_t()
        results = Database().runOnce("select date, log_value, income from logs where member=? and date between ? and ?", (self.memberName, startDate, endDate))
        received, sent, total = 0, 0, 0.0
        for result in results:
            date = QtCore.QDateTime.fromTime_t(result[0])
            income = str(result[2])
            if _("Money paid") in result[1]:
                self.payments.append(QtGui.QTreeWidgetItem(self.ui.paymentTree, [date.toString("dd.MM.yyyy hh.mm"), _("Normal"), currency(float(income))]))
            if _("cafeteria item sold") in result[1]:
                self.payments.append(QtGui.QTreeWidgetItem(self.ui.paymentTree, [date.toString("dd.MM.yyyy hh.mm"), _("Cafeteria"), currency(float(income))]))
            if _("received, sent:") in result[1]:
                received += int(result[1][len(_("received, sent:")):result[1].rfind("|")])
                sent += int(result[1].split("|")[1])
        for payment in self.payments:
            current = payment.text(2).split(" ")[0]
            total += float(current.replace(',', '.'))
        self.ui.totalLabel.setText(currency(total))
        self.ui.bytesLabel.setText("%s / %s" % (str(received), str(sent)))

class Ui_MemberReports(object):
    def setupUi(self, MemberReports, member):
        MemberReports.setObjectName("MemberReports")
        MemberReports.resize(QtCore.QSize(QtCore.QRect(0,0,453,408).size()).expandedTo(MemberReports.minimumSizeHint()))
        MemberReports.setWindowIcon(QtGui.QIcon("../../data/icons/pyKafe.png"))

        self.gridlayout = QtGui.QGridLayout(MemberReports)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.end = QtGui.QDateTimeEdit(MemberReports)
        self.end.setObjectName("end")
        self.gridlayout1.addWidget(self.end,1,0,1,1)

        self.findButton = QtGui.QToolButton(MemberReports)
        self.findButton.setIcon(QtGui.QIcon("../../data/icons/find.png"))
        self.findButton.setIconSize(QtCore.QSize(64,64))
        self.findButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.findButton.setObjectName("findButton")
        self.gridlayout1.addWidget(self.findButton,0,1,2,1)

        self.start = QtGui.QDateTimeEdit(MemberReports)
        self.start.setObjectName("start")
        self.gridlayout1.addWidget(self.start,0,0,1,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,2)

        self.buttonBox = QtGui.QDialogButtonBox(MemberReports)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,4,0,1,2)

        self.label_3 = QtGui.QLabel(MemberReports)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,3,0,1,1)

        self.bytesLabel = QtGui.QLabel(MemberReports)
        self.bytesLabel.setObjectName("bytesLabel")
        self.gridlayout.addWidget(self.bytesLabel,3,1,1,1)

        self.paymentTree = QtGui.QTreeWidget(MemberReports)
        self.paymentTree.setObjectName("paymentTree")
        self.gridlayout.addWidget(self.paymentTree,1,0,1,2)

        self.label_2 = QtGui.QLabel(MemberReports)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,1)

        self.totalLabel = QtGui.QLabel(MemberReports)
        self.totalLabel.setObjectName("totalLabel")
        self.gridlayout.addWidget(self.totalLabel,2,1,1,1)

        self.retranslateUi(MemberReports)
        self.handler = Handler(self, member)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),MemberReports.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),MemberReports.reject)
        QtCore.QObject.connect(self.findButton,QtCore.SIGNAL("clicked()"),self.handler.search)
        QtCore.QMetaObject.connectSlotsByName(MemberReports)

    def retranslateUi(self, MemberReports):
        MemberReports.setWindowTitle(QtGui.QApplication.translate("MemberReports", "Member Reports", None, QtGui.QApplication.UnicodeUTF8))
        self.findButton.setText(QtGui.QApplication.translate("MemberReports", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MemberReports", "Received/Sent data in KB:", None, QtGui.QApplication.UnicodeUTF8))
        self.paymentTree.headerItem().setText(0,QtGui.QApplication.translate("MemberReports", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.paymentTree.headerItem().setText(1,QtGui.QApplication.translate("MemberReports", "Payment", None, QtGui.QApplication.UnicodeUTF8))
        self.paymentTree.headerItem().setText(2,QtGui.QApplication.translate("MemberReports", "Cost", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MemberReports", "Total:", None, QtGui.QApplication.UnicodeUTF8))

