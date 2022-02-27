import argparse
import socket
import json
import common.variables as v
import logging
import inspect
from functools import wraps
import sys
import time
import errors

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
    s.settimeout(0.5)
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
def createServerParser():
    parser = argparse.ArgumentParser()

    parserGroup = parser.add_argument_group(title='Parameters')
    parserGroup.add_argument(
        '-a', '--addr', default=ADDRESS, help='IP address')
    parserGroup.add_argument('-p', '--port', type=int,
                             default=PORT, help='TCP port')

    return parser


@log
def createClientParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=v.DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=v.DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serverAddress = namespace.addr
    serverPort = namespace.port
    clientMode = namespace.mode

    if not 1023 < serverPort < 65536:
        clientLogger.critical(
            f'Trying to run client with incorrect port: {serverPort}. '
            f'There are only ports from 1024 to 65535 allowed. Client.py stops.')
        sys.exit(1)

    if clientMode not in ('listen', 'send'):
        clientLogger.critical(f'Incorrect client mode: {clientMode}, '
                        f'correct modes: listen , send')
        sys.exit(1)

    return serverAddress, serverPort, clientMode

@log
def processClientMessage(message, messagesList, client):
    if v.ACTION in message and message[v.ACTION] == v.PRESENCE and v.TIME in message \
            and v.USER in message and message[v.USER][v.ACCOUNT_NAME] == 'Guest':
        sendData(client, {v.RESPONSE: 200})
        return

    elif v.ACTION in message and message[v.ACTION] == v.MESSAGE and \
            v.TIME in message and v.MESSAGE_TEXT in message:
        messagesList.append((message[v.ACCOUNT_NAME], message[v.MESSAGE_TEXT]))
        return

    else:
        sendData(client, {
            v.RESPONSE: 400,
            v.ERROR: 'Bad Request'
        })
        return
    
@log
def messageFromServer(message):
    if v.ACTION in message and message[v.ACTION] == v.MESSAGE and \
            v.SENDER in message and v.MESSAGE_TEXT in message:
        print(f'Received message from user '
              f'{message[v.SENDER]}:\n{message[v.MESSAGE_TEXT]}')
        clientLogger.info(f'Received message from user '
                    f'{message[v.SENDER]}:\n{message[v.MESSAGE_TEXT]}')
    else:
        clientLogger.error(f'Received incorrect message from server: {message}')

@log
def createMessage(sock, accountName='Guest'):
    message = input('Insert message to send or "exit" to exit: ')
    if message == 'exit':
        sock.close()
        clientLogger.info('Keyboard interrupt.')
        print('Closed')
        sys.exit(0)
    messageDict = {
        v.ACTION: v.MESSAGE,
        v.TIME: time.time(),
        v.ACCOUNT_NAME: accountName,
        v.MESSAGE_TEXT: message
    }
    clientLogger.debug(f'Message dictionary was formed: {messageDict}')
    return messageDict

@log
def createPresence(accountName='Guest'):
    out = {
        v.ACTION: v.PRESENCE,
        v.TIME: time.time(),
        v.USER: {
            v.ACCOUNT_NAME: accountName
        }
    }
    clientLogger.debug(f'{v.PRESENCE} was formed for {accountName}')
    return out

@log
def processResponseAns(message):
    clientLogger.debug(f'Response answer from server: {message}')
    if v.RESPONSE in message:
        if message[v.RESPONSE] == 200:
            return '200 : OK'
        elif message[v.RESPONSE] == 400:
            raise errors.ServerError(f'400 : {message[v.ERROR]}')
    raise errors.ReqFieldMissingError(v.RESPONSE)

