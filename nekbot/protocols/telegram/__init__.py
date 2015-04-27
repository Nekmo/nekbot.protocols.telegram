from logging import getLogger
import os
import pytg
from pytg.tg import message as tg_message
from pytg.utils import coroutine, broadcast
from nekbot.protocols import Protocol
from nekbot.protocols.telegram.group_chat import GroupChatsTelegram
from nekbot.protocols.telegram.message import MessageTelegram

__author__ = 'nekmo'
__dir__ = os.path.dirname(__file__)

TELEGRAM_BIN = os.path.abspath(os.path.join(__dir__, 'bin/telegram-cli'))
TELEGRAM_PUB = os.path.abspath(os.path.join(__dir__, 'bin/server.pub'))


logger = getLogger('nekbot.protocols.telegram')


class Telegram(Protocol):
    def init(self):
        self.groupchats = GroupChatsTelegram(self)
        self.bot = None # User Bot
        self.tg = pytg.Telegram(TELEGRAM_BIN, TELEGRAM_PUB)
        # Create processing pipeline
        pipeline = broadcast([
            tg_message(self.input_message(self.tg))
        ])
        self.tg.register_pipeline(pipeline)
        # Start telegram cli
        self.tg.start()

    def prepare_message(self, body):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        body = body.decode('utf-8')
        return body

    @coroutine
    def input_message(self, tg):
        # To avoid ping flood attack, we'll respond to ping once every 10 sec
        try:
            while True:
                msg = (yield)
                self.propagate('message', MessageTelegram(self, msg))

                # Only process if the group name match
                # if msg.group.name == CHAT_GROUP:
                #     cmd = msg.message.strip().split(' ')
                #     if len(cmd) == 1:
                #         # ping command
                #         if cmd[0].lower() == 'ping':
                #             tg.msg(msg.reply.cmd, 'pong')
                #         # quit command
                #         elif cmd[0].lower() == 'quit':
                #             if msg.user.id == ADMIN_USERID:  # Checking user id
                #                 tg.msg(msg.reply.cmd, 'By your command.')  # reply to same chat (group or user)
                #                 tg.msg(msg.user.cmd, 'Good bye.')  # reply to user directly
                #                 QUIT = True
        except GeneratorExit:
            pass

    def run(self):
        while True:
            # Keep on polling so that messages will pass through our pipeline
            self.tg.poll()

    def close(self):
        logger.debug('Closing Telegram...')
        self.tg.safe_quit()