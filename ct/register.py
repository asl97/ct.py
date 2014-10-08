################################################################
# File: register.py
# Title: Function Registry Library
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.2.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

# standard modules use only in register_modules
import importlib
import register
import sys
import os


# the registry which contain the registered function

class _registry:

    def __init__(self):
        self.registered = {}

    def _setup(self,name,value):
        """set value to name in registered (dict)"""
        def internal(func):
            self.registered[name] = value
            return func
        return internal

    def _master_register(self,value,func):
        """this function is not to be use by noobs"""
        registered[value].append(func)

    def register_modules(self,module_folder):
        if os.path.isdir(module_folder):
            for filename in os.listdir(module_folder):
                if filename.endswith(".py") and not filename.startswith("_"):
                    try:
                        module = importlib.machinery(
                                os.path.basename(filename)[:-3],
                                os.path.join(module_folder,filename)
                        ).load_module()
                    except Exception as e:
                        print("[dynamic module loader]Error loading %s: %s" % (filename, e), file=sys.stderr)
                    else:
                        print("[dynamic module loader]loaded %s" % (filename))
                        for obj in vars(module).values():
                            # obj must specify a name
                            if hasattr(obj, "cmd"):
                                name = obj.cmd
                                register.registered["cmd"][name] = obj
                                if hasattr(obj, "doc"):
                                    register.registered["doc"][name] = obj.doc
                                elif hasattr(obj, "__doc__"):
                                    register.registered["doc"][name] = obj.__doc__

# registering function/hooks class

_r = _registry()
setup = _r._setup
registered = _r.registered
modules = _r.register_modules

# chatango related stuff
@setup("message",[])
def on_message(func):
    """register a function to be call on message"""
    registered["message"].append(func)

@setup("ok",[])
def on_ok(func):
    """register a function to be call on ok"""
    registered["ok"].append(func)

@setup("denied",[])
def on_denied(func):
    """register a function to be call on denied"""
    registered["denied"].append(func)

@setup("inited",[])
def on_inited(func):
    """register a function to be call on inited"""
    registered["inited"].append(func)

@setup("delete",[])
def on_delete(func):
    """register a function to be call on message"""
    registered["delete"].append(func)

@setup("deleteall",[])
def on_delete(func):
    """register a function to be call on message"""
    registered["deleteall"].append(func)

@setup("n",[])
def on_user_count_change(func):
    """register a function to be call on user count change"""
    registered["n"].append(func)

@setup("u",[])
def on_message_id(func):
    """register a function to be call on message id"""
    registered["u"].append(func)

@setup("b",[])
def on_raw_message(func):
    """register a function to be call on raw message"""
    registered["b"].append(func)

@setup("blocklist",[])
def on_receive_blocklist(func):
    """register a function to be call when blocklist is receive"""
    registered["n"].append(func)

@setup("show_fw",[])
def on_flood_warning(func):
    """register a function to be call on flood warning"""
    registered["show_fw"].append(func)

@setup("show_tb",[])
def on_flood_warning(func):
    """register a function to be call on flood ban"""
    registered["show_tb"].append(func)

@setup("tb",[])
def on_flood_warning(func):
    """register a function to be call on flood ban repeat"""
    registered["tb"].append(func)

@setup("blocked",[])
def on_blocked(func):
    """register a function to be call someone get unblocked"""
    registered["blocked"].append(func)

@setup("unblocked",[])
def on_unblocked(func):
    """register a function to be call someone get unblocked"""
    registered["unblocked"].append(func)

@setup("participant",[])
def on_participant(func):
    """register a function to be call when someone join or leave"""
    registered["participant"].append(func)

# bot related stuff
@setup("__init__",[])
def on_init(func):
    """register a function to be call on start"""
    registered["__init__"].append(func)

@setup("connect",[])
def on_connect(func):
    """register a function to be call on connect"""
    registered["connect"].append(func)

@setup("disconnect",[])
def on_disconnect(func):
    """register a function to be call on disconnect"""
    registered["disconnect"].append(func)

@setup("reconnect",[])
def on_reconnect(func):
    """register a function to be call on reconnect"""
    registered["reconnect"].append(func)

@setup("join",[])
def on_join(func):
    """register a function to be call when people join"""
    registered["join"].append(func)

@setup("leave",[])
def on_leave(func):
    """register a function to be call when people leave"""
    registered["leave"].append(func)

@setup("raw",[])
def on_raw(func):
    """register a function to be call when getting data"""
    registered["raw"].append(func)

@setup("lvl",{})
@setup("doc",{})
@setup("cmd",{})
def cmd(cmd, doc="", lvl=False):
    """register a cmd with a function to be call"""
    def __internal(func):
        registered["cmd"][cmd] = func
        if doc:
            registered["doc"][cmd] = doc
        elif func.__doc__:
            registered["doc"][cmd] = func.__doc__
        if lvl is not False:
            registered["lvl"][cmd] = lvl
        elif hasattr(func,"__lvl__"):
            registered["lvl"][cmd] = func.__lvl__
    return __internal

# functions/api

def check_cmd(cm,msg):
    if msg.body:
        for func in registered["message"]:
            tm.set_job(func,cm,msg)
        tmp = msg.body.split(" ")
        if len(tmp) == 1:
            cmd, args = tmp[0], ""
        else:
            cmd, args = tmp[0], tmp[1:]
        if cmd in registered["cmd"]:
            tm.set_job(registered["cmd"][cmd],cm,msg,args)
