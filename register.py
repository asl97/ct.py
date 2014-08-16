################################################################
# File: register.py
# Title: Function Registry Library
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.2.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

# the registry which contain the registered function

class _registry:

    def __init__(self):
        self.registered = {}

    def _setup_register(self,name,value):
        """set value to name in registered (dict)"""
        def internal(func):
            self.registered[name] = value
            return func
        return internal

    def _master_register_function(self,value,func):
        """this function is not to be use by noobs"""
        registered[value].append(func)

# registering function/hooks class

_r = _registry()
registered = _r.registered

# chatango related stuff
@_r._setup_register("message",[])
def on_message(func):
    """register a function to be call on message"""
    _r.registered["message"].append(func)

@_r._setup_register("ok",[])
def on_ok(func):
    """register a function to be call on ok"""
    _r.registered["ok"].append(func)

@_r._setup_register("denied",[])
def on_denied(func):
    """register a function to be call on denied"""
    _r.registered["denied"].append(func)

@_r._setup_register("inited",[])
def on_inited(func):
    """register a function to be call on inited"""
    _r.registered["inited"].append(func)

@_r._setup_register("delete",[])
def on_delete(func):
    """register a function to be call on message"""
    _r.registered["delete"].append(func)

@_r._setup_register("deleteall",[])
def on_delete(func):
    """register a function to be call on message"""
    _r.registered["deleteall"].append(func)

@_r._setup_register("n",[])
def on_user_count_change(func):
    """register a function to be call on user count change"""
    _r.registered["n"].append(func)

@_r._setup_register("u",[])
def on_message_id(func):
    """register a function to be call on message id"""
    _r.registered["u"].append(func)

@_r._setup_register("b",[])
def on_raw_message(func):
    """register a function to be call on raw message"""
    _r.registered["b"].append(func)

@_r._setup_register("blocklist",[])
def on_receive_blocklist(func):
    """register a function to be call when blocklist is receive"""
    _r.registered["n"].append(func)

@_r._setup_register("show_fw",[])
def on_flood_warning(func):
    """register a function to be call on flood warning"""
    _r.registered["show_fw"].append(func)

@_r._setup_register("show_tb",[])
def on_flood_warning(func):
    """register a function to be call on flood ban"""
    _r.registered["show_tb"].append(func)

@_r._setup_register("tb",[])
def on_flood_warning(func):
    """register a function to be call on flood ban repeat"""
    _r.registered["tb"].append(func)

@_r._setup_register("blocked",[])
def on_blocked(func):
    """register a function to be call someone get unblocked"""
    _r.registered["blocked"].append(func)

@_r._setup_register("unblocked",[])
def on_unblocked(func):
    """register a function to be call someone get unblocked"""
    _r.registered["unblocked"].append(func)

@_r._setup_register("participant",[])
def on_participant(func):
    """register a function to be call when someone join or leave"""
    _r.registered["participant"].append(func)

# bot related stuff
@_r._setup_register("__init__",[])
def on_init(func):
    """register a function to be call on start"""
    _r.registered["__init__"].append(func)

@_r._setup_register("connect",[])
def on_connect(func):
    """register a function to be call on connect"""
    _r.registered["connect"].append(func)

@_r._setup_register("disconnect",[])
def on_disconnect(func):
    """register a function to be call on disconnect"""
    _r.registered["disconnect"].append(func)

@_r._setup_register("reconnect",[])
def on_reconnect(func):
    """register a function to be call on reconnect"""
    _r.registered["reconnect"].append(func)

@_r._setup_register("join",[])
def on_join(func):
    """register a function to be call when people join"""
    _r.registered["join"].append(func)

@_r._setup_register("leave",[])
def on_leave(func):
    """register a function to be call when people leave"""
    _r.registered["leave"].append(func)

@_r._setup_register("raw",[])
def on_raw(func):
    """register a function to be call when getting data"""
    _r.registered["raw"].append(func)

@_r._setup_register("doc",{})
@_r._setup_register("cmd",{})
def cmd(cmd):
    """register a cmd with a function to be call"""
    def __internal(func, doc=""):
        _r.registered["cmd"][cmd] = func
        _r.registered["doc"][cmd] = doc
    return __internal

