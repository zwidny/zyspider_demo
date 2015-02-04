import json
from twisted.internet import reactor, protocol, defer


class Echo(protocol.Protocol):

    results = b''

    def dataReceived(self, data):
        print("%s: Called whenever data is received." %
              self.dataReceived.__name__)
        self.results += data

    def connectionLost(self, reason):
        print("%s: Called when the connection is shut down." %
              self.connectionLost.__name__)
        self.factory.getResult(self.results)

    def connectionMade(self):
        print("%s: Called when a connection is made." %
              self.connectionMade.__name__)
        spider_args = self.factory.spider_args
        self.transport.write(spider_args.encode('utf-8'))


class EchoClientFactory(protocol.ClientFactory):
    protocol = Echo

    def __init__(self, deferred, *args):
        self.deferred = deferred
        self.spider_args = json.dumps(args)

    def getResult(self, results):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(results)

    def startedConnecting(self, connector):
        print("%s: Called when a connection has been started." %
              self.startedConnecting.__name__)

    def clientConnectionFailed(self, connector, reason):
        print("%s: Called when a connection has failed to connect." %
              self.clientConnectionFailed.__name__)
        print(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        print("%s: Called when an established connection is lost." %
              self.clientConnectionLost.__name__)
        print(reason.getErrorMessage())


def main(host, port, *args):
    def twspider(host, port, *args):
        d = defer.Deferred()
        factory = EchoClientFactory(d, *args)
        reactor.connectTCP(host, port, factory)
        return d

    def twspider_done(e):
        reactor.stop()
        return e

    def result_print(results):
        results = results.decode('utf-8')
        results = json.loads(results)
        return results

    def result_err(err):
        print(err)

    d = twspider(host, port, *args)
    d.addCallbacks(result_print, result_err)
    d.addBoth(twspider_done)
    reactor.run()
    return d.result

if __name__ == '__main__':
    host = 'localhost'
    port = 8025
    url = 'http://news.ifeng.com/a/20141230/42830759_0.shtml'
    indicator = (('content', 'xpath', '//*[@id="main_content"]'),)
    result = main(host, port, url, indicator)
