
from utils.time_utils import millis
from comms.tcp_handler import TCPHandler
import logging
TAG = "Message Sender"
RESPONSE_TIMEOUT = 5000


class MessageSender:

    def __init__(self, handler: TCPHandler):
        self.handler = handler

    def send_message(self, msg, wait_for_response=True):

        message_sent = self.handler.send(msg)
        if not message_sent:
            return None

        if wait_for_response:
            start_time = millis()
            while True:
                response = self.handler.get_response()
                if response is not None:
                    return response
                if (millis() - start_time) >= RESPONSE_TIMEOUT:
                    logging.error(f"Response timeout: {msg}")
                    return None

