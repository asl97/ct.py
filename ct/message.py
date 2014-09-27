################################################################
# File: message.py
# Title: Message Manager
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.3.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

class message:

    def __init__(self, **kw):
        self.base_setup()
        for a, b in kw.items():
            if b == None: continue
            setattr(self, a, b)

    def base_setup(self):
        self.msgid = None
        self.time = None
        self.user = None
        self.body = None
        self.room = None
        self.raw = ""
        self.ip = None
        self.unid = ""
        self.nc = "000"
        self.fs = 12
        self.ff = "0"
        self.fc = "000"
