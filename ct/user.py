################################################################
# File: user.py
# Title: User Manager
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.3.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

class user_base:

    def __init__(self, name):
        self.name = name
        self.other_setup()

    def other_setup(self):
        pass

class user_minimum(user_base):

    pass

class user_default(user_minimum):

    def other_setup(self):
        self.rooms = {}

class user_bloated(user_default):

    pass
