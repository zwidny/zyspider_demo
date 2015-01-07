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
        send_data = self.factory.spider_args
        self.transport.write(send_data)


class EchoClientFactory(protocol.ClientFactory):
    protocol = Echo

    def __init__(self, url, indicator, deferred):
        self.deferred = deferred

        def _get_format_spider_args(url, indicator):
            spider_args = {}
            spider_args['url'] = url
            spider_args['indicator'] = indicator
            return json.dumps(spider_args).encode('utf-8')
        self.spider_args = _get_format_spider_args(url, indicator)

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


def twspider(host, port, url, indicator):
    d = defer.Deferred()
    factory = EchoClientFactory(url, indicator, d)
    reactor.connectTCP(host, port, factory)
    return d


def main(host, port, url, indicator):

    def twspider_done(e):
        reactor.stop()
        return e

    def result_print(results):
        results = results.decode('utf-8')
        results = json.loads(results)
        return results

    def result_err(err):
        print(err)

    d = twspider(host, port, url, indicator)
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
