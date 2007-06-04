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

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

class Product:
    def __init__(self, values):
        print values
        self.name, self.price, self.quantity = values.split('|',3)

class Order(QtGui.QTreeWidgetItem):
    def __init__(self, parent, product, value, quantity):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.setText(0, product)
        self.setText(1, value)
        self.setText(2, quantity)

def findProductPrice(products, name):
    for product in products:
        if product.name == name:
            return float(product.value)

class Ui_Dialog(object):
    def setupUi(self, Dialog, client):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,361,300).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setWindowIcon(QtGui.QIcon("../../data/icons/pyKafe.png"))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout1.addItem(spacerItem,0,2,1,1)

        self.addOrder = QtGui.QPushButton(Dialog)
        self.addOrder.setIcon(QtGui.QIcon("../../data/icons/edit_add.png"))
        self.addOrder.setObjectName("addOrder")
        self.gridlayout1.addWidget(self.addOrder,1,2,1,1)

        self.product = QtGui.QComboBox(Dialog)
        self.product.setObjectName("product")
        self.gridlayout1.addWidget(self.product,1,0,1,1)

        self.label = QtGui.QLabel(Dialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.quantity = QtGui.QSpinBox(Dialog)
        self.quantity.setMinimum(1)
        self.quantity.setObjectName("quantity")
        self.gridlayout1.addWidget(self.quantity,1,1,1,1)

        self.label_2 = QtGui.QLabel(Dialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,0,1,1,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,2,0,1,1)

        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout2 = QtGui.QGridLayout(self.tab)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.ordersToSend = QtGui.QTreeWidget(self.tab)
        self.ordersToSend.setObjectName("ordersToSend")
        self.gridlayout2.addWidget(self.ordersToSend,0,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.sentOrders = QtGui.QTreeWidget(self.tab_2)
        self.sentOrders.setObjectName("sentOrders")
        self.gridlayout3.addWidget(self.sentOrders,0,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")
        self.gridlayout.addWidget(self.tabWidget,1,0,1,1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.client = client
        self.products = []
        for product in client.cafeteriaContents:
            self.products.append(Product(product))
            self.product.addItem(self.products[-1].name)
        self.orders = []
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Dialog.reject)
        QtCore.QObject.connect(self.addOrder,QtCore.SIGNAL("clicked()"),self.orderAdd)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_("Cafeteria"))
        self.addOrder.setText(_("Add Order"))
        self.label.setText(_("Product"))
        self.label_2.setText(_("Quantity"))
        self.ordersToSend.headerItem().setText(0,_("Item"))
        self.ordersToSend.headerItem().setText(1,_("Cost"))
        self.ordersToSend.headerItem().setText(2,_("Quantity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _("Orders to Send"))
        self.sentOrders.headerItem().setText(0,_("Item"))
        self.sentOrders.headerItem().setText(1,_("Cost"))
        self.sentOrders.headerItem().setText(2,_("Quantity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _("Sent Orders"))

    def orderAdd(self):
        print 1234
        cost = self.quantity.value() * findProductPrice(self.products, self.product.currentText())
        self.orders.append(Order(self.ordersToSend, self.product.currentText(), cost, self.quantity.value()))
        self.client.temporders.append[self.product.currentText() + '|' + str(self.quantity.value())]
