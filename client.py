import common.utils as u
import common.variables as v

# Параметры запуска для клиента тоже решил сделать через argparse, чтобы привести всё к единообразию

if __name__ == '__main__':
    clientName = input('Please insert your name: ')

    parser = u.createParser()
    namespace = parser.parse_args()

    sock = u.getClientSocket(namespace.addr, namespace.port)

    servAddr = sock.getpeername()
    print(f'Connected to server: {servAddr[0]}:{servAddr[1]}')

    v.PRESENCE['user']['account_name'] = clientName
    u.sendData(sock, v.PRESENCE)

    while True:
        data = u.getData(sock)

        print(f'Server responses {data["response"]} - {data["alert"]}')
        if data['response'] != '200':
            break

        msg = input('Insert message (insert \'exit\' to exit): ')
        v.MESSAGE['message'] = msg
        u.sendData(sock, v.MESSAGE)

    sock.close()
