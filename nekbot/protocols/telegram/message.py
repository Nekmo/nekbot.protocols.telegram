from nekbot.protocols.telegram.group_chat import GroupChatTelegram
from nekbot.protocols.telegram.user import UserTelegram
from nekbot.protocols import Message

__author__ = 'nekmo'

# Bot ID: 110261251

# {'username': 'Nekmo', 'timestamp': '00:58', 'groupname': 'Testing', 'user': 'chat#Nekmo#14390491',
# 'peer': 'group chat', 'message': '!about', 'group': 'chat#Testing#13894118', 'media': None,
# 'groupcmd': 'Testing', 'userid': '14390491', 'groupid': '13894118', 'usercmd': 'Nekmo',
# 'msgid': '1585', 'reply': 'chat#Testing#13894118', 'type': 'message', 'ownmsg': False}

# {'username': 'Nekmo', 'timestamp': '00:58', 'groupname': None, 'user': 'chat#Nekmo#14390491',
#  'peer': 'user chat', 'message': '!about', 'group': None, 'media': None, 'groupcmd': None,
#  'userid': '14390491', 'groupid': None, 'usercmd': 'Nekmo', 'msgid': '1587', 'reply':
#  'chat#Nekmo#14390491', 'type': 'message', 'ownmsg': False}

class MessageTelegram(Message):
    def __init__(self, protocol, msg):
        user = UserTelegram(protocol, msg.user)
        self.msg = msg
        if self.is_groupchat:
            groupchat = GroupChatTelegram(protocol, msg.groupname, int(self.msg.groupid))
        else:
            groupchat = None
        if protocol.bot is None and self.msg.ownmsg:
            protocol.bot = user
        super(MessageTelegram, self).__init__(protocol, msg.message, user, groupchat)

    def reply(self, body, notice=False):
        self.protocol.tg.msg(self.msg.reply.cmd, self.protocol.prepare_message(body))

    @property
    def is_from_me(self):
        return self.msg.ownmsg

    @property
    def is_groupchat(self):
        return self.msg.groupname is not None