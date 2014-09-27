################################################################
# File: cm.py
# Title: Connection Manager
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.3.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

### Imports, Standard Modules

import re
import os
import sys
import time
import html
import queue
import random
import select
import socket
import importlib
import threading

#################################################################

### Variables, Custom & Non-Standard Modules

import requests

from . import register
from . import message
from . import room
from . import user
from . import pm
from . import ts
from . import tm

#################################################################

class connection_manager_base:

    def __init__(self, name, password, pm, module_folder):
        self.name = name
        self.password = password
        self.pm = pm
        self.module_folder = module_folder
        self.base_setup()
        self.other_setup()

    def base_setup(self):
        ### basic setting for bot
        self.running = True
        self.timer = 0.2
        self.ping_interval = 20

        ### module setting for bot

        # rooms
        self._room = room._system(self)
        self.join = self._room.join
        self.leave = self._room.leave

        # users
        self._user = user._system(self)
        self.user = self._user.add

        # make it so rooms, pm and users is accessible in the bot
        self.rooms = self._room.rooms
        self.pm = {}
        self.users = self._user.users

    def other_setup(self):
        pass

    def ping(self):
        for room_name in self.rooms:
            room = self.rooms[room_name]
            if room.ping_time < time.time():
                room.ping_time += self.ping_interval
                room.write("")

    def main(self):
        while self.running:
            conns = {self.rooms[room].sock:self.rooms[room] for room in self.rooms}
            socks = conns.keys()
            wsocks = [sock for sock,room in conns.items() if room.wbuf != b""]
            rd, wr, sp = select.select(socks, wsocks, [], self.timer)
            for sock in rd:
                con = conns[sock]
                try:
                    data = sock.recv(1024)
                    if(len(data) > 0):
                        con.read(data)
                    else:
                        con.disconnect()
                except socket.error:
                    pass
            for sock in wr:
                con = conns[sock]
                try:
                    size = sock.send(con.wbuf)
                    con.wbuf = con.wbuf[size:]
                except socket.error:
                    pass
            # do the ping in the same thread as the connection manager
            # instead of the job/task threads
            # since the ping shouldn't take too long... hopefully...
            self.ping()
            tm.tick()

    @classmethod
    def start(cm,rooms,name,password,pm=False,num_of_thread=1,module_folder="modules"):
        tm.start_job_thread(num_of_thread)
        self = cm(name, password, pm, module_folder)
        for room in rooms:
            self.join(room)
        self.main()

class connection_manager_minimum(connection_manager_base):

    def other_setup(self):
        self.room = room.minimum
        self.user = user.minimum


class connection_manager_default(connection_manager_minimum):

    def other_setup(self):
        self.room = room.default
        self.user = user.default
        register.modules(self.module_folder)

class connection_manager_bloated(connection_manager_default):

    def other_setup(self):
        self.room = room.bloated
        self.user = user.bloated
        register.modules(self.module_folder)

