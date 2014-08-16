import ct

class example(ct.connection_manager_minimum):

    @ct.register.on_connect
    def onconnect(self,room):
        print("connected to %s" % (room.name))

    @ct.register.on_reconnect
    def onreconnect(self, room):
        print("Reconnected to "+room.name)

    @ct.register.on_disconnect
    def ondisconnect(self,room):
        print("disconnected from %s" % (room.name))

    #@ct.register.on_raw
    #def onraw(self,room,args):
    #    print(args)

    @ct.register.on_message
    def onmsg(self,msg):
        print("%s@%s: %s"%(msg.user.name,msg.room.name,msg.body))

    @ct.register.cmd("!a")
    def a(self,msg,args):
        if msg.user.name == self.name: return
        msg.room.message("AAAAAAAAAAAAAAAAAAA!")

#eg: example.start(["room1","room2"],"username","password")
example.start([],"","")

