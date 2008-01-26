#!/usr/bin/python
# -*- coding: utf-8 -*-

"""PyKafe server main module """

import signal, sys

from PyQt4 import QtCore
from PyQt4 import QtGui

import mainwindow_server

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

    mainWindow = mainwindow_server.MainWindow()
    mainWindow.show()

    return app.exec_()

if __name__ == "__main__":
    main()
