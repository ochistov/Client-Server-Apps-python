import logging
import common.utils as u
import common.variables as v
import log.client_log_config

logger = logging.getLogger('client')

if __name__ == '__main__':
    logger.debug('Client.py started')
    clientName = input('Please insert your name: ')

    parser = u.createParser()
    namespace = parser.parse_args()

    sock = u.getClientSocket(namespace.addr, namespace.port)

    servAddr = sock.getpeername()
    # print(f'Connected to server: {servAddr[0]}:{servAddr[1]}')
    logger.info(f'Connected to server: {servAddr[0]}:{servAddr[1]}')

    v.PRESENCE['user']['account_name'] = clientName
    #u.sendData(sock, v.PRESENCE)
    try:
        u.sendData(sock, v.PRESENCE)
        logger.info(f'Presence successfully sended to {servAddr} : {v.PRESENCE}')
    except ConnectionResetError as e:
        logger.error(e)
        sock.close()
        exit(1)

    while True:
        try:
            data = u.getData(sock)
            logger.info(f'Data received from {servAddr} : {data}')
        except ConnectionResetError as e:
            logger.error(e)
            break

        #print(f'Server responses {data["response"]} - {data["alert"]}')
        if data['response'] != '200':
            logger.info(f'Response not equal 200, closing connection')
            break

        msg = input('Insert message (insert \'exit\' to exit): ')
        v.MESSAGE['message'] = msg
        #u.sendData(sock, v.MESSAGE)
        try:
            u.sendData(sock, v.MESSAGE)
            logger.info(f'Data successfully sended to {servAddr} : {v.MESSAGE}')
        except ConnectionResetError as e:
            logger.error(e)
            break

    logger.debug('Client.py will be stopped')
    sock.close()
