__author__ = 'nekmo'

from nekbot.protocols import User


class UserTelegram(User):
    def __init__(self, protocol, user):
        self.user = user
        User.__init__(self, protocol, user.name, user.id)

    def send_message(self, body, notice=False):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        self.protocol.tg.msg('user#%s' % self.id, body)