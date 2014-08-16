#!/usr/bin/python
import ch

class TestBot(ch.RoomManager):

  def onConnect(self, room):
    print("Connected to "+room.name)

  def onReconnect(self, room):
    print("Reconnected to "+room.name)

  def onDisconnect(self, room):
    print("Disconnected from "+room.name)

  def onHistoryMessage(self, room, user, message):
    self.safePrint(user.name + ': ' + message.body)

  def onMessage(self, room, user, message):
    # Use with PsyfrBot framework? :3
    self.safePrint('%s[%s]: %s' % (user.name, user.puid, message.body))

    if message.body.startswith("!a"):
      room.message("AAAAAAAAAAAAAA")

    if message.body.startswith("!ev"):
      try:
        room.message(str(eval(message.body.split(" ",1)[1])))
      except Exception as e:
        print(str(e))
        room.message("error, see console")

  def onMessageDelete(self, room, user, message):
    self.safePrint('deleted: '+ user.name + ': ' + message.body)

  def onFloodBan(self, room):
    print("You are flood banned in "+room.name)

  def onRaw(self, room, raw):
    print(raw)

  def onPMMessage(self, pm, user, body):
    self.safePrint('PM: ' + user.name + ': ' + body)
    pm.message(user, body) # echo

if __name__ == "__main__":
  TestBot.easy_start()
