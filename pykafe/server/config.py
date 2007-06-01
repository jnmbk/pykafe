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
from database import Database

class ClientInformation:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.session = ClientSession()

class PykafeConfiguration:
    "configuration class reads configuration values from database, you can reach them like config.my_config"
    def __init__(self):
        settings = Database().runOnce("select * from general_settings")
        for config, value in settings:
            setattr(self, config, value)
    clientList = [ClientInformation("192.168.2.3", "computer1"),
                  ClientInformation("192.168.2.4", "computer2"),
                  ClientInformation("192.168.2.5", "computer3")]
    def set(self, config, value):
        "sets given configuration as given value writes to database, this doesn't do anything if there's not a real change"
        if getattr(self, config) == value:
            return
        setattr(self, config, value)
        Database().runOnce("update general_settings set setting_value=? where setting_id=?", (value, config))
        #TODO: There may be some specific configs that may require extra work
