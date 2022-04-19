from twisted.internet import reactor
from twisted.internet import protocol
from twisted.python import failure

import logging

TCP_PORT = 10443
TAG = "Tcp Handler"


class BasicProtocol(protocol.Protocol):

    def connectionMade(self):
        logging.info(f"{TAG} - New TCP connection")
        self.factory.clients.append(self)

    def connectionLost(self, reason: failure.Failure = protocol.connectionDone):
        logging.info(f"{TAG} - Connection lost: {reason}")
        try:
            self.factory.clients.remove(self)
        except ValueError:
            pass

    def dataReceived(self, data: bytes):
        logging.info(f"{TAG} - Data received: {data.decode('utf-8')}")


class TCPHandler:

    def __init__(self):
        self.factory = protocol.ClientFactory()
        self.factory.protocol = BasicProtocol
        self.factory.clients = []

    def tcp_listen(self):
        reactor.listenTCP(TCP_PORT, self.factory)
        reactor.run(installSignalHandlers=0)

    def broadcast(self, message, newline=True):
        logging.info(f"{TAG} - Broadcasting: {message}")
        if newline:
            message = message + "\n"
        for client in self.factory.clients:
            client.transport.write(data=message.encode('utf-8'))