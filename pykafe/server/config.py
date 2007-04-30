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

#TODO: Read config from database api
from session import ClientSession

class PykafeConfiguration:
    class network:
        port = 23105
    computerList = ({"ip":"192.168.2.3", "name":"computer1", "session":ClientSession()})