from logging import getLogger
import os
import pytg2
from pytg2.utils import coroutine
import subprocess
from nekbot.protocols import Protocol
from nekbot.protocols.telegram.group_chat import GroupChatsTelegram
from nekbot.protocols.telegram.message import MessageTelegram
import telejson

__author__ = 'nekmo'

telejson_dir = os.path.dirname(os.path.abspath(telejson.__file__))

TELEGRAM_BIN = 'telegram-cli'
TELEGRAM_PUB = os.path.abspath(os.path.join(telejson_dir, 'tg-server.pub'))
print(TELEGRAM_PUB)


logger = getLogger('nekbot.protocols.telegram')


class Telegram(Protocol):
    groupchats = None
    bot = None
    tg = None
    receiver = None
    sender = None

    def init(self):
        self.groupchats = GroupChatsTelegram(self)
        self.bot = None  # User Bot
        self.tg = pytg2.Telegram(
            telegram=TELEGRAM_BIN,
            pubkey_file=TELEGRAM_PUB)
        self.receiver = self.tg.receiver
        self.sender = self.tg.sender
        # self.tg = pytg.Telegram(TELEGRAM_BIN, TELEGRAM_PUB)
        # # Create processing pipeline
        # pipeline = broadcast([
        #     tg_message(self.input_message(self.tg))
        # ])
        # self.tg.register_pipeline(pipeline)
        # # Start telegram cli
        # self.tg.start()

    def prepare_message(self, body):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        try:
            body = body.decode('utf-8')
        except:
            pass
        return body

    def run(self):
        # self.telejson.telegram_cli.set_log_level(str(6))
        # self.telejson.telegram_cli.set_log_file('/tmp/telegram.log')
        @coroutine  # from pytg2.utils import coroutine
        def handler():
            while not self.nekbot.is_quit:
                msg = (yield)  # it waits until it got a message, stored now in msg.
                self.propagate('message', MessageTelegram(self, msg))
        self.receiver.start()
        self.receiver.message(handler())

        # while True:
            # Keep on polling so that messages will pass through our pipeline
            # self.tg.poll()

    def close(self):
        logger.debug('Closing Telegram...')
        self.tg.stopCLI()