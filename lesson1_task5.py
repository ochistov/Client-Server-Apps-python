# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
# преобразовать результаты из байтовового в строковый тип на кириллице.
import subprocess as sp
from sys import platform
listToPing = input('Please input resources devided by comma: ').split(',')


def pinger(resource):
    if platform == 'win32':
        param = '-n'
        encoding = '866'
    else:
        param = '-c'
        encoding = 'utf-8'
    ping = sp.Popen(f'ping {param} 2 {resource}', stdout=sp.PIPE)
    for line in ping.stdout:
        print(line.decode(encoding))


for resource in listToPing:
    pinger(resource)
