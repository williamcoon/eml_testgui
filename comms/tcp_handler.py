from twisted.internet import reactor
from twisted.internet import protocol
from twisted.python import failure

import logging

TCP_PORT = 10443
TAG = "Tcp Handler"


class BasicProtocol(protocol.Protocol):

    def __init__(self):
        super().__init__()
        self.response = None

    def connectionMade(self):
        logging.info(f"{TAG} - New TCP connection")
        self.factory.client = self

    def connectionLost(self, reason: failure.Failure = protocol.connectionDone):
        logging.info(f"{TAG} - Connection lost: {reason}")
        self.factory.client = None

    def dataReceived(self, data: bytes):
        self.response = data.decode('utf-8')
        logging.info(f"{TAG} - Data received: {self.response}")

    def write(self, data: bytes):
        self.response = None
        self.transport.write(data=data)


class TCPHandler:

    def __init__(self):
        self.factory = protocol.ClientFactory()
        self.factory.protocol = BasicProtocol
        # self.factory.clients = []
        self.factory.client = None

    def tcp_listen(self):
        reactor.listenTCP(TCP_PORT, self.factory)
        reactor.run(installSignalHandlers=0)

    def send(self, message, newline=True):
        logging.info(f"{TAG} - Sending: {message}")
        if newline:
            message = message + "\n"
        if self.factory.client is not None:
            self.factory.client.write(data=message.encode('utf-8'))
            return True
        else:
            logging.info("No client connected.")
            return False

    def get_response(self):
        if self.factory.client is not None:
            return self.factory.client.response

    def is_connected(self):
        return self.factory.client is not None