################################################################
# File: example.py
# Title: An Example Bot for The CT Library
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 0.0.2.5
# Bug report: https://github.com/asl97/ct.py
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

from ct import cm, register

#class example(cm.connection_manager_minimum):
class example(cm.connection_manager_default):

    @register.on_connect
    def onconnect(self,room):
        print("connected to %s" % (room.name))

    @register.on_reconnect
    def onreconnect(self, room):
        print("Reconnected to "+room.name)

    @register.on_disconnect
    def ondisconnect(self,room):
        print("disconnected from %s" % (room.name))

    #@register.on_raw
    #def onraw(self,room,args):
    #    print(args)

    @register.on_message
    def onmsg(self,msg):
        print("%s@%s: %s"%(msg.user.name,msg.room.name,msg.body))

    @register.cmd("!a")
    def a(self,msg,args):
        if msg.user.name == self.name: return
        msg.room.message("AAAAAAAAAAAAAAAAAAA!")

#eg: example.start(["room1","room2"],"username","password")
example.start([],"","")

