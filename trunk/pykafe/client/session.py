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
_ = gettext.translation("pyKafe_client", fallback=True).ugettext

class ClientSession:
    """class for managing client sessions"""
    notAvailable, notConnected, working, loggedIn, requestedOpening = range(5)
    def __init__(self):
        self.state = 0
        self.user = None
        self.settings = None
        self.startTime = None
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
        if self.state == self.notAvailable:
            return _("N/A")
        elif self.state == self.working:
            return _("Ready")
        elif self.state == self.loggedIn:
            return _("Logged In")
        elif self.state == self.requestedOpening:
            return _("Requested Opening")

    def setState(self, stateNumber):
        self.state = stateNumber