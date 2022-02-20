import common.utils as u
import common.variables as v

clientName = ''

if __name__ == '__main__':
    parser = u.createParser()
    namespace = parser.parse_args()

    sock = u.getServerSocket(namespace.addr, namespace.port)

    servAddr = sock.getsockname()
    print(f'Server started at {servAddr[0]}:{servAddr[1]}')

    client, address = sock.accept()
    print(f'Client connected from {address[0]}:{address[1]}')

    while True:
        data = u.getData(client)

        if clientName == '':
            if data['action'] == 'presence' and data['user']['account_name'] != '':
                clientName = data['user']['account_name']
                v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[0]
                print(f'{data["time"]} - {data["user"]["account_name"]}')
            else:
                v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[1]

        if clientName != '' and data['action'] == 'msg':
            print(f'{data["time"]} - {clientName}: {data["message"]}')
            v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[0]
            print(
                f'Server responses {v.RESPONSE["response"]}, {v.RESPONSE["alert"]}')

            if data["message"] == 'exit':
                v.RESPONSE['response'], v.RESPONSE['alert'] = v.SERVER_RESPONSE[2]
                print(
                    f'Server responses {v.RESPONSE["response"]}, {v.RESPONSE["alert"]}')

        u.sendData(client, v.RESPONSE)

        if v.RESPONSE['response'] != '200':
            client.close()
            break

    sock.close()
