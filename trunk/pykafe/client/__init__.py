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
from PyQt4 import QtCore, QtGui
import client

"""if not server.listen(QtNetwork.QHostAddress(config.network.serverIP), config.network.port):
    #TODO: don't exit, send information to gui and retry every 3 seconds
    exit("Connection Error: %s" % server.errorString())
"""
app = QtGui.QApplication(argv)
client = client.PykafeClient(QtCore.QObject())
exit(app.exec_())