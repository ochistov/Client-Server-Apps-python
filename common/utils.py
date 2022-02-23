import argparse
import socket
import json
import common.variables as v
import logging
import inspect
from functools import wraps

ADDRESS = 'localhost'
PORT = 7777
CONNECTIONS = 50

serverLogger = logging.getLogger('server')
clientLogger = logging.getLogger('client')

def log(func):
    @wraps(func)
    def call(*args, **kwargs):
        outerFunc = inspect.stack()[1][3]
        serverLogger.debug(f'Function "{func.__name__}" is called into "{outerFunc}"')
        clientLogger.debug(f'Function "{func.__name__}" is called into "{outerFunc}"')
        return func(*args, **kwargs)
    return call

@log
def getServerSocket(addr, port):
    s = socket.socket()
    s.bind((addr, port))
    s.listen(CONNECTIONS)
    return s

@log
def getClientSocket(addr, port):
    s = socket.socket()
    s.connect((addr, port))
    return s

@log
def sendData(recipient, data):
    recipient.send(json.dumps(data).encode(v.ENCODING))

@log
def getData(sender):
    return json.loads(sender.recv(1024).decode(v.ENCODING))

@log
def createParser():
    parser = argparse.ArgumentParser()

    parserGroup = parser.add_argument_group(title='Parameters')
    parserGroup.add_argument(
        '-a', '--addr', default=ADDRESS, help='IP address')
    parserGroup.add_argument('-p', '--port', type=int,
                             default=PORT, help='TCP port')

    return parser
