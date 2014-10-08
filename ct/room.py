################################################################
# File: room.py
# Title: Room Manager
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.3.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

### Imports, Standard Modules

import re
import time
import random
import socket

### Variables, Custom & Non-Standard Modules

from . import register
from . import ts
from . import tm

class _system:

    def __init__(self, cm):
        self.rooms = {}
        self.cm = cm
        self.room = self.cm.room

    def join(self, name):
        name = name.lower()
        if not name in self.rooms:
            self.rooms[name] = self.room(name)

    def leave(self, room):
        room = room.lower()
        if room in self.rooms:
            self.rooms[room].close()
            del self.rooms[room]

class base:

    def __init__(self, name, cm):
        """cm == connection manager"""
        self.name = name
        self.cm = cm
        self.ping_time = time.time() + cm.ping_interval
        self.server = "s" + str(ts.get(name)) + ".chatango.com"
        self.base_setup()
        self.connect()

    def base_setup(self):
        self.users = {}
        self.rbuf = b""
        self.wbuf = b""
        self.wlbuf = b""
        self.wlock = False
        self.connected = False
        self.uid = str(random.randrange(10 ** 15, 10 ** 16))
        self.port = 443
        self.msg_queue = {}

    def read(self, raw):
        self.rbuf += raw
        if b"\x00" in self.rbuf:
            data = self.rbuf.split(b"\x00")
            for line in data[:-1]:
                self.process(line.rstrip().decode("utf-8"))
            self.rbuf = data[-1]

    def process(self, data):
        for func in register.registered["raw"]:
            tm.set_job(func,self.cm,self,data)
        data = data.split(":")
        cmd, args = data[0], data[1:]
        if cmd in register.registered:
            for func in register.registered[cmd]:
                if args:
                    tm.set_job(func,self,args)
                else:
                    tm.set_job(func,self)

    def fwrite(self, *args):
        data = ":".join(args).encode("utf-8") + b"\x00"
        if self.wlock:
            self.wlbuf += data
        else:
            self.wbuf += data

    def write(self, *args):
        data = ":".join(args).encode("utf-8") + b"\r\n\x00"
        if self.wlock:
            self.wlbuf += data
        else:
            self.wbuf += data

    def swlock(self, lock):
        self.wlock = lock
        if not self.wlock:
            self.wbuf += self.wlbuf
            self.wlbuf = b""

    def auth(self):
        if self.cm.name and self.cm.password:
            self.fwrite("bauth", self.name, self.uid, self.cm.name, self.cm.password)
        else:
            self.fwrite("bauth", self.name)
        self.swlock(True)

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.server, self.port))
        self.sock.setblocking(False)
        self.auth()

    def disconnect(self):
        self.sock.close()

    def message(self,msg):
        if msg:
            msg = html.escape(msg.rstrip())
            self.write("bmsg:tl2r",msg)

    def parse_message(self,msg):
        n = re.search("<n(.*?)/>", msg)
        if n: n = n.group(1)
        f = re.search("<f(.*?)>", msg)
        if f: f = f.group(1)
        msg = html.unescape(re.sub("<.*?>", "", msg))
        return msg, n, f

    def parse_font(self, f):
        try:
            r = re.search('x(\d\d)?(\d\d\d)?="(.*?)"',f)
            return r.groups()
        except:
            return None, None, None

    def getaid(self, n, uid):
        """Gets the anon's id."""
        if n == None: return "NNNN"
        try:
            return "".join(["%d" % ((int(n[i]) + int(uid[i+4])) % 10) for i in range(0,4)])
        except:
            return "NNNN"

class minimum(base):

    # register function
    @register.on_inited
    def inited(self):
        if not self.connected:
            self.connected = True
            for func in register.registered["connect"]:
                tm.set_job(func,self.cm,self)
        else:
            for func in register.registered["reconnect"]:
                tm.set_job(func,self.cm,self)
        self.swlock(False)

    @register.on_raw_message
    def raw_message(self,args):
        name = args[1]
        puid = args[3]
        rawmsg = ":".join(args[9:])
        msg, n, f = self.parse_message(rawmsg)
        if not name:
            nameColor = None
            if args[2]:
                name = "#" + args[2]
            else:
                name = "!anon" + self.getaid(n, puid)
        else:
            if n:
                nameColor = n
            else:
                nameColor = None
        if f:
            fontColor, fontFace, fontSize = self.parse_font(f)
        else:
            fontColor, fontFace, fontSize = None, None, None
        msg = message(
          time = float(args[0]),
          user = self.cm.user(name),
          body = msg,
          raw = rawmsg,
          ip = args[6],
          nc = nameColor,
          fc = fontColor,
          ff = fontFace,
          fs = fontSize,
          unid = args[4],
          room = self
        )
        self.msg_queue[args[5]] = msg

class default(minimum):

    pass

class bloated(default):

    pass
