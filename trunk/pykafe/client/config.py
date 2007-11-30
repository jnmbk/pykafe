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

#TODO: Read config from config file
class PykafeConfiguration:
    network_serverIP  = "192.168.2.2"
    network_port      = 23105
    network_localPort = 23106

    def set(self, config, value):
        setattr(self, config, value)
