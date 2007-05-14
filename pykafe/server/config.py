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

class ClientInformation:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.session = ClientSession()

class PykafeConfiguration:
    def __init__(self):
        #TODO: read general settings from database, and provide a method to write them.
        pass
    clientList = [ClientInformation("192.168.2.3", "computer1"),
                  ClientInformation("192.168.2.4", "computer2")]
    class network:
        port = 23105
    class currency:
        prefix = ""
        suffix = " YTL"
        seperator = "."
