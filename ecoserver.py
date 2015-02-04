# -*- coding: utf-8 -*-
import json
from twisted.internet import protocol, reactor, defer

from spider import crawls


class Echo(protocol.Protocol):

    def dataReceived(self, data):
        '''
        接受来自client的参数, 返回爬取结果
        '''
        print("%s: Called whenever data is received." %
              self.dataReceived.__name__)
        self.factory.processData(data.decode('utf-8'))
        result = self.factory.result
        self.transport.write(result)
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print("%s: Called when the connection is shut down." %
              self.connectionLost.__name__)

    def connectionMade(self):
        print("%s: Called when a connection is made." %
              self.connectionMade.__name__)


class EchoForctory(protocol.Factory):
    protocol = Echo

    def __init__(self, deferred, *args, **kwargs):
        self.deferred = deferred
        self.args = args
        self.kwargs = kwargs

    def processData(self, data):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback((self, data))


def main(port):

    def set_server(port):
        d = defer.Deferred()
        factory = EchoForctory(d)
        reactor.listenTCP(port, factory)
        return d

    def get_result(args):
        self, data = args
        data = json.loads(data)
        result = crawls(*data)
        results = json.dumps(result)
        self.result = results.encode('utf-8')

    def err_result(err):
        print(err)

    d = set_server(port)
    d.addCallbacks(get_result, err_result)
    reactor.run()

if __name__ == '__main__':
    port = 8025
    print("EcoServer Start at %d" % port)
    main(port)
