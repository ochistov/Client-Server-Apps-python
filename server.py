import logging
import common.utils as u
import common.variables as v
import log.server_log_config
import select
import time

clientName = ''

logger = logging.getLogger('server')
if __name__ == '__main__':
    logger.debug('Server.py was started')
    parser = u.createServerParser()
    namespace = parser.parse_args()

    sock = u.getServerSocket(namespace.addr, namespace.port)

    servAddr = sock.getsockname()

    startInfo = f'Server started at {servAddr[0]}:{servAddr[1]}'
    print(f'Server started at {servAddr[0]}:{servAddr[1]}')
    logger.info(startInfo)

    clients = []
    messages = []
    names = dict()

    sock.listen(v.MAX_CONNECTIONS)
    while True:
        try:
            client, clientAddress = sock.accept()
        except OSError as err:
            pass
        else:
            logger.info(f'Client connected from {clientAddress}')
            clients.append(client)

        recvDataList = []
        sendDataList = []
        errList = []

        try:
            if clients:
                recvDataList, sendDataList, errList = select.select(clients, clients, [], 0)
        except OSError:
            pass
        
        if recvDataList:
            for clientWithMessage in recvDataList:
                try:
                    u.processClientMessage(u.getData(clientWithMessage),
                                           messages, clientWithMessage, clients, names)
                except:
                    logger.info(f'Client {clientWithMessage.getpeername()} '
                                f'was disconnected from server.')
                    clients.remove(clientWithMessage)



                for message in messages:
                    try:
                        u.processMessage(message, names, sendDataList)
                    except Exception:
                        logger.info(f'Connection with user {message[v.DESTINATION]} was lost')
                        clients.remove(names[message[v.DESTINATION]])
                        del names[message[v.DESTINATION]]
                messages.clear()

        # if messages and sendDataList:
        #     message = {
        #         v.ACTION: v.MESSAGE,
        #         v.SENDER: messages[0][0],
        #         v.TIME: time.time(),
        #         v.MESSAGE_TEXT: messages[0][1]
        #     }
        #     del messages[0]
        #     for waitingClient in sendDataList:
        #         try:
        #             u.sendData(waitingClient, message)
        #         except:
        #             logger.info(f'Client {waitingClient.getpeername()} disconnected from the server.')
        #             waitingClient.close()
        #             clients.remove(waitingClient)







    # client, address = sock.accept()
    # clientInfo = f'Client connected from {address[0]}:{address[1]}'
    # #print(f'Client connected from {address[0]}:{address[1]}')
    # logger.info(clientInfo)

    # while True:
    #     try:
    #         data = u.getData(client)
    #         logger.info(f'Data successfully received from {address} : {data}')
    #     except ConnectionResetError as e:
    #         logger.error(e)
    #         break

    #     if clientName == '':
    #         if data['action'] == 'presence' and data['user']['account_name'] != '':
    #             clientName = data['user']['account_name']
    #             v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[0]
    #             print(f'{data["time"]} - {data["user"]["account_name"]} connected')
    #         else:
    #             v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[1]

    #     if clientName != '' and data['action'] == 'msg':
    #         print(f'{data["time"]} - {clientName}: {data["message"]}')
    #         v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[0]
    #         # print(
    #         #     f'Server responses {v.RESPONSE["response"]}, {v.RESPONSE["alert"]}')

    #         if data["message"] == 'exit':
    #             v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[2]
    #             # print(
    #             #     f'Server responses {v.RESPONSE["response"]}, {v.RESPONSE["alert"]}')

    #     #u.sendData(client, v.RESPONSE)
    #     dataToSend = v.RESPONSE
    #     try:
    #         u.sendData(client, dataToSend)
    #         logger.info(f'Data successfully sended to {address} : {dataToSend}')
    #     except ConnectionResetError as e:
    #         logger.error(e)
    #         break

    #     if v.RESPONSE['response'] != '200':
    #         client.close()
    #         break
    # logger.debug('Server.py will be stopped')

    # sock.close()
