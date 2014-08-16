################################################################
# File: ct.py
# Title: Chatango Library
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.1.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
#      not blank
#      register doc/help
################################################################

### Imports, Standard Modules

import re
import os
import imp
import sys
import time
import html
import queue
import random
import select
import socket
import threading

#################################################################

### Variables, Custom & Non-Standard Modules

import ts
import tm
import requests


#################################################################

### Class

# registering function/hooks class

registered = {}

class register:

    def _setup_register(name,value):
        def internal(func):
            registered[name] = value
            return func
        return internal

    def _master_register_function(self,value,func):
        """this function is not to be use by noobs"""
        registered[value].append(func)

    # chatango related stuff
    @_setup_register("message",[])
    def on_message(func):
        """register a function to be call on message"""
        registered["message"].append(func)

    @_setup_register("ok",[])
    def on_ok(func):
        """register a function to be call on ok"""
        registered["ok"].append(func)

    @_setup_register("denied",[])
    def on_denied(func):
        """register a function to be call on denied"""
        registered["denied"].append(func)

    @_setup_register("inited",[])
    def on_inited(func):
        """register a function to be call on inited"""
        registered["inited"].append(func)

    @_setup_register("delete",[])
    def on_delete(func):
        """register a function to be call on message"""
        registered["delete"].append(func)

    @_setup_register("deleteall",[])
    def on_delete(func):
        """register a function to be call on message"""
        registered["deleteall"].append(func)

    @_setup_register("n",[])
    def on_user_count_change(func):
        """register a function to be call on user count change"""
        registered["n"].append(func)

    @_setup_register("u",[])
    def on_message_id(func):
        """register a function to be call on message id"""
        registered["u"].append(func)

    @_setup_register("b",[])
    def on_raw_message(func):
        """register a function to be call on raw message"""
        registered["b"].append(func)

    @_setup_register("blocklist",[])
    def on_receive_blocklist(func):
        """register a function to be call when blocklist is receive"""
        registered["n"].append(func)

    @_setup_register("show_fw",[])
    def on_flood_warning(func):
        """register a function to be call on flood warning"""
        registered["show_fw"].append(func)

    @_setup_register("show_tb",[])
    def on_flood_warning(func):
        """register a function to be call on flood ban"""
        registered["show_tb"].append(func)

    @_setup_register("tb",[])
    def on_flood_warning(func):
        """register a function to be call on flood ban repeat"""
        registered["tb"].append(func)

    @_setup_register("blocked",[])
    def on_blocked(func):
        """register a function to be call someone get unblocked"""
        registered["blocked"].append(func)

    @_setup_register("unblocked",[])
    def on_unblocked(func):
        """register a function to be call someone get unblocked"""
        registered["unblocked"].append(func)

    @_setup_register("participant",[])
    def on_participant(func):
        """register a function to be call when someone join or leave"""
        registered["participant"].append(func)

    # bot related stuff
    @_setup_register("__init__",[])
    def on_init(func):
        """register a function to be call on start"""
        registered["__init__"].append(func)

    @_setup_register("connect",[])
    def on_connect(func):
        """register a function to be call on connect"""
        registered["connect"].append(func)

    @_setup_register("disconnect",[])
    def on_disconnect(func):
        """register a function to be call on disconnect"""
        registered["disconnect"].append(func)

    @_setup_register("reconnect",[])
    def on_reconnect(func):
        """register a function to be call on reconnect"""
        registered["reconnect"].append(func)

    @_setup_register("join",[])
    def on_join(func):
        """register a function to be call when people join"""
        registered["join"].append(func)

    @_setup_register("leave",[])
    def on_leave(func):
        """register a function to be call when people leave"""
        registered["leave"].append(func)

    @_setup_register("raw",[])
    def on_raw(func):
        """register a function to be call when getting data"""
        registered["raw"].append(func)

    @_setup_register("doc",{})
    @_setup_register("cmd",{})
    def cmd(cmd):
        """register a cmd with a function to be call"""
        def __internal(func, doc=""):
            registered["cmd"][cmd] = func
            registered["doc"][cmd] = doc
        return __internal

