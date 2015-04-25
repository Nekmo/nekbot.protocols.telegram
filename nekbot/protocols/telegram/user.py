__author__ = 'nekmo'

from nekbot.protocols import User


class UserTelegram(User):
    def __init__(self, protocol, user):
        User.__init__(self, protocol, user.name, user.id)