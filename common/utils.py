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
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serverAddress = namespace.addr
    serverPort = namespace.port
    clientName = namespace.name

    if not 1023 < serverPort < 65536:
        clientLogger.critical(
            f'Trying to run client with incorrect port: {serverPort}. '
            f'There are only ports from 1024 to 65535 allowed. Client.py stops.')
        sys.exit(1)

    return serverAddress, serverPort, clientName

@log
def processClientMessage(message, messagesList, client, clients, names):
    if v.ACTION in message and message[v.ACTION] == v.PRESENCE and v.TIME in message and v.USER in message:
        if message[v.USER][v.ACCOUNT_NAME] not in names.keys():
            names[message[v.USER][v.ACCOUNT_NAME]] = client
            sendData(client, {v.RESPONSE: 200})
        else:
            response = {v.RESPONSE: 400}
            response[v.ERROR] = 'Username is currently in use.'
            sendData(client, response)
            clients.remove(client)
            client.close()
        return

    elif v.ACTION in message and message[v.ACTION] == v.MESSAGE and v.TIME in message and v.MESSAGE_TEXT in message:
        messagesList.append(message)
        return

    elif v.ACTION in message and message[v.ACTION] == v.EXIT and v.ACCOUNT_NAME in message:
        clients.remove(names[message[v.ACCOUNT_NAME]])
        names[message[v.ACCOUNT_NAME]].close()
        del names[message[v.ACCOUNT_NAME]]
        return

    else:
        sendData(client, {
            v.RESPONSE: 400,
            v.ERROR: 'Bad Request'
        })
        return

def showHelp():
    print('Supported commands:')
    print('message - send message. Receeiver and text will be asked later')
    print('help - show help')
    print('exit - close messager')

@log
def messageFromServer(sock, myUsername):
    while True:
        try:
            message = getData(sock)
            if v.ACTION in message and message[v.ACTION] == v.MESSAGE and v.SENDER in message and v.DESTINATION in message and v.MESSAGE_TEXT in message and message[v.DESTINATION] == myUsername:
                print(f'\nReceived message from user {message[v.SENDER]}:'
                      f'\n{message[v.MESSAGE_TEXT]}')
                clientLogger.info(f'Received message from user {message[v.SENDER]}:'
                            f'\n{message[v.MESSAGE_TEXT]}')
            else:
                clientLogger.error(f'Incorrect message received from server: {message}')
        except errors.IncorrectDataRecievedError:
            clientLogger.error(f'Decoding of received message failed.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            clientLogger.critical(f'Connection to server has been lost.')
            break
    # if v.ACTION in message and message[v.ACTION] == v.MESSAGE and \
    #         v.SENDER in message and v.MESSAGE_TEXT in message:
    #     print(f'Received message from user '
    #           f'{message[v.SENDER]}:\n{message[v.MESSAGE_TEXT]}')
    #     clientLogger.info(f'Received message from user '
    #                 f'{message[v.SENDER]}:\n{message[v.MESSAGE_TEXT]}')
    # else:
    #     clientLogger.error(f'Received incorrect message from server: {message}')

@log
def createMessage(sock, accountName='Guest'):
    toUser = input('Insert username of message receiver: ')
    message = input('Insert message to send or "exit" to exit: ')
    if message == 'exit':
        sock.close()
        clientLogger.info('Keyboard interrupt.')
        print('Closed')
        sys.exit(0)
    messageDict = {
        v.ACTION: v.MESSAGE,
        v.TIME: time.time(),
        v.SENDER: accountName,
        v.DESTINATION: toUser,
        v.MESSAGE_TEXT: message
    }
    clientLogger.debug(f'Message dictionary was formed: {messageDict}')
    try:
        sendData(sock, messageDict)
        clientLogger.info(f'message was sent to user {toUser}')
    except Exception as e:
        print(e)
        clientLogger.critical('Connection to server was lost.')
        sys.exit(1)
    #return messageDict

@log
def createPresence(accountName):
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
def createExitMessage(accountName):
    return {
        v.ACTION: v.EXIT,
        v.TIME: time.time(),
        v.ACCOUNT_NAME: accountName
    }


@log
def processMessage(message, names, listenSocks):
    if message[v.DESTINATION] in names and names[message[v.DESTINATION]] in listenSocks:
        sendData(names[message[v.DESTINATION]], message)
        serverLogger.info(f'Message was sent to user {message[v.DESTINATION]} '
                    f'from user {message[v.SENDER]}.')
    elif message[v.DESTINATION] in names and names[message[v.DESTINATION]] not in listenSocks:
        raise ConnectionError
    else:
        serverLogger.error(
            f'User {message[v.DESTINATION]} is not connected, '
            f'unable to send message.')


@log
def processResponseAns(message):
    clientLogger.debug(f'Response answer from server: {message}')
    if v.RESPONSE in message:
        if message[v.RESPONSE] == 200:
            return '200 : OK'
        elif message[v.RESPONSE] == 400:
            raise errors.ServerError(f'400 : {message[v.ERROR]}')
    raise errors.ReqFieldMissingError(v.RESPONSE)

@log
def userInteractive(sock, username):
    showHelp()
    while True:
        command = input('Insert command: ')
        if command == 'message':
            createMessage(sock, username)
        elif command == 'help':
            showHelp()
        elif command == 'exit':
            sendData(sock, createExitMessage(username))
            print('Connection closed.')
            clientLogger.info('Connection closed by user.')
            time.sleep(0.5)
            break
        else:
            print('Wrong command, please try again. help - show supported commands.')