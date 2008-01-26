#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtNetwork

class TcpServer(QtNetwork.QTcpServer):
    def __init__(self, parent = None):
        QtNetwork.QTcpServer.__init__(self, parent)
