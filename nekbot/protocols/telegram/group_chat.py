from nekbot.protocols.base.group_chat import GroupChats

__author__ = 'nekmo'

from nekbot.protocols import GroupChat

class GroupChatTelegram(GroupChat):
    def __init__(self, protocol, receiver):
        self.receiver = receiver
        GroupChat.__init__(self, protocol, receiver.title)
        self.id = receiver.id

    def send_message(self, body):
        self.protocol.sender.send_msg(self.receiver.cmd, self.protocol.prepare_message(body))

class GroupChatsTelegram(GroupChats):
    pass