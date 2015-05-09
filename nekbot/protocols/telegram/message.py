from logging import getLogger
from datetime import datetime, timedelta
from nekbot.protocols.telegram.group_chat import GroupChatTelegram
from nekbot.protocols.telegram.user import UserTelegram
from nekbot.protocols import Message

__author__ = 'nekmo'

logger = getLogger('nekbot.protocols.telegram.message')


class MessageTelegram(Message):
    def __init__(self, protocol, msg):
        logger.debug('New message: %s' % vars(msg))
        user = UserTelegram(protocol, msg.sender)
        self.msg = msg
        if self.is_groupchat:
            groupchat = GroupChatTelegram(protocol, msg.receiver)
        else:
            groupchat = None
        if protocol.bot is None:
            protocol.bot = UserTelegram(protocol, msg.receiver)
        self.historical = msg.freshness != 'new'
        super(MessageTelegram, self).__init__(protocol, msg.text, user, groupchat)

    @property
    def is_public(self):
        return True if self.is_groupchat else False

    @property
    def is_from_me(self):
        return self.msg.own

    @property
    def is_groupchat(self):
        return self.msg.receiver.type == 'group'

    def _copy(self):
        return self.__class__(self.protocol, self.msg)
