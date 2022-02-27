import logging
import common.utils as u
import common.variables as v
import log.client_log_config
import json
import sys
import errors

logger = logging.getLogger('client')

if __name__ == '__main__':
    logger.debug('Client.py started')
    clientName = input('Please insert your name: ')

    try:
        parser = u.createClientParser()
        clientMode = parser[2]
        sock = u.getClientSocket(parser[0], parser[1])
        servAddr = sock.getpeername()
        u.sendData(sock, u.createPresence())
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
            f'Unable to connect {servAddr}, '
            f'remote computer denied connection request.')
        sys.exit(1)
    else:
        if clientMode == 'send':
            print('Mode - send message.')
        else:
            print('Mode - get message.')

        while True:
            if clientMode == 'send':
                try:
                    u.sendData(sock, u.createMessage(sock, clientName))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Соединение с сервером {servAddr} было потеряно.')
                    sys.exit(1)
            if clientMode == 'listen':
                try:
                    u.messageFromServer(u.getData(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Connection to {servAddr} was lost.')
                    sys.exit(1)



    # servAddr = sock.getpeername()
    # # print(f'Connected to server: {servAddr[0]}:{servAddr[1]}')
    # logger.info(f'Connected to server: {servAddr[0]}:{servAddr[1]}')

    # v.PRESENCE['user']['account_name'] = clientName
    # #u.sendData(sock, v.PRESENCE)
    # try:
    #     u.sendData(sock, v.PRESENCE)
    #     logger.info(f'Presence successfully sended to {servAddr} : {v.PRESENCE}')
    # except ConnectionResetError as e:
    #     logger.error(e)
    #     sock.close()
    #     exit(1)

    # while True:
    #     try:
    #         data = u.getData(sock)
    #         logger.info(f'Data received from {servAddr} : {data}')
    #     except ConnectionResetError as e:
    #         logger.error(e)
    #         break

    #     #print(f'Server responses {data["response"]} - {data["alert"]}')
    #     if data['response'] != '200':
    #         logger.info(f'Response not equal 200, closing connection')
    #         break

    #     msg = input('Insert message (insert \'exit\' to exit): ')
    #     v.MESSAGE['message'] = msg
    #     #u.sendData(sock, v.MESSAGE)
    #     try:
    #         u.sendData(sock, v.MESSAGE)
    #         logger.info(f'Data successfully sended to {servAddr} : {v.MESSAGE}')
    #     except ConnectionResetError as e:
    #         logger.error(e)
    #         break

    # logger.debug('Client.py will be stopped')
    # sock.close()
