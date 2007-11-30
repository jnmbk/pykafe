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

class Ui_PaymentDialog(object):
    def setupUi(self, PaymentDialog):
        PaymentDialog.setObjectName("PaymentDialog")
        PaymentDialog.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(PaymentDialog.minimumSizeHint()))
        PaymentDialog.setWindowIcon(QtGui.QIcon("../../data/icons/pyKafe.png"))

        self.gridlayout = QtGui.QGridLayout(PaymentDialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(PaymentDialog)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.cafeteriaWidget = QtGui.QTreeWidget(self.groupBox)
        self.cafeteriaWidget.setRootIsDecorated(False)
        self.cafeteriaWidget.setAllColumnsShowFocus(True)
        self.cafeteriaWidget.setObjectName("cafeteriaWidget")
        self.gridlayout1.addWidget(self.cafeteriaWidget,0,0,1,1)
        self.gridlayout.addWidget(self.groupBox,2,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_2 = QtGui.QLabel(PaymentDialog)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)

        self.totalCost = QtGui.QDoubleSpinBox(PaymentDialog)
        self.totalCost.setReadOnly(True)
        self.totalCost.setMaximum(1000000000.0)
        self.totalCost.setObjectName("totalCost")
        self.hboxlayout.addWidget(self.totalCost)
        self.gridlayout.addLayout(self.hboxlayout,3,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(PaymentDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,5,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(PaymentDialog)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.usedTime = QtGui.QTimeEdit(PaymentDialog)
        self.usedTime.setReadOnly(True)
        self.usedTime.setObjectName("usedTime")
        self.hboxlayout1.addWidget(self.usedTime)
        self.gridlayout.addLayout(self.hboxlayout1,1,0,1,1)

        self.label_3 = QtGui.QLabel(PaymentDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,0,0,1,1)

        self.retranslateUi(PaymentDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),PaymentDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(PaymentDialog)

    def retranslateUi(self, PaymentDialog):
        PaymentDialog.setWindowTitle(QtGui.QApplication.translate("PaymentDialog", "Payment", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PaymentDialog", "Cafeteria Costs", None, QtGui.QApplication.UnicodeUTF8))
        self.cafeteriaWidget.headerItem().setText(0,QtGui.QApplication.translate("PaymentDialog", "Product", None, QtGui.QApplication.UnicodeUTF8))
        self.cafeteriaWidget.headerItem().setText(1,QtGui.QApplication.translate("PaymentDialog", "Price", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PaymentDialog", "Total Cost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PaymentDialog", "Used Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PaymentDialog", "guest", None, QtGui.QApplication.UnicodeUTF8))
