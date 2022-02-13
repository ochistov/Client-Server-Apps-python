import argparse
import socket
import json
import common.variables as v

ADDRESS = 'localhost'
PORT = 7777
CONNECTIONS = 50


def getServerSocket(addr, port):
    s = socket.socket()
    s.bind((addr, port))
    s.listen(CONNECTIONS)
    return s


def getClientSocket(addr, port):
    s = socket.socket()
    s.connect((addr, port))
    return s


def sendData(recipient, data):
    recipient.send(json.dumps(data).encode(v.ENCODING))


def getData(sender):
    return json.loads(sender.recv(1024).decode(v.ENCODING))


def createParser():
    parser = argparse.ArgumentParser()

    parserGroup = parser.add_argument_group(title='Parameters')
    parserGroup.add_argument(
        '-a', '--addr', default=ADDRESS, help='IP address')
    parserGroup.add_argument('-p', '--port', type=int,
                             default=PORT, help='TCP port')

    return parser
