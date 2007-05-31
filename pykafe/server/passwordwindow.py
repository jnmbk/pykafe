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
from mainwindow import Ui_MainWindow
import sha

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,226,159).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setWindowIcon(QtGui.QIcon("../../data/icons/pyKafe.png"))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,2,3,1,1)

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem2,0,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem3,4,2,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,3,1,1,2)

        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,1,1,1)

        self.username = QtGui.QLineEdit(Dialog)
        self.username.setObjectName("username")
        self.gridlayout.addWidget(self.username,1,2,1,1)

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,1,1,1)

        self.password = QtGui.QLineEdit(Dialog)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridlayout.addWidget(self.password,2,2,1,1)

        self.retranslateUi(Dialog)
        self.dialog = Dialog
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),self.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),self.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_("pyKafe"))
        self.label.setText(_("Username:"))
        self.label_2.setText(_("Password:"))

    def accept(self):
        parameters = unicode(self.username.text()), sha.new(unicode(self.password.text())).hexdigest()
        result = Database().runOnce("select count(*) from members where username=? and password=? and is_cashier='1'", parameters)
        if result[0][0]:
            self.dialog.hide()
            window = QtGui.QMainWindow(self.dialog)
            ui = Ui_MainWindow()
            ui.setupUi(window, parameters[0])
            window.show()
        else:
            QtGui.QMessageBox.critical(self.dialog, _("Error"), _("Wrong username or password"))
    def reject(self):
        self.dialog.close()