# room

class room_base:

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
        for func in registered["raw"]:
            tm.set_job(func,self.cm,self,data)
        data = data.split(":")
        cmd, args = data[0], data[1:]
        if cmd in registered:
            for func in registered[cmd]:
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
        #self.pingTask = self.mgr.setInterval(self.mgr._pingDelay, self.ping)

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

class room_minimum(room_base):

    # register function
    @register.on_inited
    def inited(self):
        if not self.connected:
            self.connected = True
            for func in registered["connect"]:
                tm.set_job(func,self.cm,self)
        else:
            for func in registered["reconnect"]:
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

    @register.on_message_id
    def messageid(self,args):
        if args[0] in self.msg_queue:
            msg = self.msg_queue[args[0]]
            del self.msg_queue[args[0]]
            setattr(msg, "msgid", args[1])
            if msg.body:
                for func in registered["message"]:
                    tm.set_job(func,self.cm,msg)
                tmp = msg.body.split(" ")
                if len(tmp) == 1:
                    cmd, args = tmp[0], ""
                else:
                    cmd, args = tmp[0], tmp[1:]
                if cmd in registered["cmd"]:
                    tm.set_job(registered["cmd"][cmd],self.cm,msg,args)

class room_default(room_minimum):

    pass

class room_bloated(room_default):

    pass

# pm

class pm:

    def __init__(self):
        self.rbuf = b""
        self.wbuf = b""


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

# connection_manager

class connection_manager_base:

    def __init__(self, name, password, pm=False):
        self.name = name
        self.password = password
        self.base_setup()
        self.other_setup()

    def base_setup(self):
        self.pm = pm
        self.rooms = {}
        self.pms = {}
        self.users = {}
        self.register = register()
        self.running = True
        self.timer = 0.2
        self.ping_interval = 20

    def other_setup(self):
        pass

    def join(self, name):
        name = name.lower()
        if not name in self.rooms:
            self.rooms[name] = self.room(name,self)

    def leave(self, room):
        room = room.lower()
        if room in self.rooms:
            self.rooms[room].close()
            del self.rooms[room]

    def register_modules(self,module_folder):
        if os.path.isdir(module_folder):
            for filename in os.listdir(module_folder):
                if filename.endswith(".py") and not module.startswith("_"):
                    try:
                        module = imp.load_source(os.path.basename(filename)[:-3], filename)
                    except:
                        print("Error loading %s: %s" % (name, e), file=sys.stderr)
                    else:
                        print("loaded %s" % (name))
                        for name, obj in vars(module):
                            # if obj has specify a name, use that, else use the variable name
                            if hasattr(obj, "cmd"):
                                name = obj.cmd

                            registered["cmd"][name] = obj
                            if hasattr(obj, "doc"):
                                registered["doc"][name] = obj.doc
                            elif hasattr(obj, "__doc__"):
                                registered["doc"][name] = obj.__doc__

    def ping(self):
        for room_name in self.rooms:
            room = self.rooms[room_name]
            if room.ping_time < time.time():
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
            self.ping()
            tm.tick()

    @classmethod
    def start(cm,rooms,name,password,pm=False,num_of_thread=1,module_folder="modules"):
        tm.start_job_thread(num_of_thread)
        self = cm(name, password, pm = pm)
        for room in rooms:
            self.join(room)
        self.main()

class connection_manager_minimum(connection_manager_base):

    def other_setup(self):
        self.room = room_minimum
        self.user = user_minimum


class connection_manager_default(connection_manager_minimum):

    def other_setup(self):
        self.room = room_default
        self.user = user_default
        self.register_modules(module_folder)

class connection_manager_bloated(connection_manager_default):

    def other_setup(self):
        self.room = room_bloated
        self.user = user_bloated

