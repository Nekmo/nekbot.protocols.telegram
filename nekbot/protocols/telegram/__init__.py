from logging import getLogger
import os
import pytg2
from pytg2.utils import coroutine
import subprocess
import time
import threading
import signal
import socket
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
    features = ['newline', 'groupchats']
    tg = None
    receiver = None
    sender = None

    def init(self):
        self.tg = pytg2.Telegram(
            telegram=TELEGRAM_BIN,
            pubkey_file=TELEGRAM_PUB)
        self.receiver = self.tg.receiver
        self.sender = self.tg.sender

    def prepare_message(self, body):
        if not isinstance(body, (str, unicode)):
            body = str(body)
        try:
            body = body.decode('utf-8')
        except:
            pass
        return body

    def run(self):
        @coroutine  # from pytg2.utils import coroutine
        def handler():
            while not self.nekbot.is_quit:
                msg = (yield)  # it waits until it got a message, stored now in msg.
                self.propagate('message', MessageTelegram(self, msg))
        self.receiver.start()
        self.receiver.message(handler())

    def close(self):
        logger.debug('Closing Telegram-cli...')
        # l = threading.Thread(target=self.sender.safe_quit)
        # l.daemon = True
        # l.start()
        # l.join(5)
        # logger.debug('Send terminate signal to sender...')
        # self.sender.terminate()
        # logger.debug('Send stop signal to receiver...')
        # self.receiver.stop()
        # self.sender.s.close()
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect(('127.0.0.1', 4458))
        # s.close()