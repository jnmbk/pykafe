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

from database import Database
from PyQt4 import QtCore

def add(log_type, log_value, cashier, computer = "", member = "", income = ""):
    date = QtCore.QDateTime.currentDateTime().toTime_t()
    Database().runOnce("insert into logs (date, log_type, log_value, cashier, computer, member, income) values (?,?,?,?,?,?,?)", (date, log_type, log_value, cashier, computer, member, income))
class logTypes:
    information, warning, error, emergency = range(4)
