################################################################
# File: message.py
# Title: Message Manager
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.3.0
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import config
from . import register

class system:

    def init(self, cm):
        self.messages = {"room":{},"user":{}}
        self.room_msgs = self.messages["room"]
        self.user_msgs = self.messages["user"]
        self.cm = cm

    def process_message(self, **kw)
        message = _message(**kw)
        room = message.room
        user = message.user
        if room:
            # check if room and user are in dict
            if room not in self.room_msgs:
                self.room_msgs[room] = []
            if user not in self.user_msgs:
                self.user_msgs[user] = []

            # store lookup in short variable
            room_d = self.room_msgs[room]
            user_d = self.room_msgs[user]

            # store message in dict
            room_d.append(message)
            user_d.append(message)

            # memory leak prevention
            # aka, clearing old history
            if len(room_d) > config.max_room_history:
                room_d = room_d[-config.max_room_history:]
            if len(user_d) > config.max_user_history:
                user_d = user_d[-config.max_user_history:]
        return message

    @register.on_message_id
    def messageid(self,args):
        if args[0] in self.msg_queue:
            msg = self.msg_queue[args[0]]
            del self.msg_queue[args[0]]
            setattr(msg, "msgid", args[1])
            register.check_cmd(self.cm,msg)


class _message:

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

