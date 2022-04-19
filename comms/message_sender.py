import logging
from comms.tcp_handler import TCPHandler

TAG = "Message Sender"


class MessageSender:

    def __init__(self, handler: TCPHandler):
        self.handler = handler

    def send_message(self, msg):
        self.handler.broadcast(msg)