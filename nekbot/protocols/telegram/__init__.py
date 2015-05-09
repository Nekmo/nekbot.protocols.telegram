from logging import getLogger
import os
# import pytg
# from pytg.tg import message as tg_message
from pytg2.utils import coroutine
from pytg2.argumenttypes import peer
from nekbot.protocols import Protocol
from nekbot.protocols.telegram.group_chat import GroupChatsTelegram
from nekbot.protocols.telegram.message import MessageTelegram
from telejson import Telejson

__author__ = 'nekmo'
__dir__ = os.path.dirname(__file__)

TELEGRAM_BIN = os.path.abspath(os.path.join(__dir__, 'bin/telegram-cli'))
TELEGRAM_PUB = os.path.abspath(os.path.join(__dir__, 'bin/server.pub'))


logger = getLogger('nekbot.protocols.telegram')


class Telegram(Protocol):
    def init(self):
        self.groupchats = GroupChatsTelegram(self)
        self.bot = None # User Bot
        self.telejson = Telejson()
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
        self.telejson.start()
        self.sender = self.telejson.get_sender()
        def handler(msg):
            self.propagate('message', MessageTelegram(self, msg))
        self.telejson.handler(handler)

        # while True:
            # Keep on polling so that messages will pass through our pipeline
            # self.tg.poll()

    def close(self):
        logger.debug('Closing Telegram...')
        self.telejson.close()
        # self.tg.safe_quit()