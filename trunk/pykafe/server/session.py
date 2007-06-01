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

import locale, gettext
locale.setlocale(locale.LC_ALL, "C")
_ = gettext.translation("pyKafe_server", fallback=True).ugettext

class ClientSession:
    """class for managing client sessions"""
    notConnected, notReady, working, loggedIn, requestedOpening, waitingMoney = range(6)
    def __init__(self):
        self.state = 0
        self.user = None
        self.settings = None
        self.startTime = None
        self.endTime = None
        self.orders = []

    def isReachable(self):
        if self.state == 0:
            return False
        else:
            return True
    def isWorking(self):
        if self.state == 1:
            return True
        else:
            return False
    def isLoggedIn(self):
        if self.state == 2:
            return True
        else:
            return False
    def getCurrentState(self):
        """returns current state as a string"""
        if self.state == self.notConnected:
            return _("Not Connected")
        elif self.state == self.working:
            return _("Ready")
        elif self.state == self.loggedIn:
            return _("Logged In")
        elif self.state == self.requestedOpening:
            return _("Requested Opening")
        elif self.state == self.waitingMoney:
            return _("Waiting for Payment")
        elif self.state == self.notReady:
            return _("Not ready")

    def setState(self, stateNumber):
        self.state = stateNumber
