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

from pysqlite2 import dbapi2 as sqlite

class Database:
    databaseFile = "/home/jnmbk/.pyKafe/pyKafe.db"

    def __init__(self):
        #TODO: Handle exceptions
        self.con = sqlite.connect(self.databaseFile)
        self.cur = self.con.cursor()

    def run(self, query):
        #TODO: check for sql injection
        self.cur.execute(query)
        if not 'select' in query: self.con.commit()
        return self.cur.fetchall()