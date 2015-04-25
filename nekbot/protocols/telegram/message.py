from nekbot.protocols.telegram.user import UserTelegram
from nekbot.protocols import Message

__author__ = 'nekmo'


class MessageTelegram(Message):
    def __init__(self, protocol, msg):
        user = UserTelegram(protocol, msg.user)
        super(MessageTelegram, self).__init__(protocol, msg.message, user)
        self.msg = msg

    def reply(self, body):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        self.protocol.tg.msg(self.msg.reply.cmd, body)
