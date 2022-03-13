import logging
import common.utils as u
import common.variables as v
import log.client_log_config
import json
import sys
import errors
import threading
import time

logger = logging.getLogger('client')

if __name__ == '__main__':
    logger.debug('Client.py started')
    servIP, servPort, clientName = u.createClientParser()
    if not clientName:
        clientName = input('Please insert username: ')
    print(f'Console messager. Client module. Username: {clientName}')
    logger.info(f'Client started. Username - {clientName} Server IP - {servIP} Server port - {servPort}')

    try:
        sock = u.getClientSocket(servIP, servPort)
        u.sendData(sock, u.createPresence(clientName))
        answer = u.processResponseAns(u.getData(sock))
        logger.info(f'Established connection to server. Server response: {answer}')
        print(f'Established connection to server.')
    except json.JSONDecodeError:
        logger.error('Fail to decode received JSON.')
        sys.exit(1)
    except errors.ServerError as error:
        logger.error(f'Server was retrieve error while establish connection: {error.text}')
        sys.exit(1)
    except errors.ReqFieldMissingError as missingError:
        logger.error(f'There is no required field in servers response: {missingError.missingField}')
        sys.exit(1)
    except ConnectionRefusedError:
        logger.critical(
            f'Unable to connect {servIP}, '
            f'remote computer denied connection request.')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=u.messageFromServer, args=(sock, clientName))
        receiver.daemon = True
        receiver.start()

        userInterface = threading.Thread(target=u.userInteractive, args=(sock, clientName))
        userInterface.daemon = True
        userInterface.start()
        logger.debug('Processes started')

        while True:
            time.sleep(1)
            if receiver.is_alive() and userInterface.is_alive():
                continue
            break


        # if clientMode == 'send':
        #     print('Mode - send message.')
        # else:
        #     print('Mode - get message.')

        # while True:
        #     if clientMode == 'send':
        #         try:
        #             u.sendData(sock, u.createMessage(sock, clientName))
        #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        #             logger.error(f'Соединение с сервером {servAddr} было потеряно.')
        #             sys.exit(1)
        #     if clientMode == 'listen':
        #         try:
        #             u.messageFromServer(u.getData(sock))
        #         except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        #             logger.error(f'Connection to {servAddr} was lost.')
        #             sys.exit(1)


