#!/usr/bin/python
import os
os.system("xgettext -s --no-wrap --files-from=server.txt --output=pyKafe_server.pot")
os.system("xgettext -s --no-wrap --files-from=client.txt --output=pyKafe_client.pot")
translations = ["tr"]
for i in translations:
    os.system("msgmerge -U client_%s.po pyKafe_client.pot" % i)
    os.system("msgfmt client_%s.po -o /usr/share/locale/%s/LC_MESSAGES/pyKafe_client.mo" % (i,i))
    os.system("msgmerge -U server_%s.po pyKafe_server.pot" % i)
    os.system("msgfmt server_%s.po -o /usr/share/locale/%s/LC_MESSAGES/pyKafe_server.mo" % (i,i))
