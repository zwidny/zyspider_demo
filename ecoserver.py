# -*- coding: utf-8 -*-
import json
from twisted.internet import protocol, reactor

from spider import spider


class Echo(protocol.Protocol):

    def dataReceived(self, data):
        print("%s: Called whenever data is received." %
              self.dataReceived.__name__)
        print("Data From client: %s" % data)
        data = json.loads(data.decode('utf-8'))
        url = data.get('url')
        indicator = data.get('indicator')
        result = spider(url, indicator)
        self.transport.write(result.encode('utf-8'))

    def connectionLost(self, reason):
        print("%s: Called when the connection is shut down." %
              self.connectionLost.__name__)

    def connectionMade(self):
        print("%s: Called when a connection is made." %
              self.connectionMade.__name__)


class EchoForctory(protocol.Factory):
    protocol = Echo

    def __init__(self, *args, **kwargs):
        pass


reactor.listenTCP(8025, EchoForctory())
reactor.run()
