from logging import getLogger
from nekbot.protocols.base.group_chat import GroupChats
from nekbot.protocols.telegram.user import UsersTelegram

__author__ = 'nekmo'

from nekbot.protocols import GroupChat

logger = getLogger('nekbot.protocols.telegram.group_chat')


class GroupChatTelegram(GroupChat):
    def __init__(self, protocol, receiver):
        self.receiver = receiver
        GroupChat.__init__(self, protocol, receiver.title)
        self.users = UsersTelegram(protocol)
        self.id = receiver.id
        self.send_method

    def get_users(self, override=True):
        users = UsersTelegram(self.protocol)
        # for user in self.receiver.users():
        #     user = UserIRC(self.server, user)
        #     users[str(user)] = user
        if override: self.users = users
        self.protocol.sender.chat_info(self.receiver.cmd)
        logger.debug('Users in %s: %s' % (self.name, ', '.join(users)))
        return users

    def send_message(self, body):
        self.protocol.sender.send_msg(self.receiver.cmd, self.protocol.prepare_message(body))

class GroupChatsTelegram(GroupChats):
    pass