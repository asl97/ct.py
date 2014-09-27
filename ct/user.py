################################################################
# File: user.py
# Title: User Manager
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.3.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

class _system:

    def __init__(self, cm):
        self.users = {}
        self.cm = cm
        self.user = self.cm.user

    def add(self, name):
        self.users[name] = self.user(name)

class base:

    def __init__(self, name):
        self.name = name
        self.other_setup()

    def other_setup(self):
        pass

class minimum(base):

    pass

class default(minimum):

    def other_setup(self):
        self.rooms = {}

class bloated(default):

    pass
