import json
from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):

    def dataReceived(self, data):
        print("%s: Called whenever data is received." %
              self.dataReceived.__name__)
        print(data.decode('utf-8'))
        reactor.stop()

    def connectionLost(self, reason):
        print("%s: Called when the connection is shut down." %
              self.connectionLost.__name__)

    def connectionMade(self):
        send_data = {}
        send_data['url'] = 'http://tech.ifeng.com/a/20141230/40924964_0.shtml'
        send_data['indicator'] = ('xpath', '//*[@id="main_content"]')
        send_data = json.dumps(send_data)
        self.transport.write(send_data.encode('utf-8'))
        print("%s: Called when a connection is made." %
              self.connectionMade.__name__)


class EchoClientFactory(protocol.ClientFactory):
    protocol = Echo

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


reactor.connectTCP('localhost', 8025, EchoClientFactory())

reactor.run()
