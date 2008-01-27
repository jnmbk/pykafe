#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under GPL v2
# Copyright 2008, Ugur Cetin
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""PyKafe server main module """

import signal, sys

from PyQt4 import QtCore
from PyQt4 import QtGui

def loadTranslator():
    settings = QtCore.QSettings()
    if settings.contains("language"):
        locale = settings.value("language").toString()
    else:
        locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    translator.load(":/pykafe_%s.qm" % locale)
    QtGui.qApp.installTranslator(translator)

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("pykafe")
    app.setOrganizationName("pykafe")

    loadTranslator()

    import mainwindow_server
    mainWindow = mainwindow_server.MainWindow()
    mainWindow.show()

    return app.exec_()

if __name__ == "__main__":
    main()
