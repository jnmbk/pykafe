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

class ClientSession:
    """class for managing client sessions"""

    #state can be: 0:N/A, 1:Working, 2:LoggedIn
    state = 0
    user = None
    settings = None
    startTime = None
    orders = []

    def isReachable(self):
        if state == 0:
            return False
        else:
            return True
    def isWorking(self):
        if state == 1:
            return True
        else:
            return False
    def isLoggedIn(self):
        if state == 2:
            return True
        else:
            return False
    def getCurrentState(self):
        """returns current state as a string"""
        if self.state == 0:
            return "N/A"
        elif self.state == 1:
            return "Ready"
        else:
            return "Logged In"
    def setState(self, stateNumber):
        self.state = stateNumber