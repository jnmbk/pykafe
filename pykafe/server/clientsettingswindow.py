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
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class Ui_ClientSettingsWindow(object):
    def setupUi(self, ClientSettingsWindow, client):
        ClientSettingsWindow.setObjectName("ClientSettingsWindow")
        ClientSettingsWindow.setWindowModality(QtCore.Qt.WindowModal)
        ClientSettingsWindow.resize(QtCore.QSize(QtCore.QRect(0,0,334,107).size()).expandedTo(ClientSettingsWindow.minimumSizeHint()))
        ClientSettingsWindow.setWindowIcon(QtGui.QIcon("../../data/icons/kcontrol.png"))

        self.gridlayout = QtGui.QGridLayout(ClientSettingsWindow)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(ClientSettingsWindow)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.label_2 = QtGui.QLabel(ClientSettingsWindow)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.clientIP = QtGui.QLineEdit(ClientSettingsWindow)
        self.clientIP.setObjectName("clientIP")
        self.clientIP.setInputMask("000.000.000.000;_")
        self.gridlayout.addWidget(self.clientIP,1,1,1,1)

        self.clientID = QtGui.QLineEdit(ClientSettingsWindow)
        self.clientID.setObjectName("clientID")
        self.gridlayout.addWidget(self.clientID,0,1,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(ClientSettingsWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,2,0,1,2)

        self.retranslateUi(ClientSettingsWindow)
        if client:
            self.clientID.setText(client.name)
            self.clientIP.setText(client.ip)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),ClientSettingsWindow.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),ClientSettingsWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientSettingsWindow)
        ClientSettingsWindow.setTabOrder(self.clientID,self.clientIP)
        ClientSettingsWindow.setTabOrder(self.clientIP,self.buttonBox)

    def retranslateUi(self, ClientSettingsWindow):
        ClientSettingsWindow.setWindowTitle(_("Client Settings"))
        self.label.setText(_("Client ID:"))
        self.label_2.setText(_("Client IP:"))
