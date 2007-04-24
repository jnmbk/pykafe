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

from sys import argv, exit
from PyQt4 import QtGui
from mainwindow import Ui_MainWindow

app = QtGui.QApplication(argv)
window = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()
exit(app.exec_())
